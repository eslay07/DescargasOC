import poplib
from email import parser
import re
import time
import configurador
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
import selenium_modulo

USUARIO, PASSWORD = configurador.obtener_credenciales()

POP_SERVER = "pop.telconet.ec"
POP_PORT = 995

PROCESADOS_FILE = "procesados.txt"

def cargar_procesados():
    procesados = set()
    try:
        with open(PROCESADOS_FILE, "r") as f:
            for line in f:
                procesados.add(line.strip())
    except FileNotFoundError:
        pass
    return procesados

def guardar_procesado(uidl):
    with open(PROCESADOS_FILE, "a") as f:
        f.write(uidl + "\n")

def es_de_hoy(fecha_email):
    local_tz = timezone(timedelta(hours=-5))  # Ecuador UTC-5
    hoy = datetime.now(local_tz).date()
    return fecha_email.astimezone(local_tz).date() == hoy

def buscar_oc():
    procesados = cargar_procesados()

    print(f"🔍 POP3 conectado a: {POP_SERVER}")
    pop_conn = poplib.POP3_SSL(POP_SERVER, POP_PORT)
    pop_conn.user(USUARIO)
    pop_conn.pass_(PASSWORD)
    print(f"✅ Login correcto: {USUARIO}")

    num_messages = len(pop_conn.list()[1])
    print(f"📧 Correos detectados: {num_messages}")

    for i in range(num_messages):
        uidl = pop_conn.uidl(i+1).decode().split()[2]
        if uidl in procesados:
            continue

        print(f"➡️ Revisando ID: {i+1} UIDL: {uidl}")

        raw_email = b"\n".join(pop_conn.retr(i+1)[1])
        email_message = parser.BytesParser().parsebytes(raw_email)

        fecha_header = email_message["Date"]
        try:
            fecha_email = parsedate_to_datetime(fecha_header)
            if not es_de_hoy(fecha_email):
                print(f"⏭️ NO ES DE HOY: {fecha_email}")
                guardar_procesado(uidl)
                continue
        except Exception as e:
            print(f"⚠️ Fecha mal formada: {fecha_header} Error: {e}")
            guardar_procesado(uidl)
            continue

        asunto = email_message["subject"]
        cuerpo = ""

        if email_message.is_multipart():
            for parte in email_message.walk():
                if parte.get_content_type() == "text/plain":
                    try:
                        charset = parte.get_content_charset() or "utf-8"
                        cuerpo += parte.get_payload(decode=True).decode(charset, errors="replace")
                    except Exception as e:
                        print(f"⚠️ Error decoding parte: {e}")
        else:
            try:
                charset = email_message.get_content_charset() or "utf-8"
                cuerpo = email_message.get_payload(decode=True).decode(charset, errors="replace")
            except Exception as e:
                print(f"⚠️ Error decoding cuerpo: {e}")

        print(f"🗂️ Asunto: {asunto}")
        print(f"📄 Cuerpo (preview): {cuerpo[:100]}...")

        match_asunto = re.search(r"ORDEN COMPRA NO.(\d+)", asunto or "")
        if "Se comunica que ha sido autorizada la orden de compra" in cuerpo and match_asunto:
            numero_oc = match_asunto.group(1)
            print(f"✅ OC DETECTADA: {numero_oc}")
            guardar_procesado(uidl)
            pop_conn.quit()
            return numero_oc, "ProveedorDummy"

        guardar_procesado(uidl)

    pop_conn.quit()
    print("⏳ Fin de ronda.")
    return None, None

if __name__ == "__main__":
    while True:
        numero, proveedor = buscar_oc()
        if numero:
            print(f"🚀 Detectada OC: {numero}. Ejecutando Selenium...")
            selenium_modulo.descargar_oc(numero)
            print("✅ Selenium + mover_pdf completados. Volviendo a escuchar...\n")
        else:
            print("🔄 No hay OC nueva. Escuchando de nuevo...\n")
        time.sleep(900)  # Espera 15 min (900 segundos)

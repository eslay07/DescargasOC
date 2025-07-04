import os
import shutil
import configurador
import PyPDF2

def mover_oc():
    config = configurador.cargar_config()
    carpeta_origen = config["carpeta_analizar"]
    carpeta_destino = config["carpeta_destino"]

    print(f"📂 Analizando archivos en: {carpeta_origen}")
    print(f"📁 Destino: {carpeta_destino}")

    # Verifica existencia
    if not os.path.exists(carpeta_origen):
        print(f"❌ Carpeta origen no existe: {carpeta_origen}")
        return

    if not os.path.exists(carpeta_destino):
        print(f"⚠️ Carpeta destino no existe. Creando: {carpeta_destino}")
        os.makedirs(carpeta_destino)

    archivos = [f for f in os.listdir(carpeta_origen) if f.lower().endswith(".pdf")]
    if not archivos:
        print("📭 No se encontraron archivos PDF para mover.")
        return

    for archivo in archivos:
        ruta_archivo = os.path.join(carpeta_origen, archivo)
        try:
            with open(ruta_archivo, "rb") as f:
                pdf = PyPDF2.PdfReader(f)
                texto = ""
                for pagina in pdf.pages:
                    texto += pagina.extract_text() or ""

                if "ORDEN DE COMPRA" in texto.upper():
                    destino_final = os.path.join(carpeta_destino, archivo)
                    shutil.move(ruta_archivo, destino_final)
                    print(f"✅ Archivo movido: {archivo} -> {destino_final}")
                else:
                    print(f"⏭️ No es OC: {archivo}")

        except Exception as e:
            print(f"⚠️ Error procesando {archivo}: {e}")

    print("🚀 Proceso de mover PDF completado.")

if __name__ == "__main__":
    mover_oc()

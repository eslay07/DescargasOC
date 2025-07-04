import os
import configurador
import PyPDF2
import seafile_client

def mover_oc():
    config = configurador.cargar_config()
    carpeta_origen = config["carpeta_analizar"]
    repo_id = config["carpeta_destino"]  # se utiliza como identificador del repo en Seafile
    cliente = seafile_client.get_client_from_config()

    print(f"📂 Analizando archivos en: {carpeta_origen}")
    print(f"📁 Repo destino: {repo_id}")

    # Verifica existencia
    if not os.path.exists(carpeta_origen):
        print(f"❌ Carpeta origen no existe: {carpeta_origen}")
        return


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
                    cliente.upload_file(repo_id, ruta_archivo)
                    os.remove(ruta_archivo)
                    print(f"✅ Archivo subido: {archivo}")
                else:
                    print(f"⏭️ No es OC: {archivo}")

        except Exception as e:
            print(f"⚠️ Error procesando {archivo}: {e}")

    print("🚀 Proceso de mover PDF completado.")

if __name__ == "__main__":
    mover_oc()

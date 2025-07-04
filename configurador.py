import os
import tkinter as tk
from tkinter import filedialog
import json

CONFIG_FILE = os.path.join(os.path.expanduser("~"), "config.json")

USUARIO_ENV = "USUARIO_OC"
PASSWORD_ENV = "PASSWORD_OC"

def guardar_config(usuario, password, carpeta_destino, carpeta_analizar,
                   seafile_url, seafile_token):
    config = {
        "usuario": usuario,
        "password": password,
        "carpeta_destino": carpeta_destino,
        "carpeta_analizar": carpeta_analizar,
        "seafile_url": seafile_url,
        "seafile_token": seafile_token,
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
    print(f"✅ Configuración guardada en {CONFIG_FILE}")

def cargar_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            print(f"✅ Configuración cargada: {config}")
            return config
    except FileNotFoundError:
        print("⚠️ No se encontró configuración previa.")
        return None

def obtener_credenciales():
    """Devuelve usuario y contraseña desde variables de entorno
    USUARIO_ENV y PASSWORD_ENV. Si no existen, recurre al archivo
    de configuración."""
    config = cargar_config()
    usuario = os.getenv(USUARIO_ENV)
    password = os.getenv(PASSWORD_ENV)

    if not usuario and config:
        usuario = config.get("usuario")
    if not password and config:
        password = config.get("password")

    return usuario, password

def configurar():
    def seleccionar_carpeta_destino():
        carpeta = filedialog.askdirectory()
        entry_carpeta_destino.delete(0, tk.END)
        entry_carpeta_destino.insert(0, carpeta)

    def seleccionar_carpeta_analizar():
        carpeta = filedialog.askdirectory()
        entry_carpeta_analizar.delete(0, tk.END)
        entry_carpeta_analizar.insert(0, carpeta)

    def guardar():
        usuario = entry_usuario.get()
        password = entry_password.get()
        carpeta_destino = entry_carpeta_destino.get()
        carpeta_analizar = entry_carpeta_analizar.get()
        seafile_url = entry_seafile_url.get()
        seafile_token = entry_seafile_token.get()
        guardar_config(
            usuario,
            password,
            carpeta_destino,
            carpeta_analizar,
            seafile_url,
            seafile_token,
        )
        ventana.destroy()

    ventana = tk.Tk()
    ventana.title("Configuración")

    tk.Label(ventana, text="Usuario:").pack()
    entry_usuario = tk.Entry(ventana)
    entry_usuario.pack()

    tk.Label(ventana, text="Contraseña:").pack()
    entry_password = tk.Entry(ventana, show="*")
    entry_password.pack()

    tk.Label(ventana, text="Carpeta destino:").pack()
    entry_carpeta_destino = tk.Entry(ventana, width=50)
    entry_carpeta_destino.pack()
    tk.Button(ventana, text="Seleccionar carpeta destino", command=seleccionar_carpeta_destino).pack()

    tk.Label(ventana, text="Carpeta a analizar:").pack()
    entry_carpeta_analizar = tk.Entry(ventana, width=50)
    entry_carpeta_analizar.pack()
    tk.Button(ventana, text="Seleccionar carpeta a analizar", command=seleccionar_carpeta_analizar).pack()

    tk.Label(ventana, text="Seafile URL:").pack()
    entry_seafile_url = tk.Entry(ventana, width=50)
    entry_seafile_url.pack()

    tk.Label(ventana, text="Seafile Token:").pack()
    entry_seafile_token = tk.Entry(ventana, width=50)
    entry_seafile_token.pack()

    tk.Button(ventana, text="Guardar configuración", command=guardar).pack(pady=10)

    ventana.mainloop()

if __name__ == "__main__":
    configurar()

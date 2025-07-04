import os
import tkinter as tk
from tkinter import filedialog
import json

CONFIG_FILE = os.path.join(os.path.expanduser("~"), "config.json")

def guardar_config(usuario, password, carpeta_destino, carpeta_analizar):
    config = {
        "usuario": usuario,
        "password": password,
        "carpeta_destino": carpeta_destino,
        "carpeta_analizar": carpeta_analizar
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
        guardar_config(usuario, password, carpeta_destino, carpeta_analizar)
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

    tk.Button(ventana, text="Guardar configuración", command=guardar).pack(pady=10)

    ventana.mainloop()

if __name__ == "__main__":
    configurar()

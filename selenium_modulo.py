from selenium import webdriver
import tkinter as tk
from tkinter import messagebox
import time
import mover_pdf

def descargar_oc(numero_oc):
    print(f"🌐 Lanzando Selenium para OC: {numero_oc}")

    # Abre navegador Chrome
    driver = webdriver.Chrome()
    driver.get("https://www.google.com")  # página dummy de prueba
    print("✅ Navegador abierto. Esperando 30 s...")
    time.sleep(30)  # Mantener navegador abierto 30 s
    driver.quit()
    print("✅ Navegador cerrado.")

    # Confirma en pantalla
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Prueba Selenium", "✅ Script automático de Selenium terminó correctamente")
    root.destroy()

    # Lanza mover_pdf
    mover_pdf.mover_oc()


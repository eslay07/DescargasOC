# DescargasOC
Este proyecto es un piloto para una automatización de descarga de ordenes de
compra desde una aplicación web a un almacenamiento en la nube.

## Requisitos

- **Python ≥ 3.8.** Los scripts hacen uso de `f-strings` y bibliotecas como
  `tkinter`, `PyPDF2` y `selenium`.

## Configuración inicial

El archivo de configuración `config.json` se genera ejecutando:

```bash
python configurador.py
```

Se abrirá una pequeña ventana donde se solicitan:

1. Usuario y contraseña del correo.
2. Carpeta destino donde se almacenarán los PDF detectados.
3. Carpeta a analizar (de donde se leerán los PDF descargados).

Al pulsar **Guardar configuración**, la información se guarda en
`~/config.json`. Este archivo es leído por el resto de scripts.

## Uso de los scripts

### escuchador.py

Escanea periódicamente la cuenta de correo configurada mediante POP3 en busca
de mensajes que notifiquen una nueva Orden de Compra. Cuando detecta una,
invoca a `selenium_modulo.descargar_oc()` para iniciar el flujo de descarga.
Ejecutar con:

```bash
python escuchador.py
```

### mover_pdf.py

Revisa la carpeta configurada como origen en `config.json` y mueve al destino
los PDF que contengan la cadena "ORDEN DE COMPRA" en su texto. Puede ejecutarse
de forma independiente:

```bash
python mover_pdf.py
```

### selenium_modulo.py

Muestra un ejemplo de automatización con Selenium. Abre un navegador, espera
unos segundos y luego llama a `mover_pdf.mover_oc()` para procesar los PDF. Se
puede lanzar con:

```bash
python selenium_modulo.py
```

---
Para todos los scripts se asume que `config.json` ya ha sido creado mediante el
`configurador.py`.

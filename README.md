# DescargasOC
Este proyecto es un piloto para una automatización de descarga de ordenes de compra desde una aplicación web a un almacenamiento en la nube.

## Configuración

El archivo de configuración (`config.json`) ahora incluye dos campos adicionales para permitir la subida de archivos a un servidor **Seafile**:

```
seafile_url   # URL base del servidor Seafile
seafile_token # Token de acceso de la API
```

`carpeta_destino` se utiliza como identificador de la biblioteca o destino dentro de Seafile.

# DescargasOC
Este proyecto es un piloto para una automatización de descarga de ordenes de compra desde una aplicación web a un almacenamiento en la nube.

## Credenciales por variables de entorno

`escuchador.py` toma el usuario y la contraseña del servidor POP3 usando las variables de entorno `USUARIO_OC` y `PASSWORD_OC`. Si no se definen, se utilizarán los valores almacenados en el archivo `~/config.json` creado mediante `configurador.py`.

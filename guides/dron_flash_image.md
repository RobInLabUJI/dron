## Instalación de imagen SDK-1.0 en modalAI starling

Almacenamiento de los datos de calibración (Conectar el dron vía USB al PC):

```
> adb pull /etc/modalai

> adb pull /data/misc

``````

Descomprimir el archivo que contiene la imagen:

```
> tar -xzvf voxl2_SDK_1.0.0.tar.gz

```
Acceder al archivo:

```
> cd voxl2_SDK_1.0.0
```
Comprobar que adb detecta el dispositivo :
```
> adb devices
```

Comprobar que funciona "fastboot" (Solo habrá un output si falla la herramienta):

```
> ❯ fastboot devices
```
Ejecutar instalación:

```
> ./install.sh
```

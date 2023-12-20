# Guía de calibración (resumida)

Link: 		https://docs.modalai.com/check-calibration/
link 2:	https://docs.modalai.com/calibration/ 

## Verificar calibración

```
> voxl-check-calibration

```

## Calibrar curvas de temperatura

La controladora de vuelo debe estar con la temperatura más baja posible (Asegurar que la batería se encuentra cargada).
```
> voxl-inspect-battery

> voxl-calibrate-imu-temp

```

## Calibrar IMU

Se deben seguir los pasos que se irán indicando mediante la terminal.

- Verificar que el servidor de la IMU se esté ejecutando.

```

> voxl-inspect-services

```

- Ejecutar calibración

```
> voxl-calibrate-imu 

```

## Calibrar nivel

Entrar en "position mode" y despegar el dron, luego, inducir movimientos de "pitch" y "roll" durante 30 segundos. Finalmente, se debe llevar al dron en vuelo hasta un punto donde se le pueda dejar suspendido en el aire sin riesgo, y esperar hasta que la teminal indique que la calabración ha terminado.

```
> voxl-calibrate-px4-horizon
```

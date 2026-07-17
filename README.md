# De electrónica a desarrollo de software (con IA)

Repositorio de checkpoints semanales del curso "De electrónica a desarrollo de software con IA". Cada día de la semana tiene su propia carpeta con el código, los tests y las verificaciones de tipos/estilo.

## Instalación

```
git clone https://github.com/Nadiadoki/sdlc-electronica-nadia
cd sdlc-electronica-nadia
py -m pip install pytest mypy ruff
```

## Cómo correr los tests

Todos los tests de la semana 1:
```
py -m pytest semana1/ -v
```

Solo el ejercicio integrador del día 5 (driver UART):
```
py -m pytest semana1/uart_driver/tests/ -v
```

Verificación de tipos y estilo (ejemplo con el driver UART):
```
py -m mypy semana1/uart_driver/config.py semana1/uart_driver/parsers.py semana1/uart_driver/device.py semana1/uart_driver/recorder.py
py -m ruff check semana1/
```

## Estructura

- `semana0/` — checkpoint inicial: sensor mínimo con test.
- `semana1/dia1/` — Python idiomático: dataclasses, Enum, Protocol.
- `semana1/dia2/` — FSM orientada a objetos.
- `semana1/dia3/` — SOLID: SRP, OCP, LSP.
- `semana1/dia4/` — SOLID: ISP, DIP.
- `semana1/uart_driver/` — Ejercicio integrador "El Driver Modernizado": un driver UART reimplementado con SOLID (ver reflexión abajo).
- `AI_LOG.md` — bitácora de uso de IA durante el curso.

## Reflexión SOLID — "El Driver Modernizado" (Día 5)

El driver original en C mezclaba parsing de protocolos, logging y comunicación en funciones sueltas, con buffers globales — imposible de testear en aislamiento o de instanciar dos veces. Al reimplementarlo con SOLID:

- **SRP:** `UartConfig` solo valida configuración; `DataRecorder` solo persiste; ninguna clase hace más de una cosa.
- **OCP:** agregar un protocolo nuevo (por ejemplo CAN) significa crear una clase nueva de `MessageParser`, sin tocar `ModbusParser` ni `NMEAParser`.
- **LSP:** `ModbusParser` y `NMEAParser` son intercambiables en cualquier lugar donde se espera un `MessageParser`.
- **ISP:** no existe una interfaz "hace-todo"; cada clase implementa solo lo que necesita (`can_parse`/`parse`, o `open`/`close`/`is_open`/`read` en el caso del puerto).
- **DIP:** `UartDevice` depende de las abstracciones `MessageParser` y `SerialPort`, no de implementaciones concretas — por eso se puede testear con un puerto falso (`FakePort`), sin hardware real y sin buffers globales compartidos entre pruebas.

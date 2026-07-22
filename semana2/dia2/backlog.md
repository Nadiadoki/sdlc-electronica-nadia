# Product Backlog — Sistema de monitoreo de sensores

Formato: historia de usuario + escenarios Gherkin + estimación en story points (Fibonacci: 1, 2, 3, 5, 8, 13 — complejidad relativa, no horas).

---

## US-01: Registrar lectura de sensor

Como operador de planta,
quiero registrar la lectura de un sensor con su timestamp,
para tener un historial consultable de las mediciones.

**Story points: 3**

```
Scenario: Registrar una lectura válida
  Given un sensor con id "TEMP-01" registrado en el sistema
  When envío una lectura de 24.3 C con timestamp actual
  Then la lectura se guarda con estado "OK"
  And puedo consultarla en el historial del sensor

Scenario: Rechazar lectura de sensor inexistente
  Given que no existe ningún sensor con id "GHOST-99"
  When envío una lectura para "GHOST-99"
  Then el sistema responde con error 404
```

---

## US-02: Consultar historial de lecturas por sensor

Como operador de planta,
quiero consultar el historial de lecturas de un sensor específico,
para revisar su comportamiento en un rango de tiempo.

**Story points: 3**

```
Scenario: Consultar historial con lecturas registradas
  Given el sensor "TEMP-01" tiene 5 lecturas registradas en las últimas 24 horas
  When consulto el historial de "TEMP-01" para las últimas 24 horas
  Then recibo una lista con las 5 lecturas ordenadas por timestamp

Scenario: Consultar historial de un sensor sin lecturas
  Given el sensor "HUM-02" no tiene lecturas registradas
  When consulto el historial de "HUM-02"
  Then recibo una lista vacía, no un error
```

---

## US-03: Configurar umbral de alerta por sensor

Como administrador del sistema,
quiero configurar un umbral de alerta para cada sensor,
para que el sistema sepa cuándo una lectura es anómala.

**Story points: 2**

```
Scenario: Configurar un umbral válido
  Given el sensor "TEMP-01" no tiene umbral configurado
  When configuro un umbral de 30.0 C para "TEMP-01"
  Then el sensor queda con umbral 30.0 C guardado

Scenario: Rechazar un umbral con valor negativo para un sensor de temperatura
  Given el sensor "TEMP-01" mide en grados Celsius
  When intento configurar un umbral de -500 C
  Then el sistema rechaza la configuración con un mensaje de rango inválido
```

---

## US-04: Recibir notificación cuando se supera un umbral

Como operador de planta,
quiero recibir una notificación cuando una lectura supera el umbral configurado,
para poder reaccionar antes de que se vuelva un problema mayor.

**Story points: 5**

```
Scenario: Notificación disparada al superar el umbral
  Given el sensor "TEMP-01" tiene un umbral de 30.0 C configurado
  When llega una lectura de 35.2 C para "TEMP-01"
  Then se envía una notificación indicando la anomalía y el sensor afectado

Scenario: Sin notificación cuando la lectura está dentro del rango
  Given el sensor "TEMP-01" tiene un umbral de 30.0 C configurado
  When llega una lectura de 24.0 C para "TEMP-01"
  Then no se envía ninguna notificación
```

---

## US-05: Soportar múltiples protocolos de sensor (Modbus y NMEA)

Como integrador de hardware,
quiero que el sistema acepte lecturas tanto en formato Modbus RTU como NMEA,
para poder conectar distintos tipos de sensores sin cambiar el sistema central.

**Story points: 8**

```
Scenario: Registrar una lectura proveniente de un frame Modbus RTU
  Given un dispositivo que envía frames Modbus RTU válidos
  When el sistema recibe un frame Modbus con datos de "TEMP-01"
  Then la lectura se interpreta correctamente y se guarda en el historial

Scenario: Registrar una lectura proveniente de una sentencia NMEA
  Given un dispositivo GPS que envía sentencias NMEA tipo $GPGGA
  When el sistema recibe una sentencia $GPGGA válida
  Then la lectura se interpreta correctamente y se guarda en el historial

Scenario: Rechazar un frame que no coincide con ningún protocolo soportado
  Given un mensaje que no es ni Modbus RTU ni NMEA válido
  When el sistema intenta parsearlo
  Then se registra un error de "protocolo no reconocido" sin detener el sistema
```

---

## Contraste — así NO se escribe una historia (ejemplo ilustrativo, no forma parte del backlog real)

```
## US-XX (así NO)
Como usuario, quiero que el sistema funcione bien,
para tener una buena experiencia.
# Sin rol concreto, sin funcionalidad medible, sin criterio verificable.
```

Este ejemplo puntúa 0: no dice qué rol específico, qué funcionalidad exacta, ni cómo se verificaría que "funciona bien". Todas las historias de arriba evitan este problema con roles concretos, una acción medible y escenarios Gherkin verificables.

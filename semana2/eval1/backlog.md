# Product Backlog — Sistema de monitoreo IoT

**Contexto:** única desarrolladora de un sistema que monitorea 10 sensores de temperatura y humedad, con lecturas cada 30 segundos. Se considera anomalía cuando T > 35°C o H > 80%. El sistema debe alertar cuando detecta una anomalía.

Priorización: **MoSCoW** (Must / Should / Could / Won't this sprint). Estimación: story points Fibonacci (1, 2, 3, 5, 8, 13 — complejidad relativa, no horas).

---

## MUST (núcleo del sistema, sin esto no hay producto)

### US-01: Registrar una lectura de sensor
Como sistema de monitoreo,
quiero registrar cada lectura de un sensor con su tipo (temperatura/humedad) y timestamp,
para tener el dato base sobre el cual detectar anomalías.

**MoSCoW: Must — Story points: 3**
```
Scenario: Registrar una lectura de temperatura válida
  Given un sensor "TEMP-03" de tipo temperatura
  When se registra una lectura de 24.5°C
  Then la lectura queda almacenada con su timestamp

Scenario: Registrar una lectura de humedad válida
  Given un sensor "HUM-07" de tipo humedad
  When se registra una lectura de 55%
  Then la lectura queda almacenada con su timestamp

Scenario: Rechazar una lectura con valor fuera de rango físico posible
  Given un sensor "TEMP-03" de tipo temperatura
  When se intenta registrar una lectura de -500°C
  Then el sistema rechaza la lectura con un error de validación
```

### US-02: Detectar anomalía por temperatura
Como sistema de monitoreo,
quiero detectar cuándo una lectura de temperatura supera el umbral de 35°C,
para poder disparar una alerta a tiempo.

**MoSCoW: Must — Story points: 3**
```
Scenario: Temperatura dentro del rango normal
  Given un sensor de temperatura con umbral 35°C
  When llega una lectura de 30.0°C
  Then no se detecta ninguna anomalía

Scenario: Temperatura supera el umbral
  Given un sensor de temperatura con umbral 35°C
  When llega una lectura de 38.2°C
  Then se detecta una anomalía de temperatura

Scenario: Temperatura exactamente en el umbral
  Given un sensor de temperatura con umbral 35°C
  When llega una lectura de exactamente 35.0°C
  Then no se detecta anomalía (el umbral se supera, no se iguala)
```

### US-03: Detectar anomalía por humedad
Como sistema de monitoreo,
quiero detectar cuándo una lectura de humedad supera el umbral de 80%,
para poder disparar una alerta a tiempo.

**MoSCoW: Must — Story points: 3**
```
Scenario: Humedad dentro del rango normal
  Given un sensor de humedad con umbral 80%
  When llega una lectura de 60%
  Then no se detecta ninguna anomalía

Scenario: Humedad supera el umbral
  Given un sensor de humedad con umbral 80%
  When llega una lectura de 85%
  Then se detecta una anomalía de humedad
```

### US-04: Configurar umbrales por sensor (inyectados, no hardcodeados)
Como administradora del sistema,
quiero que los umbrales de anomalía se configuren e inyecten por sensor,
para poder ajustar la sensibilidad sin tocar el código de detección.

**MoSCoW: Must — Story points: 5**
```
Scenario: Dos sensores con umbrales distintos
  Given un sensor "TEMP-01" con umbral de 35°C y un sensor "TEMP-02" con umbral de 40°C
  When ambos reciben una lectura de 37°C
  Then "TEMP-01" reporta anomalía y "TEMP-02" no

Scenario: Cambiar el umbral de un sensor ya existente
  Given un sensor "TEMP-01" con umbral de 35°C
  When se reconfigura su umbral a 38°C
  Then una lectura de 36°C ya no se considera anomalía
```

### US-05: Enviar alerta por consola cuando hay anomalía
Como operadora de planta,
quiero recibir una alerta impresa en consola apenas se detecta una anomalía,
para reaccionar de inmediato si estoy frente a la terminal.

**MoSCoW: Must — Story points: 3**
```
Scenario: Anomalía dispara alerta por consola
  Given una anomalía detectada en el sensor "TEMP-01" con valor 40°C
  When se procesa la alerta
  Then se imprime en consola un mensaje indicando el sensor y el valor

Scenario: Sin anomalía, no hay alerta
  Given una lectura normal del sensor "TEMP-01"
  When se procesa la alerta
  Then no se imprime ningún mensaje
```

### US-06: Enviar alerta a archivo cuando hay anomalía
Como operadora de planta,
quiero que cada anomalía también quede registrada en un archivo de log,
para poder auditar el histórico de anomalías aunque no esté mirando la consola.

**MoSCoW: Must — Story points: 3**
```
Scenario: Anomalía se registra en archivo
  Given una anomalía detectada en el sensor "HUM-02" con valor 88%
  When se procesa la alerta con estrategia de archivo
  Then el archivo de log contiene una línea con el sensor y el valor

Scenario: Múltiples alertas se acumulan en el mismo archivo
  Given dos anomalías consecutivas de distintos sensores
  When ambas se procesan con estrategia de archivo
  Then el archivo contiene dos líneas, una por cada anomalía
```

---

## SHOULD (importante, pero el sistema funciona sin esto en el primer sprint)

### US-07: Consultar historial de lecturas por sensor
Como operadora de planta,
quiero consultar las últimas lecturas de un sensor específico,
para revisar su comportamiento reciente.

**MoSCoW: Should — Story points: 3**
```
Scenario: Consultar historial con lecturas registradas
  Given el sensor "TEMP-01" con 5 lecturas registradas
  When consulto su historial
  Then recibo las 5 lecturas ordenadas por timestamp

Scenario: Consultar historial de un sensor sin lecturas
  Given el sensor "HUM-05" sin lecturas registradas
  When consulto su historial
  Then recibo una lista vacía, no un error
```

### US-08: Consultar el estado actual de los 10 sensores
Como operadora de planta,
quiero ver de un vistazo el último valor reportado por cada uno de los 10 sensores,
para tener una foto general del estado de la bodega.

**MoSCoW: Should — Story points: 5**
```
Scenario: Todos los sensores han reportado al menos una vez
  Given los 10 sensores con al menos una lectura cada uno
  When consulto el estado general
  Then recibo el último valor de cada uno de los 10 sensores

Scenario: Un sensor todavía no ha reportado
  Given 9 sensores con lecturas y 1 sensor sin ninguna lectura todavía
  When consulto el estado general
  Then el sensor sin lecturas aparece marcado como "sin datos", no como error
```

### US-09: Simular múltiples sensores enviando lecturas periódicas
Como desarrolladora,
quiero un simulador que genere lecturas para los 10 sensores cada 30 segundos,
para poder probar el sistema completo sin hardware real.

**MoSCoW: Should — Story points: 8**
```
Scenario: El simulador genera una lectura por sensor en cada ciclo
  Given 10 sensores configurados en el simulador
  When transcurre un ciclo de simulación
  Then se genera exactamente una lectura por cada uno de los 10 sensores

Scenario: El simulador puede generar valores anómalos ocasionalmente
  Given el simulador configurado con una probabilidad de anomalía
  When se ejecutan suficientes ciclos
  Then al menos una lectura supera el umbral de anomalía configurado
```

---

## COULD (deseable si sobra tiempo, no crítico)

### US-10: Exportar historial de alertas a JSON
Como administradora del sistema,
quiero exportar el historial de alertas a un archivo JSON,
para poder analizarlo con otras herramientas.

**MoSCoW: Could — Story points: 2**
```
Scenario: Exportar alertas existentes
  Given 3 alertas registradas en el sistema
  When exporto el historial a JSON
  Then el archivo generado contiene un arreglo con las 3 alertas
```

### US-11: Dashboard simple en consola con resumen periódico
Como operadora de planta,
quiero un resumen impreso cada cierto tiempo con el número de anomalías detectadas,
para monitorear la salud general sin revisar cada sensor manualmente.

**MoSCoW: Could — Story points: 5**
```
Scenario: Resumen sin anomalías en el período
  Given ninguna anomalía detectada en la última hora
  When se genera el resumen periódico
  Then el resumen indica "0 anomalías en la última hora"

Scenario: Resumen con anomalías detectadas
  Given 3 anomalías detectadas en la última hora
  When se genera el resumen periódico
  Then el resumen indica "3 anomalías en la última hora" con el detalle de cada sensor
```

---

## WON'T (explícitamente fuera de alcance este sprint)

### US-12: Notificación por email/SMS
Como operadora de planta, quiero recibir alertas por correo o SMS además de consola/archivo.
**MoSCoW: Won't this sprint** — requiere integración con servicios externos (SMTP/SMS gateway) que no forman parte del alcance del Sprint 1; se reevaluará en un sprint futuro.

### US-13: Panel web de visualización
Como operadora de planta, quiero un dashboard web con gráficas en tiempo real.
**MoSCoW: Won't this sprint** — implica un frontend completo; fuera de alcance mientras el núcleo de detección de anomalías no esté probado y estable.

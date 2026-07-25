# Sprint 1 Planning

## Sprint Goal

**Detectar y alertar automáticamente cuando cualquiera de los 10 sensores reporte una lectura anómala de temperatura o humedad, con umbrales configurables por sensor y alertas duales (consola + archivo).**

Este objetivo se eligió porque es el núcleo mínimo funcional del sistema: sin registrar lecturas, detectar anomalías y alertar, no hay producto que mostrar. Todo lo demás (historial, dashboard, simulador) depende de que este núcleo exista y esté probado.

---

## Historias seleccionadas para este Sprint (6 de las 13 del backlog)

Se seleccionaron las 6 historias **Must** del backlog, dejando explícitamente fuera las Should/Could/Won't para no comprometer la calidad del núcleo por abarcar de más.

| Historia | Story points | Justificación de por qué entra en este sprint |
|---|---|---|
| US-01: Registrar lectura de sensor | 3 | Es el dato de entrada de todo el sistema; sin esto no hay nada que analizar. |
| US-02: Detectar anomalía por temperatura | 3 | Parte directa del Sprint Goal. |
| US-03: Detectar anomalía por humedad | 3 | Parte directa del Sprint Goal. |
| US-04: Configurar umbrales por sensor (inyectados) | 5 | El Sprint Goal exige umbrales *configurables*, no un valor fijo en el código — esto es lo que hace la detección reutilizable para los 10 sensores con distintas sensibilidades. |
| US-05: Alerta por consola | 3 | Parte directa del Sprint Goal ("alertas duales"). |
| US-06: Alerta a archivo | 3 | Parte directa del Sprint Goal ("alertas duales"). |

**Total: 20 story points.**

Historias explícitamente fuera de este Sprint (y por qué): US-07/US-08 (consultas de historial y estado) dependen de que el núcleo de detección ya exista y sea confiable; US-09 (simulador) es una herramienta de prueba, no parte del producto en sí — se deja como extensión opcional; US-10/US-11 son mejoras de valor agregado, no críticas; US-12/US-13 quedaron descartadas explícitamente (Won't) por alcance.

---

## Desglose en tareas (todas ≤ 4 horas)

### US-01: Registrar lectura de sensor
- [ ] Escribir test RED: registrar lectura válida (1h)
- [ ] Implementar `SensorReading` (dataclass) y método `record()` mínimo — GREEN (1h)
- [ ] Escribir test RED: rechazar lectura fuera de rango físico (1h)
- [ ] Implementar validación de rango — GREEN (1h)

### US-02 y US-03: Detectar anomalía (temperatura y humedad)
- [ ] Escribir tests RED: dentro de rango, supera umbral, umbral exacto (1.5h)
- [ ] Implementar `AnomalyDetector` con lógica de comparación — GREEN (1.5h)
- [ ] Refactor: unificar lógica de temperatura y humedad si aplica (1h)

### US-04: Umbrales inyectados por sensor
- [ ] Escribir test RED: dos sensores con umbrales distintos (1h)
- [ ] Implementar inyección de umbral en el constructor de `AnomalyDetector` — GREEN (1.5h)
- [ ] Escribir test RED + GREEN: reconfigurar umbral existente (1.5h)

### US-05 y US-06: Alertas (consola y archivo)
- [ ] Escribir test RED: `AlertStrategy` abstracta + `ConsoleAlert` (1h)
- [ ] Implementar `AlertStrategy`, `ConsoleAlert` — GREEN (1h)
- [ ] Escribir test RED: `FileAlert` escribe en archivo (1h)
- [ ] Implementar `FileAlert` y `AlertManager` que orquesta ambas — GREEN (1.5h)

Cada tarea queda dentro del límite de 4 horas exigido; las historias más grandes (US-02/03, US-04, US-05/06) se dividieron en sub-tareas de test + implementación por separado, siguiendo el mismo patrón RED→GREEN que ya se usó en la semana 2, día 3.

---

## Definition of Done (aplica a este Sprint)

Ver `semana2/dia4/DEFINITION_OF_DONE.md` para el detalle completo en Gherkin. Resumen aplicado a este Sprint:

- Cobertura de tests ≥ 80% en el código de `semana2/eval1/`.
- `ruff check` sin errores.
- `mypy` sin errores en el código de producción (tests excluidos, según se decidió el día 4).
- Cada historia implementada con TDD estricto: commit de test (RED) antes que el commit de código (GREEN), con refactor cuando aplique.
- Bitácora de IA con al menos 3 entradas específicas de esta evaluación.
- Sprint Retrospective completada al final.

# Ficha de Sistematización — Espiral 2
## ERP Django · Espiral E2: Modelado de Datos y ORM
## UTEC Celaya · Técnico en Programación (SEP 3061300006-23)

| Campo | Contenido |
|---|---|
| **Número de espiral** | 2 |
| **Nombre del ciclo** | Modelado de Datos y ORM |
| **Semanas** | W04 – W06 |
| **Fecha de inicio** | 14/10/2026 |
| **Fecha de cierre** | (completar en W06) |
| **Responsable** | [Nombre del estudiante] |
| **Asesor** | MC. Román Fernando López González |

---

## 1. Objetivo del ciclo

Diseñar, implementar y validar el esquema de base de datos completo del
ERP en Django, garantizando integridad referencial, normalización 3FN y
cobertura de pruebas ≥ 15 tests de modelo.

---

## 2. Tareas realizadas

| # | Tarea | Estado | Tiempo invertido |
|---|---|---|---|
| 1 | Diseño diagrama ER (8 entidades) | ✅ W04 | h:mm |
| 2 | Normalización 3FN y decisiones de diseño | ✅ W04 | h:mm |
| 3 | Aprobación del asesor | ⏳ W04 | — |
| 4 | Implementar models.py × 5 apps | ⏳ W05 | — |
| 5 | Ejecutar makemigrations + migrate | ⏳ W05 | — |
| 6 | Registrar en admin.py | ⏳ W05 | — |
| 7 | Agregar validators | ⏳ W06 | — |
| 8 | Suite de ≥ 15 tests de modelo | ⏳ W06 | — |
| 9 | Instalar django-jazzmin | ⏳ W06 | — |

---

## 3. Evidencias generadas (completar durante W04–W06)

- [ ] Diagrama ER aprobado: `docs/diagramas/diagrama_er.md`
- [ ] Imagen exportada: `evidencias/espiral_02/diagrama_er.png`
- [ ] Decisiones de diseño: `docs/decisiones_diseno.md`
- [ ] Tabla de entidades: `docs/entidades_atributos.md`
- [ ] Migraciones: `*/migrations/0001_initial.py` × 5 apps
- [ ] Tests: `tests/test_models.py` — resultado: ___/15 OK

---

## 4. Criterios de aceptación (se verifican en W06)

| Criterio | Estado | Evidencia |
|---|---|---|
| Diagrama ER aprobado por el asesor | ⏳ | Firma en ficha |
| `showmigrations` → `[X] 0001_initial` en 5 apps | ⏳ | Terminal |
| `/admin/` muestra las 8 entidades | ⏳ | Captura |
| ≥ 15 tests de modelo PASSED | ⏳ | Salida de tests |
| Precio negativo → ValidationError | ⏳ | Test específico |
| Correo duplicado → IntegrityError | ⏳ | Test específico |

---

## 5. Problemas encontrados y soluciones
(registrar en el momento en que ocurran — Kaizen del Sprint 0)

| Fecha | Síntoma | Causa | Solución | Cómo evitarlo |
|---|---|---|---|---|
| 14/10/2026 | `git add` ignoró `fichas/` | Regla `fichas/` en `.gitignore` línea 24 | Quitar la regla / `git add -f` | Revisar `.gitignore` al crear carpetas de entregables |

---

## 6. Lecciones aprendidas
(completar al cerrar en W06)

1.
2.
3.

---

## 7. Tiempo total invertido
(completar al cerrar en W06)

| Categoría | Horas |
|---|---|
| Diseño / planeación | |
| Implementación | |
| Pruebas | |
| Documentación | |
| **Total Espiral 2** | |

---

## 8. Aprobación formal del diagrama ER

| Rol | Nombre | Fecha | Observaciones |
|---|---|---|---|
| Desarrollador | [Nombre] | | |
| **Asesor (PO)** | **MC. Román Fernando López González** | | |

> ⚠️ **La W05 no puede iniciar sin la aprobación registrada aquí.**
> Cuando el asesor apruebe, escribir en Observaciones: `Aprobado ✅`
> (el arranque de W05 lo verifica con `findstr /i "Aprobado"`).

[ ] Fechas de inicio y cierre correctas
[ ] Tabla de tareas: todos en ✅ con tiempos reales
[ ] Evidencias: URL de Render, resultado de showmigrations, resultado de tests
[ ] git log --oneline -5 pegado en el campo de evidencias
[ ] Criterios de aceptación: todos marcados ✅
[ ] Al menos 1 problema encontrado documentado con su solución
[ ] 3 lecciones aprendidas redactadas
[ ] Tiempo total invertido calculado (W04 + W05 + W06)
[ ] Campo "Aprobación formal" con fecha y observaciones del asesor
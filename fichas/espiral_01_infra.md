# Ficha de Sistematización — Espiral 1
## ERP Django · Espiral E1: Infraestructura y Configuración Base
## UTEC Celaya · Técnico en Programación (SEP 3061300006-23)

| Campo | Contenido |
|---|---|
| **Número de espiral** | 1 |
| **Nombre del ciclo** | Infraestructura y Configuración Base |
| **Semanas** | W01 – W03 |
| **Fecha de inicio** | 02_/10/2026|
| **Fecha de cierre** | 09/10/2026|
| **Responsable** | [Josef Giovanny Moya Torres] |
| **Asesor** | MC. Román Fernando López González |

---

## 1. Objetivo del ciclo

Establecer el entorno de desarrollo portable en USB y desplegar el
proyecto Django base en Render.com, de modo que cualquier avance
posterior tenga una URL pública verificable desde el inicio del proyecto.

---

## 2. Tareas realizadas

| # | Tarea | Estado | Tiempo invertido |
|---|---|---|---|
| 1 | Configurar Python 3.11 embeddable en USB | ✅ | h:mm |
| 2 | Instalar pip y virtualenv | ✅ | h:mm |
| 3 | Configurar Git Portable | ✅ | h:mm |
| 4 | Crear scripts iniciar/finalizar sesión | ✅ | h:mm |
| 5 | Crear proyecto Django con 5 apps | ✅ | h:mm |
| 6 | Sistema de templates Fable 5 AzulERP | ✅ | h:mm |
| 7 | Configurar WhiteNoise y estáticos | ✅ | h:mm |
| 8 | Completar settings_prod.py con PostgreSQL | ✅ | h:mm |
| 9 | Crear Procfile, Dockerfile, docker-compose.yml | ✅ | h:mm |
| 10 | Crear render.yaml | ✅ | h:mm |
| 11 | Desplegar en Render.com → URL pública | ✅ | h:mm |
| 12 | Ejecutar Sprint 0 Review y Retrospectiva | ✅ | h:mm |

---

## 3. Evidencias generadas

- [ ] Repositorio GitHub: `https://github.com/tu-usuario/erp-django-utec`
- [ ] URL pública Render: `https://erp-django-utec.onrender.com`
- [ ] Captura de pantalla: `evidencias/espiral_01/render_url.png`
- [ ] Captura de pantalla: `evidencias/espiral_01/manage_check.png`
- [ ] Resultado de tests: `Ran 33 tests in X.XXXs — OK`
- [ ] Commit de cierre:
4e0f2dd (HEAD -> main, origin/main, origin/HEAD) Corregir iniciar_sesion.bat: copiar desde la raiz del USB e incluir .git
8a351e9 Reescribir .gitignore y quitar System Volume Information del repo
102d5da Arreglar PATH de git en finalizar_sesion.bat
4967690 Prueba de flujo USB
a52cb60 Quitar instalador PortableGit del repositorio
c9715bd Actualizar .gitignore y quitar herramientas portables y WorkSpace_ERP del indice
280aa94 Sprint 0 CIERRE [M1]: fichas Schmelkes + retrospectiva + evidencias
c53947a Sprint 0 CIERRE [M1]: Render.com desplegado + tests OK + Ficha Schmelkes E1
a6d773e Fix: DEBUG = False con formato estandar
3885278 Sprint 0 W03: settings_prod + Procfile + Dockerfile + render.yaml
8847098 Sprint 0 W03: <descripcion del trabajo>
32a79fd Sprint 0 W02: estado actual del proyecto
03f6b28 Sprint 0 W02: actualizacion del proyecto
4d84670 Sprint 0 W01: entorno portable + proyecto Django base + 5 apps

---

## 4. Criterios de aceptación verificados

| Criterio | ¿Cumplido? | Evidencia |
|---|---|---|
| `manage.py check --deploy` sin warnings críticos | ✅ / ❌ | Captura de terminal |
| URL pública `https://…onrender.com/` → HTTP 200 | ✅ / ❌ | Captura del navegador |
| Repositorio con ≥ 6 commits en rama `main` | ✅ / ❌ | `git log --oneline` |
| 33 tests pasando (W01 + W02 + W03) | ✅ / ❌ | Resultado pytest |
| Ficha Schmelkes E1 completa | ✅ / ❌ | Este documento |

---

## 5. Problemas encontrados y soluciones

| Problema | Causa | Solución aplicada |
|---|---|---|
| Render proponía un plan de $7/mes | Plan de pago seleccionado por defecto | Cambiar a Free |
| Start Command era gunicorn app:app | Valor genérico autocompletado | Reemplazar por gunicorn core.wsgi |
| No existe la pestaña Shell | No está en el plan gratis | Crear superusuario con variables de entorno |
| fichas/ no se subía a GitHub | Regla fichas/ en .gitignore | Quitar la regla y usar git add -f |
| Falló test de DEBUG | Espacios extra en DEBUG = False | Dejar un solo espacio |
---

## 6. Lecciones aprendidas

1. Los valores autocompletados de una plataforma (plan, comandos de inicio, runtime) se deben revisar uno por uno antes de desplegar.
2. Los tests de configuración detectan errores de formato antes de llegar a producción.
3. Hay que revisar `git status` y `.gitignore` antes de cada commit para no dejar archivos sin subir.

---

## 7. Tiempo total invertido

| Categoría | Horas |
|---|---|
| Diseño / planeación | |
| Implementación | |
| Pruebas | |
| Despliegue | |
| Documentación | |
| **Total Espiral 1** | |

---

## 8. Conexión con el trabajo recepcional

> Esta espiral aporta evidencia para el **Capítulo 4** (Desarrollo),
> sección 4.1 "Espiral 1: Infraestructura", y para el
> **Capítulo 3** (Metodología), subsección "Ciclos del modelo espiral".
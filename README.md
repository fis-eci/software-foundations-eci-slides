<div align="center">

# 🎯 Software Foundations ECI — Presentaciones

**Diapositivas interactivas de HTML para los cursos de Fundamentos de Ingeniería de Software**

[![License](https://img.shields.io/badge/Licencia-Apache%202.0-blue.svg)](./LICENSE)
[![HTML](https://img.shields.io/badge/Tecnología-HTML%20%2B%20CSS-orange.svg)](.)
[![Slides](https://img.shields.io/badge/Diapositivas-60%20slides-blue.svg)](.)
[![Institución](https://img.shields.io/badge/ECI-Julio%20Garavito-red.svg)](https://www.escuelaing.edu.co)

<br/>

*Escuela Colombiana de Ingeniería Julio Garavito · 2026*

</div>

---

## 📌 Repositorio Principal

> Este repositorio contiene **únicamente las presentaciones en HTML** generadas para los temas del curso.
> El material completo del objeto de aprendizaje — ejercicios, guías, laboratorios y recursos — se encuentra en el repositorio principal:
>
> ### 👉 [fis-eci/software-foundations-eci](https://github.com/fis-eci/software-foundations-eci)
>
> 📚 *Unidad de aprendizaje (UA) para Fundamentos de Ingeniería de Software. Guía integral para los cursos DOPO (Desarrollo Orientado por Objetos) y MYSD (Modelos y Servicios de Datos) en la Escuela Colombiana de Ingeniería. Cubre distintos temas de ambas asignaturas y buenas prácticas de calidad de software.*

---

## 🗂️ Presentaciones Disponibles

Este repositorio genera **6 presentaciones de una sola página** (archivos `.html` auto-contenidos), una por cada tema:

| # | Archivo | Tema | Slides | Cursos |
|---|---------|------|:------:|--------|
| 1 | [`CVS-presentation.html`](./CVS-presentation.html) | Control de Versiones con Git & GitHub | 16 | MYSD & DOPO |
| 2 | [`PruebasUnitarias-presentation.html`](./PruebasUnitarias-presentation.html) | Pruebas Unitarias en Java (JUnit + BlueJ) | 9 | DOPO |
| 3 | [`OracleSQL-presentation.html`](./OracleSQL-presentation.html) | Entornos Oracle SQL Developer | 11 | MYSD |
| 4 | [`SQL-PostgreVSC-presentation.html`](./SQL-PostgreVSC-presentation.html) | PostgreSQL en VS Code | 12 | MYSD |
| 5 | [`Analisis-Eclipse-presentation.html`](./Analisis-Eclipse-presentation.html) | Análisis de Software en Eclipse IDE | 15 | DOPO |
| 6 | [`Analisis-VSC-presentation.html`](./Analisis-VSC-presentation.html) | Análisis de Software en VS Code | 13 | DOPO |

### 🎨 Temas visuales por mazo

| Mazo | Fondo | Acento principal | Acento secundario |
|------|-------|-----------------|-------------------|
| CVS | `#0d1117` (GitHub Dark) | `#58a6ff` azul | `#3fb950` verde |
| Oracle SQL | `#0a0e27` (Navy oscuro) | `#00ffff` cian | `#ff6b35` naranja |
| Pruebas Unitarias | `#003366` (Java Blue) | `#f89820` naranja | `#4caf50` verde |

---

## 🎬 Cómo Ver las Presentaciones

### Opción A — En línea (sin descargar nada)

Accede directamente desde el navegador mediante **GitHub Pages**:

| Presentación | Enlace directo |
|---|---|
| Página principal | 🔗 [fis-eci.github.io/software-foundations-eci-slides](https://fis-eci.github.io/software-foundations-eci-slides/) |
| Control de Versiones (CVS) | 🔗 [CVS-presentation.html](https://fis-eci.github.io/software-foundations-eci-slides/CVS-presentation.html) |
| Pruebas Unitarias | 🔗 [PruebasUnitarias-presentation.html](https://fis-eci.github.io/software-foundations-eci-slides/PruebasUnitarias-presentation.html) |
| Oracle SQL Developer | 🔗 [OracleSQL-presentation.html](https://fis-eci.github.io/software-foundations-eci-slides/OracleSQL-presentation.html) |
| PostgreSQL en VS Code | 🔗 [SQL-PostgreVSC-presentation.html](https://fis-eci.github.io/software-foundations-eci-slides/SQL-PostgreVSC-presentation.html) |
| Análisis Software Eclipse | 🔗 [Analisis-Eclipse-presentation.html](https://fis-eci.github.io/software-foundations-eci-slides/Analisis-Eclipse-presentation.html) |
| Análisis Software VS Code | 🔗 [Analisis-VSC-presentation.html](https://fis-eci.github.io/software-foundations-eci-slides/Analisis-VSC-presentation.html) |

### Opción B — Abrir localmente

1. Clona o descarga este repositorio.
2. Abre cualquier archivo `*-presentation.html` con tu navegador (doble clic o arrastrar).
3. Usa los controles de navegación en la barra inferior.

### Opción C — Reconstruir desde las fuentes

Si modificas alguna diapositiva individual, ejecuta el script de construcción para regenerar las presentaciones:

```bash
# Requiere Python 3.x (sin dependencias externas)
python build_presentations.py
```

Esto lee todas las diapositivas de las carpetas fuente y produce los tres archivos `.html` listos para presentar.

### ⌨️ Atajos de teclado

| Tecla | Acción |
|-------|--------|
| `→` / `Espacio` | Diapositiva siguiente |
| `←` | Diapositiva anterior |
| `Inicio` | Primera diapositiva |
| `Fin` | Última diapositiva |
| `F` | Pantalla completa |

---

## 🏗️ Estructura del Repositorio

```
software-foundations-eci-slides/
│
├── 📁 CVS - MYSD & DOPO/          # Fuentes: 16 diapositivas de Control de Versiones
│   ├── 1-slide.html  →  16-slide.html
│   └── ...
│
├── 📁 Oracle SQL Developer - MYSD/ # Fuentes: 11 diapositivas de Oracle SQL
│   ├── 1-slide.html  →  11-slide.html
│   └── ...
│
├── 📁 Pruebas Unitarias - DOPO/    # Fuentes: 9 diapositivas de Pruebas Unitarias
│   ├── 1-slide.html  →  9-slide.html
│   └── ...
│
├── 📄 CVS-presentation.html        # ✅ Presentación auto-contenida (generada)
├── 📄 OracleSQL-presentation.html  # ✅ Presentación auto-contenida (generada)
├── 📄 PruebasUnitarias-presentation.html # ✅ Presentación auto-contenida (generada)
│
├── 🌐 index.html                   # Página de inicio (GitHub Pages)
├── 🐍 build_presentations.py       # Script que fusiona las diapositivas
├── 📄 CLAUDE.md                    # Guía para Claude Code
└── 📄 README.md                    # Este archivo
```

> Cada diapositiva fuente (`N-slide.html`) es un archivo HTML **auto-contenido de 1280×720 px** con todo el CSS embebido. El script de construcción las combina dentro de un `<iframe srcdoc>` que garantiza aislamiento total de estilos entre diapositivas.

---

## 🔨 Sistema de Construcción

El script `build_presentations.py` implementa las siguientes etapas:

1. **Lee** las diapositivas en orden numérico (`1-slide.html`, `2-slide.html`, …).
2. **Escapa** el HTML para incrustarlo en template literals de JavaScript (manejo especial de backticks, `</script>` y `${`).
3. **Genera** una cáscara HTML con barra de navegación, barra de progreso, escalado responsivo y soporte de pantalla completa.
4. **Verifica** que el número de diapositivas incrustadas coincida con el esperado.

Las presentaciones resultantes son archivos únicos, sin dependencias externas en tiempo de ejecución, que funcionan offline.

---

## 👤 Autor

<table>
<tr>
<td align="center">
<b>Andersson David Sánchez Méndez</b><br/>
Monitor Académico — MYSD &amp; DOPO<br/>
Escuela Colombiana de Ingeniería Julio Garavito<br/>
<br/>
<a href="mailto:andersson.sanchez-m@mail.escuelaing.edu.co">📧 andersson.sanchez-m@mail.escuelaing.edu.co</a><br/>
<a href="https://github.com/fis-eci">🐙 github.com/fis-eci</a>

<a href="https://github.com/AnderssonProgramming">🐙 github.com/AnderssonProgramming</a>
</td>
</tr>
</table>

---

## 🤝 Soporte y Contacto

¿Tienes dudas sobre el contenido, encuentras un error o quieres proponer una mejora?

- **GitHub Issues** *(recomendado)*: abre un issue en [fis-eci/software-foundations-eci](https://github.com/fis-eci/software-foundations-eci/issues) o en este mismo repositorio
- **Correo institucional**: [fis@escuelaing.edu.co](mailto:fis@escuelaing.edu.co)

---

## 📄 Licencia

```
Apache License 2.0 — Copyright 2026 Andersson David Sánchez Méndez
```

Este proyecto está distribuido bajo la [Licencia Apache 2.0](./LICENSE). Puedes usar, copiar, modificar y redistribuir el material libremente, incluso con fines comerciales, siempre que se incluya el aviso de derechos de autor y la licencia original.

---

<div align="center">

*Hecho con ❤️ para los estudiantes de Fundamentos de Ingeniería de Software · ECI 2026*

</div>

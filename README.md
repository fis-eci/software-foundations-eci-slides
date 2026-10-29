<div align="center">

# 🎯 Software Foundations ECI — Presentaciones

**Diapositivas interactivas de HTML para los cursos de Fundamentos de Ingeniería de Software**

[![License](https://img.shields.io/badge/Licencia-Apache%202.0-blue.svg)](./LICENSE)
[![HTML](https://img.shields.io/badge/Tecnología-HTML%20%2B%20CSS-orange.svg)](.)
[![Slides](https://img.shields.io/badge/Diapositivas-75%20slides-blue.svg)](.)
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
| 6 | [`Analisis-VSC-presentation.html`](./Analisis-VSC-presentation.html) | Análisis de Software en VS Code | 12 | DOPO |

### 🎨 Sistema de diseño

Todas las diapositivas comparten un único sistema de diseño (`design-system/`) con identidad de la **Escuela Colombiana de Ingeniería Julio Garavito**: logo oficial en portada y emblema en cada diapositiva, tipografía unificada (**Inter** para texto y **JetBrains Mono** para código), tarjetas de vidrio, animaciones de entrada coreografiadas, una esfera 3D en las portadas y una barra de progreso en el pie de página. Cada mazo conserva su paleta:

| Mazo | Fondo | Acento principal | Acento secundario | Terciario |
|------|-------|-----------------|-------------------|-----------|
| CVS | `#05070d` | `#58a6ff` azul | `#2ea44f` verde | `#a371f7` violeta |
| Oracle SQL | `#050820` (Navy) | `#00d4ff` cian | `#ff6b35` naranja | `#00ff88` verde |
| PostgreSQL VSC | `#040814` (Deep navy) | `#4fc3f7` cian | `#00e58a` verde | `#ff6b35` naranja |
| Pruebas Unitarias | `#031128` (Azul Java) | `#f89820` naranja | `#4caf50` verde | `#4f8ff7` azul |
| Análisis Eclipse | `#05070d` | `#f89820` naranja | `#58a6ff` azul | `#2ea44f` verde |
| Análisis VS Code | `#05070d` | `#2f9bff` azul VS Code | `#4fc3f7` cian | `#2ea44f` verde |

En los mazos de análisis, cada herramienta tiene un color fijo: SonarLint `#4f9dff`, PMD `#ff9f43`, JaCoCo `#34d399` y PIT `#f87171`.

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

Si modificas alguna diapositiva o el sistema de diseño, ejecuta el script de construcción para sincronizar el diseño y regenerar las presentaciones:

```bash
# Requiere Python 3.x (sin dependencias externas)
python build_presentations.py
```

Esto incrusta el sistema de diseño en cada diapositiva y produce los seis archivos `*-presentation.html` listos para presentar. Con `python build_presentations.py --sync` solo se actualizan las diapositivas.

### ⌨️ Atajos de teclado

| Tecla | Acción |
|-------|--------|
| `→` / `Espacio` / `Av Pág` | Diapositiva siguiente |
| `←` / `Re Pág` | Diapositiva anterior |
| `Inicio` / `Fin` | Primera / última diapositiva |
| `G` | Vista general con miniaturas de todas las diapositivas |
| `F` | Pantalla completa (modo inmersivo: la barra aparece al acercar el mouse) |
| Deslizar | Navegación táctil en celulares y tabletas |

Puedes enlazar una diapositiva concreta agregando `#n` a la URL (por ejemplo, `CVS-presentation.html#5`).

---

## 🏗️ Estructura del Repositorio

```
software-foundations-eci-slides/
│
├── 📁 CVS - MYSD & DOPO/                    # Fuentes: 16 diapositivas de Control de Versiones
│   ├── 1-slide.html  →  16-slide.html
│   └── ...
│
├── 📁 Oracle SQL Developer - MYSD/          # Fuentes: 11 diapositivas de Oracle SQL
│   ├── 1-slide.html  →  11-slide.html
│   └── ...
│
├── 📁 PostgreSQL VSC - MYSD/                # Fuentes: 12 diapositivas de PostgreSQL en VS Code
│   ├── 1-slide.html  →  12-slide.html
│   └── ...
│
├── 📁 Pruebas Unitarias - DOPO/             # Fuentes: 9 diapositivas de Pruebas Unitarias
│   ├── 1-slide.html  →  9-slide.html
│   └── ...
│
├── 📁 Analisis Software Eclipse - DOPO/     # Fuentes: 15 diapositivas de Análisis en Eclipse
│   ├── 1-slide.html  →  15-slide.html
│   └── ...
│
├── 📁 Analisis Software VSC - DOPO/         # Fuentes: 12 diapositivas de Análisis en VS Code
│   ├── 1-slide.html  →  12-slide.html
│   └── ...
│
├── 📄 CVS-presentation.html                 # ✅ Presentación auto-contenida (generada)
├── 📄 OracleSQL-presentation.html           # ✅ Presentación auto-contenida (generada)
├── 📄 SQL-PostgreVSC-presentation.html      # ✅ Presentación auto-contenida (generada)
├── 📄 PruebasUnitarias-presentation.html    # ✅ Presentación auto-contenida (generada)
├── 📄 Analisis-Eclipse-presentation.html    # ✅ Presentación auto-contenida (generada)
├── 📄 Analisis-VSC-presentation.html        # ✅ Presentación auto-contenida (generada)
│
├── 🎨 design-system/                        # Fuente única del diseño
│   ├── eci-slides.css                       # Tokens, componentes, temas por mazo y animaciones
│   ├── eci-slides.js                        # Coreografía de entrada, esfera 3D, tilt y auditoría (#qa)
│   ├── eci-logo.svg                         # Logo oficial ECI (Wikimedia Commons, CC BY-SA 4.0)
│   └── eci-emblem.svg                       # Emblema ECI para la barra superior
│
├── 🌐 index.html                            # Página de inicio (GitHub Pages)
├── 🐍 build_presentations.py                # Sincroniza el diseño y fusiona las diapositivas
├── 📄 CLAUDE.md                             # Guía para Claude Code
└── 📄 README.md                             # Este archivo
```

> Cada diapositiva fuente (`N-slide.html`) es un archivo HTML **auto-contenido de 1280×720 px**: el script de construcción incrusta el sistema de diseño entre marcadores (`<!--eci:head-->`, `<!--eci:frame-->`, `<!--eci:logo-->`), así cada archivo funciona por sí solo y todos comparten la misma fuente de estilos. Luego las combina dentro de un `<iframe srcdoc>` que garantiza aislamiento total de estilos entre diapositivas.

---

## 🔨 Sistema de Construcción

El script `build_presentations.py` implementa las siguientes etapas:

1. **Sincroniza** el sistema de diseño (`design-system/`) dentro de cada diapositiva y de `index.html`: CSS, JS, logo, marco institucional y número de página.
2. **Lee** las diapositivas en orden numérico (`1-slide.html`, `2-slide.html`, …).
3. **Escapa** el HTML para incrustarlo en template literals de JavaScript (manejo especial de backticks, `</script>` y `${`).
4. **Genera** una cáscara HTML con transiciones entre diapositivas, vista general con miniaturas, escalado responsivo, gestos táctiles y modo inmersivo de pantalla completa.
5. **Verifica** que el número de diapositivas incrustadas coincida con el esperado.

Las presentaciones resultantes son archivos únicos; solo las fuentes (Google Fonts), los íconos (Font Awesome) y las miniaturas de video se cargan desde CDN.

Para revisar el diseño de una diapositiva abre `N-slide.html#static` (sin animaciones) o `N-slide.html#static-qa`, que añade al DOM un reporte (`#qa-report`) con elementos desbordados o recortados.

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

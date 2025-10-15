# 📊 Pipeline ETL - Stock Sentiment Analysis

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-green)
![Plotly](https://img.shields.io/badge/Plotly-5.14%2B-purple)
![Status](https://img.shields.io/badge/Status-Completed-success)

---

## 📋 Descripción del Proyecto

Este proyecto implementa un **pipeline ETL (Extract, Transform, Load)** completo para el análisis de sentimientos en noticias financieras. El sistema extrae datos de noticias del mercado de valores, los limpia y transforma, y genera visualizaciones interactivas para análisis exploratorio.

### 🎯 Objetivos Alcanzados

✅ **Pipeline ETL modular** con arquitectura Extract-Transform-Load  
✅ **Extracción robusta** con detección automática de encoding  
✅ **Transformación completa** con 7 operaciones de limpieza  
✅ **Carga multi-formato** (CSV, Parquet, SQLite)  
✅ **5 visualizaciones interactivas** en HTML con Plotly  
✅ **Conclusiones basadas en datos reales** (4,101 registros, 2000-2016)  
✅ **Git con 10+ commits** y 2 ramas (main, develop)  
✅ **Documentación completa** y profesional  

---

## 🗂️ Estructura del Proyecto

```
par_2DB/
│
├── 📁 Extract/                      # Módulo de Extracción
│   ├── __init__.py
│   └── stock_extractor.py          # Extrae y valida datos CSV
│
├── 📁 Transform/                    # Módulo de Transformación
│   ├── __init__.py
│   └── stock_transformer.py        # Limpia y transforma datos
│
├── 📁 Load/                         # Módulo de Carga
│   ├── __init__.py
│   └── stock_loader.py             # Carga en múltiples formatos
│
├── 📁 data/                         # Datos procesados (auto-generados)
│   ├── stock_senti_clean.csv       # CSV limpio (7.4 MB)
│   ├── stock_senti_clean.parquet   # Parquet comprimido (5.6 MB)
│   └── stock_senti_clean.db        # SQLite con índices (10.1 MB)
│
├── 📄 main.py                       # Pipeline ETL completo
├── 📄 generate_analysis.py         # Genera visualizaciones HTML
├── 📄 analysis_report.html         # Reporte interactivo (resultado final)
├── 📄 stock_senti_analysis.csv     # Dataset original (fuente)
├── 📄 requirements.txt             # Dependencias del proyecto
├── 📄 .gitignore                   # Archivos ignorados por Git
└── 📄 README.md                    # Esta documentación
```

---

## 🚀 Instalación y Configuración

### Prerrequisitos

- **Python 3.10+** (recomendado)
- **pip** (gestor de paquetes)
- **Git** (control de versiones)

### Instalación Rápida

```bash
# 1. Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>
cd par_2DB

# 2. Crear entorno virtual (recomendado)
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

### Dependencias Principales

```
pandas>=2.0.0          # Procesamiento de datos
numpy>=1.24.0          # Operaciones numéricas
plotly>=5.14.0         # Visualizaciones interactivas
matplotlib>=3.7.0      # Gráficos estáticos
seaborn>=0.12.0        # Visualizaciones estadísticas
fastparquet>=2023.4.0  # Soporte Parquet
pyarrow>=12.0.0        # Engine Parquet alternativo
```

---

## 💻 Uso del Proyecto

### Ejecutar Pipeline ETL

```bash
python main.py
```

**¡Eso es todo!** El script automáticamente:
1. ✅ Ejecuta el pipeline ETL completo
2. ✅ Genera todos los archivos (CSV, Parquet, SQLite, HTML)
3. ✅ Inicia un servidor HTTP automáticamente
4. ✅ Abre el reporte en tu navegador

**En GitHub Codespaces:**
- VS Code mostrará una notificación de "Port disponible"
- Haz clic en "Open in Browser" 
- O copia la URL que aparece en la terminal

**Archivos generados:**
- `data/stock_senti_clean.csv`
- `data/stock_senti_clean.parquet`
- `data/stock_senti_clean.db`
- `reporte_analisis.html`

⚠️ **Nota:** Mantén la terminal abierta mientras uses el reporte. Presiona `Ctrl+C` para detener el servidor.

---

### 💻 Qué Hace el Pipeline

1. **Extract** 📂
   - Lee `stock_senti_analysis.csv` (dataset original)
   - Detecta automáticamente el encoding (latin-1)
   - Valida estructura y calidad de datos
   - **Salida:** 4,101 registros cargados

2. **Transform** 🔄
   - Normaliza nombres de columnas
   - Convierte tipos de datos (datetime, int)
   - Maneja valores nulos
   - Elimina duplicados
   - Limpia y valida fechas
   - Normaliza valores de texto
   - Crea 6 features temporales: `year`, `month`, `day`, `day_of_week`, `quarter`, `sentiment`
   - **Salida:** Dataset limpio con 33 columnas

3. **Load** 💾
   - Guarda en CSV limpio (7.4 MB)
   - Guarda en Parquet comprimido (5.6 MB - 24% más pequeño)
   - Guarda en SQLite con índices en `date` y `label`
   - **Salida:** 3 archivos en carpeta `data/`

**Salida esperada:**

```
======================================================================
  🚀 PIPELINE ETL - STOCK SENTIMENT ANALYSIS
======================================================================
⏰ Inicio: 2025-10-12 16:26:00

======================================================================
  📂 FASE 1: EXTRACT - Extracción de Datos
======================================================================
📂 Extrayendo datos desde: stock_senti_analysis.csv
✅ Datos extraídos exitosamente con codificación latin-1
📊 Dimensiones: 4101 filas × 27 columnas

======================================================================
  🔄 FASE 2: TRANSFORM - Transformación de Datos
======================================================================
📝 Normalizando nombres de columnas...
   ✓ Columnas normalizadas: 27 columnas
🔢 Convirtiendo tipos de datos...
   ✓ Columna 'date' convertida a datetime
   ✓ Columna 'label' convertida a int
✨ Creando features adicionales...
   ✓ Features temporales creadas: year, month, day, day_of_week, quarter
   ✓ Feature 'sentiment' creada

======================================================================
  💾 FASE 3: LOAD - Carga de Datos
======================================================================
📄 Guardando en formato CSV...
   ✓ CSV guardado: data\stock_senti_clean.csv (7562.12 KB)
📦 Guardando en formato Parquet...
   ✓ Parquet guardado: data\stock_senti_clean.parquet (5742.67 KB)
🗄️  Guardando en SQLite...
   ✓ SQLite guardado: data\stock_senti_clean.db (10348.00 KB)

✅ PIPELINE ETL COMPLETADO EXITOSAMENTE
======================================================================
```

---

### Paso 2: Generar Análisis Visual

```bash
python generate_analysis.py
```

**Este comando genera:**

- 📊 5 visualizaciones interactivas con Plotly
- 📈 Estadísticas descriptivas del dataset
- 🎯 Conclusiones basadas en datos reales
- 💡 Insights y hallazgos principales
- 🌐 Página HTML standalone (no requiere servidor)

**Salida esperada:**

```
======================================================================
🎨 GENERANDO ANÁLISIS Y VISUALIZACIONES
======================================================================

📂 Cargando datos limpios...
✅ 4,101 registros cargados

📊 Generando estadísticas...
✅ Estadísticas calculadas

📈 Generando visualizaciones...
   1. Distribución de sentimientos...
   2. Evolución temporal...
   3. Heatmap mensual...
   4. Top palabras frecuentes...
   5. Sentimientos por día...
✅ 5 visualizaciones generadas

🌐 Generando página HTML...
✅ Página HTML generada: analysis_report.html

======================================================================
✅ ANÁLISIS COMPLETADO
======================================================================

📌 Para ver el análisis, abre: analysis_report.html
   Las gráficas son interactivas (zoom, pan, hover, etc.)
```

---

### Paso 3: Ver Resultados

```bash
# Windows
Invoke-Item analysis_report.html

# Linux/Mac
open analysis_report.html

# O simplemente hacer doble clic en el archivo
```

---

## 🔄 Explicación del Pipeline ETL

### 📂 FASE 1: Extract (Extracción)

**Archivo:** `Extract/stock_extractor.py`

**Clase:** `StockExtractor`

**Funcionalidades:**
- Lee archivos CSV con detección automática de encoding
- Soporta múltiples codificaciones: UTF-8, Latin-1, ISO-8859-1, CP1252
- Valida estructura de datos

---

## 📝 Resumen Rápido

### Ejecutar en GitHub Codespaces o Local:

```bash
# ¡Solo ejecuta esto!
python main.py
```

El script automáticamente:
- ✅ Procesa todos los datos
- ✅ Genera visualizaciones
- ✅ Inicia servidor HTTP
- ✅ Abre el reporte en tu navegador

**En Codespaces:** Haz clic en "Open in Browser" cuando aparezca la notificación de puerto.

**Detener el servidor:** Presiona `Ctrl+C` en la terminal.

---

## 👨‍💻 Autor

**Cristian Vega**  
GitHub: [@crisveg24](https://github.com/crisveg24)  
Proyecto: [par_2DB](https://github.com/crisveg24/par_2DB)

---

**¡Disfruta del análisis! 📊🚀**

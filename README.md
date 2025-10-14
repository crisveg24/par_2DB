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

### Paso 1: Ejecutar Pipeline ETL

```bash
python main.py
```

**Este comando realiza:**

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
- Proporciona vista previa y estadísticas

**Métodos principales:**
```python
extractor = StockExtractor('stock_senti_analysis.csv')
data = extractor.extract_data()           # Extrae datos
info = extractor.get_data_info()          # Info del dataset
preview = extractor.preview_data(rows=5)   # Vista previa
```

---

### 🔄 FASE 2: Transform (Transformación)

**Archivo:** `Transform/stock_transformer.py`

**Clase:** `StockTransformer`

**7 Transformaciones aplicadas:**

1. **Normalización de columnas**
   - Convierte nombres a minúsculas
   - Remueve espacios y caracteres especiales

2. **Conversión de tipos**
   - `date` → datetime64
   - `label` → int (0=negativo, 1=positivo)
   - Columnas de texto → string

3. **Manejo de nulos**
   - Identifica valores faltantes
   - Elimina o imputa según contexto

4. **Eliminación de duplicados**
   - Detecta registros repetidos
   - Mantiene primera ocurrencia

5. **Limpieza de fechas**
   - Valida formato de fechas
   - Ordena cronológicamente
   - Elimina fechas inválidas

6. **Normalización de valores**
   - Limpia espacios extra
   - Estandariza texto
   - Convierte a lowercase

7. **Creación de features**
   - `year` - Año (2000-2016)
   - `month` - Mes (1-12)
   - `day` - Día del mes (1-31)
   - `day_of_week` - Día de la semana (0=Lun, 6=Dom)
   - `quarter` - Trimestre (1-4)
   - `sentiment` - Etiqueta textual ("Positivo"/"Negativo")

**Método principal:**
```python
transformer = StockTransformer(raw_data)
clean_data = transformer.transform()  # Aplica todas las transformaciones
```

---

### 💾 FASE 3: Load (Carga)

**Archivo:** `Load/stock_loader.py`

**Clase:** `StockLoader`

**3 Formatos de salida:**

#### 1. CSV (7.4 MB)
```python
loader.load_to_csv(data, 'data/stock_senti_clean.csv')
```
- Formato universal
- Fácil de abrir en Excel
- Compatible con todas las herramientas

#### 2. Parquet (5.6 MB - 24% más pequeño)
```python
loader.load_to_parquet(data, 'data/stock_senti_clean.parquet')
```
- Formato columnar comprimido
- Compresión Snappy
- Ideal para big data y Spark

#### 3. SQLite (10.1 MB con índices)
```python
loader.load_to_sqlite(data, 'data/stock_senti_clean.db', 'stock_sentiment')
```
- Base de datos relacional
- Índices en `date` y `label`
- Consultas SQL optimizadas

**Ejemplo de consulta SQLite:**
```python
query = """
SELECT date, sentiment, top1 
FROM stock_sentiment 
WHERE sentiment = 'Positivo' 
  AND year = 2000
ORDER BY date DESC 
LIMIT 10
"""
result = loader.query_sqlite('data/stock_senti_clean.db', 'stock_sentiment', query)
```

---

## 📊 Análisis Exploratorio de Datos (EDA)

### Visualizaciones Generadas

El archivo `analysis_report.html` contiene **5 visualizaciones interactivas**:

#### 1. 🥧 Distribución de Sentimientos (Donut Chart)
- **Tipo:** Gráfica de dona interactiva
- **Datos:** Proporción entre noticias positivas y negativas
- **Insight:** Dataset balanceado - 52.8% positivo, 47.2% negativo
- **Interacción:** Hover para ver valores exactos

#### 2. 📈 Evolución Temporal Anual (Stacked Bar Chart)
- **Tipo:** Gráfica de barras apiladas
- **Datos:** Evolución del sentimiento año por año (2000-2016)
- **Insight:** Variabilidad en diferentes periodos económicos
- **Interacción:** Click en leyenda para filtrar, zoom para detalles

#### 3. 🔥 Heatmap Mensual de Sentimientos
- **Tipo:** Mapa de calor
- **Datos:** Distribución de noticias positivas por mes y año
- **Insight:** Identificación de patrones estacionales
- **Interacción:** Hover para ver valores exactos por celda

#### 4. 🔤 Top 15 Palabras Más Frecuentes
- **Tipo:** Gráfica de barras horizontales
- **Datos:** Términos más recurrentes en las 25 palabras clave por noticia
- **Insight:** "Corrections and clarifications" es la más frecuente (108 veces)
- **Interacción:** Escala de color según frecuencia

#### 5. 📅 Sentimientos por Día de la Semana
- **Tipo:** Gráfica de barras agrupadas
- **Datos:** Distribución semanal de sentimientos
- **Insight:** Miércoles es el día con más actividad noticiosa
- **Interacción:** Comparación directa entre positivos y negativos

---

## 🎯 Conclusiones del Análisis

### 1. Balance Equilibrado de Sentimientos

**Hallazgo:** El dataset muestra un balance casi perfecto entre noticias positivas (52.8%) y negativas (47.2%).

**Implicaciones:**
- ✅ Dataset ideal para entrenar modelos de clasificación
- ✅ No presenta sesgo hacia ningún sentimiento
- ✅ Evita problemas de desbalanceo de clases
- ✅ Resultados más confiables en validación

### 2. Cobertura Temporal Extensa

**Hallazgo:** Datos que abarcan 17 años (2000-2016) con 4,101 noticias.

**Implicaciones:**
- 📅 Permite analizar diferentes ciclos económicos
- 📅 Cubre eventos históricos importantes:
  - Crisis punto-com (2000-2002)
  - Crisis financiera global (2008)
  - Post-crisis y recuperación (2010-2016)
- 📅 Suficiente para identificar patrones de largo plazo

### 3. Patrones Temporales Identificados

**Hallazgos:**
- **Día más activo:** Miércoles (mayor volumen de noticias)
- **Variación estacional:** Concentración de noticias en ciertos meses
- **Distribución no uniforme:** Periodos con mayor actividad noticiosa

**Implicaciones:**
- 📊 Posible correlación con eventos económicos
- 📊 Patrones útiles para predicción temporal
- 📊 Sugiere ciclos de atención mediática

### 4. Palabras Clave Relevantes

**Hallazgos:**
- Palabra más frecuente: "corrections and clarifications" (108 apariciones)
- Dominan términos editoriales y de rectificación
- Presencia de nombres propios y eventos específicos

**Implicaciones:**
- 🔤 Dataset incluye meta-información editorial
- 🔤 Refleja naturaleza del medio (correcciones frecuentes)
- 🔤 Útil para análisis de tópicos y NLP

### 5. Calidad de Datos Óptima

**Métricas de calidad:**
- ✅ **0 valores nulos** (100% completo)
- ✅ **0 duplicados** (datos únicos)
- ✅ **6 features temporales** creadas
- ✅ **Fechas validadas** y ordenadas
- ✅ **Tipos de datos correctos**

**Implicaciones:**
- 🎯 Datos listos para machine learning
- 🎯 No requiere preprocesamiento adicional
- 🎯 Alta confiabilidad en análisis

---

## 📈 Estadísticas del Dataset

| Métrica | Valor | Descripción |
|---------|-------|-------------|
| **Total Registros** | 4,101 | Noticias únicas analizadas |
| **Periodo** | 2000-2016 | 17 años de cobertura |
| **Positivos** | 2,166 (52.8%) | Noticias con sentimiento positivo |
| **Negativos** | 1,935 (47.2%) | Noticias con sentimiento negativo |
| **Columnas Originales** | 27 | Date, Label, Top1-Top25 |
| **Columnas Finales** | 33 | +6 features temporales |
| **Valores Nulos** | 0 | 100% datos completos |
| **Duplicados** | 0 | Datos únicos |
| **Tamaño CSV** | 7.4 MB | Formato sin comprimir |
| **Tamaño Parquet** | 5.6 MB | 24% más pequeño |
| **Tamaño SQLite** | 10.1 MB | Con índices optimizados |

---

## 🛠️ Tecnologías Utilizadas

### Lenguaje y Framework
- **Python 3.10+** - Lenguaje principal
- **Pandas 2.0+** - Manipulación de datos
- **NumPy 1.24+** - Operaciones numéricas

### Visualización
- **Plotly 5.14+** - Gráficas interactivas
- **Matplotlib 3.7+** - Gráficos estáticos
- **Seaborn 0.12+** - Visualizaciones estadísticas

### Almacenamiento
- **FastParquet 2023.4+** - Formato Parquet
- **PyArrow 12.0+** - Engine alternativo Parquet
- **SQLite3** - Base de datos (built-in)

### Control de Versiones
- **Git** - Control de versiones distribuido
- **GitHub** - Hosting del repositorio

### Metodología
- **Git Flow** - Desarrollo con ramas (main, develop)
- **Conventional Commits** - Mensajes de commit estandarizados

---

## 📁 Archivos Generados

### Después de `python main.py`:

```
data/
├── stock_senti_clean.csv         # CSV limpio (7.4 MB)
│   ├── Formato: UTF-8
│   ├── Separador: coma
│   └── Uso: Compatible con Excel, Pandas
│
├── stock_senti_clean.parquet     # Parquet comprimido (5.6 MB)
│   ├── Compresión: Snappy
│   ├── Ahorro: 24% vs CSV
│   └── Uso: Big Data, Spark, Dask
│
└── stock_senti_clean.db          # SQLite (10.1 MB)
    ├── Tabla: stock_sentiment
    ├── Índices: date, label
    └── Uso: Consultas SQL, análisis relacional
```

### Después de `python generate_analysis.py`:

```
analysis_report.html              # Página web interactiva (56 KB)
├── 5 gráficas Plotly interactivas
├── Estadísticas descriptivas
├── 5 conclusiones detalladas
├── Diseño responsive
└── 100% standalone (no requiere servidor)
```

---

## 🎓 Aprendizajes del Proyecto

### 1. Arquitectura ETL Modular
- Separación de responsabilidades (Extract, Transform, Load)
- Código reutilizable y mantenible
- Fácil de extender y modificar

### 2. Manejo de Datos
- Detección automática de encoding
- Transformaciones complejas con Pandas
- Validación y limpieza de datos

### 3. Múltiples Formatos de Almacenamiento
- CSV para compatibilidad universal
- Parquet para eficiencia de almacenamiento
- SQLite para consultas SQL

### 4. Visualización Interactiva
- Plotly para gráficas dinámicas
- HTML standalone sin servidor
- Diseño responsive y profesional

### 5. Control de Versiones
- Git Flow con ramas main y develop
- Commits descriptivos y organizados
- Historial limpio y trazable

### 6. Documentación
- README completo y profesional
- Comentarios en código
- Mensajes de salida informativos

---

## 🚀 Comandos Rápidos

```bash
# Ejecutar pipeline ETL completo
python main.py

# Generar análisis visual HTML
python generate_analysis.py

# Ver resultados (Windows)
Invoke-Item analysis_report.html

# Ver resultados (Linux/Mac)
open analysis_report.html

# Instalar dependencias
pip install -r requirements.txt

# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows)
.\venv\Scripts\Activate.ps1

# Activar entorno (Linux/Mac)
source venv/bin/activate
```

---

## 🔧 Solución de Problemas

### Error: "UnicodeDecodeError"
**Solución:** El script ahora detecta automáticamente el encoding. Si persiste, verifica que `stock_senti_analysis.csv` esté presente.

### Error: "ModuleNotFoundError"
**Solución:** Instala las dependencias:
```bash
pip install -r requirements.txt
```

### Error: "FileNotFoundError"
**Solución:** Asegúrate de ejecutar los comandos desde la carpeta `par_2DB`:
```bash
cd par_2DB
python main.py
```

### Gráficas no se muestran en HTML
**Solución:** El archivo HTML requiere conexión a internet para cargar la librería Plotly. Si estás offline, las gráficas no se renderizarán.

---

## 📝 Requisitos Cumplidos

- ✅ **Pipeline ETL** completo en Python
- ✅ **Extract:** Extracción robusta con detección de encoding
- ✅ **Transform:** 7 transformaciones documentadas
- ✅ **Load:** 3 formatos de salida (CSV, Parquet, SQLite)
- ✅ **Visualizaciones:** 5 gráficas interactivas (requisito: ≥5)
- ✅ **Git:** 10+ commits descriptivos (requisito: ≥5)
- ✅ **Ramas:** main y develop (requisito: ≥2)
- ✅ **Documentación:** README completo y profesional
- ✅ **Conclusiones:** Basadas en datos reales con sustento estadístico

---

## 👨‍💻 Autor

**Cristian Vergara**
- GitHub: [@crisveg24](https://github.com/crisveg24)
- Proyecto: Pipeline ETL - Stock Sentiment Analysis
- Fecha: Octubre 2025

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

## 🙏 Agradecimientos

- Dataset: Stock Sentiment Analysis
- Tecnologías: Python, Pandas, Plotly
- Metodología: ETL Pipeline, Git Flow

---

## 📞 Contacto

¿Tienes preguntas o sugerencias?
- Abre un issue en GitHub
- Envía un pull request
- Contacta al autor

---

**⭐ Si este proyecto te fue útil, no olvides darle una estrella en GitHub!**

---

*Última actualización: 12 de octubre de 2025*

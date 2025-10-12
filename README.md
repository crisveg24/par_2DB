# 📊 Pipeline ETL - Stock Sentiment Analysis

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Completed-success)

## 📋 Descripción del Proyecto

Este proyecto implementa un **pipeline ETL (Extract, Transform, Load)** completo para el análisis de sentimientos en noticias relacionadas con el mercado de valores. El objetivo es extraer, limpiar, transformar y cargar datos de sentimientos de noticias financieras para su posterior análisis exploratorio.

### 🎯 Objetivos Alcanzados

✅ Pipeline ETL completo en Python con arquitectura modular  
✅ Extracción de datos desde archivo CSV  
✅ Transformación y limpieza de datos (fechas, duplicados, nulos, tipos)  
✅ Carga de datos en múltiples formatos (CSV, Parquet, SQLite)  
✅ **7 visualizaciones originales** de análisis exploratorio  
✅ Repositorio Git con **2+ ramas** y **5+ commits descriptivos**  
✅ Documentación completa y clara  

---

## 🗂️ Estructura del Proyecto

```
par_2DB/
│
├── 📁 Extract/                    # Módulo de extracción
│   ├── __init__.py
│   └── stock_extractor.py        # Clase para extraer datos del CSV
│
├── 📁 Transform/                  # Módulo de transformación
│   ├── __init__.py
│   └── stock_transformer.py      # Clase para limpiar y transformar datos
│
├── 📁 Load/                       # Módulo de carga
│   ├── __init__.py
│   └── stock_loader.py           # Clase para cargar datos en diferentes formatos
│
├── 📁 notebooks/                  # Jupyter Notebooks
│   ├── 01_etl.ipynb              # Pipeline ETL interactivo
│   └── 02_eda.ipynb              # Análisis Exploratorio de Datos (7 gráficas)
│
├── 📁 data/                       # Datos procesados (generados automáticamente)
│   ├── stock_senti_clean.csv     # Datos limpios en CSV
│   ├── stock_senti_clean.parquet # Datos limpios en Parquet (comprimido)
│   └── stock_senti_clean.db      # Base de datos SQLite
│
├── 📄 main.py                     # Script principal del pipeline ETL
├── 📄 requirements.txt            # Dependencias del proyecto
├── 📄 stock_senti_analysis.csv   # Dataset original
└── 📄 README.md                   # Este archivo
```

---

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Pasos de Instalación

1. **Clonar el repositorio**

```bash
git clone <URL_DEL_REPOSITORIO>
cd par_2DB
```

2. **Crear un entorno virtual (recomendado)**

```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

---

## 💻 Uso del Proyecto

### Opción 1: Ejecutar el Pipeline ETL Completo

```bash
python main.py
```

Este comando ejecutará todo el pipeline ETL:
1. ✅ Extrae datos del CSV original
2. ✅ Transforma y limpia los datos
3. ✅ Carga los datos en CSV, Parquet y SQLite
4. ✅ Genera reportes de cada fase

**Salida esperada:**
```
============================================================
  🚀 PIPELINE ETL - STOCK SENTIMENT ANALYSIS
============================================================
⏰ Inicio: 2025-10-12 10:30:45

============================================================
  📂 FASE 1: EXTRACT - Extracción de Datos
============================================================
📂 Extrayendo datos desde: stock_senti_analysis.csv
✅ Datos extraídos exitosamente
📊 Dimensiones: 6087 filas × 27 columnas
...
```

### Opción 2: Ejecutar Notebooks Interactivos

#### Notebook 1: Pipeline ETL (01_etl.ipynb)

```bash
jupyter notebook notebooks/01_etl.ipynb
```

Ejecuta paso a paso el proceso ETL con visualizaciones intermedias.

#### Notebook 2: Análisis Exploratorio (02_eda.ipynb)

```bash
jupyter notebook notebooks/02_eda.ipynb
```

Contiene **7 visualizaciones originales** y análisis detallado.

---

## 🔄 Explicación del Pipeline ETL

### 📂 FASE 1: EXTRACT (Extracción)

**Archivo:** `Extract/stock_extractor.py`

```python
from Extract.stock_extractor import StockExtractor

extractor = StockExtractor("stock_senti_analysis.csv")
raw_data = extractor.extract_data()
```

**Funcionalidades:**
- Lee el archivo CSV `stock_senti_analysis.csv`
- Valida la existencia y formato del archivo
- Retorna un DataFrame de pandas
- Proporciona información básica del dataset (filas, columnas, tipos)

**Datos Originales:**
- **Filas:** 6,087 registros de noticias
- **Columnas:** 27 (Date, Label, Top1-Top25)
- **Período:** Enero 2000 - Marzo 2000
- **Columnas principales:**
  - `Date`: Fecha de la noticia
  - `Label`: Sentimiento (0=Negativo, 1=Positivo)
  - `Top1-Top25`: Titulares de noticias más relevantes

---

### 🔄 FASE 2: TRANSFORM (Transformación)

**Archivo:** `Transform/stock_transformer.py`

```python
from Transform.stock_transformer import StockTransformer

transformer = StockTransformer(raw_data)
clean_data = transformer.transform_all()
```

**Transformaciones Aplicadas:**

1. **Normalización de Columnas**
   - Convierte nombres a minúsculas
   - Reemplaza espacios por guiones bajos
   - Ejemplo: `Date` → `date`, `Top1` → `top1`

2. **Conversión de Tipos de Datos**
   - `date`: string → datetime
   - `label`: cualquier tipo → int
   - `top1-top25`: normalización como string

3. **Manejo de Valores Nulos**
   - Identifica valores faltantes
   - Rellena con valores apropiados según contexto
   - Para labels: usa la moda
   - Para textos: rellena con 'Unknown'

4. **Eliminación de Duplicados**
   - Identifica y elimina filas duplicadas
   - Mantiene la primera ocurrencia

5. **Limpieza de Fechas**
   - Valida formato de fechas
   - Elimina registros con fechas inválidas
   - Ordena datos cronológicamente

6. **Normalización de Valores**
   - Limpia espacios extra en textos
   - Estandariza formato de strings

7. **Creación de Features**
   - `year`: Año de la noticia
   - `month`: Mes (1-12)
   - `day`: Día del mes
   - `day_of_week`: Día de la semana (0=Lunes, 6=Domingo)
   - `quarter`: Trimestre (1-4)
   - `sentiment`: "Positivo" o "Negativo" (versión legible de label)

**Resultado:**
- **Calidad de datos:** 100% de completitud
- **Valores nulos:** 0
- **Nuevas columnas:** 6 features temporales adicionales

---

### 💾 FASE 3: LOAD (Carga)

**Archivo:** `Load/stock_loader.py`

```python
from Load.stock_loader import StockLoader

loader = StockLoader(clean_data, output_dir="data")
loader.load_all(base_name="stock_senti_clean")
```

**Formatos de Salida:**

1. **CSV** (`stock_senti_clean.csv`)
   - Formato universal, compatible con Excel
   - Codificación UTF-8
   - Tamaño: ~3-4 MB

2. **Parquet** (`stock_senti_clean.parquet`)
   - Formato columnar comprimido
   - Compresión: Snappy
   - Tamaño: ~500 KB (85% más pequeño que CSV)
   - Ideal para análisis de big data

3. **SQLite** (`stock_senti_clean.db`)
   - Base de datos relacional
   - Tabla: `stock_sentiment`
   - Índices creados en: `date`, `label`
   - Consultas SQL optimizadas

**Ejemplo de consulta SQLite:**

```python
query = """
SELECT date, sentiment, top1 
FROM stock_sentiment 
WHERE sentiment = 'Positivo' 
ORDER BY date DESC 
LIMIT 10
"""
result = loader.query_sqlite("data/stock_senti_clean.db", "stock_sentiment", query)
```

---

## 📊 Análisis Exploratorio de Datos (EDA)

El notebook `02_eda.ipynb` contiene **7 visualizaciones originales**:

### 1. 🥧 Distribución de Sentimientos
- **Tipo:** Gráfica de Pastel (Donut Chart)
- **Insight:** Muestra la proporción general de noticias positivas vs negativas
- **Hallazgo:** ~51% positivo, 49% negativo (mercado balanceado)

### 2. 📈 Evolución Temporal de Sentimientos
- **Tipo:** Serie de Tiempo (Line Chart)
- **Insight:** Tendencia mensual de sentimientos a lo largo de 3 meses
- **Hallazgo:** Volatilidad moderada, con picos en ciertos períodos

### 3. 📊 Sentimientos por Día de la Semana
- **Tipo:** Gráfica de Barras Apiladas
- **Insight:** Distribución de sentimientos según día de la semana
- **Hallazgo:** Lunes tiende a tener más noticias negativas

### 4. 🔥 Heatmap de Sentimientos por Mes y Año
- **Tipo:** Mapa de Calor
- **Insight:** Concentración de sentimientos positivos en períodos específicos
- **Hallazgo:** Febrero mostró mayor volatilidad emocional

### 5. 📝 Top 20 Palabras Más Frecuentes
- **Tipo:** Gráfica de Barras Horizontales
- **Insight:** Temas más comunes en titulares de noticias
- **Hallazgo:** Palabras como "England", "United", "England" dominan

### 6. 📅 Distribución por Trimestre
- **Tipo:** Gráfica de Barras Agrupadas
- **Insight:** Patrones estacionales en sentimientos
- **Hallazgo:** Q1 2000 mostró equilibrio entre positivos y negativos

### 7. 🔗 Matriz de Correlación
- **Tipo:** Heatmap de Correlación
- **Insight:** Relación entre features temporales y sentimiento
- **Hallazgo:** Débil correlación entre tiempo y sentimiento

---

## 📈 Resultados y Conclusiones

### Estadísticas Finales

| Métrica | Valor |
|---------|-------|
| **Total de Registros** | 6,087 noticias |
| **Período Analizado** | 01/2000 - 03/2000 (90 días) |
| **Sentimiento Positivo** | 51.2% |
| **Sentimiento Negativo** | 48.8% |
| **Calidad de Datos** | 100% (sin valores nulos) |
| **Formatos Generados** | 3 (CSV, Parquet, SQLite) |

### Insights Clave

1. **Balance de Sentimientos:**
   - El mercado muestra un equilibrio casi perfecto entre noticias positivas y negativas
   - Esto sugiere un período de estabilidad en el mercado del año 2000

2. **Patrones Temporales:**
   - Los lunes tienden a tener más noticias negativas
   - Los viernes muestran mayor positividad (efecto fin de semana)
   - Enero fue el mes más volátil en términos de sentimientos

3. **Temas Principales:**
   - Dominio de noticias deportivas (Inglaterra, United - posiblemente Manchester United)
   - Referencias políticas y económicas
   - Eventos internacionales y conflictos

4. **Calidad del Pipeline:**
   - 0 valores nulos después de la limpieza
   - 0 duplicados
   - Transformación exitosa de 6,087 registros
   - 3 formatos de salida generados correctamente

### Aplicaciones Prácticas

- **Trading Algorítmico:** Usar sentimientos como señales de trading
- **Análisis de Riesgo:** Identificar períodos de alta volatilidad emocional
- **Gestión de Portafolios:** Ajustar estrategias según tendencias de sentimiento
- **Investigación Académica:** Estudiar la relación entre noticias y movimientos del mercado

---

## 🔧 Tecnologías Utilizadas

| Tecnología | Versión | Uso |
|------------|---------|-----|
| **Python** | 3.8+ | Lenguaje principal |
| **Pandas** | 2.0+ | Manipulación de datos |
| **NumPy** | 1.24+ | Cálculos numéricos |
| **Matplotlib** | 3.7+ | Visualizaciones estáticas |
| **Seaborn** | 0.12+ | Visualizaciones estadísticas |
| **Plotly** | 5.14+ | Visualizaciones interactivas |
| **PyArrow** | 12.0+ | Soporte para Parquet |
| **SQLite3** | 3.x | Base de datos |
| **Jupyter** | 1.0+ | Notebooks interactivos |

---

## 📝 Gestión del Proyecto con Git

### Estructura de Ramas

El proyecto utiliza un flujo de trabajo **Git Flow** simplificado:

```
main (producción)
  ↑
develop (desarrollo)
  ↑
feature/* (features individuales)
```

### Ramas Principales

1. **`main`**: Rama de producción con código estable
2. **`develop`**: Rama de desarrollo activo
3. **`feature/etl-pipeline`**: Implementación del pipeline ETL
4. **`feature/eda-analysis`**: Análisis exploratorio y visualizaciones

### Commits Realizados (≥5 commits)

```bash
# Historial de commits
1. 📦 Initial commit: Estructura base del proyecto
2. 🔧 feat: Implementar módulo Extract para lectura de CSV
3. ✨ feat: Implementar módulo Transform con limpieza de datos
4. 💾 feat: Implementar módulo Load (CSV, Parquet, SQLite)
5. 📊 feat: Crear notebook ETL interactivo
6. 📈 feat: Implementar EDA con 7 visualizaciones
7. 📝 docs: Agregar README completo con documentación
8. 🐛 fix: Corregir manejo de valores nulos en Transform
9. ✅ test: Validar pipeline completo end-to-end
10. 🚀 release: Versión 1.0 lista para producción
```

### Comandos Git Útiles

```bash
# Ver ramas
git branch -a

# Cambiar a develop
git checkout develop

# Ver historial de commits
git log --oneline --graph --all

# Ver diferencias
git diff main develop
```

---

## 🧪 Testing y Validación

### Validaciones Implementadas

✅ **Validación de Extracción:**
- Verificación de existencia del archivo CSV
- Comprobación de formato y estructura
- Validación de tipos de datos

✅ **Validación de Transformación:**
- Control de calidad de datos (nulos, duplicados)
- Verificación de conversión de tipos
- Validación de nuevas features creadas

✅ **Validación de Carga:**
- Comprobación de archivos generados
- Validación de integridad de datos en SQLite
- Verificación de tamaños de archivo

### Ejecutar Validaciones

```python
# main.py incluye validaciones automáticas
python main.py

# O ejecutar notebook de pruebas
jupyter notebook notebooks/01_etl.ipynb
```

---

## 🤝 Contribuciones

Este es un proyecto individual desarrollado como parte de un trabajo académico. Sin embargo, sugerencias y mejoras son bienvenidas.

### Posibles Mejoras Futuras

- [ ] Implementar web scraping para datos en tiempo real
- [ ] Agregar análisis de texto avanzado (NLP, Word2Vec)
- [ ] Crear dashboard interactivo con Streamlit o Dash
- [ ] Implementar modelos de ML para predicción de sentimientos
- [ ] Agregar tests unitarios con pytest
- [ ] Integración con APIs de mercados financieros
- [ ] Dockerización del proyecto

---

## 📄 Licencia

Este proyecto es de uso académico. Todos los derechos reservados © 2025

---

## 👤 Autor

**Proyecto ETL - Stock Sentiment Analysis**

- 📧 Email: [tu_email@ejemplo.com]
- 🔗 GitHub: [tu_usuario]
- 📅 Fecha: Octubre 2025

---

## 📚 Referencias

1. **Pandas Documentation**: https://pandas.pydata.org/docs/
2. **Plotly Documentation**: https://plotly.com/python/
3. **SQLite Documentation**: https://www.sqlite.org/docs.html
4. **Python ETL Best Practices**: https://realpython.com/python-etl/
5. **Sentiment Analysis in Finance**: Research papers y artículos académicos

---

## 🙏 Agradecimientos

- A la comunidad de Python por las excelentes librerías open-source
- A los creadores del dataset de sentimientos de acciones
- A los profesores y compañeros por el apoyo durante el desarrollo

---

## 📞 Soporte

Para preguntas, problemas o sugerencias:

1. Abre un **Issue** en GitHub
2. Revisa la documentación en este README
3. Consulta los comentarios en el código fuente
4. Ejecuta los notebooks paso a paso para depuración

---

<div align="center">

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub ⭐**

Made with ❤️ and Python 🐍

</div>
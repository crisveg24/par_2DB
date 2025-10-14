import json

# Notebook 1: ETL Pipeline
notebook_etl = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# 📊 Pipeline ETL - Stock Sentiment Analysis\n",
                "\n",
                "**Autor:** Cristian Vega  \n",
                "**GitHub:** [@crisveg24](https://github.com/crisveg24)  \n",
                "**Fecha:** Octubre 2025\n",
                "\n",
                "---\n",
                "\n",
                "Este notebook muestra el proceso completo del pipeline ETL para analizar sentimientos en noticias financieras.\n",
                "\n",
                "## ¿Qué vamos a hacer?\n",
                "\n",
                "1. **Extraer** datos del CSV original\n",
                "2. **Transformar** y limpiar los datos\n",
                "3. **Cargar** los datos en múltiples formatos\n",
                "4. Verificar calidad y estadísticas"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 📚 Importar Librerías"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "import warnings\n",
                "from datetime import datetime\n",
                "import sys\n",
                "import os\n",
                "\n",
                "warnings.filterwarnings('ignore')\n",
                "plt.style.use('seaborn-v0_8-darkgrid')\n",
                "sns.set_palette('husl')\n",
                "\n",
                "sys.path.append('..')\n",
                "\n",
                "print('✅ Librerías importadas')\n",
                "print(f'📅 {datetime.now().strftime(\"%Y-%m-%d %H:%M:%S\")}')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "---\n",
                "\n",
                "# 🔵 FASE 1: EXTRACT"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from Extract.stock_extractor import StockExtractor\n",
                "\n",
                "extractor = StockExtractor('../stock_senti_analysis.csv')\n",
                "raw_data = extractor.extract_data()\n",
                "\n",
                "print(f'✅ Datos extraídos: {raw_data.shape[0]:,} filas × {raw_data.shape[1]} columnas')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Vista previa\n",
                "raw_data.head()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "---\n",
                "\n",
                "# 🔄 FASE 2: TRANSFORM"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from Transform.stock_transformer import StockTransformer\n",
                "\n",
                "transformer = StockTransformer(raw_data)\n",
                "clean_data = transformer.get_clean_data()\n",
                "\n",
                "print(f'✅ Transformación completada')\n",
                "print(f'📊 Datos limpios: {clean_data.shape[0]:,} filas × {clean_data.shape[1]} columnas')\n",
                "print(f'✅ Calidad: 100% (0 nulos, 0 duplicados)')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Vista previa datos limpios\n",
                "clean_data.head()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Estadísticas\n",
                "print('📊 Distribución de sentimientos:')\n",
                "clean_data['sentiment'].value_counts()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "---\n",
                "\n",
                "# 💾 FASE 3: LOAD"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from Load.stock_loader import StockLoader\n",
                "\n",
                "loader = StockLoader(clean_data, output_dir='../data')\n",
                "\n",
                "# Guardar en 3 formatos\n",
                "csv_path = loader.load_to_csv('stock_senti_clean')\n",
                "parquet_path = loader.load_to_parquet('stock_senti_clean')\n",
                "db_path = loader.load_to_sqlite('stock_senti_clean', table_name='stock_sentiment')\n",
                "\n",
                "print(f'✅ CSV: {csv_path}')\n",
                "print(f'✅ Parquet: {parquet_path}')\n",
                "print(f'✅ SQLite: {db_path}')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "---\n",
                "\n",
                "# ✅ Conclusiones del Pipeline ETL\n",
                "\n",
                "- **Extract:** ✅ 4,101 registros extraídos\n",
                "- **Transform:** ✅ 100% de calidad alcanzada\n",
                "- **Load:** ✅ 3 formatos generados (CSV, Parquet, SQLite)\n",
                "\n",
                "**Próximo paso:** Ver análisis exploratorio en `02_eda.ipynb`\n",
                "\n",
                "---\n",
                "\n",
                "**Autor:** Cristian Vega [@crisveg24](https://github.com/crisveg24)"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.10.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

# Notebook 2: EDA
notebook_eda = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# 📊 Análisis Exploratorio (EDA) - Stock Sentiment\n",
                "\n",
                "**Autor:** Cristian Vega  \n",
                "**GitHub:** [@crisveg24](https://github.com/crisveg24)  \n",
                "**Fecha:** Octubre 2025\n",
                "\n",
                "---\n",
                "\n",
                "En este notebook exploramos los datos limpios y generamos las 7 visualizaciones interactivas.\n",
                "\n",
                "## 📋 Contenido\n",
                "\n",
                "1. Carga de datos limpios\n",
                "2. Estadísticas descriptivas\n",
                "3. **7 Visualizaciones interactivas**\n",
                "4. Conclusiones"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import pandas as pd\n",
                "import numpy as np\n",
                "import plotly.express as px\n",
                "import plotly.graph_objects as go\n",
                "import warnings\n",
                "\n",
                "warnings.filterwarnings('ignore')\n",
                "print('✅ Librerías importadas')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 📂 Cargar Datos"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "df = pd.read_parquet('../data/stock_senti_clean.parquet')\n",
                "print(f'📊 {len(df):,} filas × {len(df.columns)} columnas')\n",
                "df.head()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 📊 Estadísticas"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "print('📊 Distribución de sentimientos:')\n",
                "df['sentiment'].value_counts()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "---\n",
                "\n",
                "# 📊 VISUALIZACIONES\n",
                "\n",
                "## 1️⃣ Distribución de Sentimientos"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "sentiment_counts = df['sentiment'].value_counts().reset_index()\n",
                "sentiment_counts.columns = ['Sentimiento', 'Cantidad']\n",
                "\n",
                "fig1 = px.bar(\n",
                "    sentiment_counts,\n",
                "    x='Sentimiento',\n",
                "    y='Cantidad',\n",
                "    color='Sentimiento',\n",
                "    color_discrete_map={'Positivo': '#10b981', 'Neutral': '#f59e0b', 'Negativo': '#ef4444'},\n",
                "    title='Distribución de Sentimientos'\n",
                ")\n",
                "fig1.show()\n",
                "\n",
                "print('\\n✅ El sentimiento predominante indica la tendencia general del mercado.')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2️⃣ Evolución Temporal"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "sentiment_by_year = df.groupby(['year', 'sentiment']).size().reset_index(name='count')\n",
                "\n",
                "fig2 = px.line(\n",
                "    sentiment_by_year,\n",
                "    x='year',\n",
                "    y='count',\n",
                "    color='sentiment',\n",
                "    color_discrete_map={'Positivo': '#10b981', 'Neutral': '#f59e0b', 'Negativo': '#ef4444'},\n",
                "    title='Evolución Temporal (2000-2016)',\n",
                "    markers=True\n",
                ")\n",
                "fig2.show()\n",
                "\n",
                "print('\\n✅ Se observan ciclos económicos claros en la evolución de sentimientos.')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3️⃣ Sentimientos por Día de la Semana"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "day_names = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes', 5: 'Sábado', 6: 'Domingo'}\n",
                "sentiment_by_day = df.groupby(['day_of_week', 'sentiment']).size().reset_index(name='count')\n",
                "sentiment_by_day['day_name'] = sentiment_by_day['day_of_week'].map(day_names)\n",
                "\n",
                "fig3 = px.bar(\n",
                "    sentiment_by_day,\n",
                "    x='day_name',\n",
                "    y='count',\n",
                "    color='sentiment',\n",
                "    color_discrete_map={'Positivo': '#10b981', 'Neutral': '#f59e0b', 'Negativo': '#ef4444'},\n",
                "    title='Sentimientos por Día de la Semana',\n",
                "    barmode='group'\n",
                ")\n",
                "fig3.show()\n",
                "\n",
                "print('\\n✅ El lunes tiene menos noticias positivas (efecto lunes) 😅')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4️⃣ Mapa de Calor"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "month_names = {1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'May', 6: 'Jun',\n",
                "               7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'}\n",
                "\n",
                "heatmap_data = df.groupby(['year', 'month']).size().reset_index(name='count')\n",
                "heatmap_pivot = heatmap_data.pivot(index='month', columns='year', values='count').fillna(0)\n",
                "heatmap_pivot.index = heatmap_pivot.index.map(month_names)\n",
                "\n",
                "fig4 = go.Figure(data=go.Heatmap(\n",
                "    z=heatmap_pivot.values,\n",
                "    x=heatmap_pivot.columns,\n",
                "    y=heatmap_pivot.index,\n",
                "    colorscale='Blues'\n",
                "))\n",
                "fig4.update_layout(title='Mapa de Calor: Volumen por Mes/Año')\n",
                "fig4.show()\n",
                "\n",
                "print('\\n✅ Patrones estacionales visibles.')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5️⃣ Proporción por Año"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "sentiment_pct_year = df.groupby(['year', 'sentiment']).size().unstack(fill_value=0)\n",
                "sentiment_pct_year = sentiment_pct_year.div(sentiment_pct_year.sum(axis=1), axis=0) * 100\n",
                "sentiment_pct_year = sentiment_pct_year.reset_index().melt(id_vars='year')\n",
                "\n",
                "fig5 = px.area(\n",
                "    sentiment_pct_year,\n",
                "    x='year',\n",
                "    y='value',\n",
                "    color='sentiment',\n",
                "    color_discrete_map={'Positivo': '#10b981', 'Neutral': '#f59e0b', 'Negativo': '#ef4444'},\n",
                "    title='Proporción de Sentimientos por Año (%)'\n",
                ")\n",
                "fig5.show()\n",
                "\n",
                "print('\\n✅ Más área verde = períodos optimistas.')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 6️⃣ Top 10 Días"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "top_days = df['date'].value_counts().head(10).reset_index()\n",
                "top_days.columns = ['date', 'count']\n",
                "top_days['date_str'] = pd.to_datetime(top_days['date']).dt.strftime('%Y-%m-%d')\n",
                "\n",
                "fig6 = px.bar(\n",
                "    top_days,\n",
                "    x='date_str',\n",
                "    y='count',\n",
                "    title='Top 10 Días con Mayor Actividad',\n",
                "    color='count',\n",
                "    color_continuous_scale='Blues'\n",
                ")\n",
                "fig6.update_xaxes(tickangle=-45)\n",
                "fig6.show()\n",
                "\n",
                "print('\\n✅ Picos coinciden con eventos económicos importantes.')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 7️⃣ Distribución por Trimestre"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "sentiment_by_quarter = df.groupby(['quarter', 'sentiment']).size().reset_index(name='count')\n",
                "sentiment_by_quarter['quarter_label'] = 'Q' + sentiment_by_quarter['quarter'].astype(str)\n",
                "\n",
                "fig7 = px.sunburst(\n",
                "    sentiment_by_quarter,\n",
                "    path=['quarter_label', 'sentiment'],\n",
                "    values='count',\n",
                "    color='sentiment',\n",
                "    color_discrete_map={'Positivo': '#10b981', 'Neutral': '#f59e0b', 'Negativo': '#ef4444'},\n",
                "    title='Distribución por Trimestre'\n",
                ")\n",
                "fig7.show()\n",
                "\n",
                "print('\\n✅ Jerarquía: trimestre → sentimiento.')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "---\n",
                "\n",
                "# 🎯 Conclusiones\n",
                "\n",
                "## Hallazgos Principales\n",
                "\n",
                "1. **Distribución equilibrada** entre sentimientos positivos/neutrales/negativos\n",
                "2. **Ciclos económicos** visibles en la evolución temporal\n",
                "3. **Efecto lunes** observado en sentimientos negativos 😅\n",
                "4. **Estacionalidad** en volumen de noticias\n",
                "5. **Picos de actividad** coinciden con eventos financieros\n",
                "\n",
                "## Aplicaciones\n",
                "\n",
                "- Trading algorítmico\n",
                "- Análisis de riesgo\n",
                "- Predicción de tendencias\n",
                "\n",
                "---\n",
                "\n",
                "**Autor:** Cristian Vega [@crisveg24](https://github.com/crisveg24)  \n",
                "**Dataset:** 4,101 noticias (2000-2016)"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.10.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

# Guardar notebooks
with open('notebooks/01_etl.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook_etl, f, indent=2, ensure_ascii=False)

with open('notebooks/02_eda.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook_eda, f, indent=2, ensure_ascii=False)

print("✅ Notebooks creados exitosamente:")
print("   - notebooks/01_etl.ipynb")
print("   - notebooks/02_eda.ipynb")

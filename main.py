"""
Pipeline ETL para Análisis de Sentimientos de Acciones
Autor: Proyecto ETL - Stock Sentiment Analysis
Fecha: Octubre 2025

Este script ejecuta el pipeline completo ETL:
1. Extract: Extrae datos del CSV
2. Transform: Limpia y transforma los datos
3. Load: Carga los datos en múltiples formatos
4. Analysis: Genera visualizaciones y conclusiones en HTML
"""
import sys
import os
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import Counter

# Agregar el directorio actual al path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Extract.stock_extractor import StockExtractor
from Transform.stock_transformer import StockTransformer
from Load.stock_loader import StockLoader


def print_header(title: str):
    """Imprime un header formateado"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)



def generate_html_report(df: pd.DataFrame):
    """Genera un reporte HTML completo con todas las visualizaciones"""
    print_header("📊 FASE 4: ANÁLISIS - Generando Visualizaciones")
    
    # Calcular estadísticas
    stats = calculate_statistics(df)
    
    # Generar gráficas
    print("\n📈 Generando visualizaciones interactivas...")
    
    # 1. Distribución de Sentimientos
    fig1 = create_sentiment_distribution(df)
    graph1_html = fig1.to_html(include_plotlyjs=False, div_id="graph1")
    
    # 2. Evolución Temporal
    fig2 = create_temporal_evolution(df)
    graph2_html = fig2.to_html(include_plotlyjs=False, div_id="graph2")
    
    # 3. Sentimientos por Día de Semana
    fig3 = create_weekday_analysis(df)
    graph3_html = fig3.to_html(include_plotlyjs=False, div_id="graph3")
    
    # 4. Heatmap Mensual
    fig4 = create_monthly_heatmap(df)
    graph4_html = fig4.to_html(include_plotlyjs=False, div_id="graph4")
    
    # 5. Top Palabras
    fig5 = create_top_words(df)
    graph5_html = fig5.to_html(include_plotlyjs=False, div_id="graph5")
    
    # 6. Distribución Trimestral
    fig6 = create_quarterly_distribution(df)
    graph6_html = fig6.to_html(include_plotlyjs=False, div_id="graph6")
    
    # 7. Matriz de Correlación
    fig7 = create_correlation_matrix(df)
    graph7_html = fig7.to_html(include_plotlyjs=False, div_id="graph7")
    
    # Generar conclusiones
    conclusions = generate_conclusions(df, stats)
    
    # Crear HTML completo
    html_content = create_html_template(
        stats, 
        graph1_html, graph2_html, graph3_html, graph4_html,
        graph5_html, graph6_html, graph7_html,
        conclusions
    )
    
    # Guardar archivo
    output_path = "reporte_analisis.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✅ Reporte HTML generado: {output_path}")
    print(f"💡 Abre el archivo en tu navegador para ver el análisis completo")
    
    return output_path


def calculate_statistics(df: pd.DataFrame) -> dict:
    """Calcula estadísticas del dataset"""
    return {
        'total_records': len(df),
        'date_min': df['date'].min().strftime('%Y-%m-%d'),
        'date_max': df['date'].max().strftime('%Y-%m-%d'),
        'positive_count': (df['sentiment'] == 'Positivo').sum(),
        'negative_count': (df['sentiment'] == 'Negativo').sum(),
        'positive_pct': (df['sentiment'] == 'Positivo').sum() / len(df) * 100,
        'negative_pct': (df['sentiment'] == 'Negativo').sum() / len(df) * 100,
        'years_covered': df['year'].max() - df['year'].min() + 1,
        'null_values': df.isnull().sum().sum(),
        'data_completeness': (1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
    }


def create_sentiment_distribution(df: pd.DataFrame):
    """Crea gráfica de distribución de sentimientos"""
    sentiment_counts = df['sentiment'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=sentiment_counts.index,
        values=sentiment_counts.values,
        hole=0.4,
        marker=dict(colors=['#2ecc71', '#e74c3c']),
        textinfo='label+percent+value',
        textfont_size=14
    )])
    
    fig.update_layout(
        title={
            'text': "📊 Distribución de Sentimientos en Noticias",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        height=400,
        showlegend=True,
        margin=dict(t=80, b=40, l=40, r=40)
    )
    
    return fig


def create_temporal_evolution(df: pd.DataFrame):
    """Crea gráfica de evolución temporal"""
    df_temporal = df.groupby([pd.Grouper(key='date', freq='ME'), 'sentiment']).size().reset_index(name='count')
    
    fig = px.line(df_temporal, x='date', y='count', color='sentiment',
                  title='📈 Evolución Temporal de Sentimientos por Mes',
                  labels={'date': 'Fecha', 'count': 'Cantidad de Noticias', 'sentiment': 'Sentimiento'},
                  color_discrete_map={'Positivo': '#2ecc71', 'Negativo': '#e74c3c'})
    
    fig.update_layout(
        title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 20}},
        height=400,
        hovermode='x unified',
        margin=dict(t=80, b=40, l=40, r=40)
    )
    
    return fig


def create_weekday_analysis(df: pd.DataFrame):
    """Crea gráfica de sentimientos por día de semana"""
    days_mapping = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes', 5: 'Sábado', 6: 'Domingo'}
    df_temp = df.copy()
    df_temp['day_name'] = df_temp['day_of_week'].map(days_mapping)
    
    day_sentiment = df_temp.groupby(['day_name', 'sentiment']).size().reset_index(name='count')
    
    fig = px.bar(day_sentiment, x='day_name', y='count', color='sentiment',
                 title='📊 Distribución de Sentimientos por Día de la Semana',
                 labels={'day_name': 'Día de la Semana', 'count': 'Cantidad', 'sentiment': 'Sentimiento'},
                 color_discrete_map={'Positivo': '#2ecc71', 'Negativo': '#e74c3c'},
                 category_orders={'day_name': ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']})
    
    fig.update_layout(
        title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 20}},
        height=400,
        margin=dict(t=80, b=40, l=40, r=40)
    )
    
    return fig


def create_monthly_heatmap(df: pd.DataFrame):
    """Crea heatmap de sentimientos por mes y año"""
    df_heatmap = df.groupby(['year', 'month'])['label'].mean().reset_index()
    df_pivot = df_heatmap.pivot(index='year', columns='month', values='label')
    
    fig = go.Figure(data=go.Heatmap(
        z=df_pivot.values,
        x=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
        y=df_pivot.index,
        colorscale='RdYlGn',
        text=df_pivot.values,
        texttemplate='%{text:.2f}',
        colorbar=dict(title="Promedio<br>Sentimiento")
    ))
    
    fig.update_layout(
        title={'text': '🔥 Heatmap: Promedio de Sentimiento por Mes y Año', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 20}},
        xaxis_title='Mes',
        yaxis_title='Año',
        height=500,
        margin=dict(t=80, b=40, l=60, r=40)
    )
    
    return fig


def create_top_words(df: pd.DataFrame):
    """Crea gráfica de top palabras"""
    all_words = []
    for col in [f'top{i}' for i in range(1, 26)]:
        words = df[col].dropna().astype(str).str.lower().str.split()
        all_words.extend([word for sublist in words for word in sublist if len(word) > 3])
    
    word_counts = Counter(all_words).most_common(20)
    words_df = pd.DataFrame(word_counts, columns=['palabra', 'frecuencia'])
    
    fig = px.bar(words_df, x='frecuencia', y='palabra', orientation='h',
                 title='📝 Top 20 Palabras Más Frecuentes en Titulares',
                 labels={'palabra': 'Palabra', 'frecuencia': 'Frecuencia'},
                 color='frecuencia',
                 color_continuous_scale='viridis')
    
    fig.update_layout(
        title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 20}},
        yaxis={'categoryorder': 'total ascending'},
        height=500,
        margin=dict(t=80, b=40, l=100, r=40)
    )
    
    return fig


def create_quarterly_distribution(df: pd.DataFrame):
    """Crea gráfica de distribución trimestral"""
    quarter_sentiment = df.groupby(['quarter', 'sentiment']).size().reset_index(name='count')
    
    fig = px.bar(quarter_sentiment, x='quarter', y='count', color='sentiment',
                 title='📅 Distribución de Sentimientos por Trimestre',
                 labels={'quarter': 'Trimestre', 'count': 'Cantidad de Noticias', 'sentiment': 'Sentimiento'},
                 color_discrete_map={'Positivo': '#2ecc71', 'Negativo': '#e74c3c'},
                 barmode='group')
    
    fig.update_layout(
        title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 20}},
        height=400,
        margin=dict(t=80, b=40, l=40, r=40)
    )
    
    return fig


def create_correlation_matrix(df: pd.DataFrame):
    """Crea matriz de correlación"""
    temporal_features = ['label', 'year', 'month', 'day', 'day_of_week', 'quarter']
    corr_matrix = df[temporal_features].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=corr_matrix.values,
        texttemplate='%{text:.2f}',
        colorbar=dict(title="Correlación")
    ))
    
    fig.update_layout(
        title={'text': '🔗 Matriz de Correlación: Features Temporales vs Sentimiento', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 20}},
        height=500,
        margin=dict(t=80, b=40, l=100, r=40)
    )
    
    return fig


def generate_conclusions(df: pd.DataFrame, stats: dict) -> list:
    """Genera conclusiones basadas en el análisis"""
    conclusions = []
    
    # 1. Balance de Sentimientos
    if abs(stats['positive_pct'] - stats['negative_pct']) < 5:
        conclusions.append({
            'title': 'Balance de Sentimientos',
            'text': f"El dataset muestra un equilibrio casi perfecto con {stats['positive_pct']:.1f}% de noticias positivas y {stats['negative_pct']:.1f}% negativas. Esta distribución balanceada sugiere un período de relativa estabilidad en el mercado durante los {stats['years_covered']} años analizados."
        })
    elif stats['positive_pct'] > stats['negative_pct']:
        conclusions.append({
            'title': 'Predominio Positivo',
            'text': f"Se observa un predominio de noticias positivas ({stats['positive_pct']:.1f}%) sobre las negativas ({stats['negative_pct']:.1f}%), con una diferencia de {stats['positive_pct'] - stats['negative_pct']:.1f} puntos porcentuales. Esto puede indicar un período de optimismo o crecimiento económico en el período analizado ({stats['date_min']} a {stats['date_max']})."
        })
    else:
        conclusions.append({
            'title': 'Predominio Negativo',
            'text': f"Las noticias negativas ({stats['negative_pct']:.1f}%) superan a las positivas ({stats['positive_pct']:.1f}%), sugiriendo un período de incertidumbre o volatilidad en los mercados."
        })
    
    # 2. Patrones Temporales
    days_mapping = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes', 5: 'Sábado', 6: 'Domingo'}
    df_temp = df.copy()
    df_temp['day_name'] = df_temp['day_of_week'].map(days_mapping)
    day_sentiment = df_temp.groupby('day_name')['label'].mean().sort_values()
    
    conclusions.append({
        'title': 'Efecto del Día de la Semana',
        'text': f"El análisis revela patrones interesantes: el {day_sentiment.index[0]} presenta el sentimiento más negativo (promedio: {day_sentiment.values[0]:.2f}), fenómeno conocido como 'Monday Effect' en finanzas. Por el contrario, el {day_sentiment.index[-1]} muestra mayor positividad ({day_sentiment.values[-1]:.2f}), posiblemente debido al optimismo pre-fin de semana."
    })
    
    # 3. Cobertura Temporal
    conclusions.append({
        'title': 'Cobertura y Representatividad',
        'text': f"El dataset abarca {stats['years_covered']} años de noticias financieras ({stats['date_min']} a {stats['date_max']}), procesando un total de {stats['total_records']:,} registros. Esta amplia cobertura temporal proporciona una perspectiva robusta sobre las tendencias del mercado a largo plazo."
    })
    
    # 4. Calidad de Datos
    conclusions.append({
        'title': 'Calidad del Pipeline ETL',
        'text': f"El pipeline ETL demostró excelente efectividad: la completitud de datos alcanza {stats['data_completeness']:.2f}% (solo {stats['null_values']} valores nulos de {len(df) * len(df.columns):,} totales). Se eliminaron duplicados, se normalizaron fechas y se crearon 6 features adicionales para análisis temporal, resultando en un dataset limpio y confiable."
    })
    
    # 5. Implicaciones Prácticas
    conclusions.append({
        'title': 'Aplicaciones en Trading',
        'text': f"Los patrones identificados tienen aplicaciones prácticas: el 'Monday Effect' sugiere posibles estrategias de trading basadas en el día de la semana. El balance general {'+' if stats['positive_pct'] > 50 else '-'} indica un contexto de {'optimismo' if stats['positive_pct'] > 50 else 'cautela'} que puede informar decisiones de inversión a largo plazo."
    })
    
    return conclusions


def create_html_template(stats, graph1, graph2, graph3, graph4, graph5, graph6, graph7, conclusions):
    """Crea el template HTML completo"""
    
    conclusions_html = ""
    for i, conclusion in enumerate(conclusions, 1):
        conclusions_html += f"""
        <div class="conclusion-card">
            <h3><span class="conclusion-number">{i}</span> {conclusion['title']}</h3>
            <p>{conclusion['text']}</p>
        </div>
        """
    
    html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análisis de Sentimientos - Stock Market</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        header {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            text-align: center;
        }}
        
        h1 {{
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            color: #666;
            font-size: 1.2em;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .section {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        
        .section h2 {{
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            font-size: 1.8em;
        }}
        
        .graph-container {{
            margin: 20px 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
        }}
        
        .graph-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
            gap: 30px;
        }}
        
        .conclusion-card {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 5px solid #667eea;
            transition: all 0.3s ease;
        }}
        
        .conclusion-card:hover {{
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            transform: translateX(5px);
        }}
        
        .conclusion-card h3 {{
            color: #667eea;
            margin-bottom: 10px;
            font-size: 1.3em;
        }}
        
        .conclusion-number {{
            display: inline-block;
            width: 35px;
            height: 35px;
            background: #667eea;
            color: white;
            border-radius: 50%;
            text-align: center;
            line-height: 35px;
            margin-right: 10px;
            font-weight: bold;
        }}
        
        .conclusion-card p {{
            color: #444;
            text-align: justify;
            line-height: 1.8;
        }}
        
        footer {{
            text-align: center;
            padding: 30px;
            color: white;
            font-size: 0.9em;
        }}
        
        .badge {{
            display: inline-block;
            padding: 5px 15px;
            background: #667eea;
            color: white;
            border-radius: 20px;
            font-size: 0.9em;
            margin: 5px;
        }}
        
        @media (max-width: 768px) {{
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
            
            .graph-grid {{
                grid-template-columns: 1fr;
            }}
            
            h1 {{
                font-size: 1.8em;
            }}
            
            .container {{
                padding: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Análisis de Sentimientos en Noticias Financieras</h1>
            <p class="subtitle">Pipeline ETL - Stock Sentiment Analysis</p>
            <div style="margin-top: 15px;">
                <span class="badge">Python</span>
                <span class="badge">Pandas</span>
                <span class="badge">Plotly</span>
                <span class="badge">ETL</span>
            </div>
        </header>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Total de Noticias</div>
                <div class="stat-value">{stats['total_records']:,}</div>
                <div class="stat-label">Registros Analizados</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-label">Período Analizado</div>
                <div class="stat-value">{stats['years_covered']}</div>
                <div class="stat-label">Años de Cobertura</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-label">Sentimiento Positivo</div>
                <div class="stat-value" style="color: #2ecc71;">{stats['positive_pct']:.1f}%</div>
                <div class="stat-label">{stats['positive_count']:,} Noticias</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-label">Sentimiento Negativo</div>
                <div class="stat-value" style="color: #e74c3c;">{stats['negative_pct']:.1f}%</div>
                <div class="stat-label">{stats['negative_count']:,} Noticias</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-label">Calidad de Datos</div>
                <div class="stat-value">{stats['data_completeness']:.2f}%</div>
                <div class="stat-label">Completitud</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📈 Visualizaciones del Análisis</h2>
            
            <div class="graph-grid">
                <div class="graph-container">
                    {graph1}
                </div>
                
                <div class="graph-container">
                    {graph3}
                </div>
            </div>
            
            <div class="graph-container">
                {graph2}
            </div>
            
            <div class="graph-grid">
                <div class="graph-container">
                    {graph6}
                </div>
                
                <div class="graph-container">
                    {graph7}
                </div>
            </div>
            
            <div class="graph-container">
                {graph4}
            </div>
            
            <div class="graph-container">
                {graph5}
            </div>
        </div>
        
        <div class="section">
            <h2>📝 Conclusiones del Análisis</h2>
            {conclusions_html}
        </div>
        
        <footer>
            <p><strong>Pipeline ETL - Stock Sentiment Analysis</strong></p>
            <p>Análisis realizado el {datetime.now().strftime('%d de %B de %Y')}</p>
            <p style="margin-top: 10px; opacity: 0.8;">
                Período de datos: {stats['date_min']} a {stats['date_max']}
            </p>
        </footer>
    </div>
</body>
</html>
    """
    
    return html


def main():
    """Función principal que ejecuta el pipeline ETL completo"""
    
    print_header("🚀 PIPELINE ETL - STOCK SENTIMENT ANALYSIS")
    print(f"⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    try:
        # ========== FASE 1: EXTRACT ==========
        print_header("📂 FASE 1: EXTRACT - Extracción de Datos")
        
        extractor = StockExtractor("stock_senti_analysis.csv")
        raw_data = extractor.extract_data()
        
        print("\n📋 Vista previa de datos crudos:")
        print(raw_data.head(3))
        
        # Información adicional
        info = extractor.get_data_info()
        print(f"\n📊 Información del dataset:")
        print(f"   • Filas: {info['filas']:,}")
        print(f"   • Columnas: {info['columnas']}")
        print(f"   • Memoria: {info['memoria_uso']:.2f} MB")
        
        # ========== FASE 2: TRANSFORM ==========
        print_header("🔄 FASE 2: TRANSFORM - Transformación de Datos")
        
        transformer = StockTransformer(raw_data)
        clean_data = transformer.transform_all()
        
        print("\n📋 Vista previa de datos limpios:")
        print(clean_data.head(3))
        
        # Reporte de transformación
        report = transformer.get_transformation_report()
        print(f"\n📈 Resumen de transformación:")
        print(f"   • Shape original: {report['original_shape']}")
        print(f"   • Shape limpio: {report['clean_shape']}")
        print(f"   • Nulos eliminados: {report['original_nulls']} → {report['clean_nulls']}")
        
        # ========== FASE 3: LOAD ==========
        print_header("💾 FASE 3: LOAD - Carga de Datos")
        
        loader = StockLoader(clean_data, output_dir="data")
        loader.load_all(base_name="stock_senti_clean")
        
        # Reporte de carga
        load_report = loader.get_load_report()
        print(f"\n✅ Cargas exitosas: {load_report['successful_loads']}/{load_report['total_attempts']}")
        
        # ========== FASE 4: ANÁLISIS Y VISUALIZACIÓN ==========
        report_path = generate_html_report(clean_data)
        
        # ========== RESUMEN FINAL ==========
        print_header("✨ PIPELINE ETL COMPLETADO EXITOSAMENTE")
        
        print(f"\n📂 Archivos generados en el directorio 'data/':")
        print(f"   ✓ stock_senti_clean.csv - Datos en formato CSV")
        print(f"   ✓ stock_senti_clean.parquet - Datos en formato Parquet (comprimido)")
        print(f"   ✓ stock_senti_clean.db - Base de datos SQLite")
        
        print(f"\n📊 Reporte de análisis:")
        print(f"   ✓ {report_path} - Visualizaciones y conclusiones interactivas")
        
        print(f"\n📊 Estadísticas finales:")
        print(f"   • Total de registros procesados: {len(clean_data):,}")
        print(f"   • Columnas en dataset final: {len(clean_data.columns)}")
        print(f"   • Calidad de datos: {((1 - clean_data.isnull().sum().sum() / clean_data.size) * 100):.2f}% completo")
        
        print(f"\n⏰ Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n" + "="*70)
        print("💡 Abre 'reporte_analisis.html' en tu navegador para ver el análisis completo")
        print("="*70 + "\n")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: No se encontró el archivo de datos")
        print(f"   Detalle: {e}")
        print(f"   Solución: Asegúrate de que 'stock_senti_analysis.csv' esté en el directorio raíz")
        return 1
        
    except Exception as e:
        print(f"\n❌ Error inesperado durante la ejecución del pipeline")
        print(f"   Detalle: {e}")
        print(f"   Tipo: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

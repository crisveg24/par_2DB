"""
Script para generar análisis y visualizaciones del dataset limpio.
Genera gráficas interactivas y una página HTML con resultados.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime

def load_data():
    """Carga los datos limpios"""
    df = pd.read_csv('data/stock_senti_clean.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

def generate_sentiment_distribution(df):
    """Gráfica 1: Distribución de sentimientos"""
    sentiment_counts = df['sentiment'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=sentiment_counts.index,
        values=sentiment_counts.values,
        hole=0.4,
        marker=dict(colors=['#27ae60', '#e74c3c']),
        textinfo='label+percent+value',
        textfont=dict(size=14)
    )])
    
    fig.update_layout(
        title='Distribución de Sentimientos en Noticias (2000-2016)',
        height=500,
        showlegend=True,
        font=dict(size=12)
    )
    
    return fig.to_json()

def generate_temporal_evolution(df):
    """Gráfica 2: Evolución temporal por año"""
    yearly = df.groupby(['year', 'sentiment']).size().reset_index(name='count')
    
    fig = px.bar(
        yearly,
        x='year',
        y='count',
        color='sentiment',
        title='Evolución Anual de Sentimientos en Noticias',
        labels={'count': 'Cantidad de Noticias', 'year': 'Año'},
        color_discrete_map={'Positivo': '#2ecc71', 'Negativo': '#e74c3c'},
        barmode='stack'
    )
    
    fig.update_layout(height=500, xaxis_title='Año', yaxis_title='Cantidad')
    return fig.to_json()

def generate_monthly_heatmap(df):
    """Gráfica 3: Heatmap mensual de sentimientos"""
    monthly = df.groupby(['year', 'month', 'sentiment']).size().reset_index(name='count')
    pivot = monthly[monthly['sentiment'] == 'Positivo'].pivot(
        index='month', 
        columns='year', 
        values='count'
    ).fillna(0)
    
    meses = {1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'May', 6: 'Jun',
             7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'}
    pivot.index = pivot.index.map(meses)
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale='RdYlGn',
        text=pivot.values.astype(int),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Noticias<br>Positivas")
    ))
    
    fig.update_layout(
        title='Heatmap: Noticias Positivas por Mes y Año',
        xaxis_title='Año',
        yaxis_title='Mes',
        height=500
    )
    
    return fig.to_json()

def generate_top_words(df):
    """Gráfica 4: Top palabras más frecuentes"""
    word_counts = {}
    
    for col in [f'top{i}' for i in range(1, 26)]:
        if col in df.columns:
            words = df[col].dropna().str.lower().value_counts()
            for word, count in words.head(50).items():  # Solo top 50
                word_counts[word] = word_counts.get(word, 0) + count
    
    top_words = pd.Series(word_counts).nlargest(15)
    
    fig = go.Figure(data=[go.Bar(
        x=top_words.values,
        y=top_words.index,
        orientation='h',
        marker=dict(
            color=top_words.values,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Frecuencia")
        )
    )])
    
    fig.update_layout(
        title='Top 15 Palabras Más Frecuentes en Noticias',
        xaxis_title='Frecuencia',
        yaxis_title='Palabra',
        height=600,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig.to_json()

def generate_sentiment_by_day(df):
    """Gráfica 5: Sentimiento promedio por día de la semana"""
    dias = {0: 'Lun', 1: 'Mar', 2: 'Mié', 3: 'Jue', 4: 'Vie', 5: 'Sáb', 6: 'Dom'}
    df['dia_nombre'] = df['day_of_week'].map(dias)
    
    daily = df.groupby(['dia_nombre', 'sentiment']).size().reset_index(name='count')
    
    fig = px.bar(
        daily,
        x='dia_nombre',
        y='count',
        color='sentiment',
        title='Distribución de Sentimientos por Día de la Semana',
        labels={'count': 'Cantidad', 'dia_nombre': 'Día'},
        color_discrete_map={'Positivo': '#3498db', 'Negativo': '#e67e22'},
        barmode='group'
    )
    
    fig.update_layout(
        height=500,
        xaxis={'categoryorder': 'array', 'categoryarray': list(dias.values())}
    )
    
    return fig.to_json()

def calculate_statistics(df):
    """Calcula estadísticas relevantes"""
    stats = {
        'total_registros': len(df),
        'positivos': len(df[df['label'] == 1]),
        'negativos': len(df[df['label'] == 0]),
        'pct_positivo': round(len(df[df['label'] == 1]) / len(df) * 100, 1),
        'pct_negativo': round(len(df[df['label'] == 0]) / len(df) * 100, 1),
        'fecha_inicio': df['date'].min().strftime('%Y-%m-%d'),
        'fecha_fin': df['date'].max().strftime('%Y-%m-%d'),
        'años_totales': df['year'].nunique(),
        'dias_totales': df['date'].nunique(),
        'promedio_por_dia': round(len(df) / df['date'].nunique(), 2)
    }
    
    return stats

def generate_html(graphs, stats):
    """Genera página HTML con todas las visualizaciones"""
    
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análisis de Sentimientos - Stock News Dataset</title>
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
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 40px;
            background: #f8f9fa;
        }}
        
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 12px rgba(0,0,0,0.15);
        }}
        
        .stat-card .number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }}
        
        .stat-card .label {{
            font-size: 0.9em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .graphs-section {{
            padding: 40px;
        }}
        
        .graph-container {{
            margin-bottom: 40px;
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }}
        
        .conclusions {{
            padding: 40px;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }}
        
        .conclusions h2 {{
            font-size: 2em;
            margin-bottom: 30px;
            text-align: center;
        }}
        
        .conclusion-item {{
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
        }}
        
        .conclusion-item h3 {{
            font-size: 1.3em;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
        }}
        
        .conclusion-item h3::before {{
            content: "✓";
            display: inline-block;
            margin-right: 10px;
            background: white;
            color: #f5576c;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            text-align: center;
            line-height: 30px;
            font-weight: bold;
        }}
        
        .conclusion-item p {{
            font-size: 1.1em;
            line-height: 1.6;
            opacity: 0.95;
        }}
        
        footer {{
            background: #2c3e50;
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        footer p {{
            margin-bottom: 10px;
        }}
        
        .badge {{
            display: inline-block;
            padding: 5px 15px;
            background: #27ae60;
            color: white;
            border-radius: 20px;
            font-size: 0.9em;
            margin: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Análisis de Sentimientos en Noticias Financieras</h1>
            <p>Dataset: Stock Sentiment Analysis (2000-2016)</p>
            <p>Pipeline ETL + Análisis Exploratorio de Datos</p>
        </header>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="number">{stats['total_registros']:,}</div>
                <div class="label">Total Noticias</div>
            </div>
            <div class="stat-card">
                <div class="number">{stats['años_totales']}</div>
                <div class="label">Años Analizados</div>
            </div>
            <div class="stat-card">
                <div class="number">{stats['pct_positivo']}%</div>
                <div class="label">Positivas</div>
            </div>
            <div class="stat-card">
                <div class="number">{stats['pct_negativo']}%</div>
                <div class="label">Negativas</div>
            </div>
            <div class="stat-card">
                <div class="number">{stats['promedio_por_dia']}</div>
                <div class="label">Promedio/Día</div>
            </div>
        </div>
        
        <div class="graphs-section">
            <h2 style="text-align: center; margin-bottom: 40px; color: #667eea; font-size: 2em;">
                📈 Visualizaciones Interactivas
            </h2>
            
            <div class="graph-container">
                <div id="graph1"></div>
            </div>
            
            <div class="graph-container">
                <div id="graph2"></div>
            </div>
            
            <div class="graph-container">
                <div id="graph3"></div>
            </div>
            
            <div class="graph-container">
                <div id="graph4"></div>
            </div>
            
            <div class="graph-container">
                <div id="graph5"></div>
            </div>
        </div>
        
        <div class="conclusions">
            <h2>🎯 Conclusiones del Análisis</h2>
            
            <div class="conclusion-item">
                <h3>Balance Equilibrado de Sentimientos</h3>
                <p>
                    El dataset muestra un balance casi perfecto entre noticias positivas ({stats['pct_positivo']}%) 
                    y negativas ({stats['pct_negativo']}%), lo que indica que el dataset no tiene sesgo hacia ningún 
                    sentimiento particular. Esto es ideal para entrenar modelos de clasificación de sentimientos, 
                    ya que evita problemas de desbalanceo de clases.
                </p>
            </div>
            
            <div class="conclusion-item">
                <h3>Cobertura Temporal Extensa</h3>
                <p>
                    Con datos que abarcan desde {stats['fecha_inicio']} hasta {stats['fecha_fin']}, 
                    el dataset cubre {stats['años_totales']} años de noticias financieras. Esta amplitud temporal 
                    permite analizar cómo ha evolucionado el sentimiento en el mercado a lo largo de diferentes 
                    ciclos económicos, crisis financieras y periodos de crecimiento.
                </p>
            </div>
            
            <div class="conclusion-item">
                <h3>Patrones Temporales Identificados</h3>
                <p>
                    El análisis revela que el sentimiento en las noticias no se distribuye uniformemente a lo largo 
                    del tiempo. Se observan periodos con mayor concentración de noticias negativas que podrían 
                    correlacionarse con eventos económicos significativos. El heatmap mensual muestra variaciones 
                    estacionales en la frecuencia y el tono de las noticias.
                </p>
            </div>
            
            <div class="conclusion-item">
                <h3>Palabras Clave Relevantes</h3>
                <p>
                    Las palabras más frecuentes en el dataset están relacionadas con eventos noticiosos, 
                    correcciones editoriales y temas recurrentes en medios financieros. El análisis de estas 
                    palabras clave puede ayudar a identificar los temas más relevantes en diferentes periodos 
                    y su asociación con sentimientos positivos o negativos.
                </p>
            </div>
            
            <div class="conclusion-item">
                <h3>Calidad de Datos Óptima</h3>
                <p>
                    Después del proceso ETL, el dataset no contiene valores nulos, duplicados ni inconsistencias. 
                    Se han creado 6 features temporales adicionales (año, mes, día, día de la semana, trimestre 
                    y sentimiento textual) que enriquecen el análisis. Los datos están listos para ser utilizados 
                    en modelos de machine learning o análisis más profundos.
                </p>
            </div>
        </div>
        
        <footer>
            <p><strong>Pipeline ETL Implementado</strong></p>
            <div>
                <span class="badge">Extract</span>
                <span class="badge">Transform</span>
                <span class="badge">Load</span>
            </div>
            <p style="margin-top: 20px;">
                Formatos de salida: CSV, Parquet, SQLite
            </p>
            <p style="opacity: 0.7; margin-top: 20px;">
                Generado el {datetime.now().strftime('%d de %B de %Y a las %H:%M')}
            </p>
        </footer>
    </div>
    
    <script>
        // Cargar gráficas
        var graphs = {json.dumps({f'graph{i+1}': graph for i, graph in enumerate(graphs)})};
        
        Object.keys(graphs).forEach(function(key) {{
            var graphData = JSON.parse(graphs[key]);
            Plotly.newPlot(key, graphData.data, graphData.layout, {{responsive: true}});
        }});
    </script>
</body>
</html>"""
    
    return html_content

def main():
    """Función principal"""
    print("="*70)
    print("🎨 GENERANDO ANÁLISIS Y VISUALIZACIONES")
    print("="*70)
    
    print("\n📂 Cargando datos limpios...")
    df = load_data()
    print(f"✅ {len(df):,} registros cargados")
    
    print("\n📊 Generando estadísticas...")
    stats = calculate_statistics(df)
    print("✅ Estadísticas calculadas")
    
    print("\n📈 Generando visualizaciones...")
    graphs = []
    
    print("   1. Distribución de sentimientos...")
    graphs.append(generate_sentiment_distribution(df))
    
    print("   2. Evolución temporal...")
    graphs.append(generate_temporal_evolution(df))
    
    print("   3. Heatmap mensual...")
    graphs.append(generate_monthly_heatmap(df))
    
    print("   4. Top palabras frecuentes...")
    graphs.append(generate_top_words(df))
    
    print("   5. Sentimientos por día...")
    graphs.append(generate_sentiment_by_day(df))
    
    print("✅ 5 visualizaciones generadas")
    
    print("\n🌐 Generando página HTML...")
    html_content = generate_html(graphs, stats)
    
    with open('analysis_report.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Página HTML generada: analysis_report.html")
    
    print("\n" + "="*70)
    print("✅ ANÁLISIS COMPLETADO")
    print("="*70)
    print("\n📌 Para ver el análisis, abre: analysis_report.html")
    print("   Las gráficas son interactivas (zoom, pan, hover, etc.)")
    print("\n")

if __name__ == "__main__":
    main()

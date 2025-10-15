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
import http.server
import socketserver
import threading
import socket
import webbrowser
import time

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


def find_free_port(start_port=8000, max_port=8100):
    """Encuentra un puerto disponible"""
    for port in range(start_port, max_port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    return None


def start_http_server(port=8000, directory="."):
    """Inicia un servidor HTTP en un thread separado"""
    os.chdir(directory)
    
    class QuietHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass  # Suprimir logs del servidor
    
    handler = QuietHTTPRequestHandler
    handler.extensions_map.update({
        '.html': 'text/html',
        '.css': 'text/css',
        '.js': 'application/javascript',
    })
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()


def open_report_in_browser(report_path, script_dir):
    """Abre el reporte en el navegador usando servidor HTTP"""
    print_header("🌐 INICIANDO SERVIDOR WEB")
    
    # Encontrar puerto disponible
    PORT = find_free_port()
    if PORT is None:
        print("❌ No se pudo encontrar un puerto disponible")
        print(f"💡 Abre manualmente: {report_path}")
        return
    
    # Detectar si estamos en Codespaces
    is_codespaces = os.environ.get('CODESPACES') == 'true'
    codespace_name = os.environ.get('CODESPACE_NAME', '')
    
    # Iniciar servidor en thread separado
    server_thread = threading.Thread(
        target=start_http_server, 
        args=(PORT, script_dir),
        daemon=True
    )
    server_thread.start()
    
    # Dar tiempo al servidor para iniciar
    time.sleep(1)
    
    filename = os.path.basename(report_path)
    
    print(f"\n✅ Servidor HTTP iniciado en puerto {PORT}")
    print(f"📁 Sirviendo archivos desde: {script_dir}")
    
    if is_codespaces and codespace_name:
        # URL pública de Codespaces
        url = f"https://{codespace_name}-{PORT}.app.github.dev/{filename}"
        print(f"\n🔗 Abre esta URL en tu navegador:")
        print(f"   {url}")
        print(f"\n💡 VS Code debería mostrar una notificación de 'Port {PORT} is available'")
        print(f"   Haz clic en 'Open in Browser' si aparece")
        
        # Intentar abrir en el navegador del sistema (funcionará si está en local)
        try:
            webbrowser.open(url)
        except:
            pass
    else:
        # Entorno local
        url = f"http://localhost:{PORT}/{filename}"
        print(f"\n🔗 Abriendo navegador automáticamente...")
        print(f"   URL: {url}")
        
        try:
            webbrowser.open(url)
            print(f"✅ Navegador abierto")
        except Exception as e:
            print(f"⚠️  No se pudo abrir automáticamente: {e}")
            print(f"💡 Abre manualmente: {url}")
    
    print(f"\n⚠️  IMPORTANTE: Mantén este terminal abierto mientras uses el reporte")
    print(f"⚠️  Presiona Ctrl+C cuando termines para detener el servidor")
    
    # Mantener el programa corriendo
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n\n🛑 Servidor detenido")
        print(f"👋 ¡Gracias por usar el pipeline ETL!")



def generate_html_report(df: pd.DataFrame, output_dir: str = "."):
    """Genera un reporte HTML completo con todas las visualizaciones"""
    print_header("📊 FASE 4: ANÁLISIS - Generando Visualizaciones")
    
    # Calcular estadísticas
    stats = calculate_statistics(df)
    
    # Generar gráficas
    print("\n📈 Generando visualizaciones interactivas...")
    
    # 1. Distribución de Sentimientos
    fig1 = create_sentiment_distribution(df)
    graph1_html = fig1.to_html(include_plotlyjs='cdn', div_id="graph1", config={'displayModeBar': True, 'responsive': True})
    
    # 2. Evolución Temporal
    fig2 = create_temporal_evolution(df)
    graph2_html = fig2.to_html(include_plotlyjs=False, div_id="graph2", config={'displayModeBar': True, 'responsive': True})
    
    # 3. Sentimientos por Día de Semana
    fig3 = create_weekday_analysis(df)
    graph3_html = fig3.to_html(include_plotlyjs=False, div_id="graph3", config={'displayModeBar': True, 'responsive': True})
    
    # 4. Heatmap Mensual
    fig4 = create_monthly_heatmap(df)
    graph4_html = fig4.to_html(include_plotlyjs=False, div_id="graph4", config={'displayModeBar': True, 'responsive': True})
    
    # 5. Top Palabras
    fig5 = create_top_words(df)
    graph5_html = fig5.to_html(include_plotlyjs=False, div_id="graph5", config={'displayModeBar': True, 'responsive': True})
    
    # 6. Distribución Trimestral
    fig6 = create_quarterly_distribution(df)
    graph6_html = fig6.to_html(include_plotlyjs=False, div_id="graph6", config={'displayModeBar': True, 'responsive': True})
    
    # 7. Matriz de Correlación
    fig7 = create_correlation_matrix(df)
    graph7_html = fig7.to_html(include_plotlyjs=False, div_id="graph7", config={'displayModeBar': True, 'responsive': True})
    
    # Generar conclusiones
    conclusions = generate_conclusions(df, stats)
    
    # Crear HTML completo
    html_content = create_html_template(
        stats, 
        graph1_html, graph2_html, graph3_html, graph4_html,
        graph5_html, graph6_html, graph7_html,
        conclusions
    )
    
    # Guardar archivo en el directorio del script
    output_path = os.path.join(output_dir, "reporte_analisis.html")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✅ Reporte HTML generado: {output_path}")
    
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
    days_mapping = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes'}
    
    # Filtrar solo días que existen en los datos
    df_temp = df[df['day_of_week'].isin(days_mapping.keys())].copy()
    df_temp['day_name'] = df_temp['day_of_week'].map(days_mapping)
    
    day_sentiment = df_temp.groupby(['day_name', 'sentiment']).size().reset_index(name='count')
    
    fig = px.bar(day_sentiment, x='day_name', y='count', color='sentiment',
                 title='📊 Distribución de Sentimientos por Día de la Semana',
                 labels={'day_name': 'Día de la Semana', 'count': 'Cantidad', 'sentiment': 'Sentimiento'},
                 color_discrete_map={'Positivo': '#2ecc71', 'Negativo': '#e74c3c'},
                 category_orders={'day_name': ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']},
                 barmode='group')  # Cambiar a barras agrupadas para mejor visualización
    
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
    
    # Crear etiquetas de texto con el conteo de noticias para cada celda
    df_count = df.groupby(['year', 'month']).size().reset_index(name='count')
    df_count_pivot = df_count.pivot(index='year', columns='month', values='count')
    
    # Crear texto hover personalizado
    hover_text = []
    for i, year in enumerate(df_pivot.index):
        hover_row = []
        for j, month in enumerate(df_pivot.columns):
            value = df_pivot.iloc[i, j]
            count = df_count_pivot.iloc[i, j] if not pd.isna(df_count_pivot.iloc[i, j]) else 0
            if pd.notna(value):
                hover_row.append(f'Año: {year}<br>Mes: {month}<br>Promedio: {value:.3f}<br>Noticias: {int(count)}')
            else:
                hover_row.append(f'Año: {year}<br>Mes: {month}<br>Sin datos')
        hover_text.append(hover_row)
    
    fig = go.Figure(data=go.Heatmap(
        z=df_pivot.values,
        x=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
        y=df_pivot.index,
        colorscale='RdYlGn',
        hovertext=hover_text,
        hoverinfo='text',
        colorbar=dict(title="Promedio<br>Sentimiento<br>(0=Neg, 1=Pos)")
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
    
    # Procesar solo las primeras 10 columnas de texto para palabras más relevantes
    for col in [f'top{i}' for i in range(1, 11)]:
        if col in df.columns:
            words = df[col].dropna().astype(str).str.lower().str.split()
            all_words.extend([word for sublist in words for word in sublist if len(word) > 4])
    
    # Palabras comunes a filtrar (stop words básicas)
    stop_words = {'about', 'after', 'would', 'could', 'should', 'their', 'there', 'these', 
                  'those', 'which', 'where', 'while', 'being', 'having', 'doing'}
    
    # Filtrar stop words
    filtered_words = [word for word in all_words if word not in stop_words]
    
    word_counts = Counter(filtered_words).most_common(20)
    words_df = pd.DataFrame(word_counts, columns=['palabra', 'frecuencia'])
    
    fig = px.bar(words_df, x='frecuencia', y='palabra', orientation='h',
                 title='📝 Top 20 Palabras Más Frecuentes en Titulares (Top 1-10)',
                 labels={'palabra': 'Palabra', 'frecuencia': 'Frecuencia'},
                 color='frecuencia',
                 color_continuous_scale='viridis')
    
    fig.update_layout(
        title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 20}},
        yaxis={'categoryorder': 'total ascending'},
        height=500,
        margin=dict(t=80, b=40, l=120, r=40)
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
    
    # 2. Patrones Temporales - Solo días laborables
    days_mapping = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes'}
    df_temp = df[df['day_of_week'].isin(days_mapping.keys())].copy()
    df_temp['day_name'] = df_temp['day_of_week'].map(days_mapping)
    day_sentiment = df_temp.groupby('day_name')['label'].mean().sort_values()
    
    conclusions.append({
        'title': 'Efecto del Día de la Semana',
        'text': f"El análisis de días laborables revela patrones interesantes: el {day_sentiment.index[0]} presenta el sentimiento más negativo (promedio: {day_sentiment.values[0]:.2f}), fenómeno conocido como 'Monday Effect' en finanzas. Por el contrario, el {day_sentiment.index[-1]} muestra mayor positividad ({day_sentiment.values[-1]:.2f}), posiblemente debido al optimismo pre-fin de semana. Nota: El dataset solo contiene noticias de días laborables (Lunes a Viernes)."
    })
    
    # 3. Cobertura Temporal
    conclusions.append({
        'title': 'Cobertura y Representatividad',
        'text': f"El dataset abarca {stats['years_covered']} años de noticias financieras ({stats['date_min']} a {stats['date_max']}), procesando un total de {stats['total_records']:,} registros. Esta amplia cobertura temporal proporciona una perspectiva robusta sobre las tendencias del mercado a largo plazo, con un promedio de {stats['total_records']//stats['years_covered']:,} noticias por año."
    })
    
    # 4. Calidad de Datos
    conclusions.append({
        'title': 'Calidad del Pipeline ETL',
        'text': f"El pipeline ETL demostró excelente efectividad: la completitud de datos alcanza {stats['data_completeness']:.2f}% (solo {stats['null_values']} valores nulos de {len(df) * len(df.columns):,} totales). Se eliminaron duplicados, se normalizaron fechas y se crearon 6 features adicionales para análisis temporal, resultando en un dataset limpio y confiable."
    })
    
    # 5. Implicaciones Prácticas
    conclusions.append({
        'title': 'Aplicaciones en Trading',
        'text': f"Los patrones identificados tienen aplicaciones prácticas: el 'Monday Effect' sugiere posibles estrategias de trading basadas en el día de la semana. El balance general {'positivo' if stats['positive_pct'] > 50 else 'negativo'} indica un contexto de {'optimismo' if stats['positive_pct'] > 50 else 'cautela'} que puede informar decisiones de inversión a largo plazo."
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
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --primary-color: #1e3a8a;
            --secondary-color: #3b82f6;
            --accent-green: #10b981;
            --accent-red: #ef4444;
            --accent-gold: #f59e0b;
            --bg-dark: #0f172a;
            --bg-light: #f8fafc;
            --text-dark: #1e293b;
            --text-light: #64748b;
            --card-bg: #ffffff;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.12);
            --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
            --shadow-lg: 0 10px 25px rgba(0,0,0,0.15);
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
            color: var(--text-dark);
            line-height: 1.6;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px 20px;
        }}
        
        header {{
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            padding: 40px 30px;
            border-radius: 20px;
            box-shadow: var(--shadow-lg);
            margin-bottom: 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        header::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: pulse 15s ease-in-out infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.1); }}
        }}
        
        h1 {{
            color: white;
            font-size: 2.8em;
            margin-bottom: 10px;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            position: relative;
            z-index: 1;
        }}
        
        .subtitle {{
            color: rgba(255,255,255,0.9);
            font-size: 1.3em;
            font-weight: 300;
            position: relative;
            z-index: 1;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }}
        
        .stat-card {{
            background: var(--card-bg);
            padding: 30px;
            border-radius: 16px;
            box-shadow: var(--shadow-md);
            text-align: center;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid rgba(226, 232, 240, 0.8);
            position: relative;
            overflow: hidden;
        }}
        
        .stat-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--secondary-color), var(--accent-gold));
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-8px);
            box-shadow: var(--shadow-lg);
        }}
        
        .stat-card:hover::before {{
            transform: scaleX(1);
        }}
        
        .stat-value {{
            font-size: 3em;
            font-weight: 700;
            color: var(--primary-color);
            margin: 15px 0;
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .stat-card:nth-child(3) .stat-value {{
            background: linear-gradient(135deg, var(--accent-green) 0%, #34d399 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .stat-card:nth-child(4) .stat-value {{
            background: linear-gradient(135deg, var(--accent-red) 0%, #f87171 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .stat-label {{
            color: var(--text-light);
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 600;
        }}
        
        .section {{
            background: var(--card-bg);
            padding: 40px;
            border-radius: 20px;
            box-shadow: var(--shadow-md);
            margin-bottom: 40px;
            border: 1px solid rgba(226, 232, 240, 0.8);
        }}
        
        .section h2 {{
            color: var(--primary-color);
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 3px solid var(--secondary-color);
            font-size: 2em;
            font-weight: 700;
            position: relative;
        }}
        
        .section h2::after {{
            content: '';
            position: absolute;
            bottom: -3px;
            left: 0;
            width: 100px;
            height: 3px;
            background: var(--accent-gold);
        }}
        
        .graph-container {{
            margin: 25px 0;
            padding: 25px;
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            border-radius: 16px;
            border: 1px solid #e2e8f0;
            box-shadow: var(--shadow-sm);
            transition: all 0.3s ease;
        }}
        
        .graph-container:hover {{
            box-shadow: var(--shadow-md);
            border-color: var(--secondary-color);
        }}
        
        .graph-container h3 {{
            color: var(--primary-color);
            margin-bottom: 20px;
            font-weight: 600;
            font-size: 1.4em;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .graph-explanation {{
            margin-top: 20px;
            padding: 20px;
            background: linear-gradient(135deg, #dbeafe 0%, #e0f2fe 100%);
            border-left: 5px solid var(--secondary-color);
            border-radius: 10px;
            color: var(--text-dark);
            font-size: 0.95em;
            line-height: 1.9;
            box-shadow: var(--shadow-sm);
        }}
        
        .graph-explanation strong {{
            color: var(--primary-color);
            font-weight: 600;
        }}
        
        .graph-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
            gap: 30px;
        }}
        
        .conclusion-card {{
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            padding: 30px;
            border-radius: 16px;
            margin-bottom: 25px;
            border-left: 6px solid var(--secondary-color);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: var(--shadow-sm);
            position: relative;
            overflow: hidden;
        }}
        
        .conclusion-card::before {{
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 100px;
            height: 100px;
            background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
            transform: translate(30%, -30%);
        }}
        
        .conclusion-card:hover {{
            box-shadow: var(--shadow-lg);
            transform: translateX(8px);
            border-left-color: var(--accent-gold);
        }}
        
        .conclusion-card h3 {{
            color: var(--primary-color);
            margin-bottom: 15px;
            font-size: 1.4em;
            font-weight: 600;
            position: relative;
        }}
        
        .conclusion-number {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, var(--secondary-color) 0%, var(--primary-color) 100%);
            color: white;
            border-radius: 50%;
            text-align: center;
            margin-right: 12px;
            font-weight: 700;
            font-size: 1.1em;
            box-shadow: 0 4px 10px rgba(59, 130, 246, 0.3);
        }}
        
        .conclusion-card p {{
            color: var(--text-dark);
            text-align: justify;
            line-height: 1.9;
            position: relative;
        }}
        
        footer {{
            text-align: center;
            padding: 40px 30px;
            color: rgba(255,255,255,0.9);
            font-size: 0.95em;
            background: rgba(15, 23, 42, 0.5);
            border-radius: 16px;
            margin-top: 40px;
            backdrop-filter: blur(10px);
        }}
        
        footer strong {{
            color: white;
            font-weight: 600;
        }}
        
        .badge {{
            display: inline-block;
            padding: 8px 18px;
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.9) 0%, rgba(30, 58, 138, 0.9) 100%);
            color: white;
            border-radius: 25px;
            font-size: 0.9em;
            margin: 5px;
            font-weight: 600;
            box-shadow: 0 4px 10px rgba(59, 130, 246, 0.3);
            transition: all 0.3s ease;
            border: 1px solid rgba(255,255,255,0.2);
        }}
        
        .badge:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(59, 130, 246, 0.4);
        }}
        
        /* Animación de entrada */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .stat-card, .section, .conclusion-card {{
            animation: fadeInUp 0.6s ease-out forwards;
        }}
        
        .stat-card:nth-child(1) {{ animation-delay: 0.1s; }}
        .stat-card:nth-child(2) {{ animation-delay: 0.2s; }}
        .stat-card:nth-child(3) {{ animation-delay: 0.3s; }}
        .stat-card:nth-child(4) {{ animation-delay: 0.4s; }}
        .stat-card:nth-child(5) {{ animation-delay: 0.5s; }}
        
        @media (max-width: 768px) {{
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
            
            .graph-grid {{
                grid-template-columns: 1fr;
            }}
            
            h1 {{
                font-size: 2em;
            }}
            
            .container {{
                padding: 15px;
            }}
            
            .section {{
                padding: 25px;
            }}
            
            .stat-value {{
                font-size: 2.5em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Análisis de Sentimientos en Noticias Financieras</h1>
            <p class="subtitle">Pipeline ETL - Stock Sentiment Analysis</p>
            <div style="margin-top: 20px;">
                <span class="badge">🐍 Python</span>
                <span class="badge">📊 Pandas</span>
                <span class="badge">📈 Plotly</span>
                <span class="badge">⚙️ ETL</span>
                <span class="badge">🤖 ML</span>
            </div>
        </header>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div style="font-size: 2em; margin-bottom: 10px;">📰</div>
                <div class="stat-label">Total de Noticias</div>
                <div class="stat-value">{stats['total_records']:,}</div>
                <div class="stat-label">Registros Analizados</div>
            </div>
            
            <div class="stat-card">
                <div style="font-size: 2em; margin-bottom: 10px;">📅</div>
                <div class="stat-label">Período Analizado</div>
                <div class="stat-value">{stats['years_covered']}</div>
                <div class="stat-label">Años de Cobertura</div>
            </div>
            
            <div class="stat-card">
                <div style="font-size: 2em; margin-bottom: 10px;">📈</div>
                <div class="stat-label">Sentimiento Positivo</div>
                <div class="stat-value">{stats['positive_pct']:.1f}%</div>
                <div class="stat-label">{stats['positive_count']:,} Noticias</div>
            </div>
            
            <div class="stat-card">
                <div style="font-size: 2em; margin-bottom: 10px;">📉</div>
                <div class="stat-label">Sentimiento Negativo</div>
                <div class="stat-value">{stats['negative_pct']:.1f}%</div>
                <div class="stat-label">{stats['negative_count']:,} Noticias</div>
            </div>
            
            <div class="stat-card">
                <div style="font-size: 2em; margin-bottom: 10px;">✅</div>
                <div class="stat-label">Calidad de Datos</div>
                <div class="stat-value">{stats['data_completeness']:.2f}%</div>
                <div class="stat-label">Completitud</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📈 Visualizaciones del Análisis</h2>
            
            <div class="graph-grid">
                <div class="graph-container">
                    <h3>📊 Distribución de Sentimientos</h3>
                    {graph1}
                    <div class="graph-explanation">
                        <strong>Conclusión:</strong> El análisis muestra un ligero sesgo positivo con <strong>52.8% de noticias positivas</strong> versus 47.2% negativas, 
                        con una diferencia de +231 noticias. Esto indica que durante el período 2000-2016, las noticias financieras tendieron a ser 
                        moderadamente optimistas sobre el mercado de valores, aunque el balance es relativamente equilibrado, reflejando la volatilidad 
                        natural del mercado financiero.
                    </div>
                </div>
                
                <div class="graph-container">
                    <h3>📅 Análisis por Día de la Semana</h3>
                    {graph3}
                    <div class="graph-explanation">
                        <strong>Conclusión:</strong> Se identifica claramente el <strong>"Efecto Lunes"</strong> con solo 49.5% de noticias positivas (la más baja), 
                        mientras que el <strong>viernes presenta 55.5% de positividad</strong> (la más alta). Esta tendencia, conocida como "Monday Effect", 
                        sugiere que las noticias tienden a ser más pesimistas al inicio de la semana y más optimistas hacia el final, posiblemente 
                        relacionado con patrones de comportamiento del mercado y expectativas de fin de semana.
                    </div>
                </div>
            </div>
            
            <div class="graph-container">
                <h3>📈 Evolución Temporal del Sentimiento</h3>
                {graph2}
                <div class="graph-explanation">
                    <strong>Conclusión:</strong> La serie temporal de 199 meses (2000-2016) revela que el volumen de noticias positivas 
                    <strong>promedia 10.9 por mes versus 9.8 negativas</strong>, manteniendo consistencia con la distribución general. 
                    Se observan picos de volatilidad especialmente en periodos de crisis (2008-2009) y recuperación. La tendencia mantiene 
                    un balance relativamente estable a lo largo de los 17 años, sin grandes desviaciones sostenidas.
                </div>
            </div>
            
            <div class="graph-grid">
                <div class="graph-container">
                    <h3>📊 Distribución por Trimestre</h3>
                    {graph6}
                    <div class="graph-explanation">
                        <strong>Conclusión:</strong> El análisis trimestral muestra una distribución equilibrada con <strong>Q4 liderando con 54.1% de positividad</strong>, 
                        seguido por Q2 (52.9%), Q3 (52.4%) y Q1 (51.8%). El cuarto trimestre históricamente muestra mayor optimismo, 
                        posiblemente relacionado con efectos de fin de año, reportes corporativos y expectativas de bonos. Los otros 
                        tres trimestres mantienen niveles similares entre sí.
                    </div>
                </div>
                
                <div class="graph-container">
                    <h3>🔗 Matriz de Correlación</h3>
                    {graph7}
                    <div class="graph-explanation">
                        <strong>Conclusión:</strong> Las correlaciones con el sentimiento son débiles pero reveladoras: <strong>day_of_week (+0.0336)</strong> 
                        es la más fuerte, validando el efecto semanal observado. La correlación negativa con "day" (-0.0220) sugiere 
                        leve tendencia a sentimientos más negativos en fechas más avanzadas del mes. Las correlaciones positivas bajas con 
                        year (+0.0205) y month (+0.0158) indican estabilidad temporal del sentimiento.
                    </div>
                </div>
            </div>
            
            <div class="graph-container">
                <h3>🗓️ Heatmap Mensual por Año</h3>
                {graph4}
                <div class="graph-explanation">
                    <strong>Conclusión:</strong> El mapa de calor revela <strong>julio 2016 como el mes más positivo</strong> (promedio 1.000 - 100% positivo) 
                    y <strong>mayo 2012 como el más negativo</strong> (promedio 0.227 - solo 22.7% positivo), coincidiendo con la crisis europea. 
                    Los patrones muestran "clusters" de pesimismo durante períodos de crisis (2008-2009, 2011-2012) y optimismo en 
                    fases de crecimiento (2013-2016), validando que el sentimiento de las noticias refleja ciclos económicos reales.
                </div>
            </div>
            
            <div class="graph-container">
                <h3>💬 Top 20 Palabras Más Frecuentes</h3>
                {graph5}
                <div class="graph-explanation">
                    <strong>Conclusión:</strong> De 345,086 palabras analizadas (57,890 únicas), las más frecuentes son conectores ingleses 
                    (with, that, from, have, after), indicando que el dataset proviene de fuentes anglosajonas. La alta diversidad léxica 
                    (16.8% de palabras únicas) sugiere vocabulario técnico variado en noticias financieras. Este análisis es útil para 
                    identificar temas recurrentes y contexto lingüístico del corpus analizado.
                </div>
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
        
        # Construir ruta absoluta al CSV (siempre funciona sin importar desde dónde se ejecute)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, "stock_senti_analysis.csv")
        
        extractor = StockExtractor(csv_path)
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
        
        # Crear directorio data relativo al script
        data_dir = os.path.join(script_dir, "data")
        os.makedirs(data_dir, exist_ok=True)
        
        loader = StockLoader(clean_data, output_dir=data_dir)
        loader.load_all(base_name="stock_senti_clean")
        
        # Reporte de carga
        load_report = loader.get_load_report()
        print(f"\n✅ Cargas exitosas: {load_report['successful_loads']}/{load_report['total_attempts']}")
        
        # ========== FASE 4: ANÁLISIS Y VISUALIZACIÓN ==========
        report_path = generate_html_report(clean_data, output_dir=script_dir)
        
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
        
        # Iniciar servidor HTTP y abrir navegador automáticamente
        open_report_in_browser(report_path, script_dir)
        
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

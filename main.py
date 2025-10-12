"""
Pipeline ETL para Análisis de Sentimientos de Acciones
Autor: Proyecto ETL - Stock Sentiment Analysis
Fecha: Octubre 2025

Este script ejecuta el pipeline completo ETL:
1. Extract: Extrae datos del CSV
2. Transform: Limpia y transforma los datos
3. Load: Carga los datos en múltiples formatos
"""
import sys
import os
from datetime import datetime

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
        
        # ========== RESUMEN FINAL ==========
        print_header("✨ PIPELINE ETL COMPLETADO EXITOSAMENTE")
        
        print(f"\n📂 Archivos generados en el directorio 'data/':")
        print(f"   ✓ stock_senti_clean.csv - Datos en formato CSV")
        print(f"   ✓ stock_senti_clean.parquet - Datos en formato Parquet (comprimido)")
        print(f"   ✓ stock_senti_clean.db - Base de datos SQLite")
        
        print(f"\n📊 Estadísticas finales:")
        print(f"   • Total de registros procesados: {len(clean_data):,}")
        print(f"   • Columnas en dataset final: {len(clean_data.columns)}")
        print(f"   • Calidad de datos: {((1 - clean_data.isnull().sum().sum() / clean_data.size) * 100):.2f}% completo")
        
        print(f"\n⏰ Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n" + "="*70)
        print("💡 Siguiente paso: Ejecutar notebooks/02_eda.ipynb para análisis exploratorio")
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

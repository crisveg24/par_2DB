"""
Módulo de Carga de Datos
Carga los datos limpios en diferentes formatos: CSV, Parquet, SQLite
"""
import pandas as pd
import sqlite3
import os
from pathlib import Path
from typing import Optional


class StockLoader:
    """Clase para cargar datos limpios en diferentes formatos"""
    
    def __init__(self, data: pd.DataFrame, output_dir: str = "data"):
        """
        Inicializa el loader con los datos limpios
        
        Args:
            data: DataFrame con los datos limpios
            output_dir: Directorio donde guardar los archivos
        """
        self.data = data
        self.output_dir = output_dir
        self.load_log = []
        
        # Crear directorio si no existe
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
    
    def load_all(self, base_name: str = "stock_senti_clean"):
        """
        Carga los datos en todos los formatos disponibles
        
        Args:
            base_name: Nombre base para los archivos de salida
        """
        print("\n💾 INICIANDO PROCESO DE CARGA")
        print("="*60)
        
        # Cargar en CSV
        self.load_to_csv(base_name)
        
        # Cargar en Parquet
        self.load_to_parquet(base_name)
        
        # Cargar en SQLite
        self.load_to_sqlite(base_name)
        
        print("\n✅ CARGA COMPLETADA")
        self._print_load_summary()
    
    def load_to_csv(self, file_name: str = "stock_senti_clean") -> str:
        """
        Guarda los datos en formato CSV
        
        Args:
            file_name: Nombre del archivo (sin extensión)
            
        Returns:
            Ruta completa del archivo guardado
        """
        print("\n📄 Guardando en formato CSV...")
        
        file_path = os.path.join(self.output_dir, f"{file_name}.csv")
        
        try:
            # Asegurar que no haya NaN antes de guardar - reemplazar con strings vacíos
            data_to_save = self.data.copy()
            # Reemplazar NaN solo en columnas de texto
            text_cols = data_to_save.select_dtypes(include=['object']).columns
            for col in text_cols:
                data_to_save[col] = data_to_save[col].fillna('')
            
            data_to_save.to_csv(file_path, index=False, encoding='utf-8', na_rep='')
            file_size = os.path.getsize(file_path) / 1024  # KB
            
            self.load_log.append({
                'formato': 'CSV',
                'archivo': file_path,
                'tamaño': f"{file_size:.2f} KB",
                'filas': len(self.data),
                'exitoso': True
            })
            
            print(f"   ✓ CSV guardado: {file_path}")
            print(f"   ✓ Tamaño: {file_size:.2f} KB")
            
            return file_path
            
        except Exception as e:
            print(f"   ❌ Error al guardar CSV: {e}")
            self.load_log.append({
                'formato': 'CSV',
                'error': str(e),
                'exitoso': False
            })
            raise
    
    def load_to_parquet(self, file_name: str = "stock_senti_clean") -> str:
        """
        Guarda los datos en formato Parquet
        
        Args:
            file_name: Nombre del archivo (sin extensión)
            
        Returns:
            Ruta completa del archivo guardado
        """
        print("\n📦 Guardando en formato Parquet...")
        
        file_path = os.path.join(self.output_dir, f"{file_name}.parquet")
        
        try:
            self.data.to_parquet(file_path, index=False, compression='snappy')
            file_size = os.path.getsize(file_path) / 1024  # KB
            
            self.load_log.append({
                'formato': 'Parquet',
                'archivo': file_path,
                'tamaño': f"{file_size:.2f} KB",
                'filas': len(self.data),
                'exitoso': True
            })
            
            print(f"   ✓ Parquet guardado: {file_path}")
            print(f"   ✓ Tamaño: {file_size:.2f} KB")
            print(f"   ✓ Compresión: snappy")
            
            return file_path
            
        except Exception as e:
            print(f"   ❌ Error al guardar Parquet: {e}")
            self.load_log.append({
                'formato': 'Parquet',
                'error': str(e),
                'exitoso': False
            })
            # No lanzar excepción si solo falla Parquet
            return None
    
    def load_to_sqlite(self, db_name: str = "stock_senti_clean", table_name: str = "stock_sentiment") -> str:
        """
        Guarda los datos en una base de datos SQLite
        
        Args:
            db_name: Nombre de la base de datos (sin extensión)
            table_name: Nombre de la tabla
            
        Returns:
            Ruta completa del archivo de base de datos
        """
        print("\n🗄️  Guardando en SQLite...")
        
        db_path = os.path.join(self.output_dir, f"{db_name}.db")
        
        try:
            # Conectar a la base de datos
            conn = sqlite3.connect(db_path)
            
            # Guardar el DataFrame como tabla
            self.data.to_sql(table_name, conn, if_exists='replace', index=False)
            
            # Obtener información de la tabla
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = cursor.fetchone()[0]
            
            # Crear índice en la columna date para mejorar consultas
            if 'date' in self.data.columns:
                cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_date ON {table_name}(date)")
                print(f"   ✓ Índice creado en columna 'date'")
            
            # Crear índice en la columna label
            if 'label' in self.data.columns:
                cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_label ON {table_name}(label)")
                print(f"   ✓ Índice creado en columna 'label'")
            
            conn.commit()
            conn.close()
            
            file_size = os.path.getsize(db_path) / 1024  # KB
            
            self.load_log.append({
                'formato': 'SQLite',
                'archivo': db_path,
                'tabla': table_name,
                'tamaño': f"{file_size:.2f} KB",
                'filas': row_count,
                'exitoso': True
            })
            
            print(f"   ✓ SQLite guardado: {db_path}")
            print(f"   ✓ Tabla: {table_name}")
            print(f"   ✓ Filas: {row_count}")
            print(f"   ✓ Tamaño: {file_size:.2f} KB")
            
            return db_path
            
        except Exception as e:
            print(f"   ❌ Error al guardar en SQLite: {e}")
            self.load_log.append({
                'formato': 'SQLite',
                'error': str(e),
                'exitoso': False
            })
            raise
    
    def _print_load_summary(self):
        """Imprime un resumen de las cargas realizadas"""
        print("\n" + "="*60)
        print("RESUMEN DE CARGA")
        print("="*60)
        
        successful = sum(1 for log in self.load_log if log.get('exitoso', False))
        total = len(self.load_log)
        
        print(f"\n📊 Cargas exitosas: {successful}/{total}")
        print()
        
        for i, log in enumerate(self.load_log, 1):
            if log.get('exitoso', False):
                print(f"{i}. {log['formato']}:")
                print(f"   Archivo: {log['archivo']}")
                if 'tabla' in log:
                    print(f"   Tabla: {log['tabla']}")
                print(f"   Tamaño: {log['tamaño']}")
                print(f"   Filas: {log['filas']}")
            else:
                print(f"{i}. {log['formato']}: ❌ Error - {log.get('error', 'Unknown')}")
    
    def get_load_report(self) -> dict:
        """Retorna un reporte de las cargas realizadas"""
        return {
            'loads': self.load_log,
            'successful_loads': sum(1 for log in self.load_log if log.get('exitoso', False)),
            'total_attempts': len(self.load_log)
        }
    
    @staticmethod
    def query_sqlite(db_path: str, table_name: str, query: Optional[str] = None) -> pd.DataFrame:
        """
        Ejecuta una consulta en la base de datos SQLite
        
        Args:
            db_path: Ruta a la base de datos
            table_name: Nombre de la tabla
            query: Query SQL (opcional, por defecto SELECT *)
            
        Returns:
            DataFrame con los resultados
        """
        if query is None:
            query = f"SELECT * FROM {table_name}"
        
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df


if __name__ == "__main__":
    # Prueba del loader
    from Extract.stock_extractor import StockExtractor
    from Transform.stock_transformer import StockTransformer
    
    # Extraer datos
    extractor = StockExtractor()
    raw_data = extractor.extract_data()
    
    # Transformar datos
    transformer = StockTransformer(raw_data)
    clean_data = transformer.transform_all()
    
    # Cargar datos
    loader = StockLoader(clean_data)
    loader.load_all()
    
    print("\n" + "="*60)
    print("PRUEBA DE LECTURA DESDE SQLITE")
    print("="*60)
    
    # Leer desde SQLite
    result = loader.query_sqlite(
        "data/stock_senti_clean.db",
        "stock_sentiment",
        "SELECT * FROM stock_sentiment LIMIT 5"
    )
    print(result)

"""
Módulo de Extracción de Datos
Extrae datos del archivo CSV de análisis de sentimientos de acciones
"""
import pandas as pd
import os
from typing import Optional


class StockExtractor:
    """Clase para extraer datos del CSV de stock sentiment analysis"""
    
    def __init__(self, file_path: str = "stock_senti_analysis.csv"):
        """
        Inicializa el extractor con la ruta del archivo
        
        Args:
            file_path: Ruta al archivo CSV de datos
        """
        self.file_path = file_path
        self.data = None
        
    def extract_data(self) -> pd.DataFrame:
        """
        Extrae los datos del archivo CSV con detección automática de encoding
        
        Returns:
            DataFrame con los datos extraídos
        """
        try:
            print(f"📂 Extrayendo datos desde: {self.file_path}")
            
            # Lista de encodings a probar
            encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
            
            # Intentar leer con diferentes encodings
            for encoding in encodings:
                try:
                    self.data = pd.read_csv(self.file_path, encoding=encoding)
                    print(f"✅ Datos extraídos exitosamente con encoding: {encoding}")
                    break
                except UnicodeDecodeError:
                    if encoding == encodings[-1]:  # Último intento
                        raise
                    continue
            
            print(f"📊 Dimensiones: {self.data.shape[0]} filas × {self.data.shape[1]} columnas")
            print(f"📋 Columnas: {list(self.data.columns)}")
            
            return self.data
            
        except FileNotFoundError:
            print(f"❌ Error: No se encontró el archivo {self.file_path}")
            raise
        except Exception as e:
            print(f"❌ Error al extraer datos: {str(e)}")
            raise
    
    def get_data_info(self) -> dict:
        """
        Obtiene información básica sobre los datos extraídos
        
        Returns:
            Diccionario con información del dataset
        """
        if self.data is None:
            self.extract_data()
            
        info = {
            "filas": self.data.shape[0],
            "columnas": self.data.shape[1],
            "nombres_columnas": list(self.data.columns),
            "tipos_datos": self.data.dtypes.to_dict(),
            "memoria_uso": self.data.memory_usage(deep=True).sum() / 1024**2,  # MB
            "valores_nulos": self.data.isnull().sum().to_dict()
        }
        
        return info
    
    def preview_data(self, n_rows: int = 5) -> pd.DataFrame:
        """
        Muestra una vista previa de los datos
        
        Args:
            n_rows: Número de filas a mostrar
            
        Returns:
            DataFrame con las primeras n filas
        """
        if self.data is None:
            self.extract_data()
            
        return self.data.head(n_rows)


if __name__ == "__main__":
    # Prueba del extractor
    extractor = StockExtractor()
    df = extractor.extract_data()
    
    print("\n" + "="*60)
    print("INFORMACIÓN DEL DATASET")
    print("="*60)
    info = extractor.get_data_info()
    for key, value in info.items():
        print(f"{key}: {value}")
    
    print("\n" + "="*60)
    print("VISTA PREVIA")
    print("="*60)
    print(extractor.preview_data())

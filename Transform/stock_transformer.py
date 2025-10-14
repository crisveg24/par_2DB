"""
Módulo de Transformación de Datos
Limpia y transforma los datos del análisis de sentimientos de acciones
"""
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Optional, Tuple


class StockTransformer:
    """Clase para transformar y limpiar datos de stock sentiment analysis"""
    
    def __init__(self, data: pd.DataFrame):
        """
        Inicializa el transformador con los datos a procesar
        
        Args:
            data: DataFrame con los datos crudos
        """
        self.raw_data = data.copy()
        self.clean_data = None
        self.transformation_log = []
        
    def transform_all(self) -> pd.DataFrame:
        """
        Ejecuta todas las transformaciones en orden
        
        Returns:
            DataFrame limpio y transformado
        """
        print("\n🔄 INICIANDO PROCESO DE TRANSFORMACIÓN")
        print("="*60)
        
        self.clean_data = self.raw_data.copy()
        
        # 1. Normalizar nombres de columnas
        self._normalize_column_names()
        
        # 2. Convertir tipos de datos
        self._convert_data_types()
        
        # 3. Manejar valores nulos
        self._handle_missing_values()
        
        # 4. Eliminar duplicados
        self._remove_duplicates()
        
        # 5. Validar y limpiar fechas
        self._clean_dates()
        
        # 6. Normalizar valores
        self._normalize_values()
        
        # 7. Crear features adicionales
        self._create_features()
        
        print("\n✅ TRANSFORMACIÓN COMPLETADA")
        self._print_transformation_summary()
        
        return self.clean_data
    
    def _normalize_column_names(self):
        """Normaliza los nombres de las columnas"""
        print("\n📝 Normalizando nombres de columnas...")
        
        original_columns = self.clean_data.columns.tolist()
        
        # Convertir a minúsculas y reemplazar espacios
        self.clean_data.columns = (
            self.clean_data.columns
            .str.strip()
            .str.lower()
            .str.replace(' ', '_')
            .str.replace('-', '_')
        )
        
        new_columns = self.clean_data.columns.tolist()
        
        if original_columns != new_columns:
            self.transformation_log.append({
                'paso': 'Normalización de columnas',
                'cambios': f"Columnas renombradas"
            })
            print(f"   ✓ Columnas normalizadas: {len(new_columns)} columnas")
    
    def _convert_data_types(self):
        """Convierte los tipos de datos apropiadamente"""
        print("\n🔢 Convirtiendo tipos de datos...")
        
        conversions = 0
        
        # Convertir la columna date
        if 'date' in self.clean_data.columns:
            try:
                self.clean_data['date'] = pd.to_datetime(self.clean_data['date'])
                conversions += 1
                print(f"   ✓ Columna 'date' convertida a datetime")
            except Exception as e:
                print(f"   ⚠ No se pudo convertir 'date': {e}")
        
        # Convertir label a int
        if 'label' in self.clean_data.columns:
            try:
                self.clean_data['label'] = self.clean_data['label'].astype(int)
                conversions += 1
                print(f"   ✓ Columna 'label' convertida a int")
            except Exception as e:
                print(f"   ⚠ No se pudo convertir 'label': {e}")
        
        # Convertir columnas Top a string y manejar NaN
        top_cols = [col for col in self.clean_data.columns if col.startswith('top')]
        for col in top_cols:
            # Primero rellenar NaN antes de convertir a string
            self.clean_data[col] = self.clean_data[col].fillna('')
            self.clean_data[col] = self.clean_data[col].astype(str)
            # Limpiar valores 'nan' que pudieran haber quedado
            self.clean_data[col] = self.clean_data[col].replace('nan', '')
            conversions += 1
        
        if conversions > 0:
            self.transformation_log.append({
                'paso': 'Conversión de tipos',
                'cambios': f"{conversions} columnas convertidas"
            })
    
    def _handle_missing_values(self):
        """Maneja los valores nulos"""
        print("\n🔍 Manejando valores nulos...")
        
        nulls_before = self.clean_data.isnull().sum().sum()
        
        if nulls_before == 0:
            print(f"   ✓ No se encontraron valores nulos")
            return
        
        print(f"   ⚠ Valores nulos encontrados: {nulls_before}")
        
        # Para columnas numéricas, rellenar con 0 o media según contexto
        numeric_cols = self.clean_data.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if self.clean_data[col].isnull().any():
                # Para label usar moda
                if col == 'label':
                    mode_val = self.clean_data[col].mode()[0] if not self.clean_data[col].mode().empty else 0
                    self.clean_data[col].fillna(mode_val, inplace=True)
                    print(f"   ✓ '{col}' rellenado con moda: {mode_val}")
        
        # Para columnas de texto (Top1-Top25), rellenar con string vacío
        text_cols = [col for col in self.clean_data.columns if col.startswith('top')]
        nulls_filled = 0
        for col in text_cols:
            if self.clean_data[col].isnull().any():
                null_count = self.clean_data[col].isnull().sum()
                self.clean_data[col].fillna('', inplace=True)
                nulls_filled += null_count
        
        if nulls_filled > 0:
            print(f"   ✓ {nulls_filled} valores nulos en columnas de texto rellenados con string vacío")
        
        nulls_after = self.clean_data.isnull().sum().sum()
        
        self.transformation_log.append({
            'paso': 'Manejo de nulos',
            'cambios': f"Nulos antes: {nulls_before}, después: {nulls_after}"
        })
        
        print(f"   ✓ Valores nulos procesados: {nulls_before} → {nulls_after}")
    
    def _remove_duplicates(self):
        """Elimina filas duplicadas"""
        print("\n🗑️  Eliminando duplicados...")
        
        rows_before = len(self.clean_data)
        self.clean_data = self.clean_data.drop_duplicates()
        rows_after = len(self.clean_data)
        
        duplicates_removed = rows_before - rows_after
        
        if duplicates_removed > 0:
            self.transformation_log.append({
                'paso': 'Eliminación de duplicados',
                'cambios': f"{duplicates_removed} filas duplicadas eliminadas"
            })
            print(f"   ✓ Duplicados eliminados: {duplicates_removed}")
        else:
            print(f"   ✓ No se encontraron duplicados")
    
    def _clean_dates(self):
        """Limpia y valida las fechas"""
        print("\n📅 Limpiando y validando fechas...")
        
        if 'date' not in self.clean_data.columns:
            print(f"   ⚠ No se encontró columna 'date'")
            return
        
        # Eliminar filas con fechas inválidas
        rows_before = len(self.clean_data)
        self.clean_data = self.clean_data.dropna(subset=['date'])
        rows_after = len(self.clean_data)
        
        invalid_dates = rows_before - rows_after
        
        if invalid_dates > 0:
            print(f"   ✓ Fechas inválidas eliminadas: {invalid_dates}")
            self.transformation_log.append({
                'paso': 'Limpieza de fechas',
                'cambios': f"{invalid_dates} fechas inválidas eliminadas"
            })
        else:
            print(f"   ✓ Todas las fechas son válidas")
        
        # Ordenar por fecha
        self.clean_data = self.clean_data.sort_values('date').reset_index(drop=True)
        print(f"   ✓ Datos ordenados por fecha")
    
    def _normalize_values(self):
        """Normaliza valores específicos"""
        print("\n🔧 Normalizando valores...")
        
        # Normalizar textos en columnas Top
        top_cols = [col for col in self.clean_data.columns if col.startswith('top')]
        
        for col in top_cols:
            # Limpiar espacios extra y convertir a título
            self.clean_data[col] = self.clean_data[col].str.strip()
        
        print(f"   ✓ Valores normalizados en {len(top_cols)} columnas")
        
        self.transformation_log.append({
            'paso': 'Normalización de valores',
            'cambios': f"{len(top_cols)} columnas normalizadas"
        })
    
    def _create_features(self):
        """Crea features adicionales para análisis"""
        print("\n✨ Creando features adicionales...")
        
        features_created = 0
        
        if 'date' in self.clean_data.columns:
            # Extraer componentes de fecha
            self.clean_data['year'] = self.clean_data['date'].dt.year
            self.clean_data['month'] = self.clean_data['date'].dt.month
            self.clean_data['day'] = self.clean_data['date'].dt.day
            self.clean_data['day_of_week'] = self.clean_data['date'].dt.dayofweek
            self.clean_data['quarter'] = self.clean_data['date'].dt.quarter
            features_created += 5
            
            print(f"   ✓ Features temporales creadas: year, month, day, day_of_week, quarter")
        
        # Crear feature de sentimiento binario
        if 'label' in self.clean_data.columns:
            self.clean_data['sentiment'] = self.clean_data['label'].map({
                0: 'Negativo',
                1: 'Positivo'
            })
            features_created += 1
            print(f"   ✓ Feature 'sentiment' creada")
        
        self.transformation_log.append({
            'paso': 'Creación de features',
            'cambios': f"{features_created} nuevas features creadas"
        })
    
    def _print_transformation_summary(self):
        """Imprime un resumen de las transformaciones realizadas"""
        print("\n" + "="*60)
        print("RESUMEN DE TRANSFORMACIONES")
        print("="*60)
        
        for i, log in enumerate(self.transformation_log, 1):
            print(f"{i}. {log['paso']}: {log['cambios']}")
        
        print(f"\n📊 Dataset final:")
        print(f"   - Filas: {len(self.clean_data)}")
        print(f"   - Columnas: {len(self.clean_data.columns)}")
        print(f"   - Valores nulos: {self.clean_data.isnull().sum().sum()}")
        print(f"   - Memoria: {self.clean_data.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    def get_clean_data(self) -> pd.DataFrame:
        """Retorna los datos limpios"""
        return self.clean_data if self.clean_data is not None else self.raw_data
    
    def get_transformation_report(self) -> dict:
        """Retorna un reporte detallado de las transformaciones"""
        return {
            'transformations': self.transformation_log,
            'original_shape': self.raw_data.shape,
            'clean_shape': self.clean_data.shape if self.clean_data is not None else None,
            'original_nulls': self.raw_data.isnull().sum().sum(),
            'clean_nulls': self.clean_data.isnull().sum().sum() if self.clean_data is not None else None
        }


if __name__ == "__main__":
    # Prueba del transformador
    from Extract.stock_extractor import StockExtractor
    
    extractor = StockExtractor()
    raw_data = extractor.extract_data()
    
    transformer = StockTransformer(raw_data)
    clean_data = transformer.transform_all()
    
    print("\n" + "="*60)
    print("DATOS LIMPIOS - VISTA PREVIA")
    print("="*60)
    print(clean_data.head())
    
    print("\n" + "="*60)
    print("INFORMACIÓN DE COLUMNAS")
    print("="*60)
    print(clean_data.info())

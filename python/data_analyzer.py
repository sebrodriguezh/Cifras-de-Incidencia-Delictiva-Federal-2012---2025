#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para analizar datos del CSV y generar estadísticas
"""

import pandas as pd
import json
from pathlib import Path

def analyze_csv_data(csv_file_path):
    """Analiza el CSV y retorna estadísticas clave"""
    
    try:
        print("🔄 Leyendo CSV con encoding latin-1...")
        # Leer el CSV con encoding latin-1
        df = pd.read_csv(csv_file_path, encoding='latin-1')
        print("✅ CSV leído exitosamente!")
        
        # Mostrar información del DataFrame
        print(f"📊 Columnas encontradas: {list(df.columns)}")
        print(f"📈 Filas totales: {len(df)}")
        
        # Calcular estadísticas y convertir a tipos estándar de Python
        stats = {
            'total_registros': int(len(df)),  # Convertir a int estándar
            'fecha_minima': str(df.iloc[:, 0].min()),  # Convertir a string
            'fecha_maxima': str(df.iloc[:, 0].max()),  # Convertir a string
            'conceptos_unicos': int(df['CONCEPTO'].nunique()) if 'CONCEPTO' in df.columns else 0,
            'estados_unicos': int(df['ENTIDAD'].nunique()) if 'ENTIDAD' in df.columns else 0  # AGREGAR ESTA LÍNEA
        }
        
        return stats
        
    except Exception as e:
        print(f"❌ Error leyendo CSV: {e}")
        return None

def generate_stats_json():
    """Genera un archivo JSON con las estadísticas"""
    
    # Buscar archivos CSV en la carpeta data
    data_folder = Path('data')
    csv_files = list(data_folder.glob('*.csv'))
    
    if not csv_files:
        print("No se encontraron archivos CSV en la carpeta data/")
        return None
    
    # Usar el primer CSV encontrado
    csv_file = data_folder / "IDEFF_jul25.csv"
    print(f"Analizando: {csv_file}")
    
    # Analizar datos
    stats = analyze_csv_data(csv_file)
    
    if stats:
        # Guardar en JSON
        output_file = data_folder / 'stats.json'
        with open(output_file, 'w', encoding='latin-1') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        
        print(f"Estadísticas guardadas en: {output_file}")
        print("Estadísticas calculadas:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        return stats
    
    return None

if __name__ == "__main__":
    generate_stats_json()
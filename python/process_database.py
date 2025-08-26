#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para procesar y limpiar la base de datos IDEFF
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime

def process_ideff_database():
    """Procesa la base de datos IDEFF y crea una versión limpia"""
    
    try:
        print(" Procesando base de datos IDEFF...")
        
        # Leer el CSV original
        csv_file = Path('data/IDEFF_jul25.csv')
        df = pd.read_csv(csv_file, encoding='latin-1')
        
        print(f"✅ CSV leído: {len(df)} filas, {len(df.columns)} columnas")
        print(f"📊 Columnas originales: {list(df.columns)}")
        
        # Filtrar solo años 2019-2025
        # Asumiendo que la primera columna es el año
        df['Año'] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
        df_filtered = df[(df['Año'] >= 2019) & (df['Año'] <= 2025)]
        
        print(f"📅 Filas después de filtrar años 2019-2025: {len(df_filtered)}")
        
        # Eliminar la columna temporal 'Año' que creamos para el filtro
        df_filtered = df_filtered.drop('Año', axis=1)
        print("️  Columna temporal 'Año' eliminada")
        
        # Eliminar columna INEGI si existe
        if 'INEGI' in df_filtered.columns:
            df_filtered = df_filtered.drop('INEGI', axis=1)
            print("🗑️  Columna INEGI eliminada")
        
        # Eliminar filas donde ENTIDAD sea "EXTRANJERO"
        if 'ENTIDAD' in df_filtered.columns:
            filas_antes = len(df_filtered)
            df_filtered = df_filtered[df_filtered['ENTIDAD'] != 'EXTRANJERO']
            filas_despues = len(df_filtered)
            filas_eliminadas = filas_antes - filas_despues
            
            if filas_eliminadas > 0:
                print(f" Eliminadas {filas_eliminadas} filas con ENTIDAD = 'EXTRANJERO'")
            else:
                print("✅ No se encontraron filas con ENTIDAD = 'EXTRANJERO'")
        else:
            print("⚠️  Columna 'ENTIDAD' no encontrada")
        
        print(f"📊 Filas finales después de todos los filtros: {len(df_filtered)}")
        
        # Guardar la base de datos procesada
        output_file = Path('data/IDEFF_processed.csv')
        df_filtered.to_csv(output_file, index=False, encoding='utf-8')
        print(f"💾 Base de datos procesada guardada en: {output_file}")
        
        # Generar estadísticas de la base PROCESADA (CORREGIDO)
        stats_processed = {
            'total_registros_procesados': int(len(df_filtered)),
            'fecha_minima_procesada': int(df_filtered.iloc[:, 0].min()),  # Primera columna original
            'fecha_maxima_procesada': int(df_filtered.iloc[:, 0].max()),  # Primera columna original
            'conceptos_unicos_procesados': int(df_filtered['CONCEPTO'].nunique()) if 'CONCEPTO' in df_filtered.columns else 0,
            'estados_unicos_procesados': int(df_filtered['ENTIDAD'].nunique()) if 'ENTIDAD' in df_filtered.columns else 0,
            'columnas_finales': list(df_filtered.columns)
        }
        
        # Guardar estadísticas PROCESADAS en archivo separado
        stats_processed_file = Path('data/stats_processed.json')
        with open(stats_processed_file, 'w', encoding='utf-8') as f:
            json.dump(stats_processed, f, ensure_ascii=False, indent=2)
        
        print(f"📊 Estadísticas de base procesada guardadas en: {stats_processed_file}")
        
        # Generar preview de la base PROCESADA
        preview_data = df_filtered.head(10).to_dict('records')
        preview_file = Path('data/preview_processed.json')
        with open(preview_file, 'w', encoding='utf-8') as f:
            json.dump(preview_data, f, ensure_ascii=False, indent=2)
        
        print(f"👁️  Preview de la base procesada guardado en: {preview_file}")
        
        # Mostrar resumen
        print("\n RESUMEN DE LA BASE DE DATOS PROCESADA:")
        print(f"   • Total de registros: {stats_processed['total_registros_procesados']:,}")
        print(f"   • Período: {stats_processed['fecha_minima_procesada']} - {stats_processed['fecha_maxima_procesada']}")
        print(f"   • Conceptos únicos: {stats_processed['conceptos_unicos_procesados']}")
        print(f"   • Estados únicos: {stats_processed['estados_unicos_procesados']}")
        print(f"   • Columnas finales: {len(stats_processed['columnas_finales'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error procesando la base de datos: {e}")
        return False

if __name__ == "__main__":
    process_ideff_database()
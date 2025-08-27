#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear análisis de incidencia delictiva por entidad y concepto
para la Gráfica 4 (mapa de estados)
"""

import pandas as pd
from pathlib import Path

def create_entidad_concepto_analysis():
    """
    Crea un CSV con la evolución temporal de incidencia delictiva
    por entidad federativa y concepto
    """
    
    try:
        print("🔄 Creando análisis de entidad y concepto para Gráfica 4...")
        
        # Leer el CSV procesado
        csv_file = Path('data/IDEFF_processed.csv')
        df = pd.read_csv(csv_file)
        
        print(f"✅ CSV leído: {len(df)} filas")
        
        # Columnas de meses (enero a julio)
        month_columns = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO']
        
        # Verificar que las columnas existen
        missing_columns = [col for col in month_columns if col not in df.columns]
        if missing_columns:
            print(f"❌ Columnas faltantes: {missing_columns}")
            return None
        
        # Agrupar por ENTIDAD, CONCEPTO y AÑO, sumando los meses
        print("🔄 Agrupando datos por entidad, concepto y año...")
        df_grouped = df.groupby(['ENTIDAD', 'CONCEPTO', 'AÑO'])[month_columns].sum().reset_index()
        
        # Crear un DataFrame pivoteado para el formato final
        result_data = []
        
        # Obtener entidades y conceptos únicos
        unique_entidades = sorted(df_grouped['ENTIDAD'].unique())
        unique_conceptos = sorted(df_grouped['CONCEPTO'].unique())
        
        print(f"📊 Entidades encontradas: {len(unique_entidades)}")
        print(f"📋 Conceptos encontrados: {len(unique_conceptos)}")
        
        # Crear filas para cada combinación de entidad y concepto
        for entidad in unique_entidades:
            for concepto in unique_conceptos:
                # Filtrar datos para esta combinación
                combo_data = df_grouped[(df_grouped['ENTIDAD'] == entidad) & 
                                      (df_grouped['CONCEPTO'] == concepto)]
                
                # Crear diccionario para esta fila
                row = {
                    'ENTIDAD': entidad,
                    'CONCEPTO': concepto
                }
                
                # Agregar totales por año para esta combinación
                years = sorted(combo_data['AÑO'].unique())
                for year in years:
                    year_data = combo_data[combo_data['AÑO'] == year]
                    if not year_data.empty:
                        # Sumar todos los meses (enero a julio)
                        total = year_data[month_columns].sum().sum()
                        row[year] = int(total)
                    else:
                        row[year] = 0
                
                result_data.append(row)
        
        # Crear DataFrame final
        result_df = pd.DataFrame(result_data)
        
        # Reordenar columnas: ENTIDAD, CONCEPTO, luego todos los años
        years_ordered = sorted([col for col in result_df.columns if col not in ['ENTIDAD', 'CONCEPTO']])
        final_columns = ['ENTIDAD', 'CONCEPTO'] + years_ordered
        result_df = result_df[final_columns]
        
        # Llenar valores NaN con 0
        result_df = result_df.fillna(0)
        
        # Convertir todas las columnas numéricas a enteros
        for col in result_df.columns:
            if col not in ['ENTIDAD', 'CONCEPTO']:
                result_df[col] = result_df[col].astype(int)
        
        # Guardar CSV
        output_file = 'data/entidad_concepto_analysis.csv'
        result_df.to_csv(output_file, index=False)
        
        print(f"💾 CSV generado: {output_file}")
        print(f"📊 Filas generadas: {len(result_df)}")
        print(f"📅 Años cubiertos: {years_ordered}")
        
        # Mostrar ejemplo de los datos generados
        print("\n📋 Ejemplo de datos generados:")
        print(result_df.head(10))
        
        # Mostrar estadísticas por concepto
        print("\n📈 Estadísticas por concepto:")
        for concepto in unique_conceptos:
            concepto_stats = result_df[result_df['CONCEPTO'] == concepto]
            total_concepto = concepto_stats[years_ordered].sum().sum()
            print(f"  • {concepto}: {total_concepto:,} casos totales")
        
        return result_df
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print("🚀 INICIANDO ANÁLISIS DE ENTIDAD Y CONCEPTO")
    print("=" * 50)
    
    result = create_entidad_concepto_analysis()
    
    if result is not None:
        print("\n🎉 Análisis completado exitosamente!")
        print(f"📁 Archivo generado: data/entidad_concepto_analysis.csv")
    else:
        print("\n❌ El análisis falló")

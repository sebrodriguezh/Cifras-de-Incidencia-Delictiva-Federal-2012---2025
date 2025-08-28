#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear análisis mensual de incidencia delictiva por entidad y concepto
para la Gráfica 4 mensual (mapa de estados) - enero 2024 a julio 2025
"""

import pandas as pd
from pathlib import Path

def create_monthly_entidad_concepto_analysis():
    """
    Crea un CSV con la evolución temporal mensual de incidencia delictiva
    por entidad federativa y concepto (enero 2024 - julio 2025)
    """
    
    try:
        print("🔄 Creando análisis mensual de entidad y concepto para Gráfica 4...")
        
        # Leer el CSV procesado
        csv_file = Path('data/IDEFF_processed.csv')
        df = pd.read_csv(csv_file, encoding='latin-1')
        
        # Corregir nombres de columnas con problemas de codificación
        df.columns = df.columns.str.replace('AÃ\x91O', 'AÑO')
        print(f"✅ CSV leído: {len(df)} filas")
        
        # Filtrar años 2023-2025 (incluimos 2023 para obtener diciembre como base)
        df['Año'] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
        df_filtered = df[(df['Año'] >= 2023) & (df['Año'] <= 2025)]
        
        print(f"📅 Filas después de filtrar años 2023-2025: {len(df_filtered)}")
        
        # Eliminar la columna temporal 'Año'
        df_filtered = df_filtered.drop('Año', axis=1)
        
        # Mapeo de nombres de meses a números
        month_map = {
            'ENERO': 1, 'FEBRERO': 2, 'MARZO': 3, 'ABRIL': 4, 'MAYO': 5, 'JUNIO': 6,
            'JULIO': 7, 'AGOSTO': 8, 'SEPTIEMBRE': 9, 'OCTUBRE': 10, 'NOVIEMBRE': 11, 'DICIEMBRE': 12
        }
        
        # Obtener meses disponibles en el CSV
        available_months = [col for col in df_filtered.columns if col in month_map.keys()]
        print(f"📅 Meses disponibles: {available_months}")
        
        # Obtener entidades y conceptos únicos
        unique_entidades = sorted(df_filtered['ENTIDAD'].unique())
        unique_conceptos = sorted(df_filtered['CONCEPTO'].unique())
        
        print(f"📊 Entidades encontradas: {len(unique_entidades)}")
        print(f"📋 Conceptos encontrados: {len(unique_conceptos)}")
        
        # Crear datos de resultado
        result_data = []
        
        # Procesar cada combinación de entidad y concepto
        for entidad in unique_entidades:
            for concepto in unique_conceptos:
                # Filtrar datos para esta combinación específica
                entidad_concepto_data = df_filtered[
                    (df_filtered['ENTIDAD'] == entidad) & 
                    (df_filtered['CONCEPTO'] == concepto)
                ]
                
                if entidad_concepto_data.empty:
                    continue
                
                # Procesar datos por año
                for year in [2023, 2024, 2025]:
                    year_data = entidad_concepto_data[entidad_concepto_data['AÑO'] == year]
                    if year_data.empty:
                        continue
                    
                    # Definir meses a procesar según el año
                    if year == 2023:
                        meses_a_procesar = ['DICIEMBRE']  # Solo diciembre para 2023
                    elif year == 2024:
                        meses_a_procesar = available_months  # Todos los meses disponibles para 2024
                    else:  # 2025
                        meses_a_procesar = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO']
                    
                    # Filtrar solo meses que existen en los datos
                    meses_a_procesar = [mes for mes in meses_a_procesar if mes in available_months]
                    
                    # Procesar cada mes
                    for mes in meses_a_procesar:
                        if mes not in year_data.columns:
                            continue
                        
                        # Crear identificador del mes: YYYY-MM
                        mes_id = f"{year}-{month_map[mes]:02d}"
                        
                        # Sumar todos los valores para esta entidad, concepto, año y mes
                        total = year_data[mes].sum()
                        
                        # Agregar al resultado
                        row = {
                            'ENTIDAD': entidad,
                            'CONCEPTO': concepto,
                            'MES_AÑO': mes_id,
                            'TOTAL': int(total)
                        }
                        result_data.append(row)
        
        # Crear DataFrame final
        result_df = pd.DataFrame(result_data)
        
        if result_df.empty:
            print("❌ No se generaron datos")
            return None
        
        # Pivotar para tener meses como columnas y entidad+concepto como filas
        # Crear una columna combinada para identificar cada fila única
        result_df['ENTIDAD_CONCEPTO'] = result_df['ENTIDAD'] + '_' + result_df['CONCEPTO']
        
        # Pivotar los datos
        pivot_df = result_df.pivot_table(
            index=['ENTIDAD', 'CONCEPTO'], 
            columns='MES_AÑO', 
            values='TOTAL', 
            fill_value=0,
            aggfunc='sum'
        ).reset_index()
        
        # Aplanar el índice de columnas
        pivot_df.columns.name = None
        
        # Ordenar las columnas de meses cronológicamente
        month_columns = [col for col in pivot_df.columns if col not in ['ENTIDAD', 'CONCEPTO']]
        month_columns_sorted = sorted(month_columns)
        
        final_columns = ['ENTIDAD', 'CONCEPTO'] + month_columns_sorted
        pivot_df = pivot_df[final_columns]
        
        # Convertir todos los valores numéricos a enteros
        for col in month_columns_sorted:
            pivot_df[col] = pivot_df[col].astype(int)
        
        # Guardar CSV
        output_file = 'data/monthly_entidad_concepto_analysis.csv'
        pivot_df.to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"💾 CSV generado: {output_file}")
        print(f"📊 Filas generadas: {len(pivot_df)}")
        print(f"📅 Meses cubiertos: {month_columns_sorted}")
        
        # Mostrar ejemplo de los datos generados
        print("\n📋 Ejemplo de datos generados:")
        print(pivot_df.head(10))
        
        # Mostrar estadísticas por concepto
        print("\n📈 Estadísticas por concepto:")
        for concepto in unique_conceptos:
            concepto_stats = pivot_df[pivot_df['CONCEPTO'] == concepto]
            if not concepto_stats.empty:
                total_concepto = concepto_stats[month_columns_sorted].sum().sum()
                print(f"  • {concepto}: {total_concepto:,} casos totales")
        
        return pivot_df
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("🚀 INICIANDO ANÁLISIS MENSUAL DE ENTIDAD Y CONCEPTO")
    print("=" * 60)
    
    result = create_monthly_entidad_concepto_analysis()
    
    if result is not None:
        print("\n🎉 Análisis completado exitosamente!")
        print(f"📁 Archivo generado: data/monthly_entidad_concepto_analysis.csv")
    else:
        print("\n❌ El análisis falló")


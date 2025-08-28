#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear análisis de variación porcentual mensual por entidad y concepto
para la Gráfica 4 mensual - enero 2024 a julio 2025
"""

import pandas as pd
from pathlib import Path

def create_monthly_entidad_concepto_percentage_analysis():
    """
    Crea análisis de variación porcentual mensual por entidad y concepto
    Calcula cambios mes-a-mes, usando diciembre 2023 como base para enero 2024
    """
    
    try:
        print("🔄 Creando análisis de variación porcentual mensual por entidad y concepto...")
        
        # Leer el CSV original con datos de 2023
        csv_file = Path('data/IDEFF_jul25.csv')
        df_original = pd.read_csv(csv_file, encoding='latin-1')
        
        # Corregir nombres de columnas con problemas de codificación
        df_original.columns = df_original.columns.str.replace('AÃ\x91O', 'AÑO')
        print(f"✅ CSV original leído: {len(df_original)} filas")
        
        # Filtrar solo años 2023-2025 (incluimos 2023 para diciembre como base)
        df_original['Año'] = pd.to_numeric(df_original.iloc[:, 0], errors='coerce')
        df_filtered = df_original[(df_original['Año'] >= 2023) & (df_original['Año'] <= 2025)]
        
        # Eliminar filas donde ENTIDAD sea "EXTRANJERO"
        if 'ENTIDAD' in df_filtered.columns:
            df_filtered = df_filtered[df_filtered['ENTIDAD'] != 'EXTRANJERO']
        
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
        
        # Crear datos de resultado - primero necesitamos los valores absolutos
        absolute_data = {}
        
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
                
                key = f"{entidad}_{concepto}"
                absolute_data[key] = {}
                
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
                        absolute_data[key][mes_id] = int(total)
        
        # Lista completa de meses a procesar (incluye 2023-12 para cálculos)
        meses_completos = [
            '2023-12', '2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06',
            '2024-07', '2024-08', '2024-09', '2024-10', '2024-11', '2024-12',
            '2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06', '2025-07'
        ]
        
        # Meses para mostrar en la tabla (sin diciembre 2023)
        meses_mostrar = [
            '2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06',
            '2024-07', '2024-08', '2024-09', '2024-10', '2024-11', '2024-12',
            '2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06', '2025-07'
        ]
        
        # Calcular variaciones porcentuales
        result_data = []
        
        for entidad in unique_entidades:
            for concepto in unique_conceptos:
                key = f"{entidad}_{concepto}"
                
                if key not in absolute_data:
                    continue
                
                row = {
                    'ENTIDAD': entidad,
                    'CONCEPTO': concepto
                }
                
                # Calcular variación porcentual para cada mes
                for i, mes in enumerate(meses_mostrar):
                    if i == 0:  # Primer mes (enero 2024)
                        previous_mes = '2023-12'  # Usar diciembre 2023 como base
                    else:
                        previous_mes = meses_mostrar[i-1]
                    
                    current_value = absolute_data[key].get(mes, 0)
                    previous_value = absolute_data[key].get(previous_mes, 0)
                    
                    if previous_value > 0:
                        percentage_change = ((current_value - previous_value) / previous_value) * 100
                        row[mes] = round(percentage_change, 1)
                    else:
                        row[mes] = None  # No se puede calcular variación si el valor anterior es 0
                
                result_data.append(row)
        
        # Crear DataFrame final
        result_df = pd.DataFrame(result_data)
        
        if result_df.empty:
            print("❌ No se generaron datos")
            return None
        
        # Ordenar las columnas
        final_columns = ['ENTIDAD', 'CONCEPTO'] + meses_mostrar
        result_df = result_df[final_columns]
        
        # Guardar CSV
        output_file = 'data/monthly_entidad_concepto_percentage_analysis.csv'
        result_df.to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"💾 CSV generado: {output_file}")
        print(f"📊 Filas generadas: {len(result_df)}")
        print(f"📅 Meses cubiertos: {meses_mostrar}")
        
        # Mostrar ejemplo de los datos generados
        print("\n📋 Ejemplo de datos generados:")
        print(result_df.head(10))
        
        # Mostrar estadísticas por concepto
        print("\n📈 Estadísticas por concepto:")
        for concepto in unique_conceptos:
            concepto_stats = result_df[result_df['CONCEPTO'] == concepto]
            if not concepto_stats.empty:
                # Contar cuántas variaciones positivas/negativas hay
                numeric_columns = [col for col in meses_mostrar if col in concepto_stats.columns]
                positive_changes = 0
                negative_changes = 0
                
                for col in numeric_columns:
                    values = concepto_stats[col].dropna()
                    positive_changes += (values > 0).sum()
                    negative_changes += (values < 0).sum()
                
                print(f"  • {concepto}: {positive_changes} incrementos, {negative_changes} decrementos")
        
        return result_df
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("🚀 INICIANDO ANÁLISIS DE VARIACIÓN PORCENTUAL MENSUAL POR ENTIDAD Y CONCEPTO")
    print("=" * 80)
    
    result = create_monthly_entidad_concepto_percentage_analysis()
    
    if result is not None:
        print("\n🎉 Análisis completado exitosamente!")
        print(f"📁 Archivo generado: data/monthly_entidad_concepto_percentage_analysis.csv")
    else:
        print("\n❌ El análisis falló")


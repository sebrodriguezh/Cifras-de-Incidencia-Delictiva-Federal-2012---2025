#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear análisis mensual de distribución de tipos por concepto
Período: enero 2024 a julio 2025
Similar a create_type_distribution_analysis.py pero mensual
"""

import pandas as pd
import numpy as np
from pathlib import Path

def create_monthly_type_distribution_analysis():
    """
    Crea un CSV con la distribución de tipos por concepto y mes
    para generar pie charts mensuales en la Gráfica 7
    Período: enero 2024 a julio 2025
    """
    
    try:
        print("🔄 Procesando base de datos IDEFF para análisis mensual de tipos...")
        
        # Leer el CSV original IDEFF_jul25.csv (como en create_type_distribution_analysis.py)
        csv_file = Path('data/IDEFF_jul25.csv')
        df = pd.read_csv(csv_file, encoding='latin-1')
        
        print(f"✅ CSV leído: {len(df)} filas, {len(df.columns)} columnas")
        
        # Filtrar años 2023-2025 (incluyendo 2023 para obtener diciembre como base)
        df['Año'] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
        df_filtered = df[(df['Año'] >= 2023) & (df['Año'] <= 2025)]
        
        print(f"📅 Filas después de filtrar años 2023-2025: {len(df_filtered)}")
        
        # Eliminar la columna temporal 'Año' que creamos para el filtro
        df_filtered = df_filtered.drop('Año', axis=1)
        print("🗑️ Columna temporal 'Año' eliminada")
        
        # Eliminar columna INEGI si existe
        if 'INEGI' in df_filtered.columns:
            df_filtered = df_filtered.drop('INEGI', axis=1)
            print("🗑️ Columna INEGI eliminada")
        
        # Eliminar filas donde ENTIDAD sea "EXTRANJERO"
        if 'ENTIDAD' in df_filtered.columns:
            filas_antes = len(df_filtered)
            df_filtered = df_filtered[df_filtered['ENTIDAD'] != 'EXTRANJERO']
            filas_despues = len(df_filtered)
            filas_eliminadas = filas_antes - filas_despues
            
            if filas_eliminadas > 0:
                print(f"🗑️ Eliminadas {filas_eliminadas} filas con ENTIDAD = 'EXTRANJERO'")
            else:
                print("✅ No se encontraron filas con ENTIDAD = 'EXTRANJERO'")
        else:
            print("⚠️ Columna 'ENTIDAD' no encontrada")
        
        print(f"📊 Filas finales después de todos los filtros: {len(df_filtered)}")
        
        # Columnas de meses disponibles
        month_columns = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO',
                        'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE']
        
        # Verificar qué meses existen en el DataFrame
        available_months = [mes for mes in month_columns if mes in df_filtered.columns]
        print(f"📅 Meses disponibles en datos: {available_months}")
        
        result_data = []
        
        # Obtener conceptos únicos
        unique_concepts = df_filtered['CONCEPTO'].unique()
        print(f"📊 Conceptos únicos: {len(unique_concepts)}")
        
        # Para cada concepto, crear datos mensuales
        for concepto in unique_concepts:
            concepto_data = df_filtered[df_filtered['CONCEPTO'] == concepto]
            
            # Obtener tipos únicos para este concepto
            tipos = sorted(concepto_data['TIPO'].unique())
            
            # Para cada año (incluyendo 2023 para diciembre)
            for year in [2023, 2024, 2025]:
                year_data = concepto_data[concepto_data['AÑO'] == year]
                
                if year_data.empty:
                    continue
                
                # Determinar qué meses procesar según el año
                if year == 2023:
                    meses_a_procesar = ['DICIEMBRE']  # Solo diciembre 2023 como base
                    meses_a_procesar = [mes for mes in meses_a_procesar if mes in available_months]
                elif year == 2024:
                    meses_a_procesar = available_months  # Todos los meses disponibles
                else:  # 2025
                    meses_a_procesar = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO']
                    meses_a_procesar = [mes for mes in meses_a_procesar if mes in available_months]
                
                # Para cada mes
                for mes in meses_a_procesar:
                    if mes not in year_data.columns:
                        continue
                    
                    # Crear identificador del mes
                    mes_num = available_months.index(mes) + 1
                    mes_id = f"{year}-{mes_num:02d}"
                    
                    # Crear diccionario para esta fila
                    row = {
                        'CONCEPTO': concepto,
                        'MES_AÑO': mes_id
                    }
                    
                    # Agregar totales por tipo para este mes específico
                    for tipo in tipos:
                        tipo_data = year_data[year_data['TIPO'] == tipo]
                        if not tipo_data.empty and mes in tipo_data.columns:
                            # Sumar todos los valores para este tipo en este mes
                            total = tipo_data[mes].sum()
                            row[tipo] = int(total) if pd.notna(total) else 0
                        else:
                            row[tipo] = 0
                    
                    result_data.append(row)
        
        # Crear DataFrame final
        result_df = pd.DataFrame(result_data)
        
        if result_df.empty:
            print("❌ No se generaron datos")
            return None
        
        # Ordenar por concepto y mes
        result_df = result_df.sort_values(['CONCEPTO', 'MES_AÑO'])
        
        # Asegurar que todos los valores son enteros y llenar NaN con 0
        result_df = result_df.fillna(0)
        for col in result_df.columns:
            if col not in ['CONCEPTO', 'MES_AÑO']:
                result_df[col] = result_df[col].astype(int)
        
        # Guardar resultado
        output_path = Path('data/monthly_type_distribution_analysis.csv')
        result_df.to_csv(output_path, index=False, encoding='latin-1')
        
        print(f"💾 Análisis mensual de tipos guardado en: {output_path}")
        print(f"📊 Formato: Distribución mensual de tipos por concepto")
        print(f"📊 Filas generadas: {len(result_df)}")
        print(f"📊 Columnas: {len(result_df.columns)}")
        
        # Mostrar preview de la tabla
        print(f"\n📋 PREVIEW DE LA TABLA:")
        print(result_df.head(10))
        
        # Mostrar estadísticas por concepto
        print(f"\n📊 MESES POR CONCEPTO:")
        for concepto in unique_concepts:
            count = len(result_df[result_df['CONCEPTO'] == concepto])
            print(f"   • {concepto}: {count} meses")
        
        return result_df
        
    except Exception as e:
        print(f"❌ Error creando análisis mensual de tipos: {e}")
        print("Asegúrate de que el archivo 'data/IDEFF_jul25.csv' existe")
        return None

if __name__ == "__main__":
    print("🚀 INICIANDO ANÁLISIS MENSUAL DE TIPOS POR CONCEPTO")
    print("📅 Período: enero 2024 a julio 2025")
    print("=" * 80)
    
    # Crear análisis mensual de tipos
    df_monthly_types = create_monthly_type_distribution_analysis()
    if df_monthly_types is None:
        print("❌ Falló el análisis mensual de tipos")
        exit(1)
    
    print("\n" + "=" * 80)
    print("🎉 ANÁLISIS MENSUAL DE TIPOS COMPLETADO!")
    print("📊 DataFrame generado:")
    print("   • df_monthly_types: Distribución mensual de tipos por concepto")
    print("\n💡 Los datos están listos para ser utilizados en la Gráfica 7")

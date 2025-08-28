#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear análisis de variación porcentual por entidad, concepto y tipo
"""

import pandas as pd
from pathlib import Path

def create_entidad_tipo_percentage_analysis():
    """Crea análisis de variación porcentual por entidad, concepto y tipo"""
    
    try:
        print("🔄 Creando análisis de variación porcentual por entidad, concepto y tipo...")
        
        # Leer el CSV original con datos de 2018
        csv_file = Path('data/IDEFF_jul25.csv')
        df_original = pd.read_csv(csv_file, encoding='latin-1')
        
        print(f"✅ CSV original leído: {len(df_original)} filas")
        
        # Filtrar solo años 2018-2025
        df_original['Año'] = pd.to_numeric(df_original.iloc[:, 0], errors='coerce')
        df_filtered = df_original[(df_original['Año'] >= 2018) & (df_original['Año'] <= 2025)]
        
        # Eliminar filas donde ENTIDAD sea "EXTRANJERO"
        if 'ENTIDAD' in df_filtered.columns:
            df_filtered = df_filtered[df_filtered['ENTIDAD'] != 'EXTRANJERO']
        
        print(f"📅 Filas después de filtrar años 2018-2025: {len(df_filtered)}")
        
        # Columnas de meses (ENERO a JULIO)
        meses = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO']
        
        # Agrupar por ENTIDAD, CONCEPTO, TIPO y AÑO, sumando todos los meses
        df_grouped = df_filtered.groupby(['ENTIDAD', 'CONCEPTO', 'TIPO', 'AÑO'])[meses].sum().reset_index()
        
        # Crear columna TOTAL sumando todos los meses
        df_grouped['TOTAL'] = df_grouped[meses].sum(axis=1)
        
        # Pivotar la tabla para tener años como columnas
        df_pivoted = df_grouped.pivot_table(
            index=['ENTIDAD', 'CONCEPTO', 'TIPO'], 
            columns='AÑO', 
            values='TOTAL', 
            fill_value=0
        ).reset_index()
        
        # Llenar valores NaN con 0
        df_pivoted = df_pivoted.fillna(0)
        
        # Convertir a enteros
        for year in [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]:
            if year in df_pivoted.columns:
                df_pivoted[year] = df_pivoted[year].astype(int)
        
        print(f"📊 Entidades procesadas: {df_pivoted['ENTIDAD'].nunique()}")
        print(f"📊 Conceptos procesados: {df_pivoted['CONCEPTO'].nunique()}")
        print(f"📊 Tipos procesados: {df_pivoted['TIPO'].nunique()}")
        
        # Crear DataFrame para cambios porcentuales
        df_percentage = df_pivoted[['ENTIDAD', 'CONCEPTO', 'TIPO']].copy()
        
        # Calcular cambios porcentuales año tras año
        years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
        
        # Calcular cambios % para años siguientes
        for i in range(1, len(years)):
            current_year = years[i]
            previous_year = years[i-1]
            
            if current_year in df_pivoted.columns and previous_year in df_pivoted.columns:
                # Cambio % = ((Año actual - Año anterior) / Año anterior) * 100
                # Evitar división por cero
                mask = df_pivoted[previous_year] > 0
                change_pct = pd.Series(0.0, index=df_pivoted.index)
                change_pct[mask] = ((df_pivoted.loc[mask, current_year] - df_pivoted.loc[mask, previous_year]) / 
                                   df_pivoted.loc[mask, previous_year] * 100).round(2)
                df_percentage[current_year] = change_pct
                print(f"📊 {current_year} vs {previous_year}: Cambios % calculados")
        
        # Guardar resultado (excluyendo 2018)
        df_percentage_final = df_percentage.drop(2018, axis=1, errors='ignore')
        output_path = Path('data/entidad_tipo_percentage_analysis.csv')
        df_percentage_final.to_csv(output_path, index=False, encoding='latin-1')
        
        print(f"💾 Análisis de variación porcentual guardado en: {output_path}")
        print(f"📊 Formato: Cambios % año tras año por entidad, concepto y tipo")
        
        # Mostrar preview de la tabla
        print("\n📋 PREVIEW DE LA TABLA:")
        print(df_percentage_final.head(10))
        
        return df_percentage_final
        
    except Exception as e:
        print(f"❌ Error creando análisis de variación porcentual: {e}")
        return None

if __name__ == "__main__":
    print("🚀 INICIANDO ANÁLISIS DE VARIACIÓN PORCENTUAL POR ENTIDAD, CONCEPTO Y TIPO")
    print("=" * 80)
    
    # Crear análisis de variación porcentual
    df_percentage = create_entidad_tipo_percentage_analysis()
    if df_percentage is None:
        print("❌ Falló el análisis de variación porcentual")
        exit(1)
    
    print("\n" + "=" * 80)
    print("🎉 ANÁLISIS COMPLETADO EXITOSAMENTE!")
    print("📊 DataFrame generado:")
    print("   • df_percentage: Cambios porcentuales por entidad, concepto y tipo")
    print("\n💡 Los datos están listos para ser utilizados en el dashboard")

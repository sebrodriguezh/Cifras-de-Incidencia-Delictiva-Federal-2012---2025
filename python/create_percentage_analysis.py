#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para procesar la base de datos del IDEFF
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
        df_filtered = df[(df['Año'] >= 2018) & (df['Año'] <= 2025)]
        
        print(f"📅 Filas después de filtrar años 2018-2025: {len(df_filtered)}")
        
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
        output_file = Path('data/IDEFF_processed_percentage_analysis.csv')
        df_filtered.to_csv(output_file, index=False, encoding='latin-1')
        print(f"💾 Base de datos procesada guardada en: {output_file}")
        
        return df_filtered
        
    except Exception as e:
        print(f"❌ Error procesando la base de datos: {e}")
        return False

def create_national_analysis():
    """Crea análisis nacional agrupado por concepto y año"""
    
    try:
        print("🔄 Creando análisis nacional por concepto...")
        
        # Leer el CSV procesado
        csv_file = Path('data/IDEFF_processed_percentage_analysis.csv')
        df = pd.read_csv(csv_file, encoding='latin-1')

        # Corregir nombres de columnas con problemas de codificación
        print(f"✅ CSV leído: {len(df)} filas")
        
        # Columnas de meses (ENERO a DICIEMBRE)
        meses = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 
                'JULIO']
        
        # Agrupar por CONCEPTO y AÑO, sumando todos los meses
        df_grouped = df.groupby(['CONCEPTO', 'AÑO'])[meses].sum().reset_index()
        
        # Pivotar la tabla para tener años como columnas
        df_pivoted = df_grouped.pivot(index='CONCEPTO', columns='AÑO', values=meses[0])
        
        # Para cada mes, agregar al total
        for mes in meses[1:]:
            df_pivoted += df_grouped.pivot(index='CONCEPTO', columns='AÑO', values=mes)
        
        # Llenar valores NaN con 0
        df_pivoted = df_pivoted.fillna(0)
        
        # Convertir a enteros
        df_pivoted = df_pivoted.astype(int)
        
        # Ordenar conceptos por total general (descendente)
        df_pivoted['TOTAL'] = df_pivoted.sum(axis=1)
        df_pivoted = df_pivoted.sort_values('TOTAL', ascending=False)
        df_pivoted = df_pivoted.drop('TOTAL', axis=1)
        
        # Guardar el CSV específico para la gráfica nacional
        output_file = Path('data/national_concept_percentage_analysis.csv')
        df_pivoted.to_csv(output_file, encoding='latin-1')
        
        print(f"💾 Análisis nacional guardado en: {output_file}")
        print(f"📊 Conceptos analizados: {len(df_pivoted)}")
        print(f"📅 Años cubiertos: {list(df_pivoted.columns)}")
        
        # Mostrar preview de la tabla
        print("\n📋 PREVIEW DE LA TABLA:")
        print(df_pivoted.head())
        
        # Mostrar estadísticas por concepto
        print("\n📊 ESTADÍSTICAS POR CONCEPTO:")
        for concepto in df_pivoted.index:
            total_concepto = df_pivoted.loc[concepto].sum()
            print(f"   • {concepto}: {total_concepto:,} casos totales")
        
        return df_pivoted
        
    except Exception as e:
        print(f"❌ Error creando análisis nacional: {e}")
        return False

def create_percentage_analysis(df_pivoted):
    """Crea análisis de cambios porcentuales año tras año"""
    
    try:
        print("🔄 Creando análisis de cambios porcentuales año tras año...")
        
        # Crear DataFrame para cambios porcentuales
        df_percentage = pd.DataFrame()
        
        # Calcular cambios porcentuales año tras año
        years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
        
        # 2018 no tiene cambio % (es el primer año)
        df_percentage[2018] = 0.0  # O podrías poner "N/A" o "-"
        print("✅ 2018: Año base (sin cambio %)")
        
        # Calcular cambios % para años siguientes
        for i in range(1, len(years)):
            current_year = years[i]
            previous_year = years[i-1]
            
            if current_year in df_pivoted.columns and previous_year in df_pivoted.columns:
                # Cambio % = ((Año actual - Año anterior) / Año anterior) * 100
                change_pct = ((df_pivoted[current_year] - df_pivoted[previous_year]) / df_pivoted[previous_year] * 100).round(2)
                df_percentage[current_year] = change_pct
                print(f"📊 {current_year} vs {previous_year}: Cambios % calculados")
        
        # Ordenar por el cambio promedio (solo para ordenamiento interno)
        df_percentage['PROMEDIO_CAMBIO'] = df_percentage.iloc[:, 1:].mean(axis=1)
        df_percentage = df_percentage.sort_values('PROMEDIO_CAMBIO', ascending=False)
        
        # Guardar resultado (excluyendo 2018 y PROMEDIO_CAMBIO)
        df_percentage_final = df_percentage.drop([2018, 'PROMEDIO_CAMBIO'], axis=1)
        output_path = Path('data/national_percentage_analysis.csv')
        df_percentage_final.to_csv(output_path, index=True)
        
        print(f"💾 Análisis de cambios porcentuales guardado en: {output_path}")
        print(f"�� Formato: Cambios % año tras año (2019 vs 2018, 2020 vs 2019, etc.)")
        
        return df_percentage
        
    except Exception as e:
        print(f"❌ Error creando análisis porcentual: {e}")
        return None


if __name__ == "__main__":
    print("🚀 INICIANDO PROCESAMIENTO COMPLETO DE IDEFF")
    print("=" * 50)
    
    # Paso 1: Procesar base de datos
    df_processed = process_ideff_database()
    if df_processed is False:
        print("❌ Falló el procesamiento de la base de datos")
        exit(1)
    
    print("\n" + "=" * 50)
    
    # Paso 2: Crear análisis nacional
    df_national = create_national_analysis()
    if df_national is False:
        print("❌ Falló el análisis nacional")
        exit(1)
    
    print("\n" + "=" * 50)
    
    # Paso 3: Crear análisis de cambios porcentuales
    df_percentage = create_percentage_analysis(df_national)
    if df_percentage is None:
        print("❌ Falló el análisis porcentual")
        exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 PROCESAMIENTO COMPLETADO EXITOSAMENTE!")
    print("📊 DataFrames generados:")
    print("   • df_processed: Base de datos filtrada (2018-2025)")
    print("   • df_national: Análisis nacional por concepto/año")
    print("   • df_percentage: Cambios porcentuales respecto a 2018")
    print("\n💡 Los DataFrames están en memoria para análisis adicional")
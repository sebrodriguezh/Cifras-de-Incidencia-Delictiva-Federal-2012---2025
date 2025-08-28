#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear análisis mensual de incidencia delictiva por concepto
Período: enero 2024 a julio 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path

def create_monthly_analysis():
    """
    Crea análisis mensual por concepto para gráfica de barras stacked
    Período: enero 2024 a julio 2025
    """
    
    try:
        print("🔄 Procesando base de datos IDEFF para análisis mensual...")
        csv_file = Path('data/IDEFF_processed.csv')
        df = pd.read_csv(csv_file, encoding='latin-1')
        
        print(f"✅ CSV leído: {len(df)} filas")
        print(f"📋 Columnas: {list(df.columns)}")
        
        # Normalizar nombres de columnas
        df.columns = df.columns.str.replace('AÃ\x91O', 'AÑO')
        
        # Filtrar años 2024-2025
        df_filtered = df[(df['AÑO'] >= 2024) & (df['AÑO'] <= 2025)]
        
        # Eliminar filas donde ENTIDAD sea "EXTRANJERO"
        if 'ENTIDAD' in df_filtered.columns:
            df_filtered = df_filtered[df_filtered['ENTIDAD'] != 'EXTRANJERO']
        
        print(f"📅 Filas después de filtrar 2024-2025: {len(df_filtered)}")
        print(f"📊 Conceptos únicos: {df_filtered['CONCEPTO'].unique()}")
        
        # Columnas de meses disponibles
        meses_disponibles = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO', 
                           'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE']
        
        # Verificar qué meses existen en el DataFrame
        meses_en_df = [mes for mes in meses_disponibles if mes in df_filtered.columns]
        print(f"📅 Meses disponibles en datos: {meses_en_df}")
        
        # Crear lista de períodos mensuales
        periodos = []
        
        # 2024: todos los meses disponibles
        for mes in meses_en_df:
            data_2024 = df_filtered[df_filtered['AÑO'] == 2024]
            if not data_2024.empty and mes in data_2024.columns:
                periodos.append({
                    'MES_AÑO': f"2024-{meses_en_df.index(mes)+1:02d}",
                    'AÑO': 2024,
                    'MES': mes,
                    'ORDEN': 2024 * 100 + (meses_en_df.index(mes) + 1)
                })
        
        # 2025: solo hasta julio
        meses_2025 = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO']
        for mes in meses_2025:
            if mes in meses_en_df:
                data_2025 = df_filtered[df_filtered['AÑO'] == 2025]
                if not data_2025.empty and mes in data_2025.columns:
                    periodos.append({
                        'MES_AÑO': f"2025-{meses_2025.index(mes)+1:02d}",
                        'AÑO': 2025,
                        'MES': mes,
                        'ORDEN': 2025 * 100 + (meses_2025.index(mes) + 1)
                    })
        
        print(f"📊 Períodos a procesar: {len(periodos)}")
        
        # Obtener conceptos únicos
        conceptos = sorted(df_filtered['CONCEPTO'].unique())
        print(f"📊 Conceptos: {conceptos}")
        
        # Crear DataFrame resultado
        result_data = []
        
        for periodo in periodos:
            año = periodo['AÑO']
            mes = periodo['MES']
            mes_año = periodo['MES_AÑO']
            
            # Filtrar datos para este año
            df_año = df_filtered[df_filtered['AÑO'] == año]
            
            # Crear fila para este mes
            row = {'MES_AÑO': mes_año}
            
            # Sumar por concepto para este mes específico
            for concepto in conceptos:
                df_concepto = df_año[df_año['CONCEPTO'] == concepto]
                
                if not df_concepto.empty and mes in df_concepto.columns:
                    total = df_concepto[mes].sum()
                else:
                    total = 0
                
                row[concepto] = int(total)
            
            result_data.append(row)
            print(f"✅ Procesado: {mes_año}")
        
        # Crear DataFrame resultado
        df_result = pd.DataFrame(result_data)
        
        # Ordenar por fecha
        df_result = df_result.sort_values('MES_AÑO')
        
        # Asegurar que todos los valores son enteros
        for concepto in conceptos:
            df_result[concepto] = df_result[concepto].fillna(0).astype(int)
        
        print(f"\n📊 RESULTADO:")
        print(f"   • Períodos: {len(df_result)} meses")
        print(f"   • Conceptos: {len(conceptos)}")
        print(f"   • Rango: {df_result['MES_AÑO'].min()} a {df_result['MES_AÑO'].max()}")
        
        # Guardar resultado
        output_path = Path('data/monthly_concept_analysis.csv')
        df_result.to_csv(output_path, index=False, encoding='latin-1')
        
        print(f"💾 Análisis mensual guardado en: {output_path}")
        
        # Mostrar preview
        print(f"\n📋 PREVIEW DEL CSV:")
        print(df_result.head(8))
        
        # Mostrar estadísticas por concepto
        print(f"\n📊 TOTALES POR CONCEPTO (enero 2024 - julio 2025):")
        for concepto in conceptos:
            total = df_result[concepto].sum()
            print(f"   • {concepto}: {total:,} carpetas")
        
        return df_result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Asegúrate de que el archivo 'data/IDEFF_processed.csv' existe")
        return None

if __name__ == "__main__":
    print("🚀 INICIANDO ANÁLISIS MENSUAL POR CONCEPTO")
    print("📅 Período: enero 2024 a julio 2025")
    print("=" * 80)
    
    # Crear análisis mensual
    df_monthly = create_monthly_analysis()
    if df_monthly is None:
        print("❌ Falló el análisis mensual")
        exit(1)
    
    print("\n" + "=" * 80)
    print("🎉 ANÁLISIS MENSUAL COMPLETADO!")
    print("📊 Estructura del CSV:")
    print("   • Columna 1: MES_AÑO (formato YYYY-MM)")
    print("   • Columnas 2-N: Un concepto por columna")
    print("   • Valores: Carpetas de investigación reportadas")
    print("\n💡 Perfecto para gráfica de barras stacked mensual!")

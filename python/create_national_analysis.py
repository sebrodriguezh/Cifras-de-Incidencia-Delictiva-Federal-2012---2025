#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear análisis nacional por concepto y año
Genera CSV con años como columnas y conceptos como filas
"""

import pandas as pd
from pathlib import Path

def create_national_analysis():
    """Crea análisis nacional agrupado por concepto y año"""
    
    try:
        print("🔄 Creando análisis nacional por concepto...")
        
        # Leer el CSV procesado
        csv_file = Path('data/IDEFF_processed.csv')
        df = pd.read_csv(csv_file, encoding='latin-1')

        # Corregir nombres de columnas con problemas de codificación
        df.columns = df.columns.str.replace('AÃ\x91O', 'AÑO')
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
        output_file = Path('data/national_concept_analysis.csv')
        df_pivoted.to_csv(output_file, encoding='utf-8')
        
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
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando análisis nacional: {e}")
        return False

if __name__ == "__main__":
    create_national_analysis()
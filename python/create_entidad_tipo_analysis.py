#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear análisis de incidencia delictiva por entidad, concepto y tipo
para el segundo mapa (Gráfica 4 - Mapa 2)
"""

import pandas as pd
from pathlib import Path

def create_entidad_tipo_analysis():
    """
    Crea un CSV con la evolución temporal de incidencia delictiva
    por entidad federativa, concepto y tipo
    """
    
    try:
        print("🔄 Creando análisis de entidad, concepto y tipo para Mapa 2...")
        
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
        
        # Verificar que existe la columna TIPO
        if 'TIPO' not in df.columns:
            print("❌ Columna 'TIPO' no encontrada en el CSV")
            return None
        
        # Agrupar por ENTIDAD, CONCEPTO, TIPO y AÑO, sumando los meses
        print("🔄 Agrupando datos por entidad, concepto, tipo y año...")
        df_grouped = df.groupby(['ENTIDAD', 'CONCEPTO', 'TIPO', 'AÑO'])[month_columns].sum().reset_index()
        
        # Crear un DataFrame pivoteado para el formato final
        result_data = []
        
        # Obtener entidades, conceptos y tipos únicos
        unique_entidades = sorted(df_grouped['ENTIDAD'].unique())
        unique_conceptos = sorted(df_grouped['CONCEPTO'].unique())
        unique_tipos = sorted(df_grouped['TIPO'].unique())
        
        print(f"📊 Entidades encontradas: {len(unique_entidades)}")
        print(f"📋 Conceptos encontrados: {len(unique_conceptos)}")
        print(f"🏷️ Tipos encontrados: {len(unique_tipos)}")
        
        # Crear filas para cada combinación de entidad, concepto y tipo
        for entidad in unique_entidades:
            for concepto in unique_conceptos:
                for tipo in unique_tipos:
                    # Filtrar datos para esta combinación
                    combo_data = df_grouped[(df_grouped['ENTIDAD'] == entidad) & 
                                          (df_grouped['CONCEPTO'] == concepto) &
                                          (df_grouped['TIPO'] == tipo)]
                    
                    # Crear diccionario para esta fila
                    row = {
                        'ENTIDAD': entidad,
                        'CONCEPTO': concepto,
                        'TIPO': tipo
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
        
        # Reordenar columnas: ENTIDAD, CONCEPTO, TIPO, luego todos los años
        years_ordered = sorted([col for col in result_df.columns if col not in ['ENTIDAD', 'CONCEPTO', 'TIPO']])
        final_columns = ['ENTIDAD', 'CONCEPTO', 'TIPO'] + years_ordered
        result_df = result_df[final_columns]
        
        # Llenar valores NaN con 0
        result_df = result_df.fillna(0)
        
        # Convertir todas las columnas numéricas a enteros
        for col in result_df.columns:
            if col not in ['ENTIDAD', 'CONCEPTO', 'TIPO']:
                result_df[col] = result_df[col].astype(int)
        
        # Guardar CSV
        output_file = 'data/entidad_tipo_analysis.csv'
        result_df.to_csv(output_file, index=False)
        
        print(f"💾 CSV generado: {output_file}")
        print(f"📊 Filas generadas: {len(result_df)}")
        print(f"📅 Años cubiertos: {years_ordered}")
        
        # Mostrar ejemplo de los datos generados
        print("\n📋 Ejemplo de datos generados:")
        print(result_df.head(10))
        
        # Mostrar estadísticas por concepto y tipo
        print("\n📈 Estadísticas por concepto y tipo:")
        for concepto in unique_conceptos:
            print(f"\n  📋 {concepto}:")
            concepto_data = result_df[result_df['CONCEPTO'] == concepto]
            tipos_en_concepto = sorted(concepto_data['TIPO'].unique())
            
            for tipo in tipos_en_concepto:
                tipo_data = concepto_data[concepto_data['TIPO'] == tipo]
                total_tipo = tipo_data[years_ordered].sum().sum()
                if total_tipo > 0:  # Solo mostrar tipos con datos
                    print(f"    • {tipo}: {total_tipo:,} casos totales")
        
        return result_df
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print("🚀 INICIANDO ANÁLISIS DE ENTIDAD, CONCEPTO Y TIPO")
    print("=" * 60)
    
    result = create_entidad_tipo_analysis()
    
    if result is not None:
        print("\n🎉 Análisis completado exitosamente!")
        print(f"📁 Archivo generado: data/entidad_tipo_analysis.csv")
    else:
        print("\n❌ El análisis falló")

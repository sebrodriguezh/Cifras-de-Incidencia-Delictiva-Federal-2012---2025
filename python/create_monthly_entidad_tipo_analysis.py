#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear análisis mensual de incidencia delictiva por entidad, concepto y tipo
para la Gráfica 4 mensual (segundo mapa) - enero 2024 a julio 2025
"""

import pandas as pd
from pathlib import Path

def create_monthly_entidad_tipo_analysis():
    """
    Crea un CSV con la evolución temporal mensual de incidencia delictiva
    por entidad federativa, concepto y tipo (enero 2024 - julio 2025)
    """
    
    try:
        print("🔄 Creando análisis mensual de entidad, concepto y tipo para Mapa 2...")
        
        # Leer el CSV procesado
        csv_file = Path('data/IDEFF_processed.csv')
        df = pd.read_csv(csv_file, encoding='latin-1')
        
        # Corregir nombres de columnas con problemas de codificación
        df.columns = df.columns.str.replace('AÃ\x91O', 'AÑO')
        print(f"✅ CSV leído: {len(df)} filas")
        
        # Verificar que existe la columna TIPO
        if 'TIPO' not in df.columns:
            print("❌ Columna 'TIPO' no encontrada en el CSV")
            return None
        
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
        
        # Obtener entidades, conceptos y tipos únicos
        unique_entidades = sorted(df_filtered['ENTIDAD'].unique())
        unique_conceptos = sorted(df_filtered['CONCEPTO'].unique())
        unique_tipos = sorted(df_filtered['TIPO'].unique())
        
        print(f"📊 Entidades encontradas: {len(unique_entidades)}")
        print(f"📋 Conceptos encontrados: {len(unique_conceptos)}")
        print(f"🏷️ Tipos encontrados: {len(unique_tipos)}")
        
        # Crear datos de resultado
        result_data = []
        
        # Procesar cada combinación de entidad, concepto y tipo
        for entidad in unique_entidades:
            for concepto in unique_conceptos:
                for tipo in unique_tipos:
                    # Filtrar datos para esta combinación específica
                    combo_data = df_filtered[
                        (df_filtered['ENTIDAD'] == entidad) & 
                        (df_filtered['CONCEPTO'] == concepto) &
                        (df_filtered['TIPO'] == tipo)
                    ]
                    
                    if combo_data.empty:
                        continue
                    
                    # Procesar datos por año
                    for year in [2023, 2024, 2025]:
                        year_data = combo_data[combo_data['AÑO'] == year]
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
                            
                            # Sumar todos los valores para esta entidad, concepto, tipo, año y mes
                            total = year_data[mes].sum()
                            
                            # Agregar al resultado
                            row = {
                                'ENTIDAD': entidad,
                                'CONCEPTO': concepto,
                                'TIPO': tipo,
                                'MES_AÑO': mes_id,
                                'TOTAL': int(total)
                            }
                            result_data.append(row)
        
        # Crear DataFrame final
        result_df = pd.DataFrame(result_data)
        
        if result_df.empty:
            print("❌ No se generaron datos")
            return None
        
        # Pivotar para tener meses como columnas y entidad+concepto+tipo como filas
        pivot_df = result_df.pivot_table(
            index=['ENTIDAD', 'CONCEPTO', 'TIPO'], 
            columns='MES_AÑO', 
            values='TOTAL', 
            fill_value=0,
            aggfunc='sum'
        ).reset_index()
        
        # Aplanar el índice de columnas
        pivot_df.columns.name = None
        
        # Ordenar las columnas de meses cronológicamente
        month_columns = [col for col in pivot_df.columns if col not in ['ENTIDAD', 'CONCEPTO', 'TIPO']]
        month_columns_sorted = sorted(month_columns)
        
        final_columns = ['ENTIDAD', 'CONCEPTO', 'TIPO'] + month_columns_sorted
        pivot_df = pivot_df[final_columns]
        
        # Convertir todos los valores numéricos a enteros
        for col in month_columns_sorted:
            pivot_df[col] = pivot_df[col].astype(int)
        
        # Guardar CSV
        output_file = 'data/monthly_entidad_tipo_analysis.csv'
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
                tipos_en_concepto = len(concepto_stats['TIPO'].unique())
                print(f"  • {concepto}: {total_concepto:,} casos totales, {tipos_en_concepto} tipos")
        
        return pivot_df
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("🚀 INICIANDO ANÁLISIS MENSUAL DE ENTIDAD, CONCEPTO Y TIPO")
    print("=" * 60)
    
    result = create_monthly_entidad_tipo_analysis()
    
    if result is not None:
        print("\n🎉 Análisis completado exitosamente!")
        print(f"📁 Archivo generado: data/monthly_entidad_tipo_analysis.csv")
    else:
        print("\n❌ El análisis falló")


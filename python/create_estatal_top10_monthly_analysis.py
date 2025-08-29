#!/usr/bin/env python3
"""
Script para generar análisis mensual de top 10 entidades por concepto y tipo
Para la Gráfica Estatal 2

Procesa datos de enero 2024 - julio 2025
Genera ranking mensual de entidades por mayor número de casos
"""

import pandas as pd
import json
import os

def create_estatal_top10_monthly_analysis():
    """
    Crea análisis mensual de top 10 entidades con datos agregados por:
    - Año-Mes
    - Entidad  
    - Concepto
    - Tipo
    - Casos (suma)
    """
    
    print("🚀 Generando análisis mensual de top 10 entidades...")
    
    # Cargar datos
    data_file = '../data/IDEFF_jul25.csv'
    if not os.path.exists(data_file):
        print(f"❌ Error: No se encontró {data_file}")
        return
    
    print(f"📂 Cargando datos desde {data_file}")
    
    # Intentar diferentes encodings
    encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
    df = None
    
    for encoding in encodings:
        try:
            print(f"🔄 Intentando encoding: {encoding}")
            df = pd.read_csv(data_file, encoding=encoding)
            print(f"✅ Datos cargados con encoding: {encoding}")
            break
        except UnicodeDecodeError:
            continue
    
    if df is None:
        print("❌ Error: No se pudo cargar el archivo con ningún encoding")
        return
    
    # Verificar y corregir columnas
    print(f"📋 Columnas en CSV: {list(df.columns)}")
    
    # Corregir nombres de columnas si es necesario
    df.columns = df.columns.str.replace('AÃ\x91O', 'AÑO')
    
    # El CSV tiene formato: AÑO, ENTIDAD, CONCEPTO, TIPO, ENERO, FEBRERO, ..., DICIEMBRE
    required_columns = ['AÑO', 'ENTIDAD', 'CONCEPTO', 'TIPO']
    meses_columns = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO', 
                     'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE']
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"❌ Error: Faltan columnas básicas: {missing_columns}")
        return
    
    print(f"✅ Estructura de datos: {df.shape[0]} filas, {df.shape[1]} columnas")
    
    # Filtrar período: años 2024 y 2025
    print("📅 Filtrando período 2024-2025...")
    df_filtered = df[df['AÑO'].isin([2024, 2025])].copy()
    
    print(f"📊 Datos filtrados por año: {df_filtered.shape[0]} registros")
    
    # Filtrar conceptos específicos
    conceptos_interes = [
        'CONTRA LA SALUD',
        'LEY FEDERAL CONTRA LA DELINCUENCIA ORGANIZADA (L.F.C.D.O.)'
    ]
    
    df_filtered = df_filtered[df_filtered['CONCEPTO'].isin(conceptos_interes)].copy()
    # Excluir extranjero
    df_filtered = df_filtered[df_filtered['ENTIDAD'] != 'EXTRANJERO'].copy()
    
    print(f"🎯 Datos filtrados por conceptos: {df_filtered.shape[0]} registros")
    
    # Verificar valores únicos
    print(f"📈 Conceptos únicos: {df_filtered['CONCEPTO'].unique()}")
    print(f"📈 Tipos únicos: {len(df_filtered['TIPO'].unique())} tipos")
    print(f"📈 Entidades únicas: {len(df_filtered['ENTIDAD'].unique())} entidades")
    
    # Transformar datos de formato wide a long
    print("🔄 Transformando datos de formato wide a long...")
    
    # Crear lista de registros en formato long
    registros_long = []
    
    for _, row in df_filtered.iterrows():
        year = row['AÑO']
        entidad = row['ENTIDAD']
        concepto = row['CONCEPTO']
        tipo = row['TIPO']
        
        # Para 2024: solo enero - diciembre
        if year == 2024:
            meses_usar = meses_columns  # Todos los meses
        # Para 2025: solo enero - julio
        elif year == 2025:
            meses_usar = meses_columns[:7]  # Solo hasta julio
        
        for mes_nombre in meses_usar:
            casos = row[mes_nombre] if pd.notna(row[mes_nombre]) else 0
            mes_num = meses_columns.index(mes_nombre) + 1
            anio_mes = f"{year}-{mes_num:02d}"
            
            registros_long.append({
                'ANIO_MES': anio_mes,
                'AÑO': year,
                'MES': mes_num,
                'MES_NOMBRE': mes_nombre,
                'ENTIDAD': entidad,
                'CONCEPTO': concepto,
                'TIPO': tipo,
                'CASOS': int(casos) if pd.notna(casos) else 0
            })
    
    # Crear DataFrame long
    df_long = pd.DataFrame(registros_long)
    
    # Filtrar período específico: enero 2024 - julio 2025
    df_long = df_long[
        ((df_long['AÑO'] == 2024) & (df_long['MES'] >= 1)) |
        ((df_long['AÑO'] == 2025) & (df_long['MES'] <= 7))
    ].copy()
    
    print(f"📊 Datos transformados: {df_long.shape[0]} registros")
    
    # Crear estructura de datos para fácil consulta
    # Formato: {año-mes: {concepto: {tipo: [{entidad, casos}, ...]}}}
    data_structure = {}
    
    # Obtener todos los meses ordenados
    meses_ordenados = sorted(df_long['ANIO_MES'].unique())
    print(f"📅 Meses disponibles: {meses_ordenados}")
    
    # Procesar cada mes
    for mes in meses_ordenados:
        data_structure[mes] = {}
        mes_data = df_long[df_long['ANIO_MES'] == mes]
        
        # Por cada concepto
        for concepto in conceptos_interes:
            data_structure[mes][concepto] = {}
            concepto_data = mes_data[mes_data['CONCEPTO'] == concepto]
            
            # Agregar datos "TODOS" (suma de todos los tipos)
            todos_data = concepto_data.groupby('ENTIDAD')['CASOS'].sum().reset_index()
            todos_data = todos_data.sort_values('CASOS', ascending=False).head(10)
            data_structure[mes][concepto]['TODOS'] = [
                {'entidad': row['ENTIDAD'], 'casos': int(row['CASOS'])}
                for _, row in todos_data.iterrows()
            ]
            
            # Por cada tipo específico
            tipos_concepto = concepto_data['TIPO'].unique()
            for tipo in tipos_concepto:
                tipo_data = concepto_data[concepto_data['TIPO'] == tipo]
                tipo_top10 = tipo_data.groupby('ENTIDAD')['CASOS'].sum().reset_index()
                tipo_top10 = tipo_top10.sort_values('CASOS', ascending=False).head(10)
                data_structure[mes][concepto][tipo] = [
                    {'entidad': row['ENTIDAD'], 'casos': int(row['CASOS'])}
                    for _, row in tipo_top10.iterrows()
                ]
    
    # Guardar estructura de datos
    output_file = '../data/estatal_top10_monthly_analysis.json'
    print(f"💾 Guardando datos en {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data_structure, f, ensure_ascii=False, indent=2)
    
    # Crear también CSV para tabla detallada (opcional)
    print("💾 Guardando CSV para tabla detallada...")
    df_long_sorted = df_long.sort_values(['ANIO_MES', 'CONCEPTO', 'CASOS'], ascending=[True, True, False])
    df_long_sorted.to_csv('../data/estatal_top10_monthly_analysis.csv', index=False, encoding='utf-8')
    
    print("✅ ¡Análisis mensual de top 10 entidades generado exitosamente!")
    print(f"📁 Archivos generados:")
    print(f"   - {output_file}")
    print(f"   - ../data/estatal_top10_monthly_analysis.csv")
    
    # Mostrar estadísticas finales
    print(f"\n📊 Resumen:")
    print(f"   - Período: enero 2024 - julio 2025 ({len(meses_ordenados)} meses)")
    print(f"   - Conceptos: {len(conceptos_interes)}")
    print(f"   - Total registros procesados: {df_long.shape[0]}")
    
    # Mostrar ejemplo de un mes
    if meses_ordenados:
        ejemplo_mes = meses_ordenados[0]
        print(f"\n🔍 Ejemplo - {ejemplo_mes}:")
        for concepto in conceptos_interes:
            if concepto in data_structure[ejemplo_mes]:
                top3_todos = data_structure[ejemplo_mes][concepto]['TODOS'][:3]
                print(f"   {concepto} - Top 3:")
                for i, item in enumerate(top3_todos, 1):
                    print(f"     {i}. {item['entidad']}: {item['casos']} casos")

if __name__ == "__main__":
    create_estatal_top10_monthly_analysis()

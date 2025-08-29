#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

def main():
    print("🏛️ Generando análisis estatal por concepto y tipo (Enero-Julio 2025)...")
    
    # Leer el dataset principal
    df = pd.read_csv('../data/IDEFF_jul25.csv', encoding='latin-1')
    
    # Corregir nombres de columnas
    df.columns = df.columns.str.replace('AÃ\x91O', 'AÑO')
    
    # Conceptos de interés
    conceptos_interes = [
        'CONTRA LA SALUD',
        'LEY FEDERAL CONTRA LA DELINCUENCIA ORGANIZADA (L.F.C.D.O.)'
    ]
    
    # Filtrar datos para 2025 únicamente y conceptos de interés
    df_filtered = df[
        (df['AÑO'] == 2025) & 
        (df['CONCEPTO'].isin(conceptos_interes)) &
        (df['ENTIDAD'] != 'EXTRANJERO')  # Excluir extranjero
    ].copy()
    
    print(f"📊 Registros filtrados (2025, conceptos específicos): {len(df_filtered)}")
    
    # Meses a considerar (enero a julio 2025)
    meses_2025 = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO']
    
    # Crear dataset con suma de meses por entidad, concepto y tipo
    resultados = []
    
    for concepto in conceptos_interes:
        concepto_data = df_filtered[df_filtered['CONCEPTO'] == concepto]
        
        for entidad in sorted(concepto_data['ENTIDAD'].unique()):
            entidad_data = concepto_data[concepto_data['ENTIDAD'] == entidad]
            
            for tipo in sorted(entidad_data['TIPO'].unique()):
                tipo_data = entidad_data[entidad_data['TIPO'] == tipo]
                
                # Sumar todos los meses de enero a julio 2025
                total_tipo = tipo_data[meses_2025].sum().sum()
                
                resultados.append({
                    'ENTIDAD': entidad,
                    'CONCEPTO': concepto,
                    'TIPO': tipo,
                    'TOTAL_ENE_JUL_2025': total_tipo
                })
    
    # Crear DataFrame final
    df_resultado = pd.DataFrame(resultados)
    
    # Filtrar solo registros con datos > 0 para reducir ruido
    df_resultado = df_resultado[df_resultado['TOTAL_ENE_JUL_2025'] > 0]
    
    print(f"📈 Registros con datos > 0: {len(df_resultado)}")
    
    # Verificar datos por concepto
    for concepto in conceptos_interes:
        concepto_data = df_resultado[df_resultado['CONCEPTO'] == concepto]
        total_casos = concepto_data['TOTAL_ENE_JUL_2025'].sum()
        entidades_count = concepto_data['ENTIDAD'].nunique()
        tipos_count = concepto_data['TIPO'].nunique()
        
        print(f"\n🎯 {concepto}:")
        print(f"   Total casos: {total_casos:,}")
        print(f"   Entidades con datos: {entidades_count}")
        print(f"   Tipos únicos: {tipos_count}")
        print(f"   Tipos: {sorted(concepto_data['TIPO'].unique())}")
    
    # Guardar archivo CSV
    output_file = '../data/estatal_concepto_tipo_analysis.csv'
    df_resultado.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"\n✅ Archivo guardado: {output_file}")
    print(f"📊 Total registros guardados: {len(df_resultado)}")
    
    # Mostrar preview de los datos
    print("\n📋 Preview de los datos:")
    print(df_resultado.head(10).to_string(index=False))

if __name__ == "__main__":
    main()

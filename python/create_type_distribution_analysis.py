import pandas as pd
import numpy as np

def create_type_distribution_analysis():
    """
    Crea un CSV con la distribución de tipos por concepto y año
    para generar pie charts en la Gráfica 3
    """
    
    # Leer el CSV procesado
    df = pd.read_csv('data/IDEFF_processed.csv')
    
    # Columnas de meses (enero a julio)
    month_columns = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO']
    
    # Agrupar por AÑO, CONCEPTO, TIPO y sumar los meses
    df_grouped = df.groupby(['AÑO', 'CONCEPTO', 'TIPO'])[month_columns].sum().reset_index()
    
    # Crear un DataFrame pivoteado para el formato final
    result_data = []
    
    # Obtener conceptos únicos
    unique_concepts = df_grouped['CONCEPTO'].unique()
    
    for concepto in unique_concepts:
        # Filtrar datos para este concepto
        concepto_data = df_grouped[df_grouped['CONCEPTO'] == concepto]
        
        # Obtener años únicos para este concepto
        years = sorted(concepto_data['AÑO'].unique())
        
        # Obtener tipos únicos para este concepto
        tipos = sorted(concepto_data['TIPO'].unique())
        
        # Crear filas para cada año
        for year in years:
            year_data = concepto_data[concepto_data['AÑO'] == year]
            
            # Crear diccionario para esta fila
            row = {
                'CONCEPTO': concepto,
                'AÑO': year
            }
            
            # Agregar totales por tipo para este año
            for tipo in tipos:
                tipo_data = year_data[year_data['TIPO'] == tipo]
                if not tipo_data.empty:
                    # Sumar todos los meses (enero a julio)
                    total = tipo_data[month_columns].sum().sum()
                    row[tipo] = int(total)
                else:
                    row[tipo] = 0
            
            result_data.append(row)
    
    # Crear DataFrame final
    result_df = pd.DataFrame(result_data)
    
    # Reordenar columnas: CONCEPTO, AÑO, luego todos los tipos
    tipos_ordered = sorted([col for col in result_df.columns if col not in ['CONCEPTO', 'AÑO']])
    final_columns = ['CONCEPTO', 'AÑO'] + tipos_ordered
    result_df = result_df[final_columns]
    
    # Guardar CSV
    output_file = 'data/type_distribution_analysis.csv'
    result_df.to_csv(output_file, index=False)
    
    print(f"✅ CSV generado: {output_file}")
    print(f"📊 Conceptos encontrados: {len(unique_concepts)}")
    print(f"📅 Años cubiertos: {sorted(df_grouped['AÑO'].unique())}")
    
    # Mostrar ejemplo de los datos generados
    print("\n📋 Ejemplo de datos generados:")
    print(result_df.head(10))
    
    # Mostrar estadísticas por concepto
    print("\n📈 Estadísticas por concepto:")
    for concepto in unique_concepts:
        concepto_stats = result_df[result_df['CONCEPTO'] == concepto]
        tipos_count = len([col for col in concepto_stats.columns if col not in ['CONCEPTO', 'AÑO']])
        print(f"  • {concepto}: {tipos_count} tipos diferentes")
    
    return result_df

if __name__ == "__main__":
    try:
        df_result = create_type_distribution_analysis()
        print("\n🎉 Análisis completado exitosamente!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Asegúrate de que el archivo 'data/IDEFF_processed.csv' existe")
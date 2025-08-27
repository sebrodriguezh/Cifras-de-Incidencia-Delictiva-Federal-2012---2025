import pandas as pd
import numpy as np
from pathlib import Path

def create_type_distribution_analysis():
    """
    Crea un CSV con la distribución de tipos por concepto y año
    para generar pie charts en la Gráfica 3
    """
    
    try:
        print("🔄 Procesando base de datos IDEFF para análisis de tipos...")
        
        # Leer el CSV original IDEFF_jul25.csv (como en create_percentage_analysis.py)
        csv_file = Path('data/IDEFF_jul25.csv')
        df = pd.read_csv(csv_file, encoding='latin-1')
        
        print(f"✅ CSV leído: {len(df)} filas, {len(df.columns)} columnas")
        
        # Filtrar solo años 2018-2025 (incluyendo 2018 para cálculos porcentuales)
        # Asumiendo que la primera columna es el año
        df['Año'] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
        df_filtered = df[(df['Año'] >= 2018) & (df['Año'] <= 2025)]
        
        print(f"📅 Filas después de filtrar años 2018-2025: {len(df_filtered)}")
        
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
        
        # Columnas de meses (enero a julio)
        month_columns = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO']
        
        # Agrupar por AÑO, CONCEPTO, TIPO y sumar los meses
        df_grouped = df_filtered.groupby(['AÑO', 'CONCEPTO', 'TIPO'])[month_columns].sum().reset_index()
        
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
        
        # Llenar valores NaN con 0 para evitar celdas vacías
        result_df = result_df.fillna(0)
        
        # Convertir todas las columnas numéricas a enteros
        for col in result_df.columns:
            if col not in ['CONCEPTO', 'AÑO']:
                result_df[col] = result_df[col].astype(int)
        
        # Guardar CSV
        output_file = 'data/type_distribution_analysis.csv'
        result_df.to_csv(output_file, index=False)
        
        print(f"💾 CSV generado: {output_file}")
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
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Asegúrate de que el archivo 'data/IDEFF_jul25.csv' existe")
        return None

if __name__ == "__main__":
    try:
        df_result = create_type_distribution_analysis()
        if df_result is not None:
            print("\n🎉 Análisis completado exitosamente!")
        else:
            print("\n❌ Análisis falló")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Asegúrate de que el archivo 'data/IDEFF_jul25.csv' existe")
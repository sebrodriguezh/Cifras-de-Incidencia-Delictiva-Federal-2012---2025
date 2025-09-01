#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear un CSV de análisis con datos específicos de detenidos
Incluye: detainee_name, criminal_group (homologado), charges_or_supposed_role, state_of_arrest
"""

import pandas as pd
from pathlib import Path

def crear_csv_analisis_detenidos():
    """Crea un CSV con datos específicos de detenidos para análisis"""
    
    try:
        print("🔄 Creando CSV de análisis de detenidos...")
        
        # Leer el CSV principal
        csv_file = Path('data/gabinete_detenidos_final.csv')
        df = pd.read_csv(csv_file, encoding='utf-8')
        print(f"✅ CSV leído: {len(df)} filas")
        
        # Seleccionar solo las columnas necesarias
        columnas_necesarias = [
            'detainee_name',
            'criminal_group', 
            'charges_or_supposed_role',
            'state_of_arrest'
        ]
        
        # Verificar que las columnas existen
        columnas_faltantes = [col for col in columnas_necesarias if col not in df.columns]
        if columnas_faltantes:
            print(f"❌ Columnas faltantes: {columnas_faltantes}")
            return False
        
        # Crear DataFrame con solo las columnas necesarias
        df_analisis = df[columnas_necesarias].copy()
        
        # Limpiar datos vacíos o nulos
        print("🔄 Limpiando datos...")
        
        # Reemplazar valores nulos con string vacío para mejor manejo
        df_analisis = df_analisis.fillna('')
        
        # Filtrar registros que tengan al menos detainee_name
        df_analisis = df_analisis[df_analisis['detainee_name'] != '']
        
        print(f"✅ Registros con nombre de detenido: {len(df_analisis)}")
        
        # Mostrar estadísticas por columna
        print("\n📊 ESTADÍSTICAS POR COLUMNA:")
        for col in columnas_necesarias:
            no_vacios = len(df_analisis[df_analisis[col] != ''])
            porcentaje = round((no_vacios / len(df_analisis)) * 100, 1)
            print(f"   • {col}: {no_vacios} registros ({porcentaje}%)")
        
        # Guardar CSV de análisis
        output_file = Path('data/analisis_detenidos.csv')
        df_analisis.to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"\n💾 CSV de análisis guardado en: {output_file}")
        print(f"📋 Columnas incluidas: {', '.join(columnas_necesarias)}")
        
        # Mostrar preview de los datos
        print(f"\n📋 PREVIEW DE LOS DATOS:")
        print(df_analisis.head(10).to_string(index=False))
        
        # Mostrar algunos ejemplos de grupos criminales
        grupos_unicos = df_analisis[df_analisis['criminal_group'] != '']['criminal_group'].value_counts()
        print(f"\n📊 TOP 10 GRUPOS CRIMINALES:")
        for grupo, casos in grupos_unicos.head(10).items():
            print(f"   • {grupo}: {casos} casos")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando CSV de análisis: {e}")
        return False

if __name__ == "__main__":
    crear_csv_analisis_detenidos()

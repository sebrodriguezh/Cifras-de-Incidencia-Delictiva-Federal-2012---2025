#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para analizar los cargos únicos de los dos carteles principales
Cártel del Pacífico (Los Mayos) y Cártel del Pacífico (Los Chapitos)
"""

import pandas as pd
from pathlib import Path

def analizar_cargos_carteles():
    """Analiza los cargos únicos de los dos carteles principales"""
    
    try:
        print("🔄 Analizando cargos de carteles principales...")
        
        # Leer el CSV de análisis
        csv_file = Path('data/analisis_detenidos.csv')
        df = pd.read_csv(csv_file, encoding='utf-8')
        print(f"✅ CSV leído: {len(df)} filas")
        
        # Filtrar solo registros con grupo criminal
        df_con_grupo = df[df['criminal_group'] != '']
        print(f"✅ Registros con grupo criminal: {len(df_con_grupo)}")
        
        # Definir los dos carteles principales
        carteles_principales = [
            'Cártel del Pacífico (Los Mayos)',
            'Cártel del Pacífico (Los Chapitos)'
        ]
        
        print(f"\n📊 ANÁLISIS DE CARGOS POR CARTEL:")
        print("=" * 60)
        
        for cartel in carteles_principales:
            print(f"\n🔍 {cartel.upper()}")
            print("-" * 50)
            
            # Filtrar registros del cartel específico
            df_cartel = df_con_grupo[df_con_grupo['criminal_group'] == cartel]
            
            if len(df_cartel) == 0:
                print(f"   ❌ No se encontraron registros para {cartel}")
                continue
            
            print(f"   📈 Total de detenidos: {len(df_cartel)}")
            
            # Filtrar solo registros con cargos
            df_cartel_con_cargos = df_cartel[df_cartel['charges_or_supposed_role'] != '']
            print(f"   📋 Con cargos reportados: {len(df_cartel_con_cargos)} ({round((len(df_cartel_con_cargos)/len(df_cartel))*100, 1)}%)")
            
            if len(df_cartel_con_cargos) > 0:
                # Obtener cargos únicos
                cargos_unicos = df_cartel_con_cargos['charges_or_supposed_role'].value_counts()
                
                print(f"   🎯 Cargos únicos encontrados: {len(cargos_unicos)}")
                print(f"\n   📝 LISTA DE CARGOS:")
                
                for i, (cargo, frecuencia) in enumerate(cargos_unicos.items(), 1):
                    porcentaje = round((frecuencia / len(df_cartel_con_cargos)) * 100, 1)
                    print(f"      {i:2d}. {cargo}")
                    print(f"          └─ {frecuencia} casos ({porcentaje}% del cartel)")
                    print()
            else:
                print(f"   ⚠️  No hay cargos reportados para {cartel}")
        
        # Análisis comparativo
        print(f"\n📊 ANÁLISIS COMPARATIVO:")
        print("=" * 60)
        
        for cartel in carteles_principales:
            df_cartel = df_con_grupo[df_con_grupo['criminal_group'] == cartel]
            df_cartel_con_cargos = df_cartel[df_cartel['charges_or_supposed_role'] != '']
            
            if len(df_cartel_con_cargos) > 0:
                cargos_unicos = len(df_cartel_con_cargos['charges_or_supposed_role'].unique())
                print(f"   • {cartel}: {cargos_unicos} tipos de cargos únicos")
        
        return True
        
    except Exception as e:
        print(f"❌ Error analizando cargos: {e}")
        return False

if __name__ == "__main__":
    analizar_cargos_carteles()

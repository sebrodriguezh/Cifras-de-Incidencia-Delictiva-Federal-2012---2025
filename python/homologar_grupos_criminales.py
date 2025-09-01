#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para homologar nombres de grupos criminales en el CSV
Consolida variaciones de nombres en un nombre estándar
"""

import pandas as pd
import json
from pathlib import Path

def homologar_grupos_criminales():
    """Homologa nombres de grupos criminales en el CSV"""
    
    try:
        print("🔄 Homologando nombres de grupos criminales...")
        
        # Leer el CSV
        csv_file = Path('data/gabinete_detenidos_final.csv')
        df = pd.read_csv(csv_file, encoding='utf-8')
        print(f"✅ CSV leído: {len(df)} filas")
        
        # Diccionario de homologaciones
        homologaciones = {
            # Consolidar variaciones de Los Mayos
            'Los Mayos': 'Cártel del Pacífico (Los Mayos)',
            'Cártel del Pacífico (Los Menores)': 'Cártel del Pacífico (Los Chapitos)',
            'Los Chapitos': 'Cártel del Pacífico (Los Chapitos)',
            'Cártel de Sinaloa (Los Chapitos)': 'Cártel del Pacífico (Los Chapitos)'
            
            # Agregar más homologaciones aquí según sea necesario
            # 'Variación 1': 'Nombre estándar',
            # 'Variación 2': 'Nombre estándar',
        }
        
        # Aplicar homologaciones
        cambios_aplicados = 0
        for variacion, nombre_estandar in homologaciones.items():
            # Contar cuántos registros tienen esta variación
            registros_antes = len(df[df['criminal_group'] == variacion])
            if registros_antes > 0:
                print(f"🔄 Homologando '{variacion}' → '{nombre_estandar}' ({registros_antes} registros)")
                df.loc[df['criminal_group'] == variacion, 'criminal_group'] = nombre_estandar
                cambios_aplicados += registros_antes
        
        print(f"✅ Total de cambios aplicados: {cambios_aplicados}")
        
        # Guardar CSV actualizado
        df.to_csv(csv_file, index=False, encoding='utf-8')
        print(f"💾 CSV actualizado guardado en: {csv_file}")
        
        # Regenerar análisis de grupos criminales
        print("🔄 Regenerando análisis de grupos criminales...")
        regenerar_analisis_grupos()
        
        return True
        
    except Exception as e:
        print(f"❌ Error homologando grupos: {e}")
        return False

def regenerar_analisis_grupos():
    """Regenera el análisis de grupos criminales con los nombres homologados"""
    
    try:
        # Leer el CSV actualizado
        csv_file = Path('data/gabinete_detenidos_final.csv')
        df = pd.read_csv(csv_file, encoding='utf-8')
        
        # Filtrar registros con grupo criminal
        df_con_grupo = df[df['criminal_group'].notna() & (df['criminal_group'] != '')]
        
        # Contar grupos únicos
        grupos_count = df_con_grupo['criminal_group'].value_counts()
        
        # Calcular estadísticas
        total_registros = len(df)
        total_con_grupo = len(df_con_grupo)
        total_grupos = len(grupos_count)
        
        # Crear estructura de datos
        grupos_data = []
        for i, (grupo, casos) in enumerate(grupos_count.items(), 1):
            porcentaje = round((casos / total_con_grupo) * 100, 1)
            grupos_data.append({
                'rank': i,
                'grupo': grupo,
                'casos': int(casos),
                'porcentaje': porcentaje
            })
        
        # Crear JSON final
        resultado = {
            'total_grupos': total_grupos,
            'total_casos_con_grupo': total_con_grupo,
            'grupos': grupos_data
        }
        
        # Guardar JSON
        json_file = Path('data/all_criminal_groups.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Análisis actualizado guardado en: {json_file}")
        print(f"📊 Estadísticas actualizadas:")
        print(f"   • Total registros: {total_registros}")
        print(f"   • Con grupo reportado: {total_con_grupo} ({round((total_con_grupo/total_registros)*100, 1)}%)")
        print(f"   • Grupos únicos: {total_grupos}")
        
        # Mostrar top 5
        print(f"\n📋 TOP 5 GRUPOS ACTUALIZADOS:")
        for grupo in grupos_data[:5]:
            print(f"   {grupo['rank']}. {grupo['grupo']}: {grupo['casos']} casos ({grupo['porcentaje']}%)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error regenerando análisis: {e}")
        return False

if __name__ == "__main__":
    homologar_grupos_criminales()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para optimizar el archivo GeoJSON de estados y reducir su tamaño
"""

import json
from pathlib import Path

def optimize_geojson():
    """Optimiza el archivo GeoJSON existente para reducir su tamaño"""
    
    try:
        print("🔄 Optimizando archivo GeoJSON existente...")
        
        # Ruta al archivo GeoJSON existente
        geojson_path = Path('data/geojson/estados.json')
        
        if not geojson_path.exists():
            print(f"❌ No se encontró el archivo: {geojson_path}")
            return None
        
        print(f"✅ Archivo encontrado: {geojson_path}")
        
        # Leer el archivo actual
        with open(geojson_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Mostrar tamaño actual
        current_size = geojson_path.stat().st_size / (1024 * 1024)  # MB
        print(f"📏 Tamaño actual: {current_size:.2f} MB")
        print(f"📊 Estados en el archivo: {len(data['features'])}")
        
        # Crear versión optimizada
        print("🔄 Creando versión optimizada...")
        
        # Solo mantener propiedades esenciales
        optimized_features = []
        for feature in data['features']:
            # Solo mantener NOMGEO y geometry
            optimized_feature = {
                'type': 'Feature',
                'properties': {
                    'NOMGEO': feature['properties'].get('NOMGEO', 'Estado')
                },
                'geometry': feature['geometry']
            }
            optimized_features.append(optimized_feature)
        
        # Crear estructura optimizada
        optimized_data = {
            'type': 'FeatureCollection',
            'features': optimized_features
        }
        
        # Crear archivo de respaldo
        backup_path = Path('data/geojson/estados_backup.json')
        print(f"💾 Creando respaldo en: {backup_path}")
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
        
        # Guardar versión optimizada
        print("💾 Guardando versión optimizada...")
        with open(geojson_path, 'w', encoding='utf-8') as f:
            json.dump(optimized_data, f, ensure_ascii=False, separators=(',', ':'))
        
        # Mostrar nuevo tamaño
        new_size = geojson_path.stat().st_size / (1024 * 1024)  # MB
        reduction = ((current_size - new_size) / current_size) * 100
        
        print(f"✅ Optimización completada!")
        print(f"📏 Nuevo tamaño: {new_size:.2f} MB")
        print(f"📉 Reducción: {reduction:.1f}%")
        
        return geojson_path
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print("🚀 INICIANDO OPTIMIZACIÓN DE GEOJSON")
    print("=" * 40)
    
    result = optimize_geojson()
    
    if result:
        print("\n🎉 Optimización completada exitosamente!")
        print(f"📁 Archivo optimizado: {result}")
        print("\n💡 El archivo ahora es mucho más pequeño y apto para Git")
    else:
        print("\n❌ La optimización falló")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para convertir shapefile de estados de INEGI a GeoJSON
"""

import geopandas as gpd
import json
from pathlib import Path

def convert_estados_to_geojson():
    """Convierte el shapefile de estados a GeoJSON"""
    
    try:
        print("🔄 Convirtiendo shapefile de estados a GeoJSON...")
        
        # Ruta al shapefile de estados
        shapefile_path = Path('data/shapefiles/mg_2024_integrado/conjunto_de_datos/00ent.shp')
        
        if not shapefile_path.exists():
            print(f"❌ No se encontró el archivo: {shapefile_path}")
            return None
        
        print(f"✅ Shapefile encontrado: {shapefile_path}")
        
        # Leer el shapefile
        gdf = gpd.read_file(shapefile_path)
        
        print(f"📊 Geometrías cargadas: {len(gdf)} estados")
        print(f"📋 Columnas disponibles: {list(gdf.columns)}")
        
        # Mostrar información del CRS (sistema de coordenadas)
        print(f"🗺️ CRS actual: {gdf.crs}")
        
        # Mostrar las primeras filas para ver la estructura
        print("\n📋 Primeras filas del shapefile:")
        print(gdf.head())
        
        # Convertir a WGS84 (lat/lng) si no está ya en ese sistema
        if gdf.crs and gdf.crs != 'EPSG:4326':
            print(f"\n🔄 Convirtiendo coordenadas a WGS84 (EPSG:4326)...")
            gdf = gdf.to_crs('EPSG:4326')
            print(f"✅ Coordenadas convertidas a WGS84")
        
        # Simplificar geometrías para reducir el tamaño del archivo
        # tolerance=0.001 mantiene la precisión pero reduce el tamaño
        print("\n🔄 Simplificando geometrías...")
        gdf_simple = gdf.copy()
        gdf_simple['geometry'] = gdf_simple['geometry'].simplify(tolerance=0.001)
        
        # Convertir a GeoJSON
        print("🔄 Convirtiendo a GeoJSON...")
        geojson_data = gdf_simple.to_json()
        
        # Crear directorio de salida si no existe
        output_dir = Path('data/geojson')
        output_dir.mkdir(exist_ok=True)
        
        # Guardar GeoJSON
        output_file = output_dir / 'estados.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json.loads(geojson_data), f, ensure_ascii=False, indent=2)
        
        print(f"💾 GeoJSON guardado en: {output_file}")
        
        # Mostrar estadísticas del archivo generado
        file_size = output_file.stat().st_size / (1024 * 1024)  # MB
        print(f"📏 Tamaño del archivo: {file_size:.2f} MB")
        
        # Verificar que se puede leer correctamente
        with open(output_file, 'r', encoding='utf-8') as f:
            test_data = json.load(f)
        
        print(f"✅ Archivo verificado: {len(test_data['features'])} estados")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print("🚀 INICIANDO CONVERSIÓN DE SHAPEFILE A GEOJSON")
    print("=" * 50)
    
    result = convert_estados_to_geojson()
    
    if result:
        print("\n🎉 Conversión completada exitosamente!")
        print(f"📁 Archivo generado: {result}")
        print("\n💡 Ahora puedes usar este GeoJSON en tu mapa HTML")
    else:
        print("\n❌ La conversión falló")
        print("Verifica que el shapefile existe y es válido")

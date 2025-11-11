import pandas as pd
import re

def convertir_txt_a_csv(archivo_entrada, archivo_salida='reseñas_rapido.csv'):
    """
    Convierte archivo de reseñas a formato CSV
    Soporta varios formatos de entrada
    """
    
    print(f"📂 Leyendo archivo: {archivo_entrada}")
    
    # Intentar leer como CSV directo (separado por comas, tabs, etc.)
    try:
        # Intentar con diferentes separadores
        for sep in [',', '\t', ';', '|']:
            try:
                df = pd.read_csv(archivo_entrada, sep=sep, encoding='utf-8')
                if len(df.columns) > 1:  # Si tiene múltiples columnas, probablemente funcionó
                    print(f"✅ Archivo leído correctamente con separador: '{sep}'")
                    print(f"📊 Columnas encontradas: {list(df.columns)}")
                    print(f"📝 Total de filas: {len(df)}")
                    
                    # Guardar como CSV estándar
                    df.to_csv(archivo_salida, index=False, encoding='utf-8')
                    print(f"💾 Archivo guardado como: {archivo_salida}")
                    return df
            except:
                continue
    except Exception as e:
        print(f"⚠️ No se pudo leer como CSV estándar: {e}")
    
    # Si no funcionó, intentar parsear formato personalizado
    print("🔄 Intentando parsear formato personalizado...")
    
    with open(archivo_entrada, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Ejemplo de parseo para formato de reseñas web scrapeadas
    # Ajusta este patrón según tu formato específico
    reseñas = []
    
    # Patrón para reseñas tipo: "Nombre: X\nPuntuación: Y\nComentario: Z"
    patron = r'Nombre:\s*(.+?)\n.*?Puntuación:\s*(.+?)\n.*?Comentario:\s*(.+?)(?=\n\n|\Z)'
    matches = re.finditer(patron, contenido, re.DOTALL | re.MULTILINE)
    
    for match in matches:
        reseñas.append({
            'Nombre': match.group(1).strip(),
            'Puntuación': match.group(2).strip(),
            'Comentario': match.group(3).strip()
        })
    
    if reseñas:
        df = pd.DataFrame(reseñas)
        df.to_csv(archivo_salida, index=False, encoding='utf-8')
        print(f"✅ {len(reseñas)} reseñas convertidas y guardadas")
        return df
    
    print("❌ No se pudo parsear el archivo. Por favor, verifica el formato.")
    return None


def convertir_json_a_csv(archivo_json, archivo_salida='reseñas_rapido.csv'):
    """
    Convierte archivo JSON de reseñas a CSV
    """
    try:
        df = pd.read_json(archivo_json)
        df.to_csv(archivo_salida, index=False, encoding='utf-8')
        print(f"✅ JSON convertido a CSV: {archivo_salida}")
        return df
    except Exception as e:
        print(f"❌ Error al convertir JSON: {e}")
        return None


def crear_csv_ejemplo():
    """
    Crea un archivo CSV de ejemplo con la estructura correcta
    """
    datos_ejemplo = {
        'Nombre': ['Juan Pérez', 'María García', 'Carlos López', 'Ana Martínez', 'Pedro Sánchez'],
        'Puntuación': [5, 4, 2, 5, 3],
        'Comida': [5, 4, 2, 5, 3],
        'Servicio': [5, 4, 3, 5, 3],
        'Ambiente': [5, 5, 2, 4, 4],
        'Fecha': ['hace 2 días', 'hace 1 semana', 'hace 3 semanas', 'hace 1 mes', 'hace 2 meses'],
        'Comentario': [
            'Excelente restaurante, la comida estuvo deliciosa y el servicio impecable.',
            'Muy buena experiencia, aunque el tiempo de espera fue un poco largo.',
            'La comida no estuvo tan buena como esperaba, servicio regular.',
            'Increíble lugar, definitivamente volveré. Todo estuvo perfecto.',
            'Experiencia promedio, nada extraordinario pero tampoco malo.'
        ],
        'Platos recomendados': ['Pizza Margherita', 'Pasta Carbonara', '', 'Lasagna', 'Ensalada César'],
        'Número de reseñas': [15, 8, 23, 5, 42]
    }
    
    df = pd.DataFrame(datos_ejemplo)
    df.to_csv('reseñas_ejemplo.csv', index=False, encoding='utf-8')
    print("✅ Archivo de ejemplo creado: reseñas_ejemplo.csv")
    return df


def verificar_estructura_csv(archivo_csv):
    """
    Verifica que el CSV tenga las columnas necesarias para el dashboard
    """
    columnas_requeridas = ['Nombre', 'Puntuación', 'Comentario']
    columnas_opcionales = ['Comida', 'Servicio', 'Ambiente', 'Fecha', 'Platos recomendados', 'Número de reseñas']
    
    try:
        df = pd.read_csv(archivo_csv, encoding='utf-8')
        print(f"\n📊 Estructura del archivo CSV:")
        print(f"   Total de filas: {len(df)}")
        print(f"   Columnas encontradas: {list(df.columns)}")
        
        print(f"\n✅ Columnas requeridas:")
        for col in columnas_requeridas:
            if col in df.columns:
                print(f"   ✓ {col}")
            else:
                print(f"   ✗ {col} (FALTANTE)")
        
        print(f"\n📋 Columnas opcionales:")
        for col in columnas_opcionales:
            if col in df.columns:
                print(f"   ✓ {col}")
            else:
                print(f"   - {col} (no presente)")
        
        print(f"\n📈 Primeras 3 filas:")
        print(df.head(3).to_string())
        
        return df
    except Exception as e:
        print(f"❌ Error al verificar CSV: {e}")
        return None


# ============================================
# USO DEL SCRIPT
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("🔄 CONVERTIDOR DE RESEÑAS A CSV")
    print("=" * 60)
    
    # Opción 1: Convertir tu archivo actual
    archivo_entrada = r"D:\python\blockchain\reseñas_rapido.txt"
    
    # Descomentar para convertir tu archivo:
    # df = convertir_txt_a_csv(archivo_entrada)
    
    # Opción 2: Crear archivo de ejemplo
    print("\n📝 Creando archivo CSV de ejemplo...")
    df_ejemplo = crear_csv_ejemplo()
    
    # Opción 3: Verificar estructura de un CSV existente
    print("\n🔍 Verificando estructura del CSV de ejemplo...")
    verificar_estructura_csv('reseñas_ejemplo.csv')
    
    print("\n" + "=" * 60)
    print("✅ PROCESO COMPLETADO")
    print("=" * 60)
    print("\nPróximos pasos:")
    print("1. Si tu archivo tiene formato especial, modifica la función 'convertir_txt_a_csv'")
    print("2. Ejecuta el script con tu archivo real")
    print("3. Verifica la estructura con 'verificar_estructura_csv'")
    print("4. Usa el CSV generado en tu dashboard HTML")
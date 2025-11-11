import pandas as pd
import numpy as np

# Cargar el CSV
df = pd.read_csv('reseñas.csv')

# Convertir columnas a numéricas
df['Puntuación'] = pd.to_numeric(df['Puntuación'], errors='coerce')
df['Comida'] = pd.to_numeric(df['Comida'], errors='coerce')
df['Servicio'] = pd.to_numeric(df['Servicio'], errors='coerce')
df['Ambiente'] = pd.to_numeric(df['Ambiente'], errors='coerce')

# ============ RESEÑAS NEGATIVAS (Puntuación < 3) ============
print("=" * 60)
print("RESEÑAS NEGATIVAS (Puntuación < 3)")
print("=" * 60)

negativas = df[df['Puntuación'] < 3]
print(f"\nTotal de reseñas negativas: {len(negativas)}")

# Calcular promedios excluyendo valores 0
comida_negativa = negativas[negativas['Comida'] > 0]['Comida'].mean()
servicio_negativa = negativas[negativas['Servicio'] > 0]['Servicio'].mean()
ambiente_negativa = negativas[negativas['Ambiente'] > 0]['Ambiente'].mean()

print(f"\nComida:    {comida_negativa:.2f} (N={len(negativas[negativas['Comida'] > 0])})")
print(f"Servicio:  {servicio_negativa:.2f} (N={len(negativas[negativas['Servicio'] > 0])})")
print(f"Ambiente:  {ambiente_negativa:.2f} (N={len(negativas[negativas['Ambiente'] > 0])})")

# ============ RESEÑAS POSITIVAS (Puntuación > 3) ============
print("\n" + "=" * 60)
print("RESEÑAS POSITIVAS (Puntuación > 3)")
print("=" * 60)

positivas = df[df['Puntuación'] > 3]
print(f"\nTotal de reseñas positivas: {len(positivas)}")

comida_positiva = positivas[positivas['Comida'] > 0]['Comida'].mean()
servicio_positiva = positivas[positivas['Servicio'] > 0]['Servicio'].mean()
ambiente_positiva = positivas[positivas['Ambiente'] > 0]['Ambiente'].mean()

print(f"\nComida:    {comida_positiva:.2f} (N={len(positivas[positivas['Comida'] > 0])})")
print(f"Servicio:  {servicio_positiva:.2f} (N={len(positivas[positivas['Servicio'] > 0])})")
print(f"Ambiente:  {ambiente_positiva:.2f} (N={len(positivas[positivas['Ambiente'] > 0])})")

# ============ RESEÑAS NEUTRALES (Puntuación = 3) ============
print("\n" + "=" * 60)
print("RESEÑAS NEUTRALES (Puntuación = 3)")
print("=" * 60)

neutrales = df[df['Puntuación'] == 3]
print(f"\nTotal de reseñas neutrales: {len(neutrales)}")

comida_neutral = neutrales[neutrales['Comida'] > 0]['Comida'].mean()
servicio_neutral = neutrales[neutrales['Servicio'] > 0]['Servicio'].mean()
ambiente_neutral = neutrales[neutrales['Ambiente'] > 0]['Ambiente'].mean()

print(f"\nComida:    {comida_neutral:.2f} (N={len(neutrales[neutrales['Comida'] > 0])})")
print(f"Servicio:  {servicio_neutral:.2f} (N={len(neutrales[neutrales['Servicio'] > 0])})")
print(f"Ambiente:  {ambiente_neutral:.2f} (N={len(neutrales[neutrales['Ambiente'] > 0])})")

# ============ TODAS LAS RESEÑAS ============
print("\n" + "=" * 60)
print("TODAS LAS RESEÑAS")
print("=" * 60)

comida_total = df[df['Comida'] > 0]['Comida'].mean()
servicio_total = df[df['Servicio'] > 0]['Servicio'].mean()
ambiente_total = df[df['Ambiente'] > 0]['Ambiente'].mean()
puntuacion_total = df['Puntuación'].mean()

print(f"\nTotal de reseñas: {len(df)}")
print(f"\nComida:       {comida_total:.2f}")
print(f"Servicio:     {servicio_total:.2f}")
print(f"Ambiente:     {ambiente_total:.2f}")
print(f"Puntuación:   {puntuacion_total:.2f}")

# ============ RESUMEN COMPARATIVO ============
print("\n" + "=" * 60)
print("RESUMEN COMPARATIVO")
print("=" * 60)

print("\n{:<15} {:<15} {:<15} {:<15}".format("Categoría", "Negativos", "Neutrales", "Positivos"))
print("-" * 60)
print("{:<15} {:<15.2f} {:<15.2f} {:<15.2f}".format("Comida", comida_negativa, comida_neutral, comida_positiva))
print("{:<15} {:<15.2f} {:<15.2f} {:<15.2f}".format("Servicio", servicio_negativa, servicio_neutral, servicio_positiva))
print("{:<15} {:<15.2f} {:<15.2f} {:<15.2f}".format("Ambiente", ambiente_negativa, ambiente_neutral, ambiente_positiva))
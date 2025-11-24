# 1. Convertir todo a string y limpiar espacios invisibles
df1["Nombre"] = df1["Nombre"].astype(str).str.strip()
df1["Comentario"] = df1["Comentario"].astype(str).str.strip()

df2["Nombre"] = df2["Nombre"].astype(str).str.strip()
df2["Comentario"] = df2["Comentario"].astype(str).str.strip()

# 2. Crear la clave exacta
df1["clave"] = df1["Nombre"] + "||" + df1["Comentario"]
df2["clave"] = df2["Nombre"] + "||" + df2["Comentario"]

# 3. Cuántas claves nuevas ya existen EXACTAS en df1
repetidas_en_df1 = df2[df2["clave"].isin(df1["clave"])]

print("Cantidad de coincidencias exactas encontradas:", len(repetidas_en_df1))

# Mostrar algunas coincidencias si existen
print(repetidas_en_df1.head(10))

import os
import pandas as pd
import hashlib
import unicodedata

# --- Ajusta esta carpeta ---
carpeta = r"D:\python\Dashboardreview"
archivo1 = os.path.join(carpeta, "reseñas_juntas.csv")       # histórico (old)
archivo2 = os.path.join(carpeta, "reseñas_2025-11-24.csv")   # nuevas (new)
salida_final = os.path.join(carpeta, "reseñas_juntas1.csv")
salida_drops = os.path.join(carpeta, "nuevas_eliminadas_por_dup_exacto.csv")

# ---------- Lectura sin transformar ----------
# keep_default_na=False evita convertir "" en NaN; dtype=str lee todo como str.
df_old = pd.read_csv(archivo1, dtype=str, encoding="utf-8-sig", keep_default_na=False)
df_new = pd.read_csv(archivo2, dtype=str, encoding="utf-8-sig", keep_default_na=False)

# Si tu CSV puede estar en otra codificación, intenta 'latin1' si 'utf-8-sig' falla.
# df_old = pd.read_csv(archivo1, dtype=str, encoding="latin1", keep_default_na=False)

# Añadir columna origen y un índice original
df_old = df_old.reset_index(drop=True).copy()
df_new = df_new.reset_index(drop=True).copy()
df_old["_origen"] = "old"
df_new["_origen"] = "new"
df_old["_idx_orig"] = df_old.index
df_new["_idx_orig"] = df_new.index

# Concatenar: old primero, luego new (así keep='last' conserva new en caso de conflicto)
df_comb = pd.concat([df_old, df_new], ignore_index=True)

print("Filas old:", len(df_old), " Filas new:", len(df_new), " Total combinado:", len(df_comb))

# ---------- Dedupe EXACTO por Nombre + Comentario, mantener new (keep='last') ----------
# Antes de dropear, marcar duplicados por ese subset para ver qué filas se consideran conflicto
df_comb["_is_dup_subset"] = df_comb.duplicated(subset=["Nombre", "Comentario"], keep=False)

# Hacer drop (esto es lo que estás usando)
df_sin_dup = df_comb.drop_duplicates(subset=["Nombre", "Comentario"], keep="last").copy()

print("Filas después de deduplicar (exacto Nombre+Comentario, keep='last'):", len(df_sin_dup))
eliminados = len(df_comb) - len(df_sin_dup)
print("Total eliminados:", eliminados)

# ---------- Identificar cuáles filas de 'new' fueron eliminadas por el drop ----------
# Filas 'new' originales
new_keys = df_new[["Nombre", "Comentario", "_idx_orig"]].copy()
# Crear columna clave igual que usa drop_duplicates
df_comb["_dup_key"] = df_comb["Nombre"].astype(str) + "||" + df_comb["Comentario"].astype(str)
df_sin_dup["_dup_key"] = df_sin_dup["Nombre"].astype(str) + "||" + df_sin_dup["Comentario"].astype(str)

# Todas las claves que quedaron (las que se conservan)
kept_keys = set(df_sin_dup["_dup_key"].tolist())

# Filas new con clave no en kept_keys => fueron eliminadas
new_rows = df_comb[df_comb["_origen"] == "new"].copy()
new_rows["was_kept"] = new_rows["_dup_key"].apply(lambda k: k in kept_keys)

dropped_new = new_rows[new_rows["was_kept"] == False].copy()
print("Filas 'new' que fueron eliminadas (por coincidencia exacta Nombre+Comentario):", len(dropped_new))

# ---------- Si no hay eliminadas, terminamos rápido ----------
if len(dropped_new) == 0:
    print("No se eliminaron filas new por deduplicación exacta. Archivo final guardado.")
    # Guardar resultado final (sin columnas auxiliares)
    out = df_sin_dup.drop(columns=[c for c in df_sin_dup.columns if c.startswith("_")], errors='ignore')
    out.to_csv(salida_final, index=False, encoding="utf-8-sig")
    print("Guardado en:", salida_final)
    raise SystemExit

# ---------- Preparar reporte detallado de las filas new eliminadas y su/las coincidencias old ----------
def md5(s):
    return hashlib.md5((s or "").encode("utf-8", errors="ignore")).hexdigest()

def repr_and_codes(s, limit=120):
    s = "" if s is None else str(s)
    rep = repr(s)
    codes = [(i, hex(ord(ch)), ord(ch)) for i, ch in enumerate(s[:limit])]
    return rep, codes

records = []
# Para cada fila nueva que fue eliminada busco la fila(s) old que compartan la misma clave
for _, nr in dropped_new.iterrows():
    key = nr["_dup_key"]
    # filas en el conjunto combinado que comparten la misma clave (probablemente 1 old y 1 new)
    match_rows = df_comb[df_comb["_dup_key"] == key].sort_values("_origen")  # old antes new
    # recorrer matches y guardar info
    for _, mr in match_rows.iterrows():
        rep_nom, codes_nom = repr_and_codes(mr.get("Nombre"))
        rep_com, codes_com = repr_and_codes(mr.get("Comentario"))
        records.append({
            "dup_key": key,
            "origen": mr.get("_origen"),
            "idx_orig": mr.get("_idx_orig"),
            "Nombre_repr": rep_nom,
            "Comentario_repr": rep_com,
            "Nombre_md5": md5(mr.get("Nombre")),
            "Comentario_md5": md5(mr.get("Comentario")),
            "Nombre_codes_first20": str(codes_nom[:20]),
            "Comentario_codes_first120": str(codes_com[:120])
        })

# Guardar reporte con detalles
df_report = pd.DataFrame(records)
df_report.to_csv(salida_drops, index=False, encoding="utf-8-sig")
print("Se guardó el reporte detallado de nuevas eliminadas en:", salida_drops)

# También imprime hasta 10 ejemplos por consola
print("\nEjemplos (hasta 10) de nuevas eliminadas y sus coincidencias (ver CSV para todo):\n")
for dup_key in df_report["dup_key"].unique()[:10]:
    print("=== dup_key:", dup_key)
    sub = df_report[df_report["dup_key"] == dup_key]
    print(sub.to_string(index=False))
    print("---------------------------------------------------\n")

# ---------- Opciones: guardar final manteniendo todas las columnas originales ----------
out_final = df_sin_dup.drop(columns=[c for c in df_sin_dup.columns if c.startswith("_")], errors='ignore')
out_final.to_csv(salida_final, index=False, encoding="utf-8-sig")
print("Archivo final (dedupe exacto) guardado en:", salida_final)

# FIN

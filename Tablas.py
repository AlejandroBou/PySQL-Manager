import pandas as pd
import psycopg2

# 1. Configuración de conexión [cite: 46-50]
params = {
    "host": "localhost",
    "port": 5432,
    "database": "postgres",
    "user": "odoo",
    "password": "odoo"
}

ruta_csv = r'C:\Users\Usuario1\Desktop\dockercagoento\listado.csv'

try:
    df = pd.read_csv(ruta_csv, encoding='latin1')
    print("✅ Archivo listado.csv leído correctamente.")

    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    print("✅ Conexión con PostgreSQL establecida.")

 # 5. Ampliamos los tipos a TEXT para que quepa cualquier longitud 
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contactos_mailing (
            id SERIAL PRIMARY KEY,
            nombre TEXT,
            domicilio TEXT,
            localidad TEXT,
            cp TEXT,
            telefono TEXT
        );
    """)

    # 6. Insertar usando posiciones
    for index, row in df.iterrows():
        cur.execute("""
            INSERT INTO contactos_mailing (nombre, domicilio, localidad, cp, telefono)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            str(row.iloc[0]), # Nombre
            str(row.iloc[1]), # Domicilio
            str(row.iloc[2]), # Localidad
            str(row.iloc[3]), # CP
            str(row.iloc[4])  # Teléfono
        ))


        conn.commit()
    print(f"🚀 ¡Éxito! Se han importado {len(df)} contactos.")

except Exception as e:
    print(f"❌ Ha ocurrido un error: {e}")
    if 'conn' in locals():
        conn.rollback()

finally:
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals():
        conn.close()


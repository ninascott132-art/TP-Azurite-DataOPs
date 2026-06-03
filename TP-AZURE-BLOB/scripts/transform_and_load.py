
import os
import sqlite3
import json

# Chemin relatif correct par rapport au dossier "scripts"
DATABASE_PATH = "database/dataops.db"

def create_production_table():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Étape 4 & 5 : Création de la table de production
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fct_bitcoin_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_file TEXT UNIQUE,
        extracted_message TEXT,
        transformation_status TEXT
    )
    """)
    conn.commit()
    conn.close()
    print("Table fct_bitcoin_messages prete.")

def transform_and_load_data():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Étape 6 : Extraction depuis la table de staging
    cursor.execute("SELECT source_file, message FROM stg_blob_files")
    staging_rows = cursor.fetchall()
    
    if not staging_rows:
        print("Aucune donnee en staging. Pensez a lancer load_blob_to_sql.py avant.")
        conn.close()
        return
        
    for row in staging_rows:
        source_file = row[0]
        raw_message = row[1]
        
        print(f"Lecture et transformation : {source_file}")
        
        # Étape 7 : Transformation (Nettoyage / Passage en MAJUSCULES)
        if raw_message:
            clean_message = str(raw_message).upper().strip()
            status = "SUCCESS"
        else:
            clean_message = "EMPTY"
            status = "WARNING"
            
        # Étape 8 : Insertion idempotente dans la table finale
        cursor.execute("""
        INSERT OR IGNORE INTO fct_bitcoin_messages (source_file, extracted_message, transformation_status)
        VALUES (?, ?, ?)
        """, (source_file, clean_message, status))
        
        print(f"Charge dans fct_bitcoin_messages : {source_file}")
        
    conn.commit()
    conn.close()
    print("Transformation et chargement termines !")

if __name__ == "__main__":
    create_production_table()
    transform_and_load_data()
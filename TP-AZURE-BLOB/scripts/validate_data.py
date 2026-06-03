
import json
import pandas as pd
import great_expectations as ge
import sys

def validate_json_file(file_path):
    print(f"--- Validation du fichier : {file_path} ---")
    
    # 1. Chargement sécurisé du JSON avec le bon format Pandas
    try:
        # On force la lecture sous forme de série/dictionnaire indexé
        df = pd.read_json(file_path, typ='series').to_frame().T
    except Exception as e:
        print(f"Erreur de lecture du fichier JSON : {e}")
        sys.exit(1)
        
    # 2. Conversion du DataFrame en objet Great Expectations
    ge_df = ge.from_pandas(df)
    
    # 3. Définition des règles de validation (Expectations)
    # Règle A : Vérifier que la colonne 'message' existe
    expect_col_exists = ge_df.expect_column_to_exist(column="message")
    
    # Règle B : Vérifier que le message n'est pas nul
    expect_not_null = ge_df.expect_column_values_to_not_be_null(column="message")
    
    # 4. Analyse globale des résultats
    print(f"Regle 'Colonne message existe' : {'SUCCES' if expect_col_exists.success else 'ECHEC'}")
    print(f"Regle 'Messages non nuls' : {'SUCCES' if expect_not_null.success else 'ECHEC'}")
    
    if expect_col_exists.success and expect_not_null.success:
        print("Resultat Global : Le fichier est VALIDE ! ✅")
    else:
        print("Resultat Global : Le fichier est CORROMPU ! ❌")
        sys.exit(1)

if __name__ == "__main__":
    # Test sur votre fichier du TP 2
    validate_json_file("bitcoin/year=2026/month=05/day=10/test_2.json")
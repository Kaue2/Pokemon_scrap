import pandas as pd
import json

df = pd.read_json('pokemon_caio.json')

df["url"] = "www.pokemondb.net" + df["url"]

def filtrar_evolucoes(linha):
    evolucoes = linha["evolutions"]
    pokemon_id = linha["id"]
    
    evolucoes = [e for e in evolucoes if int(e["id"]) > pokemon_id]
    
    for e in evolucoes:
        e["url"] = "www.pokemondb.net" + e["url"]
    
    return evolucoes

def tratar_ids(linha):
    pokemon_id = linha["id"]
    
    id_concatenado = f"0000{pokemon_id}"
    
    index_inicio = len(id_concatenado) - 4
    
    return id_concatenado[index_inicio:]        

def tratar_eevee(dataframe: pd.DataFrame):

    evolucoes_eevee = dataframe.loc[dataframe["id"] == "0133", "evolutions"].values[0]

    for evolucao in evolucoes_eevee:
        
        id_df = dataframe.index[dataframe["id"] == evolucao["id"]][0]
        
        dataframe.at[id_df, "evolutions"] = []


df["evolutions"] = df.apply(filtrar_evolucoes, axis=1)
df["id"] = df.apply(tratar_ids, axis=1)

tratar_eevee(df)

df.to_json('pokemon_tratado.json', orient="records", force_ascii=True)
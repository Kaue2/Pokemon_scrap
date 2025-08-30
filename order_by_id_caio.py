import pandas as pd

df = pd.read_csv('pokemon.csv')
df['id'] = df['id'].astype(int)
df = df.sort_values('id')
df['id'] = df['id'].astype(str).str.zfill(4)
df.to_csv('pokemon.csv', index=False)
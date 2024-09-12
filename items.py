import pandas as pd


items = pd.read_excel("AlbionItems.xlsx")
items = items.iloc[412:]
items = items[~items['Unique'].str.contains('@')]
items.loc[items['Unique'].str.contains('ARTEFACT', case= False), 'Name'] = 'Artefact ' + items['Name']
items = items.set_index('Unique')
items.to_csv("items.csv")

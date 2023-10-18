# Import modules
import pandas as pd

cjs = pd.read_csv('cjs.csv')
hardees = pd.read_csv('hardees.csv')

geodata = pd.concat([hardees,cjs], ignore_index = True)

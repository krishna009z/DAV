import pandas as pd

# Read the CSV file
df = pd.read_csv(r'C:\Users\KrishnaB\Downloads\IMDB Dataset.csv')

print('Shape:', df.shape)
print('\nColumns:', df.columns.tolist())
print('\nFirst few rows:')
print(df.head(3))
print('\nData types:')
print(df.dtypes)
print('\nSample review:')
print(df.iloc[0])

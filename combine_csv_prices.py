import pandas as pd
import glob

for file in glob.glob("price_csv/n_*.csv"):
    file_name = file.split('/')[1].split('n_')[1]

    n_file = pd.read_csv(file)
    f = pd.read_csv('price_csv/{}'.format(file_name))
    df = pd.concat([n_file, f]).drop_duplicates()
    df.to_csv('price_csv/combined_{}'.format(file_name))
import glob
from json import loads
import pandas as pd


def jsonify(log_file):
    with open(log_file, 'r') as f:
        output = []
        lines = f.readlines()
        for line in lines:
            output.append(loads(line))
        return pd.DataFrame(output)


for file in glob.glob("price_logs/*.log"):
    json = jsonify(file)
    file_name = file.split('/')[1].split('.')[0]
    json.to_csv('price_csv/{}.csv'.format(file_name), index=False)


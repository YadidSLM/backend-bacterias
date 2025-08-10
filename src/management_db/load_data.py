import pandas as pd
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '..', 'archivos', 'Sente', 'colomboslt2.txt')

sente = pd.read_table(file_path)

print(sente.head(10))
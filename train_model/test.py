import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('sen_word.csv', sep='\t', names=['text', 'sentiment'], header=None)

print(df)
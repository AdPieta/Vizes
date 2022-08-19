# -*- coding: utf-8 -*-
"""
Open WyScout Json File

@author: AdPieta
"""

import numpy as np
import pandas as pd
import json


def WyscoutJsonOpener(filename):
    
    
    with open (filename, 'r') as f:
        data = json.load(f)
    data = data['events']
    rows = []
    for el in data:
        row = np.array(list(el.values())).reshape(1,-1)
        rows.append(row)
    rows_df = np.concatenate(rows)
    df = pd.DataFrame(rows_df)
    dic = {}
    names = list(data[0].keys())
    for i in range(len(data[0])):
        dic[i] = names[i]
    df = df.rename(columns=dic)
    return df

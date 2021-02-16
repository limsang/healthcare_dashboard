import pandas as pd
import numpy as np

item2item = pd.read_csv('item2vec_recommend_list.csv', dtype=str)

NUMBER_OF_SPLITS = 100
for i, new_df in enumerate(np.array_split(item2item,NUMBER_OF_SPLITS)):
    with open(f"item2item_split_{i}.csv","w") as fo:
            fo.write(new_df.to_csv(index=False, header=False))
import pandas as pd
import numpy as np
set = pd.read_pickle("lexicon.pkl")
set = list(set)
wordID = np.arange(1,len(set)+1)
data = {'wordID': wordID, 'words':set}
df = pd.DataFrame(data=data)
df.set_index('wordID',inplace=True)
df.to_csv("lexicon.csv")
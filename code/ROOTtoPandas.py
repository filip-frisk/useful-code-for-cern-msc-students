""" 
Convert the ROOT file to a pandas dataframe
"""

import uproot
import pandas as pd
import logging 
logging.basicConfig(level=logging.INFO)
logging.info("Importing packages")

PATH = '../data/ntuples-ggFVBF2jet-SF-28Jan'

logging.info("Loading the data with uproot")
file = uproot.open(PATH + '.root')
logging.info("Channels in ROOT file: " + str(file.keys()) )

logging.info("Creating a pandas dataframe of ROOT file")
dfs = []
for key in file.keys():
    channel = file[key]
    df_tmp = channel.arrays(library='pd')
    df_tmp.insert(0, 'label', key)
    dfs.append(df_tmp)
    logging.info(str(key) + " converted to pandas dataframe with shape: " + str(df_tmp.shape))

df = pd.concat(dfs)
logging.info("Pandas dataframe created")

logging.info("Variables of the dataset are: "+ str(df.columns))

logging.info("Saving pandas frame into a pickle file which is faster to load")
df.to_pickle(PATH+'.pkl') 

"""
# load pickle saved data
with open('data/data_ntuples-ggFVBF2jet-SF-28Jan.pkl', 'rb') as file:
    data = pickle.load(file)

df = pd.DataFrame(data)
"""

import pickle
import pandas as pd
import matplotlib.pyplot as plt
from atlasify import atlasify # https://pypi.org/project/atlasify/ 
import logging 
logging.basicConfig(level=logging.INFO)
logging.info("Importing packages, download atlasify package with 'pip install atlasify' if needed")

PATH = '../data/ntuples-ggFVBF2jet-SF-28Jan.pkl'
signal = ['VBF']
background = ['WW', 'Zjets', 'ttbar']
variable = 'ptJ1'
variable_unit = 'GeV'
variable_bound = (0,4*10**5)

logging.info("Loading the data with pickle to create a pandas dataframe")

with open(PATH, 'rb') as file:
    data = pickle.load(file)

df = pd.DataFrame(data)

# Cleaning up weird label scheme used in HWWAnalysis Code not relevant for all
df['label'] = df['label'].str.replace(';1', '').str.replace('HWW_', '')

logging.info("Variables of the dataset are: "+ str(df.columns))


logging.info("Signal selected" + str(signal) + " and background selected: " + str(background) + " for variable: " + variable)


def plot_physical_variable(df, physical_variable, unit, signal, background, bounds):
    plt.figure()
    
    plot_data = []
    plot_weights = []
    plot_labels = []
    
    for bkg in sorted(background, key=lambda x: len(df.loc[df['label'] == x]), reverse=True):
        plot_data.append(df.loc[df['label'] == bkg][physical_variable])
        plot_weights.append(df.loc[df['label'] == bkg]['weight'])
        plot_labels.append(bkg)
    
    
    for sig in signal:
        plot_data.append(df.loc[df['label'] == sig][physical_variable]) 
        plot_weights.append(df.loc[df['label'] == sig]['weight'])
        plot_labels.append(sig)
    
    plt.hist(plot_data, bins=50, label=plot_labels, weights=plot_weights, stacked=True, range=bounds, alpha=0.5, histtype='stepfilled')
    
    plt.xlabel(physical_variable + ' [' + unit + ']')
    plt.ylabel('Events')
    plt.legend(loc='upper right')
    atlasify(subtext = "Internal KTH" + "\n" +"Monte Carlo data, all campaigns" , sub_font_size = 8) 

    ax = plt.gca() # Get the current axis
    ax.ticklabel_format(style='scientific', axis='both', scilimits=(0,0))
    
    plt.show()

logging.info("Plotting this might take some seconds...")

plot_physical_variable(df, variable,variable_unit, signal, background, variable_bound)

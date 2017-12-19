from argparse                import ArgumentParser   
from sklearn.model_selection import train_test_split as tts

import numpy  as np
import pandas as pd

def crossval(dataset):
    d = np.asmatrix(pd.read_csv(dataset).drop([".Name", ".Symbol"], axis=1))
    
    d, l = np.concatenate((d[:,:13], d[:,14:]), axis=1), d[:,13:14]
    
    ##70-30 split, 70% train data and 30% rain data
    s = tts(d, l, test_size=0.3, random_state=0)

    path  = dataset[:dataset.find('data')] + 'data/split/'

    for i in list(zip(['train-data', 'test-data', 'train-labels', 'test-labels'], s)):
        np.savetxt(path + i[0] + '.csv', i[1], delimiter=',')    
    
    return s

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('dataset', type=str, help='Scale Dataset with Binary Labels')
    args = parser.parse_args()

    if args.dataset: crossval(args.dataset)

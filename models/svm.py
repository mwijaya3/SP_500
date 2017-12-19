from sklearn.linear_model import SGDClassifier

import numpy  as np
import pandas as pd

trd = '../data/split/train-data.csv'
trl = '../data/split/train-labels.csv'

ted = '../data/split/test-data.csv'
tel = '../data/split/test-labels.csv'

X = np.asarray(pd.read_csv(trd))
y = np.asarray(pd.read_csv(trl)).reshape(295,)

d = np.asmatrix(pd.read_csv(ted))
l = np.asarray(pd.read_csv(tel))

losses    = ['hinge', 'log']
penalties = ['l1', 'l2', 'elasticnet']

for loss in losses:
    for penalty in penalties:

        results = []

        for i in range(100):

            clf = SGDClassifier(loss=loss, penalty=penalty, shuffle=True)

            clf.fit(X, y)

            c = 0.0

            for u,v in list(zip(d,l)):
                if clf.predict(u) == v: c += 1 

            results.append(c / 127)


        print(loss, penalty)
        print(sum(results) / 100, '\n')



from argparse   import ArgumentParser
from csv        import reader, writer
from sklearn    import preprocessing    as p

import numpy as np

def scale(dataset, binary):

    name = 'binary-' if binary else 'continuous-'

    with open(dataset) as csv_in, open(dataset[:5] + 'scaled/' + name + dataset[5:], 'w') as csv_out:

        w = writer(csv_out)

        categorize = np.vectorize(lambda i: 1 if i > 0 else -1)

        d = np.array(list(reader(csv_in)))

        # Separate Header
        header, d = d[0:1,:], d[1:,:]

        # Separate Identifiers
        ids, d = d[:,:2], d[:,2:].astype("float")
        
        labels = categorize(d[:,13]) if binary else p.scale(d[:,13:14])

        # Recombine Scaled Data
        d = np.concatenate((ids, 
                        p.scale(d[:,:13]), 
                        labels.reshape(labels.size, 1), 
                        # p.scale(d[:,14:18]),
                        # d[:,18:28],
                        p.scale(d[:,14:])), axis=1)
                
        # Restore Header
        d = np.concatenate((header, d))

        for row in d: writer(csv_out).writerow(row)

        return d
            
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-b', '--bin', type=str, help='Scale Dataset with Binary Labels')
    parser.add_argument('-c', '--con', type=str, help='Scale Dataset with Continuous Labels')
    args = parser.parse_args()

    if args.bin: print(args.bin); scale(args.bin, True)
    if args.con: print(args.con); scale(args.con, False)

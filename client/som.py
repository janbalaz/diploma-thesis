import matplotlib.pylab as plt
import pandas as pd
import numpy as np
from time import time
import sompy


def tmp():
    dlen = 200
    Data1 = pd.DataFrame(data=1 * np.random.rand(dlen, 2))
    Data1.values[:, 1] = (Data1.values[:, 0][:, np.newaxis] + .42 * np.random.rand(dlen, 1))[:, 0]

    Data2 = pd.DataFrame(data=1 * np.random.rand(dlen, 2) + 1)
    Data2.values[:, 1] = (-1 * Data2.values[:, 0][:, np.newaxis] + .62 * np.random.rand(dlen, 1))[:, 0]

    Data3 = pd.DataFrame(data=1 * np.random.rand(dlen, 2) + 2)
    Data3.values[:, 1] = (.5 * Data3.values[:, 0][:, np.newaxis] + 1 * np.random.rand(dlen, 1))[:, 0]

    Data4 = pd.DataFrame(data=1 * np.random.rand(dlen, 2) + 3.5)
    Data4.values[:, 1] = (-.1 * Data4.values[:, 0][:, np.newaxis] + .5 * np.random.rand(dlen, 1))[:, 0]

    Data1 = np.concatenate((Data1, Data2, Data3, Data4))

    print(Data1)
    print(len(Data1))
    mapsize = [20, 20]
    som = sompy.SOMFactory.build(Data1, mapsize, mask=None, mapshape='planar', lattice='rect', normalization='var',
                                 initialization='pca', neighborhood='gaussian', training='batch',
                                 name='sompy')
    som.train(n_job=1, verbose='debug')
    a = np.array([str(i) for i in range(800)])
    print(a)
    print(len(a))
    som.data_labels = a

    h = sompy.hitmap.HitMapView(10, 10, 'hitmap', text_size=8, show_text=True)
    h.show(som)


def main():
    tmp()


if __name__ == "__main__":
    main()

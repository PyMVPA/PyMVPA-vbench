import numpy as np
from numpy.random import randn
import random

from mvpa2 import *
import mvpa2.testing as testing

from mvpa2.datasets.base import Dataset
# so that summary binds up
import mvpa2.datasets.miscfx

# Various pre-crafted datasets/variables for testing
# !!! Must not be changed !!!
seed(1)
nsamples0, nfeatures0 = 100, 10000
vb_ds0 = Dataset(randn(nsamples0, nfeatures0),
                 sa={'targets': ['label%d' % x for x in (np.arange(nsamples0) % 5)],
                     'chunks':  np.arange(nsamples0) // 5,
                     },
                 fa={'feature_id' : np.arange(nfeatures0),
                     'feature_group' : np.arange(nfeatures0) // 4,
                     'fancy_id'   : randn(nfeatures0, 4)}
         )

vb_ds0_l2 = vb_ds0[(vb_ds0.T == 'label0') | (vb_ds0.T == 'label1')]
vb_idx0 = np.r_[slice(0,20,2), 20, 30, slice(50, 70)]

#emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*- 
#ex: set sts=4 ts=4 sw=4 noet:
from vbench.benchmark import Benchmark
from datetime import datetime

common_setup = """
from pymvpa_vb_common import *

from mvpa2.datasets.base import Dataset
# so that summary binds up
import mvpa2.datasets.miscfx
nsamples, nfeatures = 100, 10000

seed(1)
"""

setup = common_setup + """
ds = Dataset(np.random.randn(nsamples, nfeatures),
             sa={'targets': ['label%d' % x for x in (np.arange(nsamples) % 5)],
                 'chunks':  np.arange(nsamples) // 5,
                 },
             fa={'feature_id' : np.arange(nfeatures),
                 'fancy_id'   : np.random.randn(nfeatures, 4)}
            )
idx = np.r_[slice(0,20,2), 20, 30, slice(50, 70)]
"""

#----------------------------------------------------------------------
# copying

ds_copy         = Benchmark('ds.copy()', setup)
ds_copy_shallow = Benchmark('ds.copy(deep=False)', setup)

#----------------------------------------------------------------------
# indexing

ds_index_slice_samples_even = Benchmark('ds[::2]', setup)
ds_index_slice_samples_fancy = Benchmark('ds[idx]', setup)

ds_index_slice_even = Benchmark('ds[::2, ::2]', setup)
ds_index_slice_fancy = Benchmark('ds[idx, idx]', setup)

#----------------------------------------------------------------------
# accessing unique values

ds_unique_targets = Benchmark('ds.sa["targets"].unique', setup)
ds_unique_fancy_id = Benchmark('ds.fa["fancy_id"].unique', setup)

#----------------------------------------------------------------------
# misc

ds_summary      = Benchmark('ds.summary()', setup)

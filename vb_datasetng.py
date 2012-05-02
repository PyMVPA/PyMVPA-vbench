#emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*- 
#ex: set sts=4 ts=4 sw=4 noet:
from vbench.benchmark import Benchmark
from datetime import datetime

common_setup = """
from pymvpa_vb_common import *

seed(1)
"""

setup = common_setup + """
"""

#----------------------------------------------------------------------
# copying

ds_copy         = Benchmark('vb_ds0.copy()', setup)
ds_copy_shallow = Benchmark('vb_ds0.copy(deep=False)', setup)

#----------------------------------------------------------------------
# indexing

ds_index_slice_samples_even = Benchmark('vb_ds0[::2]', setup)
ds_index_slice_samples_fancy = Benchmark('vb_ds0[vb_idx0]', setup)

ds_index_slice_even = Benchmark('vb_ds0[::2, ::2]', setup)
ds_index_slice_fancy = Benchmark('vb_ds0[vb_idx0, vb_idx0]', setup)

#----------------------------------------------------------------------
# accessing unique values

ds_unique_targets = Benchmark('vb_ds0.sa["targets"].unique', setup)
ds_unique_fancy_id = Benchmark('vb_ds0.fa["fancy_id"].unique', setup)

#----------------------------------------------------------------------
# misc

ds_summary      = Benchmark('vb_ds0.summary()', setup)


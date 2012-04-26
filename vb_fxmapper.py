#emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*- 
#ex: set sts=4 ts=4 sw=4 noet:
from vbench.benchmark import Benchmark
from datetime import datetime

common_setup = """
from pymvpa_vb_common import *

seed(1)
"""
#----------------------------------------------------------------------
# mappers
setup = common_setup + """
from mvpa2.mappers.fx import mean_group_sample, mean_group_feature
"""

ds_fx_mean_group_sample = Benchmark('mean_group_sample(["targets", "chunks"])(vb_ds0)',
                                    setup)
ds_fx_mean_group_feature = Benchmark('mean_group_feature(["feature_group"])(vb_ds0)',
                                     setup)

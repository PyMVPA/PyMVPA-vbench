#emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*- 
#ex: set sts=4 ts=4 sw=4 noet:
from vbench.benchmark import Benchmark
from mvpa2.clfs.warehouse import clfswh

common_setup = """
from pymvpa_vb_common import *

from mvpa2.clfs.warehouse import clfswh
# from a warehouse to a simple dict with uniquely identifiable objects
clfswh_d = dict([(x.descr, x) for x in clfswh[:]])

seed(1)
"""

#----------------------------------------------------------------------
# classifiers

setup = common_setup + """
"""

# TODO: is it possible to have smth like 'continuation' where
#       two steps are ran in the same env but separately timed?
vb_clfs_binary_train = []
vb_clfs_binary_predict = []

for clf in clfswh['binary']:
    for nf in (2, 1000):                  # for ds with just few and lots of features
        clf_train_str = 'clfswh_d[%r].train(vb_ds0_l2[:,:%d])' % (clf.descr, nf)
        vb_clfs_binary_train.append(
            Benchmark(clf_train_str,
                  setup=setup,
                  name='%s.train(vb_ds0_l2[:,:%d])' % (clf.descr, nf)))
        # and predict on the trailing features of the dataset
        vb_clfs_binary_predict.append(
            Benchmark('clfswh_d[%r].predict(vb_ds0_l2[:,-%d:])' % (clf.descr, nf),
                  setup=setup + "\n" + clf_train_str,
                  name='%s.predict(vb_ds0_l2[:,-%d:])' % (clf.descr, nf)))

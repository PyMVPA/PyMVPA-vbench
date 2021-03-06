from vbench.api import Benchmark, GitRepo
from datetime import datetime
from itertools import chain
import logging
import os, sys

log = logging.getLogger('vb')
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler(sys.stdout))

modules = ['vb_datasetng', 'vb_fxmapper', 'vb_clfs']

log.debug("Loading benchmark modules")
by_module = {}
benchmarks = []

def extract_benchmarks(obj):
    if isinstance(obj, Benchmark):
        return [obj]
    elif isinstance(obj, list) or isinstance(obj, tuple):
        return [x for x in obj if isinstance(x, Benchmark)]
        ## no recursion for now
        #list(chain(*[extract_benchmarks(x) for x in obj]))
    else:
        return []

for modname in modules:
    log.debug("Loading %s" % modname)
    ref = __import__(modname)
    by_module[modname] = list(chain(
        *[extract_benchmarks(x) for x in ref.__dict__.values()]))
    benchmarks.extend(by_module[modname])

for bm in benchmarks:
    assert(bm.name is not None)

log.debug("Initializing settings")
import getpass
import sys

USERNAME = getpass.getuser()

try:
    import ConfigParser

    config = ConfigParser.ConfigParser()
    config.readfp(open(os.path.expanduser('~/.vbenchcfg')))

    REPO_PATH = config.get('setup', 'repo_path')
    REPO_URL = config.get('setup', 'repo_url')
    DB_PATH = config.get('setup', 'db_path')
    TMP_DIR = config.get('setup', 'tmp_dir')
except:
    cur_dir = os.path.dirname(__file__)
    REPO_PATH = os.path.join(cur_dir, 'code')
    REPO_URL = 'git://github.com/PyMVPA/PyMVPA.git'
    DB_PATH = os.path.join(cur_dir, 'db/benchmarks.db')
    TMP_DIR = os.path.join(cur_dir, 'tmp')
    # Assure corresponding directories existence
    for s in (REPO_PATH, os.path.dirname(DB_PATH), TMP_DIR):
        if not os.path.exists(s):
            os.makedirs(s)


PREPARE = """
python setup.py clean
"""
BUILD = """
"""
#python setup.py build_ext --inplace
#"""
dependencies = ['pymvpa_vb_common.py']

# next day after mvpa2 came to existence
START_DATE = datetime(2011, 07, 21)
#START_DATE = datetime(2012, 04, 1)

# Might not even be there and I do not see it used
# repo = GitRepo(REPO_PATH)

RST_BASE = 'source'

# HACK!

#timespan = [datetime(2011, 1, 1), datetime(2012, 1, 1)]

def generate_rst_files(benchmarks):
    import matplotlib as mpl
    mpl.use('Agg')
    import matplotlib.pyplot as plt

    vb_path = os.path.join(RST_BASE, 'vbench')
    fig_base_path = os.path.join(vb_path, 'figures')

    if not os.path.exists(vb_path):
        print 'creating %s' % vb_path
        os.makedirs(vb_path)

    if not os.path.exists(fig_base_path):
        print 'creating %s' % fig_base_path
        os.makedirs(fig_base_path)

    for bmk in benchmarks:
        print 'Generating rst file for %s' % bmk.name
        rst_path = os.path.join(RST_BASE, 'vbench/%s.txt' % bmk.name)

        fig_full_path = os.path.join(fig_base_path, '%s.png' % bmk.name)

        # make the figure
        plt.figure(figsize=(10, 6))
        ax = plt.gca()
        bmk.plot(DB_PATH, ax=ax)

        start, end = ax.get_xlim()

        plt.xlim([start - 30, end + 30])
        plt.savefig(fig_full_path, bbox_inches='tight')
        plt.close('all')

        fig_rel_path = 'vbench/figures/%s.png' % bmk.name
        rst_text = bmk.to_rst(image_path=fig_rel_path)
        with open(rst_path, 'w') as f:
            f.write(rst_text)

    with open(os.path.join(RST_BASE, 'index.rst'), 'w') as f:
        print >> f, """
Performance Benchmarks
======================

These historical benchmark graphs were produced with `vbench
<http://github.com/pydata/vbench>`__.

The ``pymvpa_vb_common`` setup script can be found here_

.. _here: https://github.com/XXX

Produced on a machine with

  - XXX (use lego)
  - Intel Core i7 950 processor
  - (K)ubuntu Linux 12.10
  - Python 2.7.2 64-bit (Enthought Python Distribution 7.1-2)
  - NumPy 1.6.1

.. toctree::
    :hidden:
    :maxdepth: 3
"""
        for modname, mod_bmks in sorted(by_module.items()):
            print >> f, '    vb_%s' % modname
            modpath = os.path.join(RST_BASE, 'vb_%s.rst' % modname)
            with open(modpath, 'w') as mh:
                header = '%s\n%s\n\n' % (modname, '=' * len(modname))
                print >> mh, header

                for bmk in mod_bmks:
                    print >> mh, bmk.name
                    print >> mh, '-' * len(bmk.name)
                    print >> mh, '.. include:: vbench/%s.txt\n' % bmk.name

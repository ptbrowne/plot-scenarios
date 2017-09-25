import pylab as pl
import matplotlib.pyplot as plt

pl.rcParams['figure.figsize'] = (8, 6)

from lcf import parse_lcf
import os.path as osp
import os

ipython = get_ipython()
ipython.magic('matplotlib inline')
ipython.magic("config InlineBackend.figure_format = 'retina'") # png or retina'

global dirname
global all_files
global noise

def set_dirname(new_dirname):
    global dirname, all_files, noise
    dirname = new_dirname
    all_files = os.listdir(dirname)
    noise = parse_lcf(get_file('bruit.chiq'))

def get_file(filter):
    return osp.join(dirname, [f for f in all_files if filter in f][0])

def compare(slug1, slug2):
    f1 = get_file(slug1)
    f2 = get_file(slug2)
    data = parse_lcf(f1)
    data2 = parse_lcf(f2) 
    (data['fit'] - data2['fit']).plot()
    noise['chi_re'].plot(title='%s vs %s' % (slug1, slug2))
    plt.figure()

def plot_fit(slug):
    d = parse_lcf(get_file(slug))
    d['data'].plot()
    d['fit'].plot(style=['--'], title='%s' % slug)
    plt.figure()

def print_available():
    print 'Available data: \n%s' % '\n'.join([f for f in all_files if f.endswith('.lcf')])

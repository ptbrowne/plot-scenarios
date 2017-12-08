from __future__ import print_function

g1 = set(globals())

import pylab as pl
import matplotlib.pyplot as plt

pl.rcParams['figure.figsize'] = (10, 8)

from lcf import parse_lcf
import os.path as osp
import os

from IPython.display import display, Markdown, Latex, HTML
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

ipython = get_ipython()
ipython.magic('matplotlib inline')
ipython.magic("config InlineBackend.figure_format = 'png'") # png or retina'

global dirname
global all_files
global noise

def set_style():
    plt.style.use(['seaborn-white', 'fivethirtyeight', './maureen.mplstyle'])

def set_dirname(new_dirname):
    global dirname, all_files, noise
    dirname = new_dirname
    all_files = os.listdir(dirname)
    noise = parse_lcf(get_file('bruit.chiq'))

def get_file(filter, ext=None):
    return osp.join(dirname, [f for f in all_files if filter in f and (ext is None or f.endswith(ext))][0])

def compare(slug1, slug2, res=False):
    f1 = get_file(slug1, 'lcf')
    f2 = get_file(slug2, 'lcf')
    data = parse_lcf(f1)
    data2 = parse_lcf(f2) 
    delta = (data['fit'] - data2['fit']).plot()
    noise['chi_re'].plot(title='%s - %s vs %s' % (dirname.split('/')[-1], slug1, slug2))

    legend = ['delta', 'noise']
    if res:
        res1 = data['residual'].abs().plot()
        res2 = data2['residual'].abs().plot()
        legend += ['res %s' % slug1, 'res %s' % slug2]

    plt.legend(legend)
    plt.figure()


def plot_fit(slug):
    d = parse_lcf(get_file(slug))
    d['data'].plot()
    d['fit'].plot(style=['--'], color=['#FF0000'], title='%s - %s' % (dirname.split('/')[-1], slug))
    plt.figure()


def get_available():
    return [f for f in all_files if f.endswith('.lcf')]


def show_available():
    display(Markdown('Available data: \n\n%s' % '\n'.join(['* `%s`' % f for f in get_available()])))


def add_hide():
    display(HTML('''<script>
        var code_show=false; //true -> show code at first

        function code_toggle() {
            $('div.prompt').hide(); // always hide prompt

            if (code_show){
                $('div.input').hide();
            } else {
                $('div.input').show();
            }
            code_show = !code_show
        }
        $( document ).ready(code_toggle);
    </script><a href="javascript:code_toggle()">[Toggle Code]</a>'''))

def show_globals():
    new_globals = set(globals()) - g1 - set([osp, pl])
    display(Markdown('Available globals: %s' % ','.join(('`%s`' % g for g in new_globals))))
    
set_style()
add_hide()
show_globals()

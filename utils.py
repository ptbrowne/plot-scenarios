g1 = set(globals())

import pylab as pl
import matplotlib.pyplot as plt

pl.rcParams['figure.figsize'] = (10, 8)

from lcf import parse_lcf
import os.path as osp
import os

from IPython.display import display, Markdown, Latex, HTML

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
    d['fit'].plot(style=['--'], color=['C3'], title='%s' % slug)
    plt.figure()

def show_available():
    display(Markdown('Available data: \n\n%s' % '\n'.join(['* `%s`' % f for f in all_files if f.endswith('.lcf')])))


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

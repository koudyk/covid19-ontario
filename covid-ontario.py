# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.5.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Visualizing COVID-19 cases in Ontario
# By Kendra Oudyk

# +
import pandas as pd 
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.widgets import CheckButtons
import requests
from io import StringIO 
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters() 

# %matplotlib inline

# -

# ## Load the data from the data.ontario.ca website
# Read it into a pandas dataframe, which is like a table)

data_url = 'https://data.ontario.ca/dataset/f4112442-bdc8-45d2-be3c-12efae72fb27/resource/455fd63b-603d-4608-8216-7d8647f43350/download/conposcovidloc.csv'
response = requests.get(data_url)
csv_string = response.content.decode('utf-8')
cases = pd.read_csv(StringIO(csv_string))
cases.head(4) # see the first few columns

# ## Define the population of each phu

phu_populations =   {'Algoma Public Health Unit': 114434,
                     'Brant County Health Unit': 155203,
                     'Chatham-Kent Health Unit': 106317,
                     'Durham Region Health Department': 712402,
                     'Eastern Ontario Health Unit': 208711,
                     'Grey Bruce Health Unit': 169884,
                     'Haldimand-Norfolk Health Unit': 114081,
                     'Haliburton, Kawartha, Pine Ridge District Health Unit': 188937,
                     'Halton Region Health Department': 619087,
                     'Hamilton Public Health Services': 592163,
                     'Hastings and Prince Edward Counties Health Unit': 168493,
                     'Huron Perth District Health Unit': 139757,
                     'Kingston, Frontenac and Lennox & Addington Public Health': 212719,
                     'Lambton Public Health': 130964,
                     'Leeds, Grenville and Lanark District Health Unit': 173170,
                     'Middlesex-London Health Unit': 507524,
                     'Niagara Region Public Health Department': 472485,
                     'North Bay Parry Sound District Health Unit': 129752,
                     'Northwestern Health Unit': 87675,
                     'Ottawa Public Health': 1054656,
                     'Peel Public Health': 1605952,
                     'Peterborough Public Health': 147977,
                     'Porcupine Health Unit': 83441,
                     'Region of Waterloo, Public Health': 584361,
                     'Renfrew County and District Health Unit': 108631,
                     'Simcoe Muskoka District Health Unit': 599589,
                     'Southwestern Public Health': 211498,
                     'Sudbury & District Health Unit': 199023,
                     'Thunder Bay District Health Unit': 149960,
                     'Timiskaming Health Unit': 32689,
                     'Toronto Public Health': 3120358,
                     'Wellington-Dufferin-Guelph Public Health': 311908,
                     'Windsor-Essex County Health Unit': 424830,
                     'York Region Public Health Services': 1225797}


# ## Timeline
# ### turn the dates into integers, which are easier to deal with
#

cases['Date'] = cases['Accurate_Episode_Date']
cases = cases.dropna(subset=['Date'])
cases['Date'] = [int(str(s).replace('-', '')) for s in cases['Date']]


# ### get a list of all dates until today
# We want to begin at Jan 1, 2020, but we're looking at cases in 14-day periods, so we'll start the timeline 14 days before (inclusive of) Jan 1.  

d1 = datetime.date(2019,12,18)
d2 = datetime.date.today()
datetimes = [(d1 + datetime.timedelta(days=x)) for x in range((d2-d1).days + 1)]
dates = [int(str(s).replace('-', '')) for s in datetimes]

# ## Get the relevant data 
# I.e., get the data for each PHU and day from the *cases* dataframe, and store it in a new dataframe called *data*. *data* has a row for each day, and a column for each PHU
#

# +
# initialize dataframe
data = pd.DataFrame()
data['Date'] = dates

days_in_range = 14
phus = np.unique(cases['Reporting_PHU'])  
for phu in phus:
    population = int(phu_populations[phu])
    
    # select the cases for the given PHU
    phu_cases = cases[cases['Reporting_PHU'] == phu]
    
    daily_rate = []
    for n, date in enumerate(dates):
        # select the cases for the given date, in the given PHU
        begin_date = date
        i_end_date = np.min([len(dates) - 1, n + days_in_range])
        end_date = dates[i_end_date]
        phu_cases_in_current_dates = phu_cases[phu_cases['Date'].\
                                               between(begin_date, end_date)]
        
        # calculate the infection rate
        n_cases = len(phu_cases_in_current_dates)
        rate = n_cases / population * 10000
        daily_rate.append(rate)
    data[phu] = daily_rate
    
# remove last 14 days
data = data[:-days_in_range]
datetimes = datetimes[:-days_in_range]
    
data.head(4) # visualize the first few rows
# -

# ## Visualize the timeline for each PHU in a separate plot

# +
# visualize
matplotlib.rc('font', size = 22)
matplotlib.rc('figure', max_open_warning = 0)

ymax = np.max(data.loc[:, data.columns != 'Date'].values) + 2
ymin = - .03
linewidth = 4

alpha = .1
days = 14
for phu in phus:
    
    p = data[phu]
    t = datetimes
    
    fig, ax = plt.subplots(figsize=(20, 10))
    
    ax.plot(datetimes, p, color='black', linewidth=linewidth)
    
    ax.axhspan(ymin, 0.05*days, facecolor='blue', alpha=alpha)
    ax.axhspan(0.05*days, 0.1*days, facecolor='green', alpha=alpha)
    ax.axhspan(0.1*days, 0.25*days, facecolor='yellow', alpha=alpha)
    ax.axhspan(0.25*days, 0.5*days, facecolor='darkorange', alpha=alpha)
    ax.axhspan(0.5*days, ymax, facecolor='red', alpha=alpha)
    
    plt.ylim([ymin, ymax])
    plt.xlabel('Date')
    plt.ylabel('# infected per 10,000\nin past 14 days')
    plt.title('%s' %phu)
# -
# ## Visualize the timelines for all PHUs on the same interactive plot
# *Color/line scheme A*

# +
# This code was based on https://stackoverflow.com/questions/31410043/hiding-lines-after-showing-a-pyplot-figure/31417070

# %matplotlib notebook

matplotlib.rc('font', size = 14)

linewidth=4
alpha=.1
ymax = np.max(data.loc[:, data.columns != 'Date'].values) + 2
ymin = - .2
days = 14

def main():
    
    NUM_COLORS = 34
    LINE_STYLES = ['solid', 'dashed', 'dashdot', 'dotted']
    COLORS = ['DarkRed', 'red', 'DarkKhaki', 'Lime', 'Green', 'DeepSkyBlue', 'Blue', 'Violet', 'black']
    LINE_COLORS = []
    for color in COLORS:
        for style in LINE_STYLES:
            LINE_COLORS.append(color)
    NUM_STYLES = len(LINE_STYLES)
    cm = plt.get_cmap('gist_rainbow')
    cm = plt.get_cmap('nipy_spectral')
    
    x = datetimes
    fig, ax = plt.subplots(figsize=(14,10))
    ax.set_xlim(datetimes[0], datetimes[-1])
    ax.axhspan(ymin, 0.05*days, facecolor='blue', alpha=alpha)
    ax.axhspan(0.05*days, 0.1*days, facecolor='green', alpha=alpha)
    ax.axhspan(0.1*days, 0.25*days, facecolor='yellow', alpha=alpha)
    ax.axhspan(0.25*days, 0.5*days, facecolor='darkorange', alpha=alpha)
    ax.axhspan(0.5*days, ymax, facecolor='red', alpha=alpha)
    
    for i, phu in enumerate(phus[0:]):
        y = data[phu]
        #color = cm(i//NUM_STYLES*float(NUM_STYLES)/NUM_COLORS)
        #color = LINE_COLORS[i]
        #linestyle = LINE_STYLES[i%NUM_STYLES]
        #ax.plot(x, y, label=phu, color=color, linestyle=linestyle)
        ax.plot(x, y, label=phu)

    ax.legend(loc='best', bbox_to_anchor=(0.01, 1),
              ncol=2, borderaxespad=0, title=' ',#title='Regional public health unit',
              frameon=False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_ylim(ymin, ymax)
    ax.set_ylabel('# infected cases per 10,000')
    ax.set_xlabel('Date')

    fig.subplots_adjust(top=0.4)
    fig.suptitle('Left-click on a PHU name to show/hide it   |   Right-click to hide all   |   Middle-click to show all',
                 va='top', size='large', y=1)

    leg = interactive_legend()
    return fig, ax, leg

def interactive_legend(ax=None):
    if ax is None:
        ax = plt.gca()
    if ax.legend_ is None:
        ax.legend()

    return InteractiveLegend(ax.get_legend())

class InteractiveLegend(object):
    def __init__(self, legend):
        self.legend = legend
        self.fig = legend.axes.figure

        self.lookup_artist, self.lookup_handle = self._build_lookups(legend)
        self._setup_connections()

        self.update()

    def _setup_connections(self):
        for artist in self.legend.texts + self.legend.legendHandles:
            artist.set_picker(10) # 10 points tolerance

        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)

    def _build_lookups(self, legend):
        labels = [t.get_text() for t in legend.texts]
        handles = legend.legendHandles
        label2handle = dict(zip(labels, handles))
        handle2text = dict(zip(handles, legend.texts))

        lookup_artist = {}
        lookup_handle = {}
        for artist in legend.axes.get_children():
            if artist.get_label() in labels:
                handle = label2handle[artist.get_label()]
                lookup_handle[artist] = handle
                lookup_artist[handle] = artist
                lookup_artist[handle2text[handle]] = artist

        lookup_handle.update(zip(handles, handles))
        lookup_handle.update(zip(legend.texts, handles))

        return lookup_artist, lookup_handle

    def on_pick(self, event):
        handle = event.artist
        if handle in self.lookup_artist:

            artist = self.lookup_artist[handle]
            artist.set_visible(not artist.get_visible())
            self.update()

    def on_click(self, event):
        if event.button == 3:
            visible = False
        elif event.button == 2:
            visible = True
        else:
            return

        for artist in self.lookup_artist.values():
            artist.set_visible(visible)
        self.update()

    def update(self):
        for artist in self.lookup_artist.values():
            handle = self.lookup_handle[artist]
            if artist.get_visible():
                handle.set_visible(True)
            else:
                handle.set_visible(False)
        self.fig.canvas.draw()

    def show(self):
        plt.show()

if __name__ == '__main__':
    fig, ax, leg = main()
    plt.tight_layout()
    plt.show()
# -

# ## Visualize the timelines for all PHUs on the same interactive plot
# *Color/line scheme B*

# +
# This code was based on https://stackoverflow.com/questions/31410043/hiding-lines-after-showing-a-pyplot-figure/31417070

# %matplotlib notebook

matplotlib.rc('font', size = 14)

linewidth=4
alpha=.1
ymax = np.max(data.loc[:, data.columns != 'Date'].values) + 2
ymin = - .2
days = 14

def main():
    
    NUM_COLORS = 34
    LINE_STYLES = ['solid', 'dashed', 'dashdot', 'dotted']
    COLORS = ['DarkRed', 'red', 'DarkKhaki', 'Lime', 'Green', 'DeepSkyBlue', 'Blue', 'Violet', 'black']
    LINE_COLORS = []
    for color in COLORS:
        for style in LINE_STYLES:
            LINE_COLORS.append(color)
    NUM_STYLES = len(LINE_STYLES)
    cm = plt.get_cmap('gist_rainbow')
    cm = plt.get_cmap('nipy_spectral')
    
    x = datetimes
            
    fig, ax = plt.subplots(figsize=(14,10))
    ax.set_xlim(datetimes[0], datetimes[-1])
    ax.axhspan(ymin, 0.05*days, facecolor='blue', alpha=alpha)
    ax.axhspan(0.05*days, 0.1*days, facecolor='green', alpha=alpha)
    ax.axhspan(0.1*days, 0.25*days, facecolor='yellow', alpha=alpha)
    ax.axhspan(0.25*days, 0.5*days, facecolor='darkorange', alpha=alpha)
    ax.axhspan(0.5*days, ymax, facecolor='red', alpha=alpha)
    
    for i, phu in enumerate(phus[0:]):
        y = data[phu]
        #color = cm(i//NUM_STYLES*float(NUM_STYLES)/NUM_COLORS)
        color = LINE_COLORS[i]
        linestyle = LINE_STYLES[i%NUM_STYLES]
        ax.plot(x, y, label=phu, color=color, linestyle=linestyle)

    ax.legend(loc='best', bbox_to_anchor=(0.01, 1),
              ncol=2, borderaxespad=0, title=' ',#title='Regional public health unit',
              frameon=False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_ylim(ymin, ymax)
    ax.set_ylabel('# infected cases per 10,000')
    ax.set_xlabel('Date')

    fig.subplots_adjust(top=0.4)
    fig.suptitle('Left-click on a PHU name to show/hide it   |   Right-click to hide all   |   Middle-click to show all',
                 va='top', size='large', y=1)

    leg = interactive_legend()
    def line_hover(event):
        for line in ax.get_lines():
            if line.contains(event)[0]:
                print(line.get_label())
    fig.canvas.mpl_connect('motion_notify_event', line_hover) 
    return fig, ax, leg

def interactive_legend(ax=None):
    if ax is None:
        ax = plt.gca()
    if ax.legend_ is None:
        ax.legend()

    return InteractiveLegend(ax.get_legend())

class InteractiveLegend(object):
    def __init__(self, legend):
        self.legend = legend
        self.fig = legend.axes.figure

        self.lookup_artist, self.lookup_handle = self._build_lookups(legend)
        self._setup_connections()

        self.update()

    def _setup_connections(self):
        for artist in self.legend.texts + self.legend.legendHandles:
            artist.set_picker(10) # 10 points tolerance

        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)

    def _build_lookups(self, legend):
        labels = [t.get_text() for t in legend.texts]
        handles = legend.legendHandles
        label2handle = dict(zip(labels, handles))
        handle2text = dict(zip(handles, legend.texts))

        lookup_artist = {}
        lookup_handle = {}
        for artist in legend.axes.get_children():
            if artist.get_label() in labels:
                handle = label2handle[artist.get_label()]
                lookup_handle[artist] = handle
                lookup_artist[handle] = artist
                lookup_artist[handle2text[handle]] = artist

        lookup_handle.update(zip(handles, handles))
        lookup_handle.update(zip(legend.texts, handles))

        return lookup_artist, lookup_handle

    def on_pick(self, event):
        handle = event.artist
        if handle in self.lookup_artist:

            artist = self.lookup_artist[handle]
            artist.set_visible(not artist.get_visible())
            self.update()

    def on_click(self, event):
        if event.button == 3:
            visible = False
        elif event.button == 2:
            visible = True
        else:
            return

        for artist in self.lookup_artist.values():
            artist.set_visible(visible)
        self.update()

    def update(self):
        for artist in self.lookup_artist.values():
            handle = self.lookup_handle[artist]
            if artist.get_visible():
                handle.set_visible(True)
            else:
                handle.set_visible(False)
        self.fig.canvas.draw()

    def show(self):
        plt.show()
        

if __name__ == '__main__':
    fig, ax, leg = main()
    plt.tight_layout()
    
    plt.show()
# -


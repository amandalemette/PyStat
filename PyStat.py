import sys
sys.setrecursionlimit(5000)

# Importing Libraries *----------------------------------------------------*
from tkinter import *
from tkinter import (filedialog, scrolledtext, messagebox)
import tkinter.messagebox
import tkinter.ttk as ttk
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt # pylab

#--------------------------------------------------------------------------*
fnlist = ['Arial','Times','Symbol','Verdana','Courier']
fn = fnlist[4]  # Font used

# Auxiliary Functions *----------------------------------------------------*
def selection():
    global n,nr,data,checkdata,dataH
    file = filedialog.askopenfilename()
    if not file.endswith('.csv'):
            messagebox.showinfo("Error in load file", "Filetype must be a .csv")
    else:
            data = pd.read_csv(file) # , sep = ";"
            btn2 = Button(window, text="File read") 
            btn2.grid(column=4, row=1)
            n = data.shape[1] # numero de colunas = parametros
            nr = data.shape[0] # numero de linhas
            dataH = data # save dataframe
            data = data.values # data is a numpy array
            checkdata = 1
#--------------------------------------------------------------------------*
def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):
    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))

    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=["white","white"],
                     threshold=None, **textkw):

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts

def statis():
    global n,nr,data,checkdata,cor
    
    if (checkdata == 0):
        messagebox.showinfo('Atention!!!', 'Please, select the csv.file to run this option.')
        return
        
    def opfile():
        global fileR
        fileR = open('Results.txt', 'w')
        fileR.write('==========================================\n')
        fileR.write('|                   RESULTS               |\n')
        fileR.write('==========================================\n')
        fileR.write('\n')
        fileR.write('\n')
        fileR.write('Number of datasets:  {0}\n' .format(n))
        fileR.write('Datasets amount   :  {0}\n' .format(nr))
        return
    
    if CheckVar1.get() == 1 and (CheckVar2.get() == 1 or 
                                 CheckVar3.get() == 1 or
                                 CheckVar4.get() == 1 or
                                 CheckVar5.get() == 1 or
                                 CheckVar6.get() == 1 or
                                 CheckVar7.get() == 1):
        messagebox.showinfo('Atention!!!', 'Please, select All or the other options.')
        
    elif CheckVar1.get() == 1:

        opfile()
        average = dataH.mean().values
        median = dataH.median().values
        var = dataH.var().values
        stand = dataH.std().values
        cov = dataH.cov().values
        cor = dataH.corr().values

        fileR.write('\nAverage:\n')
        for i in range(n):
            fileR.write("{0:+.5e}\n".format(average[i]))
                
        fileR.write('\nMedian:\n')
        for i in range(n):
            fileR.write("{0:+.5e}\n".format(median[i]))
            
        fileR.write('\nStandard deviation:\n')
        for i in range(n):
            fileR.write("{0:+.5e}\n".format(stand[i]))    
            
        fileR.write('\nVariance:\n')
        for i in range(n):
            fileR.write("{0:+.5e}\n".format(var[i]))
            
        fileR.write('\nCorrelation:\n')
        for i in range(n): # linha
            if i != 0:
                fileR.write("\n")
            for k in range(n): # coluna
                fileR.write("{0:+.5e} ".format(cor[i,k]))
                
                
        fileR.write('\n\nCovariation:\n')
        for i in range(n): # linha
            if i != 0:
                fileR.write("\n")
            for k in range(n): # coluna
                fileR.write("{0:+.5e} ".format(cov[i,k]))  
                
    else:

        opfile()
        if CheckVar2.get() == 1: # Average
            average = np.zeros(n)
            for i in range(n):
                average[i] = np.mean(data[:,i])
            
            fileR.write('\nAverage:\n')
            for i in range(n):
                fileR.write("{0:+.5e}\n".format(average[i]))


        if CheckVar3.get() == 1: #"Median"
            median = np.zeros(n)
            for i in range(n):
                median[i] = np.median(data[:,i])
                
            fileR.write('\nMedian:\n')
            for i in range(n):
                fileR.write("{0:+.5e}\n".format(median[i]))
            
        if CheckVar4.get() == 1: #"Standard deviation"
            stand = np.zeros(n)
            for i in range(n):
                stand[i] = data[:,i].std()
            
            fileR.write('\nStandard deviation:\n')
            for i in range(n):
                fileR.write("{0:+.5e}\n".format(stand[i]))   
            
        if CheckVar5.get() == 1:  #"Variance"
            var = np.zeros(n)
            for i in range(n):
                var[i] = data[:,i].var()
             
            fileR.write('\nVariance:\n')
            for i in range(n):
                fileR.write("{0:+.5e}\n".format(var[i]))
         
        if CheckVar6.get() == 1:  #"Correlation matrix" 
            cor = np.zeros((n,n)) 
            for k in range(n):
                for j in range(n):
                    cor[k,j]=correlation(data[:,k],data[:,j])  
            
            fileR.write('\nCorrelation:\n')
            for i in range(n): # linha
                if i != 0:
                    fileR.write("\n")
                for k in range(n): # coluna
                    fileR.write("{0:+.5e} ".format(cor[i,k]))
            
        if CheckVar7.get() == 1:  #"Covariation matrix"
            cov = np.zeros((n,n))  
            for k in range(n):
                for j in range(n):
                    cov[k,j]=covariance(data[:,k],data[:,j])
            
            fileR.write('\n\nCovariation:\n')
            for i in range(n): # linha
                if i != 0:
                    fileR.write("\n")
                for k in range(n): # coluna
                    fileR.write("{0:+.5e} ".format(cov[i,k]))  
                
    fileR.close()
    
    file = open("Results.txt")
    dados = file.read()
    file.close()    
    window = Tk()
    window.title("Results")
    txt = scrolledtext.ScrolledText(window)
    txt.insert(INSERT,dados)
    txt.grid(column=0,row=0)
    window.mainloop()   
#--------------------------------------------------------------------------*
def plotcorr():
    global cor,dataH
    Tit = dataH.columns.values
    cm = combo.get()
    fig, ax = plt.subplots()
    im, cbar = heatmap(cor, Tit, Tit, ax=ax,
                   cmap=cm,
                   vmin=-1, vmax=1,
                   cbarlabel="Correlation Coefficient")
    texts = annotate_heatmap(im, valfmt="{x:.2f}")

    ax.set_xticks(np.arange(len(Tit)))
    ax.set_yticks(np.arange(len(Tit)))

    ax.set_xticklabels(Tit)
    ax.set_yticklabels(Tit)
    fig.tight_layout()
    ax.get_figure().savefig('graph_correlationmatrix.png')
    plt.show()

    
#--------------------------------------------------------------------------*
def plothist():
    global dataH,n

    dataH.hist(grid=False)
    plt.tight_layout()
    plt.savefig("graph_histogram.png")
    plt.show()
    
#--------------------------------------------------------------------------*
# Main Program *-----------------------------------------------------------*
#--------------------------------------------------------------------------*

global n,nr,data,checkdata, fileR, dataH, cor
window = Tk()
window.title("Ecfio\N{REGISTERED SIGN} :: PyStat")

checkdata = 0
ini = 0
window.geometry('420x450') # window size Width#Height
lbl0 = Label(window, text="")
lbl0.grid(column=0, row=ini)

ini = ini+1
lbl = Label(window, text="Load csv file", font=(fn,12)) #font=("Arial Bold", 20))
lbl.grid(column=2, row=ini)

lbl2 = Label(window, text="")
lbl2.grid(column=3, row=ini)

btn = Button(window, text="Select", command=selection) 
btn.grid(column=4, row=ini)

ini = ini+1
lbl0 = Label(window, text="")
lbl0.grid(column=0, row=ini)

ini = ini+1
lbl0 = Label(window, text=" Select the analyzes ", font=(fn, 14,'bold'))
lbl0.grid(columnspan=5, row=ini)

ini = ini+1
lbl0 = Label(window, text="")
lbl0.grid(column=0, row=ini)

CheckVar1 = IntVar()
CheckVar2 = IntVar()
CheckVar3 = IntVar()
CheckVar4 = IntVar()
CheckVar5 = IntVar()
CheckVar6 = IntVar()
CheckVar7 = IntVar()
CheckVar8 = IntVar()
fft = 12
c1 = Checkbutton(window, text="All", variable=CheckVar1, onvalue = 1, offvalue = 0) #, height=5, width = 20)
c2 = Checkbutton(window, text="Average", variable=CheckVar2, onvalue = 1, offvalue = 0) #, height=5, width = 20)
c3 = Checkbutton(window, text="Median", variable=CheckVar3, onvalue = 1, offvalue = 0) #, height=5, width = 20)
c4 = Checkbutton(window, text="Standard deviation", variable=CheckVar4, onvalue = 1, offvalue = 0) #, height=5, width = 20)
c5 = Checkbutton(window, text="Variance", variable=CheckVar5, onvalue = 1, offvalue = 0) #, height=5, width = 20)
c6 = Checkbutton(window, text="Correlation matrix", variable=CheckVar6, onvalue = 1, offvalue = 0) #, height=5, width = 20)
c7 = Checkbutton(window, text="Covariation matrix", variable=CheckVar7, onvalue = 1, offvalue = 0) #, height=5, width = 20)

ini = ini+1
col = 1
c1.grid(column=col, row=ini, sticky='w')
c2.grid(column=col, row=ini+1, sticky='w')
c3.grid(column=col, row=ini+2, sticky='w')
c4.grid(column=col, row=ini+3, sticky='w')
c5.grid(column=col, row=ini+4, sticky='w')
c6.grid(column=col, row=ini+5, sticky='w')
c7.grid(column=col, row=ini+6, sticky='w')

ini = ini+7
btn0 = Button(window, text="Calc", command = statis)
btn0.grid(column=4, row=ini-4) 

############################
ini = ini+1
lbl0 = Label(window, text="")
lbl0.grid(column=0, row=ini)

ini = ini+1
lbl0 = Label(window, text=" Plot ", font=(fn, 14,'bold'))
lbl0.grid(columnspan=5, row=ini)

ini = ini+1
lbl0 = Label(window, text="")
lbl0.grid(column=0, row=ini)

ini = ini+1
lbl0 = Label(window, text="Select the colormap", font=(fn, 12))
lbl0.grid(column=1, row=ini)

combo = ttk.Combobox(window, width=15)
combo['values']= ('twilight', 'twilight_shifted', 'hsv','viridis', 'plasma', 'inferno', 'magma', 'cividis','Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn','coolwarm')
combo.current(1) #set the selected item
combo.grid(column=2, row=ini)

ini = ini+1
lbl0 = Label(window, text="Correlation Graph", font=(fn, 12))
lbl0.grid(columnspan=3, row=ini, sticky = E)

btn0 = Button(window, text="Plot", command = plotcorr)
btn0.grid(column=4, row=ini) 

##############################
ini = ini+1
lbl0 = Label(window, text="Histogram", font=(fn, 12))
lbl0.grid(columnspan=3, row=ini, sticky= E)

btn0 = Button(window, text="Plot", command = plothist)
btn0.grid(column=4, row=ini)

ini = ini+1
lbl0 = Label(window, text="")
lbl0.grid(column=0, row=ini)

window.mainloop()
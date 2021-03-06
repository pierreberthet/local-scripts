import numpy as np
import json
import matplotlib
#matplotlib.use('Agg')
import pylab as pl
import sys
import pprint as pp
import difflib
#from difflib_data import *
# Plot the different figures for the merged spikes and voltages recordings.
# This file, as the MergeSpikefiles.py should be one level up than Test/..., the output of a simulation.
import glob
import scipy.stats as stats

def get_weights(folder):
    fparam = folder+'Test/Parameters/simulation_parameters.json'
    f = open(fparam, 'r')
    params = json.load(f)
    
    params['multi_n']+=1
    
    source_rew= folder+params['rewards_multi_fn']+'_'
    rewards = np.zeros((params['multi_n'], params['n_iterations']))
    
    for i in xrange(params['multi_n']):
        rewards[i] = np.loadtxt(source_rew+str(i))
    
    
    #for i in xrange(lend1):
    #    for j in xrange(params['n_actions']):
    #        wd1_m[i,j] = np.mean(wd1[:,i,j])
    #        wd1_std[i,j] = np.std(wd1[:,i,j])
    #        wd2_m[i,j] = np.mean(wd2[:,i,j])
    #        wd2_std[i,j] = np.std(wd2[:,i,j])
    #for i in xrange(lenrp):
    #    for j in xrange(params['n_actions']*params['n_states']):
    #        wrp_m[i,j] = np.mean(wrp[:,i,j])
    #        wrp_std[i,j] = np.std(wrp[:,i,j])

    return rewards

def stars(p):
    if p < 0.0001:
        return "****"
    elif (p < 0.001):
        return "***"
    elif (p < 0.01):
        return "**"
    elif (p < 0.05):
        return "*"
    else:
        return "-"





######################################
######################################


if len(sys.argv)<2: 
    print "Need 2 folders for comparison"
    pass

fname ={}

for i in xrange(1,len(sys.argv)):
    fname[i-1] = sys.argv[i]+'/'

params={}

for i in xrange(len(fname)):
    params[i]=json.load(open(fname[i]+'Test/Parameters/simulation_parameters.json'))


#print 'Do the simulations match? ',  params[:]['n_recordings']==params[:]['n_recordings']

#diff = difflib.ndiff(open(fparam1,'r').readlines(), open(fparam2,'r').readlines())
#print ''.join(diff)

rew = {}

for i in xrange(len(fname)):
    rew[i] = get_weights(fname[i])
start = 4
startpd = 11

#shift = start*params[1]['block_len']*params[1]['t_iteration']/params[1]['resolution']
#shift_rew = start*params[1]['block_len']
#shiftpd = startpd*params[1]['block_len']*params[1]['t_iteration']/params[1]['resolution']
#shiftpd_rew = startpd*params[1]['block_len']
p = len(fname)-1
perf = {}
for i in xrange(len(fname)):
    #perf[i] = np.zeros(params[1]['multi_n'], dtype=float)
    perf[i] = []
j=0
#for i in xrange(shift_rew, params1['n_iterations']):
#    r1[j]=sum(rewa[:,i])
#    r2[j]=sum(rewb[:,i])
#    j+=1

#for i in xrange(start, params1['n_blocks']):
for f in xrange(len(fname)-1):
    j=0
    for i in xrange(params[f]['multi_n']):
        for q in xrange(start, params[f]['n_blocks']):
            perf[f]= np.append(perf[f],rew[f][i,q*params[f]['block_len']-6:q*params[f]['block_len']-1])
        j+=1
j=0
for i in xrange(params[p]['multi_n']):
    for q in xrange(startpd, params[p]['n_blocks']):
        perf[p] = np.append(perf[p], rew[p][i,q*params[p]['block_len']-6:q*params[p]['block_len']-1])
    j+=1


#for f in xrange(len(fname)-1):
#    perf[f] = perf[f]/((params[f]['n_blocks']-start)*5.)
#
#perf[p] = perf[p]/((params[p]['n_blocks']-startpd)*5.)


fig = pl.figure()
ax = fig.add_subplot(111)
ax.hlines(1./3., 0, 8, colors='gray', linestyles='dotted', label='chance')
print 'PERF'
for i in xrange(len(fname)):
    print  fname[i], 'mean= ',  np.mean(perf[i]), 'SD=', np.std(perf[i])
    for j in xrange(len(fname)):
        print fname[j], 'mean ',  np.mean(perf[j]), 'SD=', np.std(perf[j])
        print 'T-TEST: ', stats.ttest_ind(perf[i],perf[j])
        print 'F-TEST: ', stats.f_oneway(perf[i], perf[j])
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print '\n'
    print 'F-TEST: ', stats.f_oneway(perf[i], [.33333])
    print '+++++++++++++++++++++++++++++++'
print '\n'
print '\n'

bp = ax.boxplot([perf[v] for v in perf.iterkeys()])



ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
ax.tick_params(axis='x', direction='out')
ax.tick_params(axis='y', length=0)


ax.grid(axis='y', color="0.9", linestyle='-', linewidth=1)
ax.set_axisbelow(True)




# colors, as before
import brewer2mpl
bmap = brewer2mpl.get_map('Set2', 'qualitative', len(fname))
colors = bmap.mpl_colors

for i in range(0, len(bp['boxes'])):
    bp['boxes'][i].set_color(colors[i])
    # we have two whiskers!
    bp['whiskers'][i*2].set_color(colors[i])
    bp['whiskers'][i*2 + 1].set_color(colors[i])
    bp['whiskers'][i*2].set_linewidth(2)
    bp['whiskers'][i*2 + 1].set_linewidth(2)
    # top and bottom fliers
    # (set allows us to set many parameters at once)
    bp['fliers'][i * 2].set(markerfacecolor=colors[i],
        marker='o', alpha=0.75, markersize=6,
        markeredgecolor='none')
    bp['fliers'][i * 2 + 1].set(markerfacecolor=colors[i],
        marker='o', alpha=0.75, markersize=6,
        markeredgecolor='none')
    bp['medians'][i].set_color('black')
    bp['medians'][i].set_linewidth(3)
    # and 4 caps to remove
    for c in bp['caps']:
        c.set_linewidth(0)


for i in range(len(bp['boxes'])):
    box = bp['boxes'][i]
    box.set_linewidth(0)
    boxX = []
    boxY = []
    for j in range(5):
        boxX.append(box.get_xdata()[j])
        boxY.append(box.get_ydata()[j])
        boxCoords = zip(boxX,boxY)
        boxPolygon = pl.Polygon(boxCoords, facecolor = colors[i], linewidth=0)
        ax.add_patch(boxPolygon)



#y_max = np.max(np.concatenate((low_mut_100, high_mut_100)))
#y_min = np.min(np.concatenate((low_mut_100, high_mut_100)))
#print y_max

y = 0.26
yA = 1.1
yB = 0.

ax.annotate("", xy=(3, .83), xycoords='data', 
    xytext=(2, .83), textcoords='data',
    arrowprops=dict(arrowstyle="-", ec='#aaaaaa',
    connectionstyle="bar,fraction=0.1"))
ax.text(2.5, .79, '$ns$',
    horizontalalignment='center',
    verticalalignment='center', fontsize='large')

ax.annotate("", xy=(5, y), xycoords='data', 
    xytext=(4, y), textcoords='data',
    arrowprops=dict(arrowstyle="-", ec='#aaaaaa',
    connectionstyle="bar,fraction=0.1"))
ax.text(4.5, .22, '$ns$',
    horizontalalignment='center',
    verticalalignment='center', fontsize='large')


ax.annotate("", xy=(8, .59), xycoords='data', 
    xytext=(7, .59), textcoords='data',
    arrowprops=dict(arrowstyle="-", ec='#aaaaaa',
    connectionstyle="bar,fraction=0.1"))
ax.text(7.5, .55, '$ns$',
    horizontalalignment='center',
    verticalalignment='center', fontsize='large')

si = 12 

parms = {
    'axes.labelsize': si,
    'text.fontsize': si,
    'legend.fontsize': si,
    'xtick.labelsize': si,
    'ytick.labelsize': si,
    'text.usetex': False,
    'figure.figsize': [6., 7.]
}
pl.rcParams.update(parms)
                                                                                               
ax.set_ylim([0.,1.05])
ax.set_xticklabels(['Full','no\nD1', 'no\nD2', 'no\nRP', 'no\nEfference', 'no\nLI', 'no\nSF', 'PD'])
ax.set_xticklabels(['Full', 'no\nSF', 'no\nD1', 'no\nD2', 'no\nEfference', 'no\nLI', 'no\nRP', 'PD'])
ax.set_ylabel('Average success ratio for the last 5 trials of each block')
ax.set_ylabel('Average success ratio for the last 5 trials of the last 5 blocks')

pl.savefig('anovatest_.pdf', bbox_inches='tight', dpi=600)
pl.savefig('anovatest_.eps', bbox_inches='tight', dpi=600)
pl.savefig('anovatest_.tiff', bbox_inches='tight', dpi=600)
pl.savefig('anovatest_.png', bbox_inches='tight', dpi=600)

#pl.show()





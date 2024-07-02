import matplotlib.pyplot as plt
import numpy as np
import re
import os

# internal constants

parser_comment = '#'
config_file    = 'cohpgfx.cfg'

# configuration params and their default values

cfg_dosfile    = 'output_no_peaks.txt'

cfg_figsize       = [6, 12]
cfg_height_ratios = [1, 1, 1, 1]
cfg_hspace        = 0.4
cfg_legend_loc    = 'upper right'
cfg_xlabel        = 'Energy, eV'
cfg_xlim          = [-10, 15]
cfg_ylim_cohp     = [-1.0, 1.5]
cfg_ylim_dos      = [0.0, 3.5]

cfg_cohp_title    = 'COHP'
cfg_sstates_title = 's-states DOS'
cfg_pstates_title = 'p-states DOS'
cfg_dstates_title = 'd-states DOS'

cfg_dcohp_label = 'dCOHP'

cfg_imagefile = 'cohpgfx.pdf'
cfg_format    = 'pdf'

cfg_uimode = False 
cfg_tight_layout = False

# column's names lists

sstates = []
pstates = []
dstates = []

energy = ''
dcohp  = ''

# greetings!

print('cohpgfx v0 - script tool for COHP&DOS diagrams from \n')

# configuration file parsing

def cfg_parser(string):
	tokens = []
	string = re.split(parser_comment, string)[0]
	if string == '':
		return []
	tmp = re.split(r'\'|\"', string)
	if len(tmp) % 2 == 0:
		return []
	for i in range(len(tmp)):
		if i % 2 == 0:
			tokens.extend(re.split(r'\ |\t', tmp[i]))
		else:
			tokens.append(tmp[i])
	while '' in tokens:
		tokens.remove('')
	return tokens

if os.path.exists(config_file):
	f = open(config_file, 'r')
	for i in f:
		tokens = cfg_parser(i)
		if len(tokens) < 1:
			continue
		if tokens[0] == 'dosfile':
			cfg_dosfile = tokens[1];
			print('cfg_dosfile       = ', cfg_dosfile, ' ok')
		if tokens[0] == 'figsize':
			cfg_figsize = [int(tokens[1]), int(tokens[2])]
			print('cfg_figsize       = ', cfg_figsize, ' ok')
		if tokens[0] == 'height_ratios':
			cfg_height_ratios = [int(tokens[1]), int(tokens[2]), int(tokens[3]), int(tokens[4])]
			print('cfg_height_ratios = ', cfg_height_ratios, ' ok')
		if tokens[0] == 'hspace':
			cfg_hspace = float(tokens[1])
			print('cfg_hspace        = ', cfg_hspace, ' ok')
		if tokens[0] == 'legend_loc':
			cfg_legend_loc = tokens[1];
			print('cfg_legend_loc    = ', cfg_legend_loc, ' ok')
		if tokens[0] == 'xlabel':
			cfg_xlabel = tokens[1];
			print('cfg_xlabel        = ', cfg_xlabel, ' ok')
		if tokens[0] == 'xlim':
			cfg_xlim = [float(tokens[1]), float(tokens[2])]
			print('cfg_xlim          = ', cfg_xlim, ' ok')
		if tokens[0] == 'ylim_cohp':
			cfg_ylim_cohp = [float(tokens[1]), float(tokens[2])]
			print('cfg_ylim_cohp     = ', cfg_ylim_cohp, ' ok')
		if tokens[0] == 'ylim_dos':
			cfg_ylim_dos = [float(tokens[1]), float(tokens[2])]
			print('cfg_ylim_dos      = ', cfg_ylim_dos, ' ok')
		if tokens[0] == 'cohp_title':
			cfg_cohp_title = tokens[1];
			print('cfg_cohp_title    = ', cfg_cohp_title, ' ok')
		if tokens[0] == 'sstates_title':
			cfg_sstates_title = tokens[1];
			print('cfg_sstates_title = ', cfg_sstates_title, ' ok')
		if tokens[0] == 'pstates_title':
			cfg_pstates_title = tokens[1];
			print('cfg_pstates_title = ', cfg_pstates_title, ' ok')
		if tokens[0] == 'dstates_title':
			cfg_dstates_title = tokens[1];
			print('cfg_dstates_title = ', cfg_dstates_title, ' ok')
		if tokens[0] == 'dcohp_label':
			cfg_dcohp_label = tokens[1];
			print('cfg_dcohp_label   = ', cfg_dcohp_label, ' ok')
		if tokens[0] == 'imagefile':
			cfg_imagefile = tokens[1];
			print('cfg_imagefile     = ', cfg_imagefile, ' ok')
		if tokens[0] == 'format':
			cfg_format = tokens[1];
			print('cfg_format        = ', cfg_format, ' ok')
		if tokens[0] == 'uimode':
			cfg_uimode = True
			print('cfg_uimode ok')
		if tokens[0] == 'tight_layout':
			cfg_tight_layout = True
			print('cfg_tight_layout ok')

	f.close()
	
# loading DOS data

dos_data = np.genfromtxt(cfg_dosfile, 
                         delimiter      = '\t', 
                         filling_values = 0.0, 
                         names          = True, 
                         invalid_raise  = False) # invalid_raise is for debug!

# sorting column's names to plot

energy = dos_data.dtype.names[0];
dcohp  = dos_data.dtype.names[1];

for i in dos_data.dtype.names:
	if   re.search(r'\ds', i) != None:
		sstates.append(i)
	elif re.search(r'\dp', i) != None:
		pstates.append(i)
	elif re.search(r'\dd', i) != None:
		dstates.append(i)

# plotting setup

fig, ax = plt.subplots(4, 
                       1, 
                       figsize     = cfg_figsize,
                       gridspec_kw = {
                                      'height_ratios': cfg_height_ratios,
                                      'hspace'       : cfg_hspace
                                     })

if cfg_tight_layout == True:
	fig.tight_layout()

# plotting COHP

ax[0].plot(dos_data[energy], 
           dos_data[dcohp],
           label = cfg_dcohp_label)

ax[0].set_title (cfg_cohp_title)
ax[0].set_xlabel(cfg_xlabel)
ax[0].set_xlim  (cfg_xlim)
ax[0].set_ylim  (cfg_ylim_cohp)
ax[0].legend    (loc = cfg_legend_loc)

# plottinng DOS for s states

for i in sstates:
	ax[1].plot(dos_data[energy], 
                   dos_data[i],
                   label = i)

ax[1].set_title (cfg_sstates_title)
ax[1].set_xlabel(cfg_xlabel)
ax[1].set_xlim  (cfg_xlim)
ax[1].set_ylim  (cfg_ylim_dos)
ax[1].legend    (loc = cfg_legend_loc)

# plottinng DOS for p states

for i in pstates:
	ax[2].plot(dos_data[energy], 
                   dos_data[i],
                   label = i)

ax[2].set_title (cfg_pstates_title)
ax[2].set_xlabel(cfg_xlabel)
ax[2].set_xlim  (cfg_xlim)
ax[2].set_ylim  (cfg_ylim_dos)
ax[2].legend    (loc = cfg_legend_loc)

# plottinng DOS for d states

for i in dstates:
	ax[3].plot(dos_data[energy], 
                   dos_data[i],
                   label = i)

ax[3].set_title (cfg_dstates_title)
ax[3].set_xlabel(cfg_xlabel)
ax[3].set_xlim  (cfg_xlim)
ax[3].set_ylim  (cfg_ylim_dos)
ax[3].legend    (loc = cfg_legend_loc)

# if UI mode is toggled, a window with results shows up

if cfg_uimode == True:
	plt.show()

# an image renders into pdf file

plt.savefig(cfg_imagefile, format = cfg_format)



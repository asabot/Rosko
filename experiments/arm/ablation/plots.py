import pandas
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.cm as cm
import numpy as np
import os
import re
import sys
from matplotlib import ticker as mticker




def plot_rosko_vs_arm_ablate(fname = 'rosko_vs_arm_ablate'):
	plt.rcParams.update({'font.size': 12})
	markers = ['o','v','s','d','^']
	colors = ['b','g','k','m','r']
	labels = ['ARMCL', 'CAKE','rosko', 'rosko+reordering', 'rosko+reorder+sp_tiling']
	sparsity = [70, 72, 75, 77, 80, 82, 85, 87, 90, 92, 95, 97, 99]
	df1 = pandas.read_csv('result_ablate_arm')
	runtime_armcl = [df1[(df1['algo'] == 'armcl') & (df1['sp'] == 1)]['time'].mean()]*len(sparsity)
	runtime_cake = [df1[(df1['algo'] == 'cake') & (df1['sp'] == 1)]['time'].mean()]*len(sparsity)
	a = open('reports_arm_ablate/report_armcl','r').read().split('\n')
	x = (((int(re.search(r'\d+', a[5]).group())*64.0) / runtime_armcl[0]) / 1e9)
	x += (((int(re.search(r'\d+', a[6]).group())*64.0) / runtime_armcl[0]) / 1e9)
	dram_bw_armcl = [x]*len(sparsity)
	dram_io_armcl = [x*runtime_armcl[0]]*len(sparsity)
	#
	a = open('reports_arm_ablate/report_cake','r').read().split('\n')
	x = (((int(re.search(r'\d+', a[5]).group())*64.0) / runtime_cake[0]) / 1e9)
	x += (((int(re.search(r'\d+', a[6]).group())*64.0) / runtime_cake[0]) / 1e9)
	dram_bw_cake = [x]*len(sparsity)
	dram_io_cake = [x*runtime_cake[0]]*len(sparsity)
	dram_bw_rosko_reorder=[]; dram_bw_rosko=[]; runtime_rosko = []; runtime_rosko_reorder	= []
	dram_io_rosko_reorder=[]; dram_io_rosko=[];
	dram_bw_rosko_reorder_tile =[]; runtime_rosko_reorder_tile = []; dram_io_rosko_reorder_tile = [];
	#	
	for i in range(len(sparsity)):
		# multiply by 64 bytes since external memory request non-cacheable 
		# and L2-data cache refills/writeback PMUs
		# in ARM are expressed in terms of number of cache lines
		a = open('reports_arm_ablate/report_rosko_%d' % (sparsity[i]),'r').read().split('\n')
		# cpu_time1 = float(re.search(r'\d+\.\d+', a[8]).group())
		cpu_time = df1[(df1['algo'] == 'rosko') & (df1['sp'] == sparsity[i])]['time'].mean()
		x = ((int(re.search(r'\d+', a[5]).group())*64.0) / cpu_time) / 1e9
		x += ((int(re.search(r'\d+', a[6]).group())*64.0) / cpu_time) / 1e9
		dram_bw_rosko.append(x)
		dram_io_rosko.append(x*cpu_time)
		runtime_rosko.append(cpu_time)
		#
		a = open('reports_arm_ablate/report_rosko_reorder_%d' % (sparsity[i]),'r').read().split('\n')
		# cpu_time1 = float(re.search(r'\d+\.\d+', a[8]).group())
		cpu_time = df1[(df1['algo'] == 'rosko+reorder') & (df1['sp'] == sparsity[i])]['time'].mean()
		x = ((int(re.search(r'\d+', a[5]).group())*64.0) / cpu_time) / 1e9
		x += ((int(re.search(r'\d+', a[6]).group())*64.0) / cpu_time) / 1e9
		dram_bw_rosko_reorder.append(x)
		dram_io_rosko_reorder.append(x*cpu_time)
		runtime_rosko_reorder.append(cpu_time)
		#
		a = open('reports_arm_ablate/report_rosko_reorder_tile_%d' % (sparsity[i]),'r').read().split('\n')
		# cpu_time1 = float(re.search(r'\d+\.\d+', a[8]).group())
		cpu_time = df1[(df1['algo'] == 'rosko+reorder+sp_tiling') & (df1['sp'] == sparsity[i])]['time'].mean()
		x = ((int(re.search(r'\d+', a[5]).group())*64.0) / cpu_time) / 1e9
		x += ((int(re.search(r'\d+', a[6]).group())*64.0) / cpu_time) / 1e9
		dram_bw_rosko_reorder_tile.append(x)
		dram_io_rosko_reorder_tile.append(x*cpu_time)
		runtime_rosko_reorder_tile.append(cpu_time)
		#
	# plt.subplot(1, 2, 1)
	plt.figure(figsize = (6,4))
	plt.plot(sparsity, runtime_armcl, label = labels[0], color = colors[0])
	plt.plot(sparsity, runtime_cake, label = labels[1], color = colors[1])
	plt.plot(sparsity, runtime_rosko, label = labels[2], color = colors[2])
	plt.plot(sparsity, runtime_rosko_reorder, label = labels[3],  color = colors[3])
	plt.plot(sparsity, runtime_rosko_reorder_tile, label = labels[4],  color = colors[4])
	#
	plt.ticklabel_format(useOffset=False, style='plain')
	plt.title('(a) Runtime on ARM CPU', fontsize = 24)
	plt.xlabel("Sparsity (%)", fontsize = 24)
	plt.ylabel("Runtime (sec)", fontsize = 24)
	plt.xticks(fontsize = 20)
	plt.yticks(fontsize = 20)
	plt.legend(loc = "lower left", prop={'size': 12})
	plt.savefig("%s_perf.pdf" % fname, bbox_inches='tight')
	plt.show()
	plt.clf()
	plt.close('all')
	#
	#
	plt.figure(figsize = (6,4))
	plt.plot(sparsity, dram_bw_armcl, label = labels[0], color = colors[0])
	plt.plot(sparsity, dram_bw_cake, label = labels[1], color = colors[1])
	plt.plot(sparsity, dram_bw_rosko, label = labels[2], color = colors[2])
	plt.plot(sparsity, dram_bw_rosko_reorder, label = labels[3], color = colors[3])
	plt.plot(sparsity, dram_bw_rosko_reorder_tile, label = labels[4], color = colors[4])
	#
	plt.title('(b) DRAM Bandwidth on ARM CPU', fontsize = 24)
	plt.xlabel("Sparsity (%)", fontsize = 24)
	plt.xticks(fontsize = 20)
	plt.yticks(range(5), fontsize = 20)
	plt.ylabel("DRAM Bw (GB/s)", fontsize = 24)
	plt.legend(loc = "center left", prop={'size': 14})
	plt.savefig("%s_dram.pdf" % fname, bbox_inches='tight')
	plt.show()
	plt.clf()
	plt.close('all')
	#
	#
	plt.figure(figsize = (6,4))
	plt.plot(sparsity, dram_io_armcl, label = labels[0], color = colors[0])
	plt.plot(sparsity, dram_io_cake, label = labels[1], color = colors[1])
	plt.plot(sparsity, dram_io_rosko, label = labels[2], color = colors[2])
	plt.plot(sparsity, dram_io_rosko_reorder, label = labels[3], color = colors[3])
	plt.plot(sparsity, dram_io_rosko_reorder_tile, label = labels[4], color = colors[4])
	#
	plt.title('(c) DRAM IO on ARM CPU', fontsize = 24)
	plt.xlabel("Sparsity (%)", fontsize = 24)
	plt.ylabel("DRAM IO (GB)", fontsize = 24)
	plt.xticks(fontsize = 20)
	plt.yticks(fontsize = 20)
	plt.legend(loc = "center left", prop={'size': 14})
	plt.savefig("%s_io.pdf" % fname, bbox_inches='tight')
	plt.show()
	plt.clf()
	plt.close('all')


plot_rosko_vs_arm_ablate()




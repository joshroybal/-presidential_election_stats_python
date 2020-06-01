#!/usr/bin/env python

import sys
import statistics

# procedure definitions
def compute_stats(x):
	stats_list = []
	stats_list.append('%.2f' % min(x))
	stats_list.append('%.2f' % max(x))
	stats_list.append('%.2f' % statistics.mean(x))
	stats_list.append('%.2f' % statistics.sample_standard_deviation(x))
	stats_list.append('%.2f' % statistics.median(x))
	stats_list.append('%.2f' % statistics.median_deviation(x))
	stats_list.append('%.3f' % statistics.skewness(x))
	return stats_list

def write_row(outfile, row_list, flag):
	if flag == 'flat':
		outfile.write('%-14s ' % row_list[0])
		outfile.write('%s ' % row_list[1])
		for stat in row_list[2:-1]:
			outfile.write('%8s' % stat)
		outfile.write('%9s' % row_list[-1])
	elif flag == 'html':
		outfile.write('<tr>')
		for x in row_list: outfile.write('<td>' + x + '</td>')
		outfile.write('<tr>')
	else:
		if (flag == 'csv'): outfile.write(','.join(row_list))
		if (flag == 'tab'): outfile.write('\t'.join(row_list))
	outfile.write('\n')

def print_table(outfile, list_table, flag):
	headers = ['STATE','P','MIN','MAX','AVG','STD','MDN','MAD','SKW']
	if flag == 'html':
		outfile.write('<tr>')
		for hdr in headers: outfile.write('<th>' + hdr + '</th>')
		outfile.write('</tr>\n')
	else:
		write_row(outfile, headers, flag)
	for state in sorted(list_table):
		if state == 'U. S. Total': continue
		write_row(outfile, [state, 'D'] + list_table[state]['D'], flag)
		write_row(outfile, [state, 'R'] + list_table[state]['R'], flag)
		write_row(outfile, [state, 'I'] + list_table[state]['I'], flag)
	write_row(outfile, ['U. S. Total', 'D'] + list_table['U. S. Total']['D'], flag)
	write_row(outfile, ['U. S. Total', 'R'] + list_table['U. S. Total']['R'], flag)
	write_row(outfile, ['U. S. Total', 'I'] + list_table['U. S. Total']['I'], flag)
	if flag == 'html': outfile.write('</table>\n')

# main program
formats = ['csv','flat','html','tab']
if len(sys.argv) < 2 or sys.argv[1] not in formats:
	print 'Usage: ' + sys.argv[0] + ' csv|flat|html|tab'
	sys.exit(0)

# input section
results = {}
infile = open('results.txt', 'rb')
for line in infile:
	field_list = line.strip().split(',')
	if field_list[0] not in results:
		results[field_list[0]] = { 'D':[], 'R':[], 'I':[] }
	results[field_list[0]]['D'].append(100.*float(field_list[1]))
	results[field_list[0]]['R'].append(100.*float(field_list[2]))
	results[field_list[0]]['I'].append(100.*float(field_list[3]))
infile.close()

# core processing section
# compute results statistics
stats_report = {}
for state in results:
	if state not in stats_report:
		stats_report[state] = { 'D':[], 'R':[], 'I':[] }
	stats_report[state]['D'] = compute_stats(results[state]['D'])
	stats_report[state]['R'] = compute_stats(results[state]['R'])
	stats_report[state]['I'] = compute_stats(results[state]['I'])

# compute swings
swings = {}
for state in stats_report:
	if state not in swings:
		swings[state] = { 'D':[], 'R':[], 'I':[] }
	px = results[state]['D']
	py = results[state]['R']
	pz = results[state]['I']
	n = min(len(px), len(py), len(pz))
	for i in range(1, n):
		swings[state]['D'].append(px[i] - px[i-1])
		swings[state]['R'].append(py[i] - py[i-1])
		swings[state]['I'].append(pz[i] - pz[i-1])

# compute swings statistics
swings_report = {}
for state in results:
	if state not in swings_report:
		swings_report[state] = { 'D':[], 'R':[], 'I':[] }
	swings_report[state]['D'] = compute_stats(swings[state]['D'])
	swings_report[state]['R'] = compute_stats(swings[state]['R'])
	swings_report[state]['I'] = compute_stats(swings[state]['I'])

# output section
if sys.argv[1] == 'html':
	filename = 'report.html'
elif sys.argv[1] == 'csv':
	filename = 'report.csv'
else:
	filename = 'report.txt'
outfile = open(filename, 'wb')
if sys.argv[1] == 'html':
	outfile.write('<!DOCTYPE html>\n')
	outfile.write('<html>\n')
	outfile.write('<head>\n')
	outfile.write('<link id="styleinfo" media="all">\n')
	outfile.write('<script type="text/javascript" src="style.js" defer></script>\n')
	outfile.write('</head>\n')
	outfile.write('<body>\n')
	outfile.write('<p>results report</p>\n')
	outfile.write('<table id="stats_table">\n')
else:
	outfile.write('results report\n')
print_table(outfile, stats_report, sys.argv[1])
print
if sys.argv[1] == 'html':
	outfile.write('<p>swings report</p>\n')
	outfile.write('<table id="swings_table">\n')
else:
	outfile.write('swings report\n')
print_table(outfile, swings_report, sys.argv[1])
if sys.argv[1] == 'html':
	outfile.write('</body>\n')
	outfile.write('</html>\n')
outfile.close()
print 'tables written to file ' + filename

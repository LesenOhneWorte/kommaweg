#!/usr/bin/python

import sys

with open(sys.argv[1],'r') as data_file:
	raw_data = data_file.read()

data = raw_data.split('\n')
data_out_list = []

for data_line in data:
	data_line_split = data_line.split(';')
	new_data_list = []
	for data_field in data_line_split:
		comma_pos = data_field.find(',')
		if comma_pos > -1:
			new_field = data_field[:comma_pos]+'.'+data_field[comma_pos+1:]
			new_data_list.append(new_field)
		else:
			new_data_list.append(data_field)
	new_data_line = ';'.join(new_data_list)
	data_out_list.append(new_data_line)

data_out = '\n'.join(data_out_list)

out_name = sys.argv[1][:sys.argv[1].find('.csv')] + '_comma_removed.csv'

with open(out_name,'w') as out_file:
	out_file.write(data_out)

#!/usr/bin/python

import sys, re, datetime

with open(sys.argv[1],'r') as data_file:
	raw_data = data_file.read()

data = raw_data.split('\n')
data_out_list = []

date_de = re.compile('\d{2}.\d{2}.\d{4}')
date_en = re.compile('\d{2}/\d{2}/\d{2}')
prob_code_reg = re.compile('\d{3}[A-Z]{2}\d{8}')

for data_line in data:
	data_line_split = data_line.split(';')
	date_birth_from_prob_code = None
	if prob_code_reg.fullmatch(data_line_split[0]):
		date_birth_from_prob_code = datetime.date(int(data_line_split[0][-4:]),int(data_line_split[0][-6:-4]),int(data_line_split[0][-8:-6]))
	new_data_list = []
	date_birth = None
	date_test = None
	for data_field in data_line_split:
		comma_pos = data_field.find(',')
		if comma_pos > -1:
			new_field = data_field[:comma_pos]+'.'+data_field[comma_pos+1:]
			new_data_list.append(new_field)
		else:
			date = None
			result = date_de.fullmatch(data_field)
			if result:
				date_list = data_field.split('.')
				date = datetime.date(int(date_list[2]),int(date_list[1]),int(date_list[0]))
				if data_line_split.index(data_field) == 4:
					date_birth = date
					if date_birth_from_prob_code:
						date_dif = date_birth - date_birth_from_prob_code
						if date_dif != 0:
							print(data_line_split[0],date_dif)
							date_birth = date_birth_from_prob_code
							date = date_birth_from_prob_code
				elif data_line_split.index(data_field) == 6:
					date_test = date
			else:
				result = date_en.fullmatch(data_field)
				if result:
					date_list = data_field.split('/')
					date = datetime.date(int(date_list[2])+2000,int(date_list[0]),int(date_list[1]))
					if data_line_split.index(data_field) == 4:
						date_birth = date
					elif data_line_split.index(data_field) == 6:
						date_test = date
			if date:
				data_field = date.strftime('%d.%m.%Y')
			new_data_list.append(data_field)
	if date_birth and date_test:
		age = date_test - date_birth
		age = int(age.total_seconds() / (60*60*24))
		if new_data_list[-1] != str(age):
			new_data_list.append(str(age))
	if data.index(data_line) == 0:
		new_data_list.append('AGE_DAYS')
	new_data_line = ';'.join(new_data_list)
	data_out_list.append(new_data_line)

data_out = '\n'.join(data_out_list)

out_name = sys.argv[1][:sys.argv[1].find('.csv')] + '_replaced.csv'

with open(out_name,'w') as out_file:
	out_file.write(data_out)

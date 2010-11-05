import os, sys
#holycrapcomment
def line_parser(line):
	return None
	
def open_files(fin_name, fout_name = "out.txt"):
	return open(fin_name, "r"), open(fout_name, "w")

def get_new_temp(val):
	rep = [0.0] * 5
	if val > 80:
		rep[4] = 1.0
	elif val > 59:
		rep[3] = 1.0
	elif val > 53:
		rep[2] = 1.0
	elif val > 44:
		rep[1] = 1.0
	else:
		rep[0] = 1.0
	return rep
	
def get_new_temp_range_bits(val):
	rep = [0.0] * 10
	i = int(val - 40.0) / 5
	if i < 0 or i > 9:
		return rep
	rep[i] = 1.0
	return rep
	
def get_new_day_month_bits(val):
	rep = [0.0] * 5
	if val >= 244:
		rep[4] = 1.0
	elif val >= 213:
		rep[3] = 1.0
	elif val >= 182:
		rep[2] = 1.0
	elif val >= 152:
		rep[1] = 1.0
	else:
		rep[0] = 1.0
	return rep

def get_new_day_10bit(val):
	#121-273 (152 total / 10 bits ~= 16 days/bit)
	val = val - 121
	val = int(val / 15.2)
	rep = [0.0] * 10
	rep[val] = 1.0
	return rep

def print_usage():
	print "USAGE: python [<source-file>.py] [<number-of-inputs>] [<temp-index>] [<day-index>] [<input-file>] [(opt)<output-file>]"

def bad_args(argv):
	argc = len(argv)
	if argc < 5 or argc > 6:
		return True
	return False

def parse_header(fin, fout, num_vars, new_num_vars):
	fpos = 0
	while True:
		fpos = fin.tell()
		line = fin.readline()
		if len(line) == 0:
			print "EOF before header parsed"
			return False
		line_list = line.split(" ")
		if num(line_list[0]):
			fin.seek(fpos)
			return True
		if num(line_list[-1]):
			if int(line_list[-1]) == num_vars:
				line_list[-1] = str(new_num_vars)
				line = " ".join(map(str, line_list))
				line += "\n"
		fout.write(line)
		
def num(s):
	try:
		float(s)
		return True
	except:
		return False

if __name__ == "__main__":
	
	bits_adding = 10 + 10 - 2
	if bad_args(sys.argv):
		print_usage()
		sys.exit()

	try:
		num_vars, temp_index, day_index = map(int, sys.argv[1:4])
		fin, fout = open_files(*sys.argv[4:])
	except:
		print "Error in arguments"
		print_usage()
		sys.exit()

	if not parse_header(fin, fout, num_vars, num_vars + bits_adding):
		print "Error in header, are you doing it wrong?"
		print_usage()
		sys.exit()
	
	eof = False
	first, second = 0, 0
	temp_first = True
	if temp_index > day_index:
		temp_first = False
		first = day_index
		second = temp_index
	else:
		first = temp_index
		second = day_index
	while not eof:
		line = fin.readline().split(" ")
		if len(line) < num_vars:
			eof = True
			continue
		new_line = line[0:first]
		if temp_first:
			new_line.extend(get_new_temp_range_bits(float(line[first])))
		else:
			new_line.extend(get_new_day_10bit(float(line[first])))	
		new_line.extend(line[first + 1: second])
		if temp_first:
			new_line.extend(get_new_day_10bit(float(line[second])))	
		else:
			new_line.extend(get_new_temp_range_bits(float(line[second])))
		new_line.extend(line[second + 1:])
		fout.write(" ".join(map(str, new_line)))
	

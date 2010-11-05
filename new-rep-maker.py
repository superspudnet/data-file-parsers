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
	
def get_new_day(val):
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


if __name__ == "__main__":
	argc = len(sys.argv)
	if argc < 2 or argc > 3:
		print "USAGE: python <source-file>.py <input-file> (output-file)"
		sys.exit()
	
	fin, fout = open_files(*sys.argv[1:])
	eof = False
	while not eof:
		line = fin.readline().split(" ")
		if len(line) < 14:
			eof = True
			continue
		new_line = get_new_temp_range_bits(float(line[0]))
		new_line.extend(line[1:5])
		new_line.extend(get_new_day(float(line[5])))
		new_line.extend(line[6:])
		fout.write(" ".join(map(str, new_line)))
		
	

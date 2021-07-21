# Naomi Yescas

# Generate JSON file from command text file
# Format:
# 	<Command>  <Page>  <Query or CMD (c/q)>  <Description> 

import json

cmd_file = open("commands.txt", 'r')

cmd_dict = {}

# Each line add first element as dictionary Key
# Subsequent elements are added to a list
# Last lement is description -> join to string
for line in cmd_file:
	dict_line = line
	line_list = dict_line.strip().split()
	if len(line_list) >= 4:
		cmd_dict[line_list[0]] = [line_list[1], line_list[2], " ".join(line_list[3:])]

# Print Command and Description
for key in cmd_dict:
	print(key + ": " + cmd_dict[key][2])

# Create Json file and populate with command dict 
with open("commands.json", 'w') as cmd_json:
	json.dump(cmd_dict, cmd_json)

cmd_json.close()
cmd_file.close()

import os
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

intent = open(os.path.join(script_dir, 'intents.json'),'r')
f_proj = open(os.path.join(script_dir, 'x_project_out.txt'),'r')
f_dep = open(os.path.join(script_dir, 'x_department_out.txt'),'r')
fout = open(os.path.join(script_dir, 'project_out.txt'),'w')

intents = intent.read()
#print(intents)
line = f_proj.readline()
line = line.replace("<TH>",'')    
line = line.replace("<TR>",'')    
line = line.replace("<TD>",'')    
line = line.replace("<TABLE BORDER=1>id</TH>name</TH>updated_at</TH>created_at</TH>",'')
line = line.split("</TD>")
line = line[:-1]
project_size = (int)(len(line)/4)
project_string = "\t\t{\n\t\t\t\"tag\": \"X\",\n\t\t\t\"patterns\":[\n\t\t\t\t\"X\",\n\t\t\t\t\"project of X\",\n\t\t\t\t\"project related to X\",\n\t\t\t\t\"X project\"\n\t\t\t],\n\t\t\t\"responses\":[\n\t\t\t\t\"Please type 'y' to confirm that the type of projects you want is 'X'\\nIf not, please clearly state your needs again. Thanks:)\"\n\t\t\t],\n\t\t\t\"context_set\":\"WantX\",\n\t\t\t\"type\": 1\n\t\t},\n\t\t{\n\t\t\t\"tag\": \"X_Set\",\n\t\t\t\"patterns\":[\"y\"],\n\t\t\t\"responses\":[\n\t\t\t\t\"We set 'X' to your seatching conditions.\\nYou can continue to add otherconditions you want.\\nIf that's all, please enter 'g' to get the results.\"\n\t\t\t],\n\t\t\t\"context_filter\": \"WantX\",\n\t\t\t\"type\": 2\n\t\t}"
write_cnt = 0
project_set = set()
for i in range(project_size):
    if(line[i*4+1] in project_set):
        continue
    if(write_cnt!=0 and intents.find(line[i*4+1])==-1):
        fout.write(",\n")
    if(intents.find(line[i*4+1])==-1):
        project = line[i*4+1]
        output = project_string.replace('X',project)
        fout.write(output)
        write_cnt += 1
        project_set.add(project)

fout.close()
fout = open(os.path.join(script_dir, 'department_out.txt'),'w')
line = f_dep.readline()
line = line.replace("<TH>",'')    
line = line.replace("<TR>",'')    
line = line.replace("<TD>",'')    
line = line.replace("<TABLE BORDER=1>id</TH>user_id</TH>country</TH>university</TH>name_of_pi</TH>department</TH>start_date</TH>end_date</TH>apply_copi_end_date</TH>project_title</TH>project_content</TH>link</TH>location</TH>updated_at</TH>created_at</TH>",'')
line = line.split("</TD>")
dep_size = len(line)/15
dep_string = "\t\t{\n\t\t\t\"tag\": \"D\",\n\t\t\t\"patterns\":[\n\t\t\t\t\"D\",\n\t\t\t\t\"Department of D\"\n\t\t\t],\n\t\t\t\"responses\":[\n\t\t\t\t\"Please type 'y' to confirm that the department of projects you want is 'D'. If not, please clearly explain your needs again. Thanks:)\"\n\t\t\t],\n\t\t\t\"context_set\": \"WantD\",\n\t\t\t\"type\": 3\n\t\t},\n\t\t{\n\t\t\t\"tag\": \"D_Set\",\n\t\t\t\"patterns\":[\"y\"],\n\t\t\t\"responses\":[\n\t\t\t\t\"We set 'D' to your searching conditions.\\nYou can continue to add other conditions you want.\\nIf that's all, please enter 'g' to get ypur results.\"\n\t\t\t],\n\t\t\t\"context_filter\": \"wantD\",\n\t\t\t\"type\": 4\n\t\t}"
write_cnt = 0
department_set = set()
for i in range(dep_size):
    if(line[i*15+5] in department_set):
        continue
    if(write_cnt!=0 and intents.find(line[i*15+5])==-1):
        fout.write(",\n")
    if(intents.find(line[i*15+5])==-1):
        dep = line[i*15+5].replace(' ','_')
        output = dep_string.replace('D', dep)
        fout.write(output)
        write_cnt += 1
        department_set.add(dep)
#print(line[i*15+5])

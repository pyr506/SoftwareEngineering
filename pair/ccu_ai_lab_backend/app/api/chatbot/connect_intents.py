import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file1", type=str, help="input the first file (ie. intents.json)",nargs='+')
parser.add_argument("file2", type=str, help="input the second file (ie. project_out.txt)",nargs='+')
parser.add_argument("output", type=str, help="output file name (ie. first_out.txt)",nargs='+')

args = parser.parse_args()
first_file = str(args.file1)
sec_file = str(args.file2)
f1 = open(first_file[2:-2],'r')
f2 = open(sec_file[2:-2],'r')
out_file = args.output
#print(type(out_file))
out_file = out_file[0]
#print(out_file)
fout = open(out_file,'w')
f1_content = f1.read()
f2_content = f2.read()
if(len(f2_content)>5):
    fout.write(f1_content[:-7]+",\n"+f2_content+f1_content[-7:])
else:
    fout.write(f1_content)

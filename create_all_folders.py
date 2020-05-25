import os
from shutil import copyfile
from translate import Translator   
import googletrans  
from pprint import pprint  
import imghdr

def correct_image_path(line):
    if(line.startswith("![image]")):
        return line.replace("(","(../")
    return line

def WriteHeader(src, dst, category):    
    lines = ""  
    translator = googletrans.Translator() 
    #translator = Translator(from_lang="chinese", to_lang="english")
    with open(src, "r") as src_file:
        temp = []
        for line in src_file:
            temp.append(correct_image_path(line))

        # method 1
        #print("original line:" + line)
        #eng_line = translator.translate(line)
        #print("eng_line:" + eng_line)

        # method 2           
        #chinese_lines = ' '.join([temp_line for temp_line in temp])
        #print(chinese_lines)        
        #lines = translator.translate(chinese_lines, dest='en').text   
        #print(lines)
        lines = ' '.join([temp_line for temp_line in temp])

    src_file.close()
    dst_file = open(dst, 'w')
    header = "---\ndraft: true\ncategories: [\"" + category + "\"]\n---\n"
    print("header\n" + header)
    dst_file.write(header)
    #dst_file.write(''.join([line for line in lines]))
    dst_file.write(lines)
    dst_file.close()

#####################################################################
# record all the folders we are going to copy from github repos
#####################################################################
GITHUB_PATH = "/home/evan/evansin-github"
exception_list = [".git", ".idea", "MANAGE", "RESEARCH-", "Personal", "Memo", "PROJECT-", "COMPANY-", "evansin100", "HW-IP-GPU-Mali"]
dirs = os.listdir(GITHUB_PATH)
clone_folder = []
for name in dirs:
    skip = 0
    if(os.path.isdir(GITHUB_PATH + "/" + name)):
        for exception in exception_list:
            if name.startswith(exception):
                print("exception found, not copied:" + name)
                skip = 1
                continue
        if skip == 0:
            clone_folder.append(name)

#####################################################################
#print(clone_folder)
# create folder 
#####################################################################
for name in clone_folder:
    if not os.path.isdir(name):
        os.mkdir("post/"+name.lower())

#####################################################################
# copy readme.md as the single file in each folder 
# TODO: should be refined and extended (copy all the content from repo)
#####################################################################
for name in clone_folder:
    src = GITHUB_PATH + "/" + name + "/README.md"
    dst = "post/" + name.lower() + "/README.md"
    if os.path.isfile(src):
        print("copy from:" + src + " to " + dst)
        WriteHeader(src,dst,name)


#####################################################################
# copy image 
#####################################################################
for name in clone_folder:
    src_dir = GITHUB_PATH + "/" + name
    dst_dir = "post/" + name.lower()
    dirs = os.listdir(src_dir)
    for file_name in dirs:
        if (file_name.endswith(".png")):
            src_path = GITHUB_PATH + "/" + name + "/" + file_name          
            dst_path = "post/" + name.lower() + "/" + file_name          
            copyfile(src_path, dst_path)


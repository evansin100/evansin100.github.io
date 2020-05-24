import os
from shutil import copyfile
from translate import Translator   

GITHUB_PATH = "/home/evan/evansin-github"
exception_list = [".git", ".idea", "MANAGE", "RESEARCH-", "Personal", "Memo", "PROJECT-", "COMPANY-",]
dirs = os.listdir(GITHUB_PATH)
clone_folder = []

def WriteHeader(src, dst, category):    
    lines = []
    translator = Translator(from_lang="chinese", to_lang="english")
    with open(src, "r") as src_file:
        for line in src_file:
            #print("original line:" + line)
            #eng_line = translator.translate(line)
            #print("eng_line:" + eng_line)
            lines.append(line + "   \n")
    src_file.close()

    dst_file = open(dst, 'w')
    header = "---\ndraft: true\ncategories: [\"" + category + "\"]\n---\n"
    print("header\n" + header)
    dst_file.write(header)
    dst_file.write(''.join([line for line in lines]))
    dst_file.close()

#####################################################################
# record all the folders we are going to copy from github repos
#####################################################################
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
        os.mkdir(name)

#####################################################################
# copy readme.md as the single file in each folder 
# TODO: should be refined and extended (copy all the content from repo)
#####################################################################
for name in clone_folder:
    src = GITHUB_PATH + "/" + name + "/README.md"
    dst = name + "/README.md"
    if os.path.isfile(src):
        print("copy from:" + src + " to " + dst)
        WriteHeader(src,dst,name)

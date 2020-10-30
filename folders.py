import os
from imutils import paths


path = "YOUR_DIRECTORY_PATH"
#dirs=os.listdir(path)
#print(dirs)
dirs_path=list(paths.list_images(path))
s1=""
s2=""
c=1
for i in dirs_path:
    b = i.split("/")#SPLIT BASED ON YOUR PATH
    # print(b)
    #USE THE INDEX BASED ON YOUR FOLDER NAME. CHECK THE INDEX BY UNCOMMENTING THE PREVIOUS LINE :)
    if(b[8]=='YOUR FOLDER/DIRECTORY NAME'):
        #CHANGE YOUR INDEX BASED ON THE PATHS. THE FOLLOWING LINE DIFFERS BASED ON YOUR REQUIREMENT
        if(s1 != b[9] or s2 != b[10]):
            print(s1,s2,c)#PRINT YOUR FOLDER NAMES ALONG WITH THE COUNT. YOU CAN WRITE THIS TO YOUR CSV FILE AS WELL USING CSV MODULE :)
            c=1
            s1=b[9]#ASSIGN BASED ON YOUR INDEX
            s2=b[10]#ASSIGN BASED ON YOUR INDEX
        else:
            c+=1 
print(c)#Final file count


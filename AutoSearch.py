#
# PROJECT NAME :- Stack Overflow Auto Search Tool
# Creater of This Project :- Amit Gopal Singh Paikra
#
# How to give Input?
#ex :- In cli - python AutoSearch.py arg1 arg2
# arg1 -> file ( ex:- pythonfile.py , cppfile.cpp )
# arg2 -> No. of result you want, like 2 it shows 2 new tab means 2 diff. results
#         if No value passed then 3 is default

################################################
# change this version 
pythonversion = "python" # "python3"
cppversion = "g++" # "python"
#
################################################

from subprocess import Popen , PIPE 
import sys
import requests

argv_list = sys.argv
len_argv_list = len(sys.argv)

# argv[1] --> filename
# argv[2] --> no of search
def load_browser(url , n ):
    n = int(n)
    req = requests.get( url )
    jsonData = req.json()

    url_links = []
        
    upto = 1
    for i in jsonData['items'] :
        if i['is_answered']  and upto <= n :
            url_links.append(i['link'])
            upto += 1 
    if len(url_links) == 0 :
        sys.exit("No related information found!!!")    
    for j in url_links :
        Popen( [pythonversion , "-m" , "webbrowser" , "-t" , j ])


def chech_extension( filename ) :
    for i in range( 0 , len( filename )):
        if filename[i] == '.' :
            return filename[i : len(filename) ]
    return ""

def auto_search_python(filename ):
    var = ""
    try :
        p = Popen( [pythonversion , filename] , stderr = PIPE , universal_newlines = True  )
        if p.stderr.readline() == "" :
            print("No Error found!!!")
        elif p.stderr.readline() != "" :
            var = p.stderr.readlines()[-1]
    except Exception as e:
        sys.exit(e)

    return ("https://api.stackexchange.com/"+"/2.2/search?order=desc&sort=activity&tagged=python&intitle={}&site=stackoverflow".format(var))

def auto_search_java(filename) :
    print("java")

def auto_search_cpp(filename) :
    var = ""
    try :
        p = Popen( [cppversion , filename] , stderr = PIPE , universal_newlines = True )
        filecontent = p.stderr.readlines()
        if len(filecontent) == 0 :
            sys.exit("No Error Found!!!")
        elif len(filename) != 0 :
            # print(p.stderr.readlines())
            var = filecontent[2]
            var = var[:-1]
            var = ' '.join(var.split()[1:])
            
    except Exception as e :
        sys.exit(e)
    
    return ("https://api.stackexchange.com/"+"/2.2/search?order=desc&sort=activity&tagged=c++&intitle={}&site=stackoverflow".format(var))        
    


if __name__ == "__main__" :
    
    if len_argv_list != 1 :

        n = 3
        if len_argv_list == 3 :
            n = int(argv_list[2])
        
        filename = argv_list[1]
        ext_use = chech_extension(filename)
        url = ""

        if ext_use == ".py" :
            url = auto_search_python(filename)

        elif ext_use == ".java" :
            auto_search_java(filename)

        elif ext_use == ".cpp" :
           url =  auto_search_cpp(filename)
        #    print(url)

        elif ext_use == ".c" :
            print("c prog")

        else :
            sys.exit("Execution error for given file {}".format(filename))
        print(url)
        if url != "":
            load_browser(url , n )
        else :
            sys.exit("No URL found!!! for loading browser")
            
    



## RbxLua obsfucator
## Confuzius

import re
import string
import os
import random

usedVars = []
def randVar():
    a = random.randint(5,35)
    while True:
        varN = ""
        for i in range(1,a):
            if 1 == random.randint(0,1):
                varN += "b"
            else:
                varN += "d"
        if not varN in usedVars:
            break
    usedVars.append(varN)
    return varN

def randCharArray(strings):
    pureText = list(set(''.join(strings)))
    return pureText

def indexCharList(word,charList):
    luaArray = ""
    for i,v in enumerate(word):
        if i+1 != len(word):
            luaArray += "bdbd[" + str(charList.index(v)) + "].."
        else:
            luaArray += "bdbd[" + str(charList.index(v)) + "]"
    return luaArray

def luaify(obj,name):
    # Translate python tables to lua syntax
    d = "a"

def obsfucate(lua):
    # ((?<=\t| |{|,)[a-zA-Z0-9_]+(?=.\= )) - Variable regex
    vNames = re.findall("((?<=\t| |{|,)[a-zA-Z0-9_]+(?=.\= ))", lua)
    vNames = list(set(vNames))

    # (?<!")(?<=\W)Service+(?=\W)(?!") - Replace var regex
    for v in vNames:
        lua = re.sub("(?<!\")(?<=\W)"+v+"+(?=\W)(?!\")",randVar(),lua)

    # (?<=function )[\w]+ - Function name regex
    fNames = re.findall("(?<=function )[\w]+", lua)
    fNames = list(set(fNames))
    for v in fNames:
        lua = re.sub("(?<!\")(?<=\W)"+v+"+(?=\W)(?!\")",randVar(),lua)

    # Regex for function paramerers
    pNamesDirty = re.findall("(?<=function)(.+\))", lua)
    pNamesClean = re.findall("(?<=\(|,)[a-zA-Z0-9_]+(?=\)|,)",str(pNamesDirty))
    pNames = list(set(pNamesClean))
    for v in pNames:
        lua = re.sub("(?<!\")(?<=\W)"+v+"+(?=\W)(?!\")",randVar(),lua)

    # ([\"]+?(.+?)[\"]+?) - String regex
    strings = re.findall("[\"]+?(.+?)[\"]+?",lua)
    charList = randCharArray(strings)
    for word in strings:
        lua = re.sub("[\"]+?"+word+"[\"]+?",indexCharList(word,charList),lua)
    
    #lua = lua.replace("\n"," ")
    #lua = lua.replace("\t"," ")
    print(lua)

#open file
fileIO = open('C:\\',"r")
lua = fileIO.read()
obsfucate(lua)

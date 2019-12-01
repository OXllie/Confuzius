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

def indexCharList(word,charList,name):
    luaArray = ""
    for i,v in enumerate(word):
        if i+1 != len(word):
            luaArray += name+"[" + str(charList.index(v)+1) + "].."
        else:
            luaArray += name+"[" + str(charList.index(v)+1) + "]"
    return luaArray

def luaify(obj,name):
    # Translate python tables to lua syntax
    luaobj = name + "={"
    for i in obj:
        luaobj += "\""+i+"\","
    luaobj = luaobj[:-1]+"}"
    return luaobj

def obsfucate(lua):
    # ((?<=\n|\t| |{|,)[a-zA-Z0-9_]+(?=.\= )) - Variable regex
    vNames = re.findall("((?<=\n|\t| |{|,)[a-zA-Z0-9_]+(?=.\= ))", lua)
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
    name = randVar()
    for word in strings:
        lua = re.sub("[\"]+?"+word+"[\"]+?",indexCharList(word,charList,name),lua)

    charDef = luaify(charList,name)
    lua = charDef + lua
    
    #lua = lua.replace("\n"," ")
    #lua = lua.replace("\t"," ")
    print(lua)


fileIO = open('C:\\Users\\Oliver\\Desktop\\lua example.txt',"r")
lua = fileIO.read()
obsfucate(lua)

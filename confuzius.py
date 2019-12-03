## RbxLua obsfucator
## Confuzius

import re
import random

usedVars = []
def randVar():
    # Generates a random variable name with no collisions
    while True:
        a = random.randint(5,35)
        varN = ""
        for i in range(1,a):
            varN += random.choice(["d","b"])
        if not varN in usedVars:
            break
    usedVars.append(varN)
    return varN

def randCharArray(strings):
    # Takes all strings found and generates a python list of all unique characters
    pureText = list(set(''.join(strings)))
    return pureText

def indexCharList(word,charList,name):
    # Generates the lua for concatenating references to the array to produce an obsfucated string output
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
    # Variable regex
    vNames = re.findall("((?<=\n|\t| |{|,)[a-zA-Z0-9_]+(?=.\= ))", lua)
    vNames = list(set(vNames))
    # Replace variable
    for v in vNames:
        lua = re.sub("(?<!\")(?<=\W)"+v+"+(?=\W)(?!\")",randVar(),lua)

    # Function name regex
    fNames = re.findall("(?<=function )[\w]+", lua)
    fNames = list(set(fNames))
    # Replace function
    for v in fNames:
        lua = re.sub("(?<!\")(?<=\W)"+v+"+(?=\W)(?!\")",randVar(),lua)

    # Function parameters regex
    pNamesDirty = re.findall("(?<=function)(.+\))", lua)
    pNamesClean = re.findall("(?<=\(|,)[a-zA-Z0-9_]+(?=\)|,)",str(pNamesDirty))
    pNames = list(set(pNamesClean))
    # Replace function parameters
    for v in pNames:
        lua = re.sub("(?<!\")(?<=\W)"+v+"+(?=\W)(?!\")",randVar(),lua)

    # String regex
    strings = re.findall("[\"]+?(.+?)[\"]+?",lua)
    charList = randCharArray(strings)
    name = randVar()
    # Replace strings
    for word in strings:
        lua = re.sub("[\"]+?"+word+"[\"]+?",indexCharList(word,charList,name),lua)
    
    # Generates a lua array containing all the characters defined in charList and appends it to the script
    charDef = luaify(charList,name)
    lua = charDef + lua
    
    #lua = lua.replace("\n"," ")
    #lua = lua.replace("\t"," ")
    print(lua)


fileIO = open('C:\\Users\\Oliver\\Desktop\\lua example.txt',"r")
lua = fileIO.read()
obsfucate(lua)

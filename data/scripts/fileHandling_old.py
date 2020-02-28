from data.scripts import utilities as util

class general:
    
    def checkSection(self, filePath, section):
        
        fileData = open(filePath, "r")
    
        check = False
        count = 0
        
        search = ("[" + section.capitalize() + "]")
        
        for line in fileData:
            
            if line[:-1] == search:
                
                check = True
                
                break
            
            else:
                
                check = False
                count += 1
                
        if check == False:
            
            count = -1
            
            fileData.close()
            
            return count
            
        else:
            
            fileData.close()
            
            return count
        
    def readFile(self, filePath):
    
        fileData = open(filePath, "r")
                
        lines = {}
        countLine = 0
        
        for line in fileData:
            
            lines[countLine] = line[:-1]
            
            countLine += 1
            
        return lines

class item:
    
    def get(self, filePath):
        
        count = general.checkSection(filePath, "item")
    
        lines = general.readFile(filePath)
        
        content = {}
        contentList = list()
        breakVar = 0
        itemCount = 0
        
        for entry in lines:
            
            if entry <= count:
                
                pass
            
            else:
            
                if lines[entry] == "":
                    
                    if breakVar == 1:
                        
                        break
                    
                    else:
                    
                        breakVar += 1
                    
                else:
                    
                    line = lines[entry]
                    
                    tmp = line.split(";")
                    
                    portList = tmp[3].split(",")
                    
                    itemName = (tmp[0].lower() + ".name")
                    itemBuy = (tmp[0].lower() + ".buy")
                    itemSell = (tmp[0].lower() + ".sell")
                    itemPort = (tmp[0].lower() + ".port")
                    itemAttribute = (tmp[0].lower() + ".attribute")
                    itemSubattribute = (tmp[0].lower() + ".subattribute")
                    
                    content[itemName] = tmp[0]
                    content[itemBuy] = tmp[1]
                    content[itemSell] = tmp[2]
                    content[itemPort] = portList
                    content[itemAttribute] = tmp[4]
                    content[itemSubattribute] = tmp[5]
                    
                    contentList.append(tmp[0].lower())
                    
                    itemCount += 1
        
        return content, contentList
    
    def set(self, filePath, name, buy, sell, ports, attribute, subattribute): #WIP
        
        count = general.checkSection(filePath, "item")
        
        lines =  general.readFile(filePath)
        
        itemName = (name + ".name")
        itemBuy = (name + ".buy")
        itemSell = (name + ".sell")
        itemPort = (name + ".port")
        itemAttribute = (name + ".attribute")
        itemSubattribute = (name + ".subattribute")
        
        for entry in lines:
            
            if entry <= count:
                
                pass
            
            else:
            
                if lines[entry] == "":
                    
                    if breakVar == 2:
                        
                        break
                    
                    else:
                    
                        pass
                    
                else:
                    
                    pass

class area:
    
    def get(self, filePath):
        
        count = general.checkSection(filePath, "area")
    
        lines = general.readFile(filePath)
        
        content = {}
        contentList = list()
        breakVar = 0
        areaCount = 0
        
        for entry in lines:
            
            if entry <= count:
                
                pass
            
            else:
            
                if lines[entry] == "":
                    
                    if breakVar == 1:
                        
                        break
                    
                    else:
                    
                        breakVar += 1
                    
                else:
                    
                    line = lines[entry]
                    
                    tmp = line.split(";")
                    
                    subareaList = tmp[1].split(",")
                    
                    areaName = (tmp[0].lower() + ".name")
                    areaSubarea = (tmp[0].lower() + ".subarea")
                    
                    content[areaName] = tmp[0]
                    content[areaSubarea] = subareaList
                    
                    contentList.append(tmp[0].lower())
                    
                    areaCount += 1
            
        return content, contentList

class subarea:
    
    def get(self, filePath):
        
        count = general.checkSection(filePath, "subarea")
    
        lines = general.readFile(filePath)
        
        content = {}
        contentList = list()
        breakVar = 0
        subareaCount = 0
        
        for entry in lines:
            
            if entry <= count:
                
                pass
            
            else:
            
                if lines[entry] == "":
                    
                    if breakVar == 1:
                        
                        break
                    
                    else:
                    
                        breakVar += 1
                    
                else:
                    
                    line = lines[entry]
                    
                    tmp = line.split(";")
                    
                    portsList = tmp[1].split(",")
                    
                    subareaName = (tmp[0].lower() + ".name")
                    subareaPort = (tmp[0].lower() + ".port")
                    
                    content[subareaName] = tmp[0]
                    content[subareaPort] = portsList
                    
                    contentList.append(tmp[0].lower())
                    
                    subareaCount += 1
            
        return content, contentList
    
class attribute:
    
    def get(self, filePath):
        
        count = general.checkSection(filePath, "attribute")
    
        lines = general.readFile(filePath)
        
        content = {}
        contentList = list()
        breakVar = 0
        attributeCount = 0
        
        for entry in lines:
            
            if entry <= count:
                
                pass
            
            else:
            
                if lines[entry] == "":
                    
                    if breakVar == 1:
                        
                        break
                    
                    else:
                    
                        breakVar += 1
                    
                else:
                    
                    line = lines[entry]
                    
                    tmp = line.split(";")
                    
                    subattributeList = tmp[1].split(",")
                    
                    attributeName = (tmp[0].lower() + ".name")
                    attributeSubattribute = (tmp[0].lower() + ".subattribute")
                    
                    content[attributeName] = tmp[0]
                    content[attributeSubattribute] = subattributeList
                    
                    contentList.append(tmp[0].lower())
                    
                    attributeCount += 1
                    
        return content, contentList

def getIniCont(filePath):
    
    content = {}
    
    fileData = open(filePath, "r")
    
    for line in fileData:
        
        d1, d2 = util.sepData(line)
        
        content[d1] = d2[:-1]
        
    fileData.close()
    
    return content

def getLang():
        
    activeSettings = getIniCont("data/settings.ini")
    
    langPack = ("data/lang/" + activeSettings["lang"] + ".ini")
    
    lang = getIniCont(langPack)
    
    return lang
    
if __name__ == '__main__':
    
    pass

















































# end
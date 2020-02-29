from data.scripts import utilities as util
import json

class general:

    def getIniCont(self, filePath):

        content = {}

        with open(filePath, "r") as file:

            for line in file:

                value1, value2 = util.sepData(line)

                content[value1] = value2[:-1]

        return content

    def getLang(self, filePath):

        activeSettings = self.getIniCont(filePath)

        langPack = ("data/lang/" + activeSettings["lang"] + ".ini")

        lang = self.getIniCont(langPack)

        return lang

class project:

    def load(self, filePath):

        with open(filePath, "r") as file:

            data = json.load(file)

        return data

        """itemData = item().get(filePath)
        areaData = area().get(filePath)
        sareaData = subarea().get(filePath)
        attrData = attribute().get(filePath)

        return itemData, areaData, sareaData, attrData

class item:

    def get(self, dataPath):

        if project == "None":

            return -1

        else:

            fileData = (dataPath)

            with open(fileData) as file:

                data = json.load(file)

            items = data["item"]

            return items

class area:

    def get(self, dataPath):

        if project == "None":

            return -1

        else:

            fileData = (dataPath)

            with open(fileData) as file:

                data = json.load(file)

            areas = data["area"]

            return areas

class subarea:

    def get(self, dataPath):

        if project == "None":

            return -1

        else:

            fileData = (dataPath)

            with open(fileData) as file:

                data = json.load(file)

            subareas = data["sarea"]

            return subareas

class attribute:

    def get(self, dataPath):

        if project == "None":

            return -1

        else:

            fileData = (dataPath)

            with open(fileData) as file:

                data = json.load(file)

            attributes = data["attr"]

            return attributes"""
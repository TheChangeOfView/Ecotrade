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

    def setIniCont(self, filePath, toWrite):

        #content = list()

        #content = toWrite.split("\n")

        with open(filePath, "w") as file:

            for line in toWrite:

                file.write(line)

    def getLang(self, filePath):

        activeSettings = self.getIniCont(filePath)

        langPack = ("data/lang/" + activeSettings["lang"] + ".ini")

        lang = self.getIniCont(langPack)

        return lang

class project:

    def load(self, filePath):

        try:

            with open(filePath, "r") as file:

                data = json.load(file)

        except:

            return -1

        return data

    def save(self, filePath, data):

        try:

            with open(filePath, "w") as file:

                json.dump(data, file)
            
        except:

            return -1

        return 0
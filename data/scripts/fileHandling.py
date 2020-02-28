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

class item:

    def get(self, project):

        if project == "None":

            return -1

        else:

            fileData = ("save/" + project + ".json")

            with open(fileData) as file:

                data = json.load(file)

            items = data["item"]

            return 0

class area:

    def get(self, project):

        if project == "None":

            return -1

        else:

            fileData = ("save/" + project + ".json")

            with open(fileData) as file:

                data = json.load(file)

            areas = data["area"]

            return 0

class subarea:

    def get(self, project):

        if project == "None":

            return -1

        else:

            fileData = ("save/" + project + ".json")

            with open(fileData) as file:

                data = json.load(file)

            subarea = data["sarea"]

            return 0

class attribute:

    def get(self, project):

        if project == "None":

            return -1

        else:

            fileData = ("save/" + project + ".json")

            with open(fileData) as file:

                data = json.load(file)

            attributes = data["attr"]

            return 0
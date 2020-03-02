######################################
# ---------------------------------- #
######################################

# --- Imports

import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
import os
import sys
from data.scripts import utilities as util
from data.scripts import fileHandling as hand

# --- Global Variables

infoPath = "data/info.ini"
settingsPath = "data/settings.ini"
projectData = {"name": None}
projectChanges = False
lang = dict()
eDestroy = 0

######################################
# ---------------------------------- #
######################################

def main(): # Main Function

    global lang

    lang = hand.general().getLang(settingsPath)

    root = tk.Tk()
    root.resizable(height = False, width = False)

    windowWidth = 1050
    windowHeight = 950
    
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)

    root.geometry("+{}+{}".format(positionRight, positionDown))

    mainScreen = scrMain(master = root)
    root.mainloop()

######################################
# ---------------------------------- #
######################################

class scrMain(): # Main GUI
    
    def __init__(self, master = None): # GUI Init
        
        #--- Initialize Variables
        
        info = hand.general().getIniCont(infoPath)
        
        activeFstSelect = ""
        activeSndSelect = ""
        activeTrdSelect = ""
        activeOffer = ""
        itemImage = tk.PhotoImage(file = "data/noImage.pgm")
        
        sortingOptions = (lang["titleItem"], lang["titleArea"], lang["titleSubarea"], lang["titlePort"], lang["titleAttribute"], lang["titleSubattribute"])
        
        #####################################
        # --------- Create Window --------- #
        #####################################

        self.master = master
        self.frame = ttk.Frame(self.master)
        
        # --- Master Settings
        
        master.title(info["name"] + " - v. " + info["ver"] + "." + info["subVer"])
        
        ########################################
        # --------- Creating Widgets --------- #
        ########################################
        
        # --- Listboxes Masterframe
        
        self.FRM_listboxes = ttk.Frame(self.frame)
        
        # --- First Listbox (Upper Left)
        
        self.LBL_stSelect = ttk.Label(self.FRM_listboxes, text = activeFstSelect)
        self.LBX_stSelect = tk.Listbox(self.FRM_listboxes, height = 22, width = 65, selectmode = "single", exportselection = False)
        self.SLB_stSelect = ttk.Scrollbar(self.FRM_listboxes, orient = tk.VERTICAL, command = self.LBX_stSelect.yview)
        self.LBX_stSelect["yscrollcommand"] = self.SLB_stSelect.set
        
        self.LBX_stSelect.bind("<<ListboxSelect>>", self.LBX_stSelect_callback)

        # --- Second Listbox (Upper Upper Right)
        
        self.LBL_ndSelect = ttk.Label(self.FRM_listboxes, text = activeSndSelect)
        self.LBX_ndSelect = tk.Listbox(self.FRM_listboxes, height = 11, width = 65, selectmode = "single", exportselection = False)
        self.SLB_ndSelect = ttk.Scrollbar(self.FRM_listboxes, orient = tk.VERTICAL, command = self.LBX_ndSelect.yview)
        self.LBX_ndSelect["yscrollcommand"] = self.SLB_ndSelect.set

        self.LBX_ndSelect.bind("<<ListboxSelect>>", self.LBX_ndSelect_callback)
        
        # --- Third Listbox (Lower Upper Right)
        
        self.LBL_rdSelect = ttk.Label(self.FRM_listboxes, text = activeTrdSelect)
        self.LBX_rdSelect = tk.Listbox(self.FRM_listboxes, height = 11, width = 65, selectmode = "single", exportselection = False)
        self.SLB_rdSelect = ttk.Scrollbar(self.FRM_listboxes, orient = tk.VERTICAL, command = self.LBX_rdSelect.yview)
        self.LBX_rdSelect["yscrollcommand"] = self.SLB_rdSelect.set

        self.LBX_rdSelect.bind("<<ListboxSelect>>", self.LBX_rdSelect_callback)

        # --- Offer Box (Lower) max. 35 char

        TRW_offerColumnList = (f"{lang['titleItem']} / {lang['titlePort']}", lang["titleBuy"], lang["titleSell"])

        self.TRW_offer = ttk.Treeview(self.FRM_listboxes, columns = TRW_offerColumnList, show = "headings", height = 25)

        self.TRW_offer.heading(0, text = TRW_offerColumnList[0])
        self.TRW_offer.column(0, width = 650)
        self.TRW_offer.heading(1, text = TRW_offerColumnList[1])
        self.TRW_offer.column(1, width = 75)
        self.TRW_offer.heading(2, text = TRW_offerColumnList[2])
        self.TRW_offer.column(2, width = 75)

        self.SLB_offer = ttk.Scrollbar(self.FRM_listboxes, orient = tk.VERTICAL, command = self.TRW_offer.yview)
        self.TRW_offer["yscrollcommand"] = self.SLB_offer.set

        self.TRW_offer.bind("<<TreeviewSelect>>", self.TRW_offer_callback)
        
        # --- Sorting Combobox
        
        self.LBL_sorting = ttk.Label(self.frame, text = lang["browserSort"])
        self.CBB_sorting = ttk.Combobox(self.frame, state = "readonly", width = 25, values = sortingOptions)       
        self.CBB_sorting.current(0)
        self.CBB_sorting.bind("<<ComboboxSelected>>", self.CBB_Sorting_callback)
        
        # --- Attributes Masterframe
        
        self.LBF_Attributes = ttk.Labelframe(self.frame, text = lang["attributesTitle"])
        
        # --- Attributes
        
        self.IMG_item = ttk.Label(self.LBF_Attributes, image = itemImage)
        self.IMG_item.image = itemImage
        
        self.FRM_value = ttk.Frame(self.LBF_Attributes)
        
        self.LBL_itemBuy = ttk.Label(self.FRM_value, text = lang["attributesBuy"])
        self.itemBuyActiveTextvariable = tk.StringVar()
        self.ETY_itemBuyActive = ttk.Entry(self.FRM_value, width = 12, state = "disabled", textvariable = self.itemBuyActiveTextvariable, justify = "center")
        
        self.LBL_itemSell = ttk.Label(self.FRM_value, text = lang["attributesSell"])
        self.itemSellActiveTextvariable = tk.StringVar()
        self.ETY_itemSellActive = ttk.Entry(self.FRM_value, width = 12, state = "disabled", textvariable = self.itemSellActiveTextvariable, justify = "center")
        
        self.FRM_name = ttk.Frame(self.LBF_Attributes)
        self.LBL_name = ttk.Label(self.FRM_name, text = lang["attributesItem"], width = 35)
        self.TXT_nameActive = tk.Text(self.FRM_name, width = 20, height = 3, state = "disabled")
        
        self.FRM_port = ttk.Frame(self.LBF_Attributes)
        self.LBL_port = ttk.Label(self.FRM_port, text = lang["attributesPort"], width = 35)
        self.TXT_portActive = tk.Text(self.FRM_port, width = 20, height = 3, state = "disabled")
        
        self.FRM_area = ttk.Frame(self.LBF_Attributes)
        self.LBL_area = ttk.Label(self.FRM_area, text = lang["attributesArea"], width = 35)
        self.TXT_areaActive = tk.Text(self.FRM_area, width = 20, height = 3, state = "disabled")
        
        self.FRM_subarea = ttk.Frame(self.LBF_Attributes)
        self.LBL_subarea = ttk.Label(self.FRM_subarea, text = lang["attributesSubarea"], width = 35)
        self.TXT_subareaActive = tk.Text(self.FRM_subarea, width = 20, height = 3, state = "disabled")
        
        self.FRM_attribute = ttk.Frame(self.LBF_Attributes)
        self.LBL_attribute = ttk.Label(self.FRM_attribute, text = lang["attributesAttribute"], width = 35)
        self.TXT_attributeActive = tk.Text(self.FRM_attribute, width = 20, height = 3, state = "disabled")
        
        self.FRM_subattribute = ttk.Frame(self.LBF_Attributes)
        self.LBL_subattribute = ttk.Label(self.FRM_subattribute, text = lang["attributesSubattribute"], width = 35)
        self.TXT_subattributeActive = tk.Text(self.FRM_subattribute, width = 20, height = 3, state = "disabled")
        
        # --- Buttons Masterframe
        
        self.FRM_buttons = ttk.Frame(self.frame)
        self.FRM_Subbuttons = ttk.Frame(self.FRM_buttons)
        
        # --- Buttons
        
        self.BTN_add = ttk.Button(self.FRM_buttons, text = lang["buttonObjectAdd"], width = 34, command = self.objectAdd)
        self.BTN_edit = ttk.Button(self.FRM_buttons, text = lang["buttonObjectEdit"], width = 16, command = self.objectEdit, state = "disabled")
        self.BTN_remove = ttk.Button(self.FRM_buttons, text = lang["buttonObjectRemove"], width = 16, command = self.objectRemove, state = "disabled")
        self.BTN_new = ttk.Button(self.FRM_Subbuttons, text = lang["buttonProjectNew"], width = 34, command = self.projectNew)
        self.BTN_save = ttk.Button(self.FRM_Subbuttons, text = lang["buttonProjectSave"], width = 16, command = None)
        self.BTN_load = ttk.Button(self.FRM_Subbuttons, text = lang["buttonProjectLoad"], width = 16, command = self.projectLoad)
        self.BTN_delete = ttk.Button(self.FRM_Subbuttons, text = lang["buttonProjectDelete"], width = 34, command = None)
        self.BTN_settings = ttk.Button(self.FRM_buttons, text = lang["buttonGeneralSettings"], width = 16, command = self.openSettings)
        self.BTN_quit = ttk.Button(self.FRM_buttons, text = lang["buttonGeneralQuit"], width = 16, command = self.programQuit)
        
        ######################################
        # --------- Allign Widgets --------- #
        ######################################
        
        # --- Master Grid
        
        self.frame.grid(column = 0, row = 0)
        
        # --- First Listbox (Upper Left)
        
        self.LBL_stSelect.grid(column = 0, row = 0, columnspan = 2)
        self.LBX_stSelect.grid(column = 0, row = 1, rowspan = 3, sticky = (tk.N, tk.S))
        self.SLB_stSelect.grid(column = 1, row = 1, rowspan = 3, sticky = (tk.N, tk.S))
        
        # --- Second Listbox (Upper Upper Right)
        
        self.LBL_ndSelect.grid(column = 3, row = 0, columnspan = 2)
        self.LBX_ndSelect.grid(column = 3, row = 1)
        self.SLB_ndSelect.grid(column = 4, row = 1, sticky = (tk.N, tk.S))
        
        # --- Third Listbox (Lower Upper Right)
        
        self.LBL_rdSelect.grid(column = 3, row = 2, columnspan = 2)
        self.LBX_rdSelect.grid(column = 3, row = 3)
        self.SLB_rdSelect.grid(column = 4, row = 3, sticky = (tk.N, tk.S))
        
        # --- Offer Box (Lower)
        
        self.TRW_offer.grid(column = 0, row = 4, columnspan = 4, sticky = (tk.W, tk.E), pady = 5)
        self.SLB_offer.grid(column = 4, row = 4, sticky = (tk.N, tk.S), pady = 5)
        
        # --- Listboxes Masterframe
        
        self.FRM_listboxes.grid(column = 1, row = 1, rowspan = 3, padx = 6)
        
        # --- Sorting Combobox
        
        self.LBL_sorting.grid(column = 2, row = 1, padx = 2, sticky = (tk.N))
        self.CBB_sorting.grid(column = 3, row = 1, padx = 2, sticky = (tk.N))
        
        # --- Attributes
        
        self.IMG_item.grid(column = 0, row = 0, pady = 20)
        
        self.LBL_itemBuy.grid(column = 0, row = 0)
        self.ETY_itemBuyActive.grid(column = 0, row = 1)
        self.LBL_itemSell.grid(column = 1, row = 0)
        self.ETY_itemSellActive.grid(column = 1, row = 1)
        
        self.FRM_value.grid(column = 0, row = 1, sticky = (tk.N), pady = 2) 
        
        self.LBL_name.grid(column = 0, row = 0, sticky = (tk.W))
        self.TXT_nameActive.grid(column = 0, row = 1)
        
        self.FRM_name.grid(column = 0, row = 2, sticky = (tk.N), pady = 2) 
        
        self.LBL_port.grid(column = 0, row = 0, sticky = (tk.W))
        self.TXT_portActive.grid(column = 0, row = 1)
        
        self.FRM_port.grid(column = 0, row = 3, sticky = (tk.N), pady = 2)
        
        self.LBL_area.grid(column = 0, row = 0, sticky = (tk.W))
        self.TXT_areaActive.grid(column = 0, row = 1)
        
        self.FRM_area.grid(column = 0, row = 4, sticky = (tk.N), pady = 2)
        
        self.LBL_subarea.grid(column = 0, row = 0, sticky = (tk.W))
        self.TXT_subareaActive.grid(column = 0, row = 1)
        
        self.FRM_subarea.grid(column = 0, row = 5, sticky = (tk.N), pady = 2)
        
        self.LBL_attribute.grid(column = 0, row = 0, sticky = (tk.W))
        self.TXT_attributeActive.grid(column = 0, row = 1)
        
        self.FRM_attribute.grid(column = 0, row = 6, sticky = (tk.N), pady = 2)
        
        self.LBL_subattribute.grid(column = 0, row = 0, sticky = (tk.W))
        self.TXT_subattributeActive.grid(column = 0, row = 1)
        
        self.FRM_subattribute.grid(column = 0, row = 7, sticky = (tk.N), pady = 2)
        
        # --- Attributes Masterframe
        
        self.LBF_Attributes.grid(column = 2, row = 2, columnspan = 2, padx = 2, sticky = (tk.N, tk.S))
        
        # --- Buttons
        
        self.BTN_add.grid(column = 1, row = 1, columnspan = 2)
        self.BTN_edit.grid(column = 1, row = 2, sticky = (tk.W))
        self.BTN_remove.grid(column = 2, row = 2, sticky = (tk.E))

        self.BTN_new.grid(column = 1, row = 1, columnspan = 2)
        self.BTN_save.grid(column = 1, row = 2, sticky = (tk.W))
        self.BTN_load.grid(column = 2, row = 2, sticky = (tk.E))
        self.BTN_delete.grid(column = 1, row = 3, columnspan = 2)

        self.BTN_settings.grid(column = 1, row = 4, sticky = (tk.W))
        self.BTN_quit.grid(column = 2, row = 4, sticky = (tk.E))
        
        # --- Buttons Masterframe

        self.FRM_Subbuttons.grid(column = 1, row = 3, columnspan = 2, pady = 5)
        
        self.FRM_buttons.grid(column = 2, row = 3, columnspan = 2, pady = 12, sticky = (tk.S))
        
        # --- Final Pack
        
        self.frame.pack()

        self.LBX_stSelect.delete(0, tk.END)
        self.LBX_ndSelect.delete(0, tk.END)
        self.LBX_rdSelect.delete(0, tk.END)
        self.TRW_offer.delete(*self.TRW_offer.get_children())

        projectData.clear()

        projectData["name"] = "active(None)"

        projectData["item"] = dict()
        projectData["area"] = dict()
        projectData["sarea"] = dict()
        projectData["port"] = dict()
        projectData["attr"] = dict()
        projectData["sattr"] = dict()

        self.browserSetFirstSection()
        self.setItemInfo(None)

        self.CBB_Sorting_callback(None)

    def CBB_Sorting_callback(self, event):
        
        value = self.CBB_sorting.current()

        self.LBX_stSelect.config(state = "normal")
        self.LBX_ndSelect.config(state = "normal")
        self.LBX_rdSelect.config(state = "normal")

        self.LBX_stSelect.delete(0, tk.END)
        self.LBX_ndSelect.delete(0, tk.END)
        self.LBX_rdSelect.delete(0, tk.END)
        self.TRW_offer.delete(*self.TRW_offer.get_children())
        
        if value == 0: #Item
            
            self.LBL_stSelect.config(text = lang["titleItem"])
            self.LBL_ndSelect.config(text = "-")
            self.LBL_rdSelect.config(text = "-")
            
            self.LBX_stSelect.config(state = "normal")
            self.LBX_ndSelect.config(state = "disabled")
            self.LBX_rdSelect.config(state = "disabled")
        
        elif value == 1: #Area
            
            self.LBL_stSelect.config(text = lang["titleArea"])
            self.LBL_ndSelect.config(text = lang["titleSubarea"])
            self.LBL_rdSelect.config(text = lang["titlePort"])
            
            self.LBX_stSelect.config(state = "normal")
            self.LBX_ndSelect.config(state = "normal")
            self.LBX_rdSelect.config(state = "normal")
        
        elif value == 2: #Subarea
            
            self.LBL_stSelect.config(text = lang["titleSubarea"])
            self.LBL_ndSelect.config(text = lang["titlePort"])
            self.LBL_rdSelect.config(text = "-")
            
            self.LBX_stSelect.config(state = "normal")
            self.LBX_ndSelect.config(state = "normal")
            self.LBX_rdSelect.config(state = "disabled")
        
        elif value == 3: #Port
            
            self.LBL_stSelect.config(text = lang["titlePort"])
            self.LBL_ndSelect.config(text = "-")
            self.LBL_rdSelect.config(text = "-")
            
            self.LBX_stSelect.config(state = "normal")
            self.LBX_ndSelect.config(state = "disabled")
            self.LBX_rdSelect.config(state = "disabled")
        
        elif value == 4: #Attribute
            
            self.LBL_stSelect.config(text = lang["titleAttribute"])
            self.LBL_ndSelect.config(text = lang["titleSubattribute"])
            self.LBL_rdSelect.config(text = lang["titleItem"])
            
            self.LBX_stSelect.config(state = "normal")
            self.LBX_ndSelect.config(state = "normal")
            self.LBX_rdSelect.config(state = "normal")
        
        elif value == 5: #Subattribute
            
            self.LBL_stSelect.config(text = lang["titleSubattribute"])
            self.LBL_ndSelect.config(text = lang["titleItem"])
            self.LBL_rdSelect.config(text = "-")
            
            self.LBX_stSelect.config(state = "normal")
            self.LBX_ndSelect.config(state = "normal")
            self.LBX_rdSelect.config(state = "disabled")
        
        else:
            
            pass

        if projectData["name"] == None:

            return -1

        else:

            self.browserSetFirstSection()

        self.setItemInfo(None)
        self.BTN_edit.config(state = "disabled")
        self.BTN_remove.config(state = "disabled")

    def LBX_stSelect_callback(self, event):

        if self.LBX_stSelect.curselection() == ():

            return -1

        else:

            if self.CBB_sorting.current() == 0: # - Item

                #clean up Sections

                self.LBX_ndSelect.delete(0, tk.END)
                self.LBX_rdSelect.delete(0, tk.END)
                self.TRW_offer.delete(*self.TRW_offer.get_children())

                # get ID of selected Item

                allItems = self.LBX_stSelect.get(0, tk.END)
                selectionIndex = self.LBX_stSelect.curselection()
                selectionList = [allItems[item] for item in selectionIndex]
                selection = selectionList[0]

                for entry in projectData["item"]:

                    if projectData["item"][entry]["name"] == selection:

                        itemID = entry

                insertList = list()

                # get needed data from available ports

                for port in projectData["item"][itemID]["port"]:

                    value = projectData["item"][itemID]["port"][port]

                    buy, sell = value.split("-")

                    insertList.append((port, buy, sell))

                # insert data into offeringlist

                for entry in insertList:

                    self.TRW_offer.insert("", "end", values = entry)

                ###############################
                #---------setItemInfo---------#
                ###############################

                item = {

                    "name" : projectData["item"][itemID]["name"],
                    "image" : projectData["item"][itemID]["image"],
                    "port" : "-",
                    "buy" : "-",
                    "sell" : "-",
                    "attr" : projectData["item"][itemID]["attr"],
                    "sattr" : projectData["item"][itemID]["sattr"],
                    "sarea" : "-",
                    "area" : "-"

                }

                self.setItemInfo(item)

                self.BTN_edit.config(state = "normal")
                self.BTN_remove.config(state = "normal")

            elif self.CBB_sorting.current() == 1: # - Area

                self.LBX_ndSelect.delete(0, tk.END)
                self.LBX_rdSelect.delete(0, tk.END)
                self.TRW_offer.delete(*self.TRW_offer.get_children())

                allAreas = self.LBX_stSelect.get(0, tk.END)
                selectionIndex = self.LBX_stSelect.curselection()
                selectionList = [allAreas[area] for area in selectionIndex]
                selection = selectionList[0]

                if selection == lang["generalAll"]:

                    sortList = list()

                    for entry in projectData["sarea"]:

                        sortList.append(projectData["sarea"][entry]["name"])

                    sortList.sort()

                    if len(projectData["sarea"]) > 1:

                        self.LBX_ndSelect.insert(tk.END, lang["generalAll"])

                    for entry in sortList:

                        self.LBX_ndSelect.insert(tk.END, entry)

                    ###############################
                    #---------setItemInfo---------#
                    ###############################

                    self.setItemInfo(None)

                    self.BTN_edit.config(state = "disabled")
                    self.BTN_remove.config(state = "disabled")

                else:

                    for entry in projectData["area"]:

                        if projectData["area"][entry]["name"] == selection:

                            areaID = entry

                    sortList = list()

                    for entry in projectData["area"][areaID]["sarea"]:

                        sortList.append(entry)

                    if len(sortList) > 1:

                        self.LBX_ndSelect.insert(tk.END, lang["generalAll"])

                    sortList.sort()

                    for entry in sortList:

                        self.LBX_ndSelect.insert(tk.END, entry)

                    ###############################
                    #---------setItemInfo---------#
                    ###############################

                    item = {

                        "name" : "-",
                        "image" : "None",
                        "port" : "-",
                        "buy" : "-",
                        "sell" : "-",
                        "attr" : "-",
                        "sattr" : "-",
                        "sarea" : "-",
                        "area" : projectData["area"][areaID]["name"]

                    }

                    self.setItemInfo(item)

                    self.BTN_edit.config(state = "normal")
                    self.BTN_remove.config(state = "normal")

            elif self.CBB_sorting.current() == 2: # - Subarea

                #clean up Sections

                self.LBX_ndSelect.delete(0, tk.END)
                self.LBX_rdSelect.delete(0, tk.END)
                self.TRW_offer.delete(*self.TRW_offer.get_children())

                # get ID of selected Item

                allSarea = self.LBX_stSelect.get(0, tk.END)
                selectionIndex = self.LBX_stSelect.curselection()
                selectionList = [allSarea[sarea] for sarea in selectionIndex]
                selection = selectionList[0]

                if selection == lang["generalAll"]:

                    sortList = list()

                    for entry in projectData["port"]:

                        sortList.append(projectData["port"][entry]["name"])

                    sortList.sort()

                    for entry in sortList:

                        self.LBX_ndSelect.insert(tk.END, entry)

                    ###############################
                    #---------setItemInfo---------#
                    ###############################

                    self.setItemInfo(None)

                    self.BTN_edit.config(state = "disabled")
                    self.BTN_remove.config(state = "disabled")
                
                else:

                    for entry in projectData["sarea"]:

                        if projectData["sarea"][entry]["name"] == selection:

                            sareaID = entry

                    sortList = list()

                    for entry in projectData["sarea"][sareaID]["port"]:

                        sortList.append(entry)

                    sortList.sort()

                    for entry in sortList:

                        self.LBX_ndSelect.insert(tk.END, entry)

                    ###############################
                    #---------setItemInfo---------#
                    ###############################

                    for area in projectData["area"]:

                        for sarea in projectData["area"][area]["sarea"]:

                            if sarea == projectData["sarea"][sareaID]["name"]:

                                sareaMaster = projectData["area"][area]["name"]

                    item = {

                        "name" : "-",
                        "image" : "None",
                        "port" : "-",
                        "buy" : "-",
                        "sell" : "-",
                        "attr" : "-",
                        "sattr" : "-",
                        "sarea" : projectData["sarea"][sareaID]["name"],
                        "area" : sareaMaster

                    }

                    self.setItemInfo(item)

                    self.BTN_edit.config(state = "normal")
                    self.BTN_remove.config(state = "normal")

            elif self.CBB_sorting.current() == 3: # - Port

                # clean up Sections

                self.LBX_ndSelect.delete(0, tk.END)
                self.LBX_rdSelect.delete(0, tk.END)
                self.TRW_offer.delete(*self.TRW_offer.get_children())

                # get selected port

                allPorts = self.LBX_stSelect.get(0, tk.END)
                selectionIndex = self.LBX_stSelect.curselection()
                selectionList = [allPorts[port] for port in selectionIndex]
                selection = selectionList[0]

                itemList = list()
                insertList = list()

                # check items for port availabilty - return list of items contained in active port

                for item in projectData["item"]:

                    ports = projectData["item"][item]["port"]

                    for entry in ports:

                        if entry == selection:

                            itemList.append(item)

                # get needed data from available items (name, buy-value, sell-value)

                for entry in itemList:

                    name = projectData["item"][entry]["name"]

                    value = projectData["item"][entry]["port"][selection]
                    
                    buy, sell = value.split("-")

                    insertList.append((name, buy, sell))

                # insert data into offeringlist

                for entry in insertList:

                    self.TRW_offer.insert("", "end", values = entry)

                ###############################
                #---------setItemInfo---------#
                ###############################

                for sarea in projectData["sarea"]:

                    for entry in projectData["sarea"][sarea]["port"]:

                        if entry == selection:

                            portSarea = projectData["sarea"][sarea]["name"]

                for area in projectData["area"]:

                    for entry in projectData["area"][area]["sarea"]:

                        if entry == portSarea:

                            portArea = projectData["area"][area]["name"]

                item = {

                    "name" : "-",
                    "image" : "None",
                    "port" : selection,
                    "buy" : "-",
                    "sell" : "-",
                    "attr" : "-",
                    "sattr" : "-",
                    "sarea" : portSarea,
                    "area" : portArea

                }

                self.setItemInfo(item)

                self.BTN_edit.config(state = "normal")
                self.BTN_remove.config(state = "normal")

            elif self.CBB_sorting.current() == 4: # - Attribute

                self.LBX_ndSelect.delete(0, tk.END)
                self.LBX_rdSelect.delete(0, tk.END)
                self.TRW_offer.delete(*self.TRW_offer.get_children())

                allAttrs = self.LBX_stSelect.get(0, tk.END)
                selectionIndex = self.LBX_stSelect.curselection()
                selectionList = [allAttrs[attr] for attr in selectionIndex]
                selection = selectionList[0]

                if selection == lang["generalAll"]:

                    sortList = list()

                    for entry in projectData["sattr"]:

                        sortList.append(projectData["sattr"][entry]["name"])

                    sortList.sort()

                    if len(projectData["sattr"]) > 1:

                        self.LBX_ndSelect.insert(tk.END, lang["generalAll"])
                    
                    for entry in sortList:

                        self.LBX_ndSelect.insert(tk.END, entry)

                    ###############################
                    #---------setItemInfo---------#
                    ###############################

                    self.setItemInfo(None)

                    self.BTN_edit.config(state = "disabled")
                    self.BTN_remove.config(state = "disabled")

                else:

                    for entry in projectData["attr"]:

                        if projectData["attr"][entry]["name"] == selection:

                            attrID = entry

                    sortList = list()

                    for entry in projectData["attr"][attrID]["sattr"]:

                        sortList.append(entry)

                    sortList.sort()

                    if len(sortList) > 1:

                        self.LBX_ndSelect.insert(tk.END, lang["generalAll"])

                    for entry in sortList:

                        self.LBX_ndSelect.insert(tk.END, entry)

                    ###############################
                    #---------setItemInfo---------#
                    ###############################

                    item = {

                        "name" : "-",
                        "image" : "None",
                        "port" : "-",
                        "buy" : "-",
                        "sell" : "-",
                        "attr" : projectData["attr"][attrID]["name"],
                        "sattr" : "-",
                        "sarea" : "-",
                        "area" : "-"

                    }

                    self.setItemInfo(item)

                    self.BTN_edit.config(state = "normal")
                    self.BTN_remove.config(state = "normal")

            elif self.CBB_sorting.current() == 5: # - Subttribute

                self.LBX_ndSelect.delete(0, tk.END)
                self.LBX_rdSelect.delete(0, tk.END)
                self.TRW_offer.delete(*self.TRW_offer.get_children())

                allSattrs = self.LBX_stSelect.get(0, tk.END)
                selectionIndex = self.LBX_stSelect.curselection()
                selectionList = [allSattrs[sattr] for sattr in selectionIndex]
                selection = selectionList[0]

                itemList = list()

                # check items for subattribute availability - return list of items contained in active subattribute

                if selection == lang["generalAll"]:

                    sortList = list()

                    for entry in projectData["item"]:

                        sortList.append(projectData["item"][entry]["name"])

                    sortList.sort()

                    for entry in sortList:

                        self.LBX_ndSelect.insert(tk.END, entry)

                    ###############################
                    #---------setItemInfo---------#
                    ###############################

                    self.setItemInfo(None)

                    self.BTN_edit.config(state = "disabled")
                    self.BTN_remove.config(state = "disabled")

                else:

                    for item in projectData["item"]:

                        if projectData["item"][item]["sattr"] == selection:

                            itemList.append(item)

                    sortList = list()

                    for entry in itemList:

                        sortList.append(projectData["item"][entry]["name"])

                    sortList.sort()

                    for entry in sortList:

                        self.LBX_ndSelect.insert(tk.END, entry)

                    ###############################
                    #---------setItemInfo---------#
                    ###############################

                    for entry in projectData["sattr"]:

                            if projectData["sattr"][entry]["name"] == selection:

                                sattrID = entry

                    for attr in projectData["attr"]:

                        for sattr in projectData["attr"][attr]["sattr"]:

                            if sattr == projectData["sattr"][sattrID]["name"]:

                                sattrMaster = projectData["attr"][attr]["name"]

                    item = {

                        "name" : "-",
                        "image" : "None",
                        "port" : "-",
                        "buy" : "-",
                        "sell" : "-",
                        "attr" : sattrMaster,
                        "sattr" : projectData["sattr"][sattrID]["name"],
                        "sarea" : "-",
                        "area" : "-"

                    }

                    self.setItemInfo(item)

                    self.BTN_edit.config(state = "normal")
                    self.BTN_remove.config(state = "normal")

    def LBX_ndSelect_callback(self, event):

        if self.LBX_ndSelect.curselection() == ():

            return -1

        else:

            if self.CBB_sorting.current() == 0: # - Item - None

                pass

            elif self.CBB_sorting.current() == 1: # - Area - Subarea

                #clean up Sections

                self.LBX_rdSelect.delete(0, tk.END)
                self.TRW_offer.delete(*self.TRW_offer.get_children())

                # get ID of selected Item

                allSarea = self.LBX_stSelect.get(0, tk.END)
                selectionIndex = self.LBX_stSelect.curselection()
                selectionList = [allSarea[sarea] for sarea in selectionIndex]
                selectionFirst = selectionList[0]

                allSarea = self.LBX_ndSelect.get(0, tk.END)
                selectionIndex = self.LBX_ndSelect.curselection()
                selectionList = [allSarea[sarea] for sarea in selectionIndex]
                selection = selectionList[0]

                if selection == lang["generalAll"]:

                    if selectionFirst == lang["generalAll"]:

                        sortList = list()

                        for entry in projectData["port"]:

                            sortList.append(projectData["port"][entry]["name"])

                        sortList.sort()

                        for entry in sortList:

                            self.LBX_rdSelect.insert(tk.END, entry)

                        ###############################
                        #---------setItemInfo---------#
                        ###############################

                        self.setItemInfo(None)

                    else:

                        for entry in projectData["area"]:

                            if projectData["area"][entry]["name"] == selectionFirst:

                                areaID = entry

                        sareaList = projectData["area"][areaID]["sarea"]

                        portIDList = list()

                        for sarea in sareaList:

                            for entry in projectData["sarea"]:

                                if projectData["sarea"][entry]["name"] == sarea:

                                    sareaID = entry

                                    portIDList.append(sareaID)

                        portList = list()

                        for entry in portIDList:

                            for portName in projectData["sarea"][entry]["port"]:

                                portList.append(portName)

                        portList.sort()

                        for entry in portList:

                            self.LBX_rdSelect.insert(tk.END, entry)

                        ###############################
                        #---------setItemInfo---------#
                        ###############################

                        item = {

                            "name" : "-",
                            "image" : "None",
                            "port" : "-",
                            "buy" : "-",
                            "sell" : "-",
                            "attr" : "-",
                            "sattr" : "-",
                            "sarea" : "-",
                            "area" : selectionFirst

                        }

                        self.setItemInfo(item)
                
                    self.BTN_edit.config(state = "disabled")
                    self.BTN_remove.config(state = "disabled")

                else:

                    for entry in projectData["sarea"]:

                        if projectData["sarea"][entry]["name"] == selection:

                            sareaID = entry

                    sortList = list()

                    for entry in projectData["sarea"][sareaID]["port"]:

                        sortList.append(entry)

                    sortList.sort()

                    for entry in sortList:

                        self.LBX_rdSelect.insert(tk.END, entry)

                    ###############################
                    #---------setItemInfo---------#
                    ###############################

                    if selectionFirst == lang["generalAll"]:

                        for area in projectData["area"]:

                            for entry in projectData["area"][area]["sarea"]:

                                if entry == selection:

                                    sareaMaster = projectData["area"][area]["name"]

                    else:

                        sareaMaster = selectionFirst

                    item = {

                        "name" : "-",
                        "image" : "None",
                        "port" : "-",
                        "buy" : "-",
                        "sell" : "-",
                        "attr" : "-",
                        "sattr" : "-",
                        "sarea" : selection,
                        "area" : sareaMaster

                    }

                    self.setItemInfo(item)

                    self.BTN_edit.config(state = "normal")
                    self.BTN_remove.config(state = "normal")

            elif self.CBB_sorting.current() == 2: # - Subarea - Port

                #clean up Sections

                self.LBX_rdSelect.delete(0, tk.END)
                self.TRW_offer.delete(*self.TRW_offer.get_children())

                # get ID of selected Item

                allPort = self.LBX_ndSelect.get(0, tk.END)
                selectionIndex = self.LBX_ndSelect.curselection()
                selectionList = [allPort[port] for port in selectionIndex]
                selection = selectionList[0]

                itemList = list()
                insertList = list()

                # check items for port availabilty - return list of items contained in active port

                for item in projectData["item"]:

                    ports = projectData["item"][item]["port"]

                    for entry in ports:

                        if entry == selection:

                            itemList.append(item)

                # get needed data from available items (name, buy-value, sell-value)

                for entry in itemList:

                    name = projectData["item"][entry]["name"]

                    value = projectData["item"][entry]["port"][selection]
                    
                    buy, sell = value.split("-")

                    insertList.append((name, buy, sell))

                # insert data into offeringlist

                for entry in insertList:

                    self.TRW_offer.insert("", "end", values = entry)

                ###############################
                #---------setItemInfo---------#
                ###############################

                allSarea = self.LBX_stSelect.get(0, tk.END)
                selectionIndex = self.LBX_stSelect.curselection()
                selectionList = [allSarea[sarea] for sarea in selectionIndex]
                activeSarea = selectionList[0]

                if activeSarea == lang["generalAll"]:

                    for sarea in projectData["sarea"]:

                        for entry in projectData["sarea"][sarea]["port"]:

                            if entry == selection:

                                portSarea = projectData["sarea"][sarea]["name"]

                else:

                    portSarea = activeSarea

                for area in projectData["area"]:

                    for entry in projectData["area"][area]["sarea"]:

                        if entry == portSarea:

                            portArea = projectData["area"][area]["name"]

                item = {

                    "name" : "-",
                    "image" : "None",
                    "port" : selection,
                    "buy" : "-",
                    "sell" : "-",
                    "attr" : "-",
                    "sattr" : "-",
                    "sarea" : portSarea,
                    "area" : portArea

                }

                self.setItemInfo(item)

                self.BTN_edit.config(state = "normal")
                self.BTN_remove.config(state = "normal")

            elif self.CBB_sorting.current() == 3: # - Port - None

                pass

            elif self.CBB_sorting.current() == 4: # - Attribute - Subattribute

                #clean up Sections

                self.LBX_rdSelect.delete(0, tk.END)
                self.TRW_offer.delete(*self.TRW_offer.get_children())

                allSattr = self.LBX_stSelect.get(0, tk.END)
                selectionIndex = self.LBX_stSelect.curselection()
                selectionList = [allSattr[sattr] for sattr in selectionIndex]
                selectionFirst = selectionList[0]

                allSattr = self.LBX_ndSelect.get(0, tk.END)
                selectionIndex = self.LBX_ndSelect.curselection()
                selectionList = [allSattr[sattr] for sattr in selectionIndex]
                selection = selectionList[0]

                if selection == lang["generalAll"]:

                    if selectionFirst == lang["generalAll"]:

                        sortList = list()

                        for entry in projectData["item"]:

                            sortList.append(projectData["item"][entry]["name"])

                        sortList.sort()

                        for entry in sortList:

                            self.LBX_rdSelect.insert(tk.END, entry)

                        ###############################
                        #---------setItemInfo---------#
                        ###############################

                        self.setItemInfo(None)

                    else:

                        for entry in projectData["attr"]:

                            if projectData["attr"][entry]["name"] == selectionFirst:

                                attrID = entry

                        sattrList = projectData["attr"][attrID]["sattr"]

                        itemList = list()

                        for entry in sattrList:

                            for item in projectData["item"]:

                                if projectData["item"][item]["sattr"] == entry:

                                    itemList.append(item)

                        sortList = list()

                        for entry in itemList:

                            sortList.append(projectData["item"][entry]["name"])

                        sortList.sort()

                        for entry in sortList:

                            self.LBX_rdSelect.insert(tk.END, entry)

                        ###############################
                        #---------setItemInfo---------#
                        ###############################

                        item = {

                            "name" : "-",
                            "image" : "None",
                            "port" : "-",
                            "buy" : "-",
                            "sell" : "-",
                            "attr" : selectionFirst,
                            "sattr" : "-",
                            "sarea" : "-",
                            "area" : "-"

                        }

                        self.setItemInfo(item)
                
                    self.BTN_edit.config(state = "disabled")
                    self.BTN_remove.config(state = "disabled")

                else:

                    itemList = list()

                    for item in projectData["item"]:

                        if projectData["item"][item]["sattr"] == selection:

                            itemList.append(item)

                    sortList = list()

                    for entry in itemList:

                        sortList.append(projectData["item"][entry]["name"])

                    sortList.sort()

                    for entry in sortList:

                        self.LBX_rdSelect.insert(tk.END, entry)

                    ###############################
                    #---------setItemInfo---------#
                    ###############################

                    if selectionFirst == lang["generalAll"]:

                        for attr in projectData["attr"]:

                            for entry in projectData["attr"][attr]["sattr"]:

                                if entry == selection:

                                    sattrMaster = projectData["attr"][attr]["name"]

                    else:

                        sattrMaster = selectionFirst

                    item = {

                        "name" : "-",
                        "image" : "None",
                        "port" : "-",
                        "buy" : "-",
                        "sell" : "-",
                        "attr" : sattrMaster,
                        "sattr" : selection,
                        "sarea" : "-",
                        "area" : "-"

                    }

                    self.setItemInfo(item)

                    self.BTN_edit.config(state = "normal")
                    self.BTN_remove.config(state = "normal")

            elif self.CBB_sorting.current() == 5: # - Subttribute - Item

                #clean up Sections

                self.LBX_rdSelect.delete(0, tk.END)
                self.TRW_offer.delete(*self.TRW_offer.get_children())

                # get ID of selected Item

                allItem = self.LBX_ndSelect.get(0, tk.END)
                selectionIndex = self.LBX_ndSelect.curselection()
                selectionList = [allItem[item] for item in selectionIndex]
                selection = selectionList[0]

                for entry in projectData["item"]:

                    if projectData["item"][entry]["name"] == selection:

                        itemID = entry

                insertList = list()

                # get needed data from available ports

                for port in projectData["item"][itemID]["port"]:

                    value = projectData["item"][itemID]["port"][port]

                    buy, sell = value.split("-")

                    insertList.append((port, buy, sell))

                # insert data into offeringlist

                for entry in insertList:

                    self.TRW_offer.insert("", "end", values = entry)

                ###############################
                #---------setItemInfo---------#
                ###############################

                item = {

                    "name" : projectData["item"][itemID]["name"],
                    "image" : projectData["item"][itemID]["image"],
                    "port" : "-",
                    "buy" : "-",
                    "sell" : "-",
                    "attr" : projectData["item"][itemID]["attr"],
                    "sattr" : projectData["item"][itemID]["sattr"],
                    "sarea" : "-",
                    "area" : "-"

                }

                self.setItemInfo(item)

                self.BTN_edit.config(state = "normal")
                self.BTN_remove.config(state = "normal")

    def LBX_rdSelect_callback(self, event):

        if self.LBX_rdSelect.curselection() == ():

            return -1

        else:

            if self.CBB_sorting.current() == 0: # - Item - None - None

                pass

            elif self.CBB_sorting.current() == 1: # - Area - Subarea - Port

                #clean up Sections

                self.TRW_offer.delete(*self.TRW_offer.get_children())

                # get ID of selected Item

                allPort = self.LBX_rdSelect.get(0, tk.END)
                selectionIndex = self.LBX_rdSelect.curselection()
                selectionList = [allPort[port] for port in selectionIndex]
                selection = selectionList[0]

                itemList = list()
                insertList = list()

                # check items for port availabilty - return list of items contained in active port

                for item in projectData["item"]:

                    ports = projectData["item"][item]["port"]

                    for entry in ports:

                        if entry == selection:

                            itemList.append(item)

                # get needed data from available items (name, buy-value, sell-value)

                for entry in itemList:

                    name = projectData["item"][entry]["name"]

                    value = projectData["item"][entry]["port"][selection]
                    
                    buy, sell = value.split("-")

                    insertList.append((name, buy, sell))

                # insert data into offeringlist

                for entry in insertList:

                    self.TRW_offer.insert("", "end", values = entry)

                ###############################
                #---------setItemInfo---------#
                ###############################

                for sarea in projectData["sarea"]:

                    for entry in projectData["sarea"][sarea]["port"]:

                        if entry == selection:

                            portSarea = projectData["sarea"][sarea]["name"]

                for area in projectData["area"]:

                    for entry in projectData["area"][area]["sarea"]:

                        if entry == portSarea:

                            portArea = projectData["area"][area]["name"]

                item = {

                    "name" : "-",
                    "image" : "None",
                    "port" : selection,
                    "buy" : "-",
                    "sell" : "-",
                    "attr" : "-",
                    "sattr" : "-",
                    "sarea" : portSarea,
                    "area" : portArea

                }

                self.setItemInfo(item)

                self.BTN_edit.config(state = "normal")
                self.BTN_remove.config(state = "normal")

            elif self.CBB_sorting.current() == 2: # - Subarea - Port - None

                pass

            elif self.CBB_sorting.current() == 3: # - Port - None - None

                pass

            elif self.CBB_sorting.current() == 4: # - Attribute - Subattribute - Item

                #clean up Sections

                self.TRW_offer.delete(*self.TRW_offer.get_children())

                # get ID of selected Item

                allItem = self.LBX_rdSelect.get(0, tk.END)
                selectionIndex = self.LBX_rdSelect.curselection()
                selectionList = [allItem[item] for item in selectionIndex]
                selection = selectionList[0]

                for entry in projectData["item"]:

                    if projectData["item"][entry]["name"] == selection:

                        itemID = entry

                insertList = list()

                # get needed data from available ports

                for port in projectData["item"][itemID]["port"]:

                    value = projectData["item"][itemID]["port"][port]

                    buy, sell = value.split("-")

                    insertList.append((port, buy, sell))

                # insert data into offeringlist

                for entry in insertList:

                    self.TRW_offer.insert("", "end", values = entry)

                ###############################
                #---------setItemInfo---------#
                ###############################

                item = {

                    "name" : projectData["item"][itemID]["name"],
                    "image" : projectData["item"][itemID]["image"],
                    "port" : "-",
                    "buy" : "-",
                    "sell" : "-",
                    "attr" : projectData["item"][itemID]["attr"],
                    "sattr" : projectData["item"][itemID]["sattr"],
                    "sarea" : "-",
                    "area" : "-"

                }

                self.setItemInfo(item)

                self.BTN_edit.config(state = "normal")
                self.BTN_remove.config(state = "normal")

            elif self.CBB_sorting.current() == 5: # - Subttribute - Item - None

                pass

    def TRW_offer_callback(self, event):

        active = self.TRW_offer.selection()

        entry = list(dict(self.TRW_offer.item(active))["values"])[0]

        if self.CBB_sorting.get() == lang["titlePort"] or self.CBB_sorting.get() == lang["titleArea"] or self.CBB_sorting.get() == lang["titleSubarea"]:

            for item in projectData["item"]:

                if projectData["item"][item]["name"] == entry:

                    itemID = item

            if self.CBB_sorting.get() == lang["titlePort"]:

                allItems = self.LBX_stSelect.get(0, tk.END)
                selectionIndex = self.LBX_stSelect.curselection()
                selectionList = [allItems[item] for item in selectionIndex]
                activePort = selectionList[0]

            elif self.CBB_sorting.get() == lang["titleArea"]:

                allItems = self.LBX_rdSelect.get(0, tk.END)
                selectionIndex = self.LBX_rdSelect.curselection()
                selectionList = [allItems[item] for item in selectionIndex]
                activePort = selectionList[0]

            elif self.CBB_sorting.get() == lang["titleSubarea"]:

                allItems = self.LBX_ndSelect.get(0, tk.END)
                selectionIndex = self.LBX_ndSelect.curselection()
                selectionList = [allItems[item] for item in selectionIndex]
                activePort = selectionList[0]

            else:

                return -1

            for port in projectData["item"][itemID]["port"]:

                if port == activePort:

                    value = projectData["item"][itemID]["port"][port]

                    itemBuy, itemSell = value.split("-")

            for sarea in projectData["sarea"]:

                for port in projectData["sarea"][sarea]["port"]:

                    if port == activePort:

                        itemSarea = projectData["sarea"][sarea]["name"]

            for area in projectData["area"]:

                for sarea in projectData["area"][area]["sarea"]:

                    if sarea == itemSarea:

                        itemArea = projectData["area"][area]["name"]

            item = {

                "name" : entry,
                "image" : projectData["item"][itemID]["image"],
                "port" : activePort,
                "buy" : itemBuy,
                "sell" : itemSell,
                "attr" : projectData["item"][itemID]["attr"],
                "sattr" : projectData["item"][itemID]["sattr"],
                "sarea" : itemSarea,
                "area" : itemArea

            }

            self.setItemInfo(item)

        else:

            for port in projectData["port"]:

                if projectData["port"][port]["name"] == entry:

                    portID = port

            if self.CBB_sorting.get() == lang["titleItem"]:

                allItems = self.LBX_stSelect.get(0, tk.END)
                selectionIndex = self.LBX_stSelect.curselection()
                selectionList = [allItems[item] for item in selectionIndex]
                activeItem = selectionList[0]

            elif self.CBB_sorting.get() == lang["titleAttribute"]:

                allItems = self.LBX_rdSelect.get(0, tk.END)
                selectionIndex = self.LBX_rdSelect.curselection()
                selectionList = [allItems[item] for item in selectionIndex]
                activeItem = selectionList[0]

            elif self.CBB_sorting.get() == lang["titleSubattribute"]:

                allItems = self.LBX_ndSelect.get(0, tk.END)
                selectionIndex = self.LBX_ndSelect.curselection()
                selectionList = [allItems[item] for item in selectionIndex]
                activeItem = selectionList[0]

            else:

                return -1

            for sarea in projectData["sarea"]:

                for port in projectData["sarea"][sarea]["port"]:

                    if port == entry:

                        itemSarea = projectData["sarea"][sarea]["name"]

            for area in projectData["area"]:

                for sarea in projectData["area"][area]["sarea"]:

                    if sarea == itemSarea:

                        itemArea = projectData["area"][area]["name"]

            for item in projectData["item"]:

                if projectData["item"][item]["name"] == activeItem:

                    itemImage = projectData["item"][item]["image"]
                    itemAttr = projectData["item"][item]["attr"]
                    itemSattr = projectData["item"][item]["sattr"]

                    value = projectData["item"][item]["port"][entry]

                    itemBuy, itemSell = value.split("-")

            item = {

                "name" : activeItem,
                "image" : itemImage,
                "port" : entry,
                "buy" : itemBuy,
                "sell" : itemSell,
                "attr" : itemAttr,
                "sattr" : itemSattr,
                "sarea" : itemSarea,
                "area" : itemArea

            }

            self.setItemInfo(item)

    def toplevelDestroy_callback(self, event):

        try:

            scrObjAdd.buttonMainClose(self.addObj)

        except:

            pass

        global eDestroy

        if eDestroy == 0:

            self.browserSetFirstSection()

            eDestroy = 1

        else:

            pass

    def objectAdd(self):

        global eDestroy

        eDestroy = 0

        self.addObjectScreen = tk.Toplevel(self.master)
        self.addObjectScreen.grab_set()
        self.addObjectScreen.resizable(height = False, width = False)

        windowWidth = 320
        windowHeight = 486
        
        positionRight = int(self.addObjectScreen.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.addObjectScreen.winfo_screenheight()/2 - windowHeight/2)

        self.addObjectScreen.geometry("+{}+{}".format(positionRight, positionDown))

        self.addObjectScreen.protocol("WM_DELETE_WINDOW", lambda: self.toplevelDestroy_callback(None))
        self.addObjectScreen.bind("<Destroy>", self.toplevelDestroy_callback)

        self.addObj = scrObjAdd(self.addObjectScreen)

    def objectEdit(self):

        self.editObjectScreen = tk.Toplevel(self.master)
        self.editObjectScreen.grab_set()
        self.editObjectScreen.resizable(height = False, width = False)

        self.editObj = scrObjEdit(self.editObjectScreen)

    def objectRemove(self):

        active = self.CBB_sorting.current()

        try:

            allItems = self.LBX_stSelect.get(0, tk.END)
            selectionIndex = self.LBX_stSelect.curselection()
            selectionList = [allItems[item] for item in selectionIndex]
            selectionFst = selectionList[0]

        except:

            selectionFst = None

        try:

            allItems = self.LBX_ndSelect.get(0, tk.END)
            selectionIndex = self.LBX_ndSelect.curselection()
            selectionList = [allItems[item] for item in selectionIndex]
            selectionSnd = selectionList[0]

        except:

            selectionSnd = None

        try:

            allItems = self.LBX_rdSelect.get(0, tk.END)
            selectionIndex = self.LBX_rdSelect.curselection()
            selectionList = [allItems[item] for item in selectionIndex]
            selectionTrd = selectionList[0]

        except:

            selectionTrd = None

        try:

            selectionIndex = self.TRW_offer.selection()

            selectionTRW = list(dict(self.TRW_offer.item(selectionIndex))["values"])[0]

        except:

            selectionIndex = ()

        if selectionIndex == ():

            selectionTRW = None

        if selectionTRW != None:

            delete = 3
            selection = selectionTRW

        elif selectionTrd != None:

            delete = 2
            selection = selectionTrd

        elif selectionSnd != None:

            delete = 1
            selection = selectionSnd

        elif selectionFst != None:

            delete = 0
            selection = selectionFst

        else:

            return -1

        msgCont = lang["promptObjectRemoveText"].split("/")

        msg = f"{msgCont[0]} {lang['titleEntry']} ({selection}){msgCont[1]}\n{msgCont[2]}\n\n{msgCont[3]}"

        alert = messagebox.askokcancel(f"{lang['programName']} - {lang['promptObjectRemove']}", msg, icon = "warning")

        if alert == True:

            if delete == 0:

                self.objectRemoveFstLBX()

            elif delete == 1:

                self.objectRemoveSndLBX()

            elif delete == 2:

                self.objectRemoveTrdLBX()

            elif delete == 3:

                self.objectRemoveTRW()

        else:

            return -1

    def projectNew(self):

        global projectData

        alertMsgLine1, alertMsgLine2 = str(lang["promptNewProjectAlertText"]).split("/")

        alert = messagebox.askokcancel(title = f"{lang['programName']} - {lang['promptNewProjectAlert']}", message = "\n\n".join([alertMsgLine1, alertMsgLine2]))

        if alert == False:

            return -1

        else:

            self.LBX_stSelect.delete(0, tk.END)
            self.LBX_ndSelect.delete(0, tk.END)
            self.LBX_rdSelect.delete(0, tk.END)
            self.TRW_offer.delete(*self.TRW_offer.get_children())

            projectData.clear()

            projectData["name"] = "active(None)"

            projectData["item"] = dict()
            projectData["area"] = dict()
            projectData["sarea"] = dict()
            projectData["port"] = dict()
            projectData["attr"] = dict()
            projectData["sattr"] = dict()

            self.browserSetFirstSection

            projectChanges = False

    def projectLoad(self):

        global projectData

        info = hand.general().getIniCont(infoPath)

        filePath = filedialog.askopenfilename(
            
            initialdir = (sys.path[0] + "\\save"),
            title = f"{lang['programName']} - {lang['promptLoadProject']}",
            filetypes = (

                (f"{info['name']} Database File",f"*{info['dbExtension']}"),
                ("all files","*.*")

                )

            )

        if filePath == "":

            return -1

        projectData = hand.project().load(filePath)

        projName = projectData["name"]

        projectData["name"] = f"active({projName})"

        self.browserSetFirstSection()

    def openSettings(self):

        self.settingsScreen = tk.Toplevel(self.master)
        self.settingsScreen.grab_set()
        self.settingsScreen.resizable(height = False, width = False)

        self.settings = scrSettings(self.settingsScreen)

    def programQuit(self):

        if projectChanges == True:

            alertMsgLine1, alertMsgLine2 = str(lang["promptQuitProgramAlertText"]).split("/")

            alert = messagebox.askyesno(title = lang["promptQuitProgramAlert"], message = "\n\n".join([alertMsgLine1, alertMsgLine2]))

            if alert == True:

                self.frame.quit()

            else:

                return -1

        else:

            self.frame.quit()

    def objectRemoveFstLBX(self):

        allItems = self.LBX_stSelect.get(0, tk.END)
        selectionIndex = self.LBX_stSelect.curselection()
        selectionList = [allItems[item] for item in selectionIndex]
        selection = selectionList[0]

        active = self.CBB_sorting.current()

        if active == 0: #item

            for item in projectData["item"]:

                if projectData["item"][item]["name"] == selection:

                    itemID = item

            self.projectDelItem(itemID)

            self.browserSetFirstSection()

        if active == 1: #area

            for area in projectData["area"]:

                if projectData["area"][area]["name"] == selection:

                    areaID = area

            self.projectDelArea(areaID)

        elif active == 2: #sarea

            for sarea in projectData["sarea"]:

                if projectData["sarea"][sarea]["name"] == selection:

                    sareaID = sarea

            self.projectDelSarea(sareaID)

        elif active == 3: #port

            for port in projectData["port"]:

                if projectData["port"][port]["name"] == selection:

                    portID = port

            self.projectDelPort(portID)

        elif active == 4: #attr

            for attr in projectData["attr"]:

                if projectData["attr"][attr]["name"] == selection:

                    attrID = attr

            self.projectDelAttr(attrID)

        elif active == 5: #sattr

            for sattr in projectData["sattr"]:

                if projectData["sattr"][sattr]["name"] == selection:

                    sattrID = sattr

            self.projectDelSattr(sattrID)
          
        self.browserSetFirstSection()

    def objectRemoveSndLBX(self):

        allItems = self.LBX_ndSelect.get(0, tk.END)
        selectionIndex = self.LBX_ndSelect.curselection()
        selectionList = [allItems[item] for item in selectionIndex]
        selection = selectionList[0]

        active = self.CBB_sorting.current()

        if active == 0: #item - none

            pass

        if active == 1: #area - sarea

            for sarea in projectData["sarea"]:

                if projectData["sarea"][sarea]["name"] == selection:

                    sareaID = sarea

            self.projectDelSarea(sareaID)

        elif active == 2: #sarea - port

            for port in projectData["port"]:

                if projectData["port"][port]["name"] == selection:

                    portID = port

            self.projectDelPort(portID)

        elif active == 3: #port - none

            pass

        elif active == 4: #attr - sattr

            for sattr in projectData["sattr"]:

                if projectData["sattr"][sattr]["name"] == selection:

                    sattrID = sattr

            self.projectDelSattr(sattrID)

        elif active == 5: #sattr - item

            for item in projectData["item"]:

                if projectData["item"][item]["name"] == selection:

                    itemID = item

            self.projectDelItem(itemID)

            self.browserSetFirstSection()
          
        self.browserSetFirstSection()

    def objectRemoveTrdLBX(self):

        allItems = self.LBX_rdSelect.get(0, tk.END)
        selectionIndex = self.LBX_rdSelect.curselection()
        selectionList = [allItems[item] for item in selectionIndex]
        selection = selectionList[0]

        active = self.CBB_sorting.current()

        if active == 0: #item - none - none

            pass

        if active == 1: #area - sarea - port

            for port in projectData["port"]:

                if projectData["port"][port]["name"] == selection:

                    portID = port

            self.projectDelPort(portID)

        elif active == 2: #sarea - port - none

            pass

        elif active == 3: #port - none - none

            pass

        elif active == 4: #attr - sattr - item

            for item in projectData["item"]:

                if projectData["item"][item]["name"] == selection:

                    itemID = item

            self.projectDelItem(itemID)

            self.browserSetFirstSection()

        elif active == 5: #sattr - item - none

            pass
          
        self.browserSetFirstSection()

    def objectRemoveTRW(self):

        activeSelection = self.TRW_offer.selection()

        selection = list(dict(self.TRW_offer.item(activeSelection))["values"])[0]

        active = self.CBB_sorting.current()

        if active == 0 or active == 4 or active == 5: #item, attr, sattr

            for port in projectData["port"]:

                if projectData["port"][port]["name"] == selection:

                    portID = port

            self.projectDelPort(portID)

        elif active == 1 or active == 2 or active == 3: #area, sarea, port

            for item in projectData["item"]:

                if projectData["item"][item]["name"] == selection:

                    itemID = item

            self.projectDelItem(itemID)

        self.browserSetFirstSection()            

    def projectDelItem(self, itemID):

        del projectData["item"][itemID]

    def projectDelArea(self, areaID):

        delSarea = list()

        for sarea in projectData["area"][areaID]["sarea"]:

            for entry in projectData["sarea"]:

                if projectData["sarea"][entry]["name"] == sarea:

                    delSarea.append(entry)

        for entry in delSarea:

            self.projectDelSarea(entry)

        del projectData["area"][areaID]

    def projectDelSarea(self, sareaID):

        delPort = list()

        for port in projectData["sarea"][sareaID]["port"]:

            for entry in projectData["port"]:

                if projectData["port"][entry]["name"] == port:

                    delPort.append(entry)

        for entry in delPort:

            self.projectDelPort(entry)

        del projectData["sarea"][sareaID]

    def projectDelPort(self, portID):

        delItem = list()

        for item in projectData["item"]:

            if projectData["port"][portID]["name"] in projectData["item"][item]["port"]:

                delItem.append(item)

        for item in delItem:

            del projectData["item"][item]["port"][projectData["port"][portID]["name"]]

        del projectData["port"][portID]

    def projectDelAttr(self, attrID):

        delSattr = list()

        for sattr in projectData["attr"][attrID]["sattr"]:

            for entry in projectData["sattr"]:

                if projectData["sattr"][entry]["name"] == sattr:

                    delSattr.append(entry)

        for entry in delSattr:

            self.projectDelSattr(entry)

        del projectData["attr"][attrID]

    def projectDelSattr(self, sattrID):

        delItem = list()

        for item in projectData["item"]:

            if projectData["sattr"][sattrID]["name"] in projectData["item"][item]["sattr"]:

                delItem.append(item)

        for item in delItem:

            del projectData["item"][item]["sattr"][projectData["sattr"][sattrID]["name"]]

        del projectData["sattr"][sattrID]

    def setItemInfo(self, item):

        if item == None:

            item = {

                "name" : "-",
                "image" : "None",
                "port" : "-",
                "buy" : "-",
                "sell" : "-",
                "attr" : "-",
                "sattr" : "-",
                "sarea" : "-",
                "area" : "-"

            }

        if item["image"] == "None":

            itemImage = tk.PhotoImage(file = "data/noImage.pgm")

        else:

            itemImage = tk.PhotoImage(file = item["image"])

        self.IMG_item.config(image = itemImage)
        self.IMG_item.image = itemImage
        
        self.itemBuyActiveTextvariable.set(item["buy"])
        
        self.itemSellActiveTextvariable.set(item["sell"])
        
        self.TXT_nameActive.config(state = "normal")
        self.TXT_nameActive.delete(1.0, "end")
        self.TXT_nameActive.insert(1.0, item["name"])
        self.TXT_nameActive.config(state = "disabled")
        
        self.TXT_portActive.config(state = "normal")
        self.TXT_portActive.delete(1.0, "end")
        self.TXT_portActive.insert(1.0, item["port"])
        self.TXT_portActive.config(state = "disabled")
        
        self.TXT_areaActive.config(state = "normal")
        self.TXT_areaActive.delete(1.0, "end")
        self.TXT_areaActive.insert(1.0, item["area"])
        self.TXT_areaActive.config(state = "disabled")
        
        self.TXT_subareaActive.config(state = "normal")
        self.TXT_subareaActive.delete(1.0, "end")
        self.TXT_subareaActive.insert(1.0, item["sarea"])
        self.TXT_subareaActive.config(state = "disabled")
        
        self.TXT_attributeActive.config(state = "normal")
        self.TXT_attributeActive.delete(1.0, "end")
        self.TXT_attributeActive.insert(1.0, item["attr"])
        self.TXT_attributeActive.config(state = "disabled")
        
        self.TXT_subattributeActive.config(state = "normal")
        self.TXT_subattributeActive.delete(1.0, "end")
        self.TXT_subattributeActive.insert(1.0, item["sattr"])
        self.TXT_subattributeActive.config(state = "disabled")
        
    def browserSetFirstSection(self):

        activeSorting = self.CBB_sorting.get()

        self.LBX_stSelect.delete(0, tk.END)
        self.LBX_ndSelect.delete(0, tk.END)
        self.LBX_rdSelect.delete(0, tk.END)
        self.TRW_offer.delete(*self.TRW_offer.get_children())

        self.BTN_edit.config(state = "disabled")
        self.BTN_remove.config(state = "disabled")

        if activeSorting == lang["titleItem"]:

            sortList = list()

            for item in projectData["item"]:

                sortList.append(projectData["item"][item]["name"])

            sortList.sort()

            for entry in sortList:

                self.LBX_stSelect.insert(tk.END, entry)
            
        elif activeSorting == lang["titleArea"]:

            sortList = list()

            for area in projectData["area"]:

                sortList.append(projectData["area"][area]["name"])

            sortList.sort()

            if len(projectData["area"]) > 1:

                self.LBX_stSelect.insert(tk.END, lang["generalAll"])

            for entry in sortList:

                self.LBX_stSelect.insert(tk.END, entry)

        elif activeSorting == lang["titleSubarea"]:

            sortList = list()

            for sarea in projectData["sarea"]:

                sortList.append(projectData["sarea"][sarea]["name"])

            sortList.sort()

            if len(projectData["sarea"]) > 1:

                self.LBX_stSelect.insert(tk.END, lang["generalAll"])

            for entry in sortList:

                self.LBX_stSelect.insert(tk.END, entry)

        elif activeSorting == lang["titlePort"]:

            sortList = list()

            for port in projectData["port"]:

                sortList.append(projectData["port"][port]["name"])

            sortList.sort()

            for entry in sortList:

                self.LBX_stSelect.insert(tk.END, entry)

        elif activeSorting == lang["titleAttribute"]:

            sortList = list()

            for attr in projectData["attr"]:

                sortList.append(projectData["attr"][attr]["name"])

            sortList.sort()

            if len(projectData["attr"]) > 1:

                self.LBX_stSelect.insert(tk.END, lang["generalAll"])

            for entry in sortList:

                self.LBX_stSelect.insert(tk.END, entry)

        elif activeSorting == lang["titleSubattribute"]:

            sortList = list()

            for sattr in projectData["sattr"]:

                sortList.append(projectData["sattr"][sattr]["name"])

            sortList.sort()

            if len(projectData["sattr"]) > 1:

                self.LBX_stSelect.insert(tk.END, lang["generalAll"])

            for entry in sortList:

                self.LBX_stSelect.insert(tk.END, entry)

class scrObjAdd:

    def __init__(self, master):

        self.master = master
        self.frame = ttk.Frame(self.master)

        self.master.title(f"{lang['programName']} - {lang['promptObjectAdd']}")
        
        ########################################
        # --------- Creating Widgets --------- #
        ########################################

        # --- Register ---

        self.NTB_main = ttk.Notebook(self.frame)

        self.FRM_ntbItem = ttk.Frame(self.NTB_main)

        self.FRM_ntbItem.columnconfigure(0, weight = 1)
        self.FRM_ntbItem.columnconfigure(1, weight = 1)

        self.FRM_ntbArea = ttk.Frame(self.NTB_main)

        self.FRM_ntbArea.columnconfigure(0, weight = 1)
        self.FRM_ntbArea.columnconfigure(1, weight = 1)

        self.FRM_ntbSarea = ttk.Frame(self.NTB_main)

        self.FRM_ntbSarea.columnconfigure(0, weight = 1)
        self.FRM_ntbSarea.columnconfigure(1, weight = 1)

        self.FRM_ntbPort = ttk.Frame(self.NTB_main)

        self.FRM_ntbPort.columnconfigure(0, weight = 1)
        self.FRM_ntbPort.columnconfigure(1, weight = 1)

        self.FRM_ntbAttr = ttk.Frame(self.NTB_main)

        self.FRM_ntbAttr.columnconfigure(0, weight = 1)
        self.FRM_ntbAttr.columnconfigure(1, weight = 1)

        self.FRM_ntbSattr = ttk.Frame(self.NTB_main)

        self.FRM_ntbSattr.columnconfigure(0, weight = 1)
        self.FRM_ntbSattr.columnconfigure(1, weight = 1)
        
        self.NTB_main.add(self.FRM_ntbItem, text = lang["titleItem"])
        self.NTB_main.add(self.FRM_ntbArea, text = lang["titleArea"])
        self.NTB_main.add(self.FRM_ntbSarea, text = lang["titleSubarea"])
        self.NTB_main.add(self.FRM_ntbPort, text = lang["titlePort"])
        self.NTB_main.add(self.FRM_ntbAttr, text = lang["titleAttribute"])
        self.NTB_main.add(self.FRM_ntbSattr, text = lang["titleSubattribute"])
        
        self.NTB_main.bind("<<NotebookTabChanged>>", self.NTB_main_callback)

        # --- Register #01 - Items --- name, available Ports with value, attr, subattr

        self.LBL_nbtItemName = ttk.Label(self.FRM_ntbItem, text = f"{lang['titleName']}:")
        self.ETY_nbtItemName = ttk.Entry(self.FRM_ntbItem, width = 23)

        self.FRM_nbtItemImage = ttk.Frame(self.FRM_ntbItem)

        self.FRM_nbtItemImage.columnconfigure(0, weight = 1)
        self.FRM_nbtItemImage.columnconfigure(1, weight = 1)

        self.LBL_nbtItemImage = ttk.Label(self.FRM_nbtItemImage, text = f"{lang['titleImageFile']}:")

        self.FRM_nbtItemImageEntry = ttk.Frame(self.FRM_nbtItemImage)

        self.ETY_nbtItemImageEntry = ttk.Entry(self.FRM_nbtItemImageEntry, width = 18)
        self.BTN_nbtItemImageEntry = ttk.Button(self.FRM_nbtItemImageEntry, text = "...", width = 3, command = self.buttonItemImage)

        self.LBL_nbtItemAttr = ttk.Label(self.FRM_ntbItem, text = f"{lang['titleItem']}-{lang['titleAttribute']}:")
        self.CBB_nbtItemAttr = ttk.Combobox(self.FRM_ntbItem, state = "readonly")

        self.CBB_nbtItemAttr.bind("<<ComboboxSelected>>", self.CBB_nbtItemAttr_callback)

        self.LBL_nbtItemSattr = ttk.Label(self.FRM_ntbItem, text = f"{lang['titleItem']}-{lang['titleSubattribute']}:")
        self.CBB_nbtItemSattr = ttk.Combobox(self.FRM_ntbItem, state = "readonly")

        self.FRM_nbtItemPortTree = ttk.Frame(self.FRM_ntbItem)

        TRW_nbtItemPortColumnList = (f"{lang['titlePort']}, {lang['titleBuy']}, {lang['titleSell']}")

        self.TRW_nbtItemPortTree = ttk.Treeview(self.FRM_nbtItemPortTree, columns = TRW_nbtItemPortColumnList, show = "headings", height = 10)

        self.TRW_nbtItemPortTree.heading(0, text = lang["titlePort"])
        self.TRW_nbtItemPortTree.column(0, width = 175)
        self.TRW_nbtItemPortTree.heading(1, text = lang["titleBuy"])
        self.TRW_nbtItemPortTree.column(1, width = 50)
        self.TRW_nbtItemPortTree.heading(2, text = lang["titleSell"])
        self.TRW_nbtItemPortTree.column(2, width = 50)

        self.SLB_nbtItemPortTree = ttk.Scrollbar(self.FRM_nbtItemPortTree, orient = tk.VERTICAL, command = self.TRW_nbtItemPortTree.yview)
        self.TRW_nbtItemPortTree["yscrollcommand"] = self.SLB_nbtItemPortTree.set

        self.TRW_nbtItemPortTree.bind("<<TreeviewSelect>>", self.TRW_nbtItemPortTree_callback)

        self.FRM_nbtItemPortEntry = ttk.Frame(self.FRM_ntbItem)

        self.FRM_nbtItemPortEntry.columnconfigure(0, weight = 1)
        self.FRM_nbtItemPortEntry.columnconfigure(1, weight = 1)

        self.CBB_nbtItemPortEntry = ttk.Combobox(self.FRM_nbtItemPortEntry, width = 24, state = "readonly")

        self.CBB_nbtItemPortEntry.bind("<<ComboboxSelected>>", self.CBB_nbtItemPortEntry_callback)

        self.FRM_nbtItemPortEntryValue = ttk.Frame(self.FRM_nbtItemPortEntry)

        self.ETY_nbtItemPortEntryValueBuy = ttk.Entry(self.FRM_nbtItemPortEntryValue, width = 9)
        self.ETY_nbtItemPortEntryValueSell = ttk.Entry(self.FRM_nbtItemPortEntryValue, width = 9)

        self.FRM_nbtItemPortButtons = ttk.Frame(self.FRM_ntbItem)

        self.FRM_nbtItemPortButtons.columnconfigure(0, weight = 1)
        self.FRM_nbtItemPortButtons.columnconfigure(1, weight = 1)

        self.BTN_nbtItemPortButtonsAdd = ttk.Button(self.FRM_nbtItemPortButtons, text = lang["buttonGeneralAdd"], width = 20, command = self.buttonItemAddPort)
        self.BTN_nbtItemPortButtonsRemove = ttk.Button(self.FRM_nbtItemPortButtons, text = lang["buttonGeneralRemove"], width = 20, command = self.buttonItemRemovePort)

        # --- Register #02 - Area --- name

        self.LBL_nbtAreaName = ttk.Label(self.FRM_ntbArea, text = f"{lang['titleName']}:")
        self.ETY_nbtAreaName = ttk.Entry(self.FRM_ntbArea, width = 23)

        # --- Register #03 - Sarea --- name, area

        self.LBL_nbtSareaName = ttk.Label(self.FRM_ntbSarea, text = f"{lang['titleName']}:")
        self.ETY_nbtSareaName = ttk.Entry(self.FRM_ntbSarea, width = 23)

        self.LBL_nbtSareaMaster = ttk.Label(self.FRM_ntbSarea, text = f"{lang['titleArea']}:")
        self.CBB_nbtSareaMaster = ttk.Combobox(self.FRM_ntbSarea, state = "readonly")

        # --- Register #04 - Port --- name, sarea, available items with value

        self.LBL_nbtPortName = ttk.Label(self.FRM_ntbPort, text = f"{lang['titleName']}:")
        self.ETY_nbtPortName = ttk.Entry(self.FRM_ntbPort, width = 23)

        self.LBL_nbtPortArea = ttk.Label(self.FRM_ntbPort, text = f"{lang['titlePort']}-{lang['titleArea']}:")
        self.CBB_nbtPortArea = ttk.Combobox(self.FRM_ntbPort, state = "readonly")

        self.CBB_nbtPortArea.bind("<<ComboboxSelected>>", self.CBB_nbtPortArea_callback)

        self.LBL_nbtPortSarea = ttk.Label(self.FRM_ntbPort, text = f"{lang['titlePort']}-{lang['titleSubarea']}:")
        self.CBB_nbtPortSarea = ttk.Combobox(self.FRM_ntbPort, state = "readonly")

        self.FRM_nbtPortItemTree = ttk.Frame(self.FRM_ntbPort)

        TRW_nbtPortItemColumnList = (f"{lang['titleItem']}, {lang['titleBuy']}, {lang['titleSell']}")

        self.TRW_nbtPortItemTree = ttk.Treeview(self.FRM_nbtPortItemTree, columns = TRW_nbtPortItemColumnList, show = "headings", height = 10)

        self.TRW_nbtPortItemTree.heading(0, text = lang["titleItem"])
        self.TRW_nbtPortItemTree.column(0, width = 175)
        self.TRW_nbtPortItemTree.heading(1, text = lang["titleBuy"])
        self.TRW_nbtPortItemTree.column(1, width = 50)
        self.TRW_nbtPortItemTree.heading(2, text = lang["titleSell"])
        self.TRW_nbtPortItemTree.column(2, width = 50)

        self.SLB_nbtPortItemTree = ttk.Scrollbar(self.FRM_nbtPortItemTree, orient = tk.VERTICAL, command = self.TRW_nbtPortItemTree.yview)
        self.TRW_nbtPortItemTree["yscrollcommand"] = self.SLB_nbtPortItemTree.set

        self.TRW_nbtPortItemTree.bind("<<TreeviewSelect>>", self.TRW_nbtPortItemTree_callback)

        self.FRM_nbtPortItemEntry = ttk.Frame(self.FRM_ntbPort)

        self.FRM_nbtPortItemEntry.columnconfigure(0, weight = 1)
        self.FRM_nbtPortItemEntry.columnconfigure(1, weight = 1)

        self.CBB_nbtPortItemEntry = ttk.Combobox(self.FRM_nbtPortItemEntry, width = 24, state = "readonly")

        self.CBB_nbtPortItemEntry.bind("<<ComboboxSelected>>", self.CBB_nbtPortItemEntry_callback)

        self.FRM_nbtPortItemEntryValue = ttk.Frame(self.FRM_nbtPortItemEntry)

        self.ETY_nbtPortItemEntryValueBuy = ttk.Entry(self.FRM_nbtPortItemEntryValue, width = 9)
        self.ETY_nbtPortItemEntryValueSell = ttk.Entry(self.FRM_nbtPortItemEntryValue, width = 9)

        self.FRM_nbtPortItemButtons = ttk.Frame(self.FRM_ntbPort)

        self.FRM_nbtPortItemButtons.columnconfigure(0, weight = 1)
        self.FRM_nbtPortItemButtons.columnconfigure(1, weight = 1)

        self.BTN_nbtPortItemButtonsAdd = ttk.Button(self.FRM_nbtPortItemButtons, text = lang["buttonGeneralAdd"], width = 20, command = self.buttonPortAddItem)
        self.BTN_nbtPortItemButtonsRemove = ttk.Button(self.FRM_nbtPortItemButtons, text = lang["buttonGeneralRemove"], width = 20, command = self.buttonPortRemoveItem)

        # --- Register #05 - Attr --- name

        self.LBL_nbtAttrName = ttk.Label(self.FRM_ntbAttr, text = f"{lang['titleName']}:")
        self.ETY_nbtAttrName = ttk.Entry(self.FRM_ntbAttr, width = 23)

        # --- Register #06 - Sattr --- name, attr

        self.LBL_nbtSattrName = ttk.Label(self.FRM_ntbSattr, text = f"{lang['titleName']}:")
        self.ETY_nbtSattrName = ttk.Entry(self.FRM_ntbSattr, width = 23)

        self.LBL_nbtSattrMaster = ttk.Label(self.FRM_ntbSattr, text = f"{lang['titleAttribute']}:")
        self.CBB_nbtSattrMaster = ttk.Combobox(self.FRM_ntbSattr, state = "readonly")

        # --- Main Buttons ---

        self.FRM_buttons = ttk.Frame(self.frame)

        self.BTN_add = ttk.Button(self.FRM_buttons, text = lang["buttonGeneralAdd"], command = self.buttonMainAdd)
        self.BTN_close = ttk.Button(self.FRM_buttons, text = lang["buttonGeneralClose"], command = self.buttonMainClose)

        ######################################
        # --------- Allign Widgets --------- #
        ######################################

        # --- Register #01 - Items ---
        
        self.LBL_nbtItemName.grid(column = 0, row = 0, sticky = (tk.W), padx = 5, pady = 5)
        self.ETY_nbtItemName.grid(column = 1, row = 0, sticky = (tk.E), padx = 5, pady = 5)

        self.FRM_nbtItemImage.grid(column = 0, row = 1, columnspan = 2, sticky = (tk.W, tk.E), padx = 5, pady = 1)

        self.LBL_nbtItemImage.grid(column = 0, row = 0, sticky = (tk.W))

        self.FRM_nbtItemImageEntry.grid(column = 1, row = 0, sticky = (tk.E))

        self.ETY_nbtItemImageEntry.grid(column = 1, row = 0, padx = 2)
        self.BTN_nbtItemImageEntry.grid(column = 2, row = 0)

        self.LBL_nbtItemAttr.grid(column = 0, row = 2, sticky = (tk.W), padx = 5, pady = 2)
        self.CBB_nbtItemAttr.grid(column = 1, row = 2, sticky = (tk.E), padx = 5, pady = 2)

        self.LBL_nbtItemSattr.grid(column = 0, row = 3, sticky = (tk.W), padx = 5, pady = 2)
        self.CBB_nbtItemSattr.grid(column = 1, row = 3, sticky = (tk.E), padx = 5, pady = 2)

        self.FRM_nbtItemPortTree.grid(column = 0, row = 4, columnspan = 2, sticky = (tk.W, tk.E), padx = 5, pady = 2)

        self.TRW_nbtItemPortTree.grid(column = 0, row = 0)
        self.SLB_nbtItemPortTree.grid(column = 1, row = 0, sticky = (tk.N, tk.S))

        self.FRM_nbtItemPortEntry.grid(column = 0, row = 5, columnspan = 2, sticky = (tk.W, tk.E), padx = 5)

        self.CBB_nbtItemPortEntry.grid(column = 0, row = 0, sticky = (tk.W))

        self.FRM_nbtItemPortEntryValue.grid(column = 1, row = 0, sticky = (tk.E))

        self.ETY_nbtItemPortEntryValueBuy.grid(column = 0, row = 0, padx = 2)
        self.ETY_nbtItemPortEntryValueSell.grid(column = 1, row = 0, padx = 1)

        self.FRM_nbtItemPortButtons.grid(column = 0, row = 6, columnspan = 2, padx = 5, pady = 2)

        self.BTN_nbtItemPortButtonsAdd.grid(column = 0, row = 0)
        self.BTN_nbtItemPortButtonsRemove.grid(column = 1, row = 0)

        # --- Register #02 - Area ---

        self.LBL_nbtAreaName.grid(column = 0, row = 1, sticky = (tk.W), padx = 5, pady = 5)
        self.ETY_nbtAreaName.grid(column = 1, row = 1, sticky = (tk.E), padx = 5, pady = 5)

        # --- Register #03 - Sarea ---

        self.LBL_nbtSareaName.grid(column = 0, row = 1, sticky = (tk.W), padx = 5, pady = 5)
        self.ETY_nbtSareaName.grid(column = 1, row = 1, sticky = (tk.E), padx = 5, pady = 5)

        self.LBL_nbtSareaMaster.grid(column = 0, row = 2, sticky = (tk.W), padx = 5, pady = 2)
        self.CBB_nbtSareaMaster.grid(column = 1, row = 2, sticky = (tk.E), padx = 5, pady = 2)

        # --- Register #04 - Port ---

        self.LBL_nbtPortName.grid(column = 0, row = 0, sticky = (tk.W), padx = 5, pady = 5)
        self.ETY_nbtPortName.grid(column = 1, row = 0, sticky = (tk.E), padx = 5, pady = 5)

        self.LBL_nbtPortArea.grid(column = 0, row = 1, sticky = (tk.W), padx = 5, pady = 2)
        self.CBB_nbtPortArea.grid(column = 1, row = 1, sticky = (tk.E), padx = 5, pady = 2)

        self.LBL_nbtPortSarea.grid(column = 0, row = 2, sticky = (tk.W), padx = 5, pady = 2)
        self.CBB_nbtPortSarea.grid(column = 1, row = 2, sticky = (tk.E), padx = 5, pady = 2)

        self.FRM_nbtPortItemTree.grid(column = 0, row = 3, columnspan = 2, sticky = (tk.W, tk.E), padx = 5, pady = 2)

        self.TRW_nbtPortItemTree.grid(column = 0, row = 0)
        self.SLB_nbtPortItemTree.grid(column = 1, row = 0, sticky = (tk.N, tk.S))

        self.FRM_nbtPortItemEntry.grid(column = 0, row = 4, columnspan = 2, sticky = (tk.W, tk.E), padx = 5)

        self.CBB_nbtPortItemEntry.grid(column = 0, row = 0, sticky = (tk.W))

        self.FRM_nbtPortItemEntryValue.grid(column = 1, row = 0, sticky = (tk.E))

        self.ETY_nbtPortItemEntryValueBuy.grid(column = 0, row = 0, padx = 2)
        self.ETY_nbtPortItemEntryValueSell.grid(column = 1, row = 0, padx = 1)

        self.FRM_nbtPortItemButtons.grid(column = 0, row = 5, columnspan = 2, padx = 5, pady = 2)

        self.BTN_nbtPortItemButtonsAdd.grid(column = 0, row = 0)
        self.BTN_nbtPortItemButtonsRemove.grid(column = 1, row = 0)

        # --- Register #05 - Attr ---

        self.LBL_nbtAttrName.grid(column = 0, row = 1, sticky = (tk.W), padx = 5, pady = 5)
        self.ETY_nbtAttrName.grid(column = 1, row = 1, sticky = (tk.E), padx = 5, pady = 5)

        # --- Register #06 - Sattr ---

        self.LBL_nbtSattrName.grid(column = 0, row = 1, sticky = (tk.W), padx = 5, pady = 5)
        self.ETY_nbtSattrName.grid(column = 1, row = 1, sticky = (tk.E), padx = 5, pady = 5)

        self.LBL_nbtSattrMaster.grid(column = 0, row = 2, sticky = (tk.W), padx = 5, pady = 2)
        self.CBB_nbtSattrMaster.grid(column = 1, row = 2, sticky = (tk.E), padx = 5, pady = 2)

        # --- Register ---

        self.NTB_main.grid(column = 0, row = 0, padx = 3, pady = 3)

        # --- Main Buttons ---

        self.BTN_add.grid(column = 0, row = 0)
        self.BTN_close.grid(column = 1, row = 0)

        self.FRM_buttons.grid(column = 0, row = 1, sticky = (tk.E), padx = 4, pady = 3)

        # --- Main Frame ---

        self.frame.grid(column = 0, row = 0)

        # --- Final Pack

        self.frame.pack()

        self.getInitialValues()

    def getInitialValues(self):

        empty = list()
        empty.append("")

        # -- item --

        entryList = list()

        entryList.append(f"-- {lang['titleItem'].lower()} --")

        for item in projectData["item"]:

            entryList.append(projectData["item"][item]["name"])

        self.CBB_nbtPortItemEntry.config(values = entryList)
        self.CBB_nbtPortItemEntry.current(0)

        # -- port --

        entryList = list()

        entryList.append(f"-- {lang['titlePort'].lower()} --")

        for port in projectData["port"]:

            entryList.append(projectData["port"][port]["name"])

        self.CBB_nbtItemPortEntry.config(values = entryList)
        self.CBB_nbtItemPortEntry.current(0)

        # -- attr --

        entryList = list()

        entryList.append(f"-- {lang['titleAttribute'].lower()} --")

        for attr in projectData["attr"]:

            entryList.append(projectData["attr"][attr]["name"])

        self.CBB_nbtItemAttr.config(values = entryList)
        self.CBB_nbtItemAttr.current(0)

        self.CBB_nbtSattrMaster.config(values = entryList)
        self.CBB_nbtSattrMaster.current(0)

        self.CBB_nbtItemSattr.config(values = empty)
        self.CBB_nbtItemSattr.current(0)
        self.CBB_nbtItemSattr.config(state = "disabled")

        # -- area --

        entryList = list()

        entryList.append(f"-- {lang['titleArea'].lower()} --")

        for area in projectData["area"]:

            entryList.append(projectData["area"][area]["name"])

        self.CBB_nbtPortArea.config(values = entryList)
        self.CBB_nbtPortArea.current(0)

        self.CBB_nbtSareaMaster.config(values = entryList)
        self.CBB_nbtSareaMaster.current(0)

        self.CBB_nbtPortSarea.config(values = empty)
        self.CBB_nbtPortSarea.current(0)
        self.CBB_nbtPortSarea.config(state = "disabled")


        # -- other --

        self.ETY_nbtItemName.delete(0, tk.END)
        self.ETY_nbtItemImageEntry.delete(0, tk.END)
        self.TRW_nbtItemPortTree.delete(*self.TRW_nbtItemPortTree.get_children())

        self.ETY_nbtAttrName.delete(0, tk.END)

        self.ETY_nbtSattrName.delete(0, tk.END)

        self.ETY_nbtPortName.delete(0, tk.END)
        self.TRW_nbtPortItemTree.delete(*self.TRW_nbtPortItemTree.get_children())

        self.ETY_nbtAreaName.delete(0, tk.END)

        self.ETY_nbtSareaName.delete(0, tk.END)

        self.ETY_nbtItemPortEntryValueBuy.delete(0, tk.END)
        self.ETY_nbtItemPortEntryValueSell.delete(0, tk.END)

        self.ETY_nbtPortItemEntryValueBuy.delete(0, tk.END)
        self.ETY_nbtPortItemEntryValueBuy.delete(0, tk.END)

        self.BTN_nbtItemPortButtonsAdd.config(state = "disabled")
        self.BTN_nbtItemPortButtonsRemove.config(state = "disabled")
        self.BTN_nbtPortItemButtonsAdd.config(state = "disabled")
        self.BTN_nbtPortItemButtonsRemove.config(state = "disabled")

    def NTB_main_callback(self, event):

        self.getInitialValues()

    def CBB_nbtItemAttr_callback(self, event):

        active = self.CBB_nbtItemAttr.get()

        if active == f"-- {lang['titleAttribute'].lower()} --":

            empty = list()
            empty.append("")

            self.CBB_nbtItemSattr.config(values = empty)
            self.CBB_nbtItemSattr.current(0)
            self.CBB_nbtItemSattr.config(state = "disabled")

        else:

            for attr in projectData["attr"]:

                if projectData["attr"][attr]["name"] == active:

                    attrID = attr

            sattrList = list()

            for sattr in projectData["attr"][attrID]["sattr"]:

                sattrList.append(sattr)

            sattrList.insert(0, f"-- {lang['titleSubattribute'].lower()} --")

            self.CBB_nbtItemSattr.config(values = sattrList, state = "readonly")
            self.CBB_nbtItemSattr.current(0)

    def CBB_nbtItemPortEntry_callback(self, event):

        active = self.CBB_nbtItemPortEntry.get()

        if active == f"-- {lang['titlePort'].lower()} --":

            self.BTN_nbtItemPortButtonsAdd.config(state = "disabled")

        else:

            self.BTN_nbtItemPortButtonsAdd.config(state = "normal")

    def CBB_nbtPortArea_callback(self, event):

        active = self.CBB_nbtPortArea.get()

        if active == f"-- {lang['titleArea'].lower()} --":

            empty = list()
            empty.append("")

            self.CBB_nbtPortSarea.config(values = empty)
            self.CBB_nbtPortSarea.current(0)
            self.CBB_nbtPortSarea.config(state = "disabled")

        else:    

            for area in projectData["area"]:

                if projectData["area"][area]["name"] == active:

                    areaID = area

            sareaList = list()

            for sarea in projectData["area"][areaID]["sarea"]:

                sareaList.append(sarea)

            sareaList.insert(0, f"-- {lang['titleSubarea'].lower()} --")

            self.CBB_nbtPortSarea.config(values = sareaList, state = "readonly")
            self.CBB_nbtPortSarea.current(0)

    def CBB_nbtPortItemEntry_callback(self, event):

        active = self.CBB_nbtPortItemEntry.get()

        if active == f"-- {lang['titleItem'].lower()} --":

            self.BTN_nbtPortItemButtonsAdd.config(state = "disabled")

        else:

            self.BTN_nbtPortItemButtonsAdd.config(state = "normal")

    def TRW_nbtItemPortTree_callback(self, event):

        self.BTN_nbtItemPortButtonsRemove.config(state = "normal")

    def TRW_nbtPortItemTree_callback(self, event):

        self.BTN_nbtPortItemButtonsRemove.config(state = "normal")

    def buttonItemImage(self):

        filePath = filedialog.askopenfilename(
            
            initialdir = (sys.path[0]),
            title = lang["promptLoadImage"],
            filetypes = (

                ("Graphics Interchange Format", "*.gif"),
                ("Portable Graymap", "*.pgm"),
                ("all files","*.*")

                )

            )

        self.ETY_nbtItemImageEntry.delete(0, tk.END)
        self.ETY_nbtItemImageEntry.insert(0, filePath)

    def buttonItemAddPort(self):

        if self.CBB_nbtItemPortEntry != f"-- {lang['titlePort'].lower()} --":

            name = self.CBB_nbtItemPortEntry.get()
            buy = self.ETY_nbtItemPortEntryValueBuy.get()
            sell = self.ETY_nbtItemPortEntryValueSell.get()

            insertList = (name, buy, sell)

            self.TRW_nbtItemPortTree.insert("", "end", values = insertList)

            self.CBB_nbtItemPortEntry.current(0)
            self.ETY_nbtItemPortEntryValueBuy.delete(0, tk.END)
            self.ETY_nbtItemPortEntryValueSell.delete(0, tk.END)

    def buttonItemRemovePort(self):

        selection = self.TRW_nbtItemPortTree.selection()

        self.TRW_nbtItemPortTree.delete(selection)

        self.BTN_nbtItemPortButtonsRemove.config(state = "disabled")

    def buttonPortAddItem(self):

        if self.CBB_nbtPortItemEntry != f"-- {lang['titleItem'].lower()} --":

            name = self.CBB_nbtPortItemEntry.get()
            buy = self.ETY_nbtPortItemEntryValueBuy.get()
            sell = self.ETY_nbtPortItemEntryValueSell.get()

            insertList = (name, buy, sell)

            self.TRW_nbtPortItemTree.insert("", "end", values = insertList)

            self.CBB_nbtPortItemEntry.current(0)
            self.ETY_nbtPortItemEntryValueBuy.delete(0, tk.END)
            self.ETY_nbtPortItemEntryValueSell.delete(0, tk.END)

    def buttonPortRemoveItem(self):

        selection = self.TRW_nbtPortItemTree.selection()

        self.TRW_nbtPortItemTree.delete(selection)

        self.BTN_nbtPortItemButtonsRemove.config(state = "disabled")

    def buttonMainAdd(self):

        active = self.NTB_main.index(self.NTB_main.select())

        if active == 0: #item

            itemName = self.ETY_nbtItemName.get()
            itemImage = self.ETY_nbtItemImageEntry.get()
            itemAttr = self.CBB_nbtItemAttr.get()
            itemSattr = self.CBB_nbtItemSattr.get()

            if itemImage == "":

                itemImage = "None"

            trwEntries = self.TRW_nbtItemPortTree.get_children()

            itemPort = dict()

            for entry in trwEntries:

                port = dict(self.TRW_nbtItemPortTree.item(entry))["values"]

                value = f"{port[1]}-{port[2]}"

                itemPort[port[0]] = value

            if itemName == "" or itemAttr == "" or itemSattr == "":

                info = hand.general().getIniCont(infoPath)

                title = info["name"] + " - v. " + info["ver"] + "." + info["subVer"]

                messagebox.showinfo(title, lang["promptGeneralRequiredArguments"])

                return -1

            for item in projectData["item"]:

                if str(projectData["item"][item]["name"]).lower() == itemName.lower():

                    info = hand.general().getIniCont(infoPath)

                    title = info["name"] + " - v. " + info["ver"] + "." + info["subVer"]

                    messagebox.showinfo(title, lang["promptGeneralNameTaken"])

                    return -1

            check = False
            count = 0

            while check != True:

                if count >= 1000000:

                    return -1

                itemID = f"item{count:06d}"

                if itemID in projectData["item"]:

                    check = True

                else:

                    count += 1

            projectData["item"][itemID] = dict()

            projectData["item"][itemID]["name"] = itemName
            projectData["item"][itemID]["image"] = itemImage
            projectData["item"][itemID]["port"] = itemPort
            projectData["item"][itemID]["attr"] = itemAttr
            projectData["item"][itemID]["sattr"] = itemSattr

        elif active == 1: #area

            areaName = self.ETY_nbtAreaName.get()

            if areaName == "":

                info = hand.general().getIniCont(infoPath)

                title = info["name"] + " - v. " + info["ver"] + "." + info["subVer"]

                messagebox.showinfo(title, lang["promptGeneralRequiredArguments"])

                return -1

            for area in projectData["area"]:

                if str(projectData["area"][area]["name"]).lower() == areaName.lower():

                    info = hand.general().getIniCont(infoPath)

                    title = info["name"] + " - v. " + info["ver"] + "." + info["subVer"]

                    messagebox.showinfo(title, lang["promptGeneralNameTaken"])

                    return -1

            check = False
            count = 0

            while check != True:

                if count >= 1000000:

                    return -1

                areaID = f"area{count:06d}"

                if areaID in projectData["area"]:

                    check = True

                else:

                    count += 1

            projectData["area"][areaID] = dict()

            projectData["area"][areaID]["name"] = areaName
            projectData["area"][areaID]["sarea"] = list()

        elif active == 2: #sarea

            sareaName = self.ETY_nbtSareaName.get()
            sareaMaster = self.CBB_nbtSareaMaster.get()

            if sareaName == "" or sareaMaster == f"-- {lang['titleArea'].lower()} --":

                info = hand.general().getIniCont(infoPath)

                title = info["name"] + " - v. " + info["ver"] + "." + info["subVer"]

                messagebox.showinfo(title, lang["promptGeneralRequiredArguments"])

                return -1

            for sarea in projectData["sarea"]:

                if str(projectData["sarea"][sarea]["name"]).lower() == sareaName.lower():

                    info = hand.general().getIniCont(infoPath)

                    title = info["name"] + " - v. " + info["ver"] + "." + info["subVer"]

                    messagebox.showinfo(title, lang["promptGeneralNameTaken"])

                    return -1

            check = False
            count = 0

            while check != True:

                if count >= 1000000:

                    return -1

                sareaID = f"sarea{count:06d}"

                if sareaID in projectData["sarea"]:

                    check = True

                else:

                    count += 1

            projectData["sarea"][sareaID] = dict()

            projectData["sarea"][sareaID]["name"] = sareaName
            projectData["sarea"][sareaID]["port"] = list()

            for area in projectData["area"]:

                if projectData["area"][area]["name"] == sareaMaster:

                    areaID = area

            projectData["area"][areaID]["sarea"].append(sareaName)

        elif active == 3: #port

            portName = self.ETY_nbtPortName.get()
            portArea = self.CBB_nbtPortArea.get()
            portSarea = self.CBB_nbtPortSarea.get()

            trwEntries = self.TRW_nbtPortItemTree.get_children()

            portItem = dict()

            for entry in trwEntries:

                item = dict(self.TRW_nbtPortItemTree.item(entry))["values"]

                value = f"{item[1]}-{item[2]}"

                portItem[item[0]] = value

            for entry in portItem:

                for item in projectData["item"]:

                    if projectData["item"][item]["name"] == entry:

                        projectData["item"][item]["port"][portName] = portItem[entry]

            for sarea in projectData["sarea"]:

                if projectData["sarea"][sarea]["name"] == portSarea:

                    projectData["sarea"][sarea]["port"].append(portName)

            check = False
            count = 0

            while check != True:

                if count >= 1000000:

                    return -1

                portID = f"port{count:06d}"

                if portID in projectData["port"]:

                    check = True

                else:

                    count += 1

            projectData["port"][portID] = dict()

            projectData["port"][portID]["name"] = portName

        elif active == 4: #attr

            attrName = self.ETY_nbtAttrName.get()

            if attrName == "":

                info = hand.general().getIniCont(infoPath)

                title = info["name"] + " - v. " + info["ver"] + "." + info["subVer"]

                messagebox.showinfo(title, lang["promptGeneralRequiredArguments"])

                return -1

            for attr in projectData["attr"]:

                if str(projectData["attr"][attr]["name"]).lower() == attrName.lower():

                    info = hand.general().getIniCont(infoPath)

                    title = info["name"] + " - v. " + info["ver"] + "." + info["subVer"]

                    messagebox.showinfo(title, lang["promptGeneralNameTaken"])

                    return -1

            check = False
            count = 0

            while check != True:

                if count >= 1000000:

                    return -1

                attrID = f"attr{count:06d}"

                if attrID in projectData["attr"]:

                    check = True

                else:

                    count += 1

            projectData["attr"][attrID] = dict()

            projectData["attr"][attrID]["name"] = attrName
            projectData["attr"][attrID]["sattr"] = list()

        elif active == 5: #sattr

            sattrName = self.ETY_nbtSattrName.get()
            sattrMaster = self.CBB_nbtSattrMaster.get()

            if sattrName == "" or sattrMaster == f"-- {lang['titleAttribute'].lower()} --":

                info = hand.general().getIniCont(infoPath)

                title = info["name"] + " - v. " + info["ver"] + "." + info["subVer"]

                messagebox.showinfo(title, lang["promptGeneralRequiredArguments"])

                return -1

            for sattr in projectData["sattr"]:

                if str(projectData["sattr"][sattr]["name"]).lower() == sattrName.lower():

                    info = hand.general().getIniCont(infoPath)

                    title = info["name"] + " - v. " + info["ver"] + "." + info["subVer"]

                    messagebox.showinfo(title, lang["promptGeneralNameTaken"])

                    return -1

            check = False
            count = 0

            while check != True:

                if count >= 1000000:

                    return -1

                sattrID = f"sattr{count:06d}"

                if sattrID in projectData["sattr"]:

                    check = True

                else:

                    count += 1

            projectData["sattr"][sattrID] = dict()

            projectData["sattr"][sattrID]["name"] = sattrName

            for attr in projectData["attr"]:

                if projectData["attr"][attr]["name"] == sattrMaster:

                    attrID = attr

            projectData["attr"][attrID]["sattr"].append(sattrName)

        self.getInitialValues()

    def buttonMainClose(self):

        self.master.destroy()

class scrObjEdit:

    def __init__(self, master):

        self.master = master
        self.frame = ttk.Frame(self.master)

        self.frame.grid(column = 0, row = 0)

        

        self.frame.pack()

    def windowQuit(self):

        self.master.destroy()

class scrSettings:

    def __init__(self, master):

        self.master = master
        self.frame = ttk.Frame(self.master)

        self.frame.grid(column = 0, row = 0)

        

        self.frame.pack()

    def windowQuit(self):

        self.master.destroy()

######################################
# ---------------------------------- #
######################################
        
if __name__ == '__main__':
    main()
    
    
"""

get item of a treeview

active = self.TRW_nbtItemPortTree.selection()

item = dict(self.TRW_nbtItemPortTree.item(active))["values"]

print(item)    
    
    
"""
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#end
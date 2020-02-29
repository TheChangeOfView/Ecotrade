######################################
# ---------------------------------- #
######################################

# --- Imports

import tkinter as tk
from tkinter import ttk, filedialog
import os
import sys
from data.scripts import utilities as util
from data.scripts import fileHandling as hand

# --- Global Variables

infoPath = "data/info.ini"
settingsPath = "data/settings.ini"
projectData = {"name": None}

######################################
# ---------------------------------- #
######################################

def main(): # Main Function

    root = tk.Tk()
    mainScreen = scrMain(master = root)
    mainScreen.mainloop()

######################################
# ---------------------------------- #
######################################

class scrMain(ttk.Frame): # Main GUI
    
    def __init__(self, master = None): # GUI Init
        
        #--- Initialize Variables
        
        info = hand.general().getIniCont(infoPath)
        lang = hand.general().getLang(settingsPath)
        
        activeFstSelect = ""
        activeSndSelect = ""
        activeTrdSelect = ""
        activeOffer = ""
        itemImage = tk.PhotoImage(file = "data/noImage.pgm")
        
        sortingOptions = (lang["item"], lang["area"], lang["subarea"], lang["port"], lang["attribute"], lang["subattribute"])
        
        #####################################
        # --------- Create Window --------- #
        #####################################
    
        super().__init__(master)
        self.master = master
        
        # --- Master Settings
        
        master.title(info["name"] + " - v. " + info["ver"] + "." + info["subVer"])
        
        ########################################
        # --------- Creating Widgets --------- #
        ########################################
        
        # --- Listboxes Masterframe
        
        self.FRM_listboxes = ttk.Frame(master)
        
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

        TRW_offerColumnList = (f"{lang['item']} / {lang['port']}", lang["buy"], lang["sell"])

        self.TRW_offer = ttk.Treeview(self.FRM_listboxes, columns = TRW_offerColumnList, show = "headings", height = 25)

        self.TRW_offer.heading(0, text = TRW_offerColumnList[0])
        self.TRW_offer.column(0, width = 650)
        self.TRW_offer.heading(1, text = TRW_offerColumnList[1])
        self.TRW_offer.column(1, width = 75)
        self.TRW_offer.heading(2, text = TRW_offerColumnList[2])
        self.TRW_offer.column(2, width = 75)

        self.SLB_offer = ttk.Scrollbar(self.FRM_listboxes, orient = tk.VERTICAL, command = self.TRW_offer.yview)
        self.TRW_offer["yscrollcommand"] = self.SLB_offer.set

        items = [                                               # to be deleted

            ("test", "5", "1"),
            ("another test", "50", "30")

        ]

        for i in items:

            self.TRW_offer.insert("", "end", values = i)
        
        # --- Sorting Combobox
        
        self.LBL_sorting = ttk.Label(master, text = lang["sort"])
        self.CBB_sorting = ttk.Combobox(master, state = "readonly", width = 25, values = sortingOptions)       
        self.CBB_sorting.current(0)
        self.CBB_sorting.bind("<<ComboboxSelected>>", self.CBB_Sorting_callback)
        
        # --- Attributes Masterframe
        
        self.LBF_Attributes = ttk.Labelframe(master, text = lang["attributes"])
        
        # --- Attributes
        
        self.IMG_item = ttk.Label(self.LBF_Attributes, image = itemImage)
        self.IMG_item.image = itemImage
        
        self.FRM_value = ttk.Frame(self.LBF_Attributes)
        
        self.LBL_itemBuy = ttk.Label(self.FRM_value, text = lang["buy"])
        self.itemBuyActiveTextvariable = tk.StringVar()
        self.ETY_itemBuyActive = ttk.Entry(self.FRM_value, width = 12, state = "disabled", textvariable = self.itemBuyActiveTextvariable, justify = "center")
        
        self.LBL_itemSell = ttk.Label(self.FRM_value, text = lang["sell"])
        self.itemSellActiveTextvariable = tk.StringVar()
        self.ETY_itemSellActive = ttk.Entry(self.FRM_value, width = 12, state = "disabled", textvariable = self.itemSellActiveTextvariable, justify = "center")
        
        self.FRM_name = ttk.Frame(self.LBF_Attributes)
        self.LBL_name = ttk.Label(self.FRM_name, text = lang["item-name"], width = 35)
        self.TXT_nameActive = tk.Text(self.FRM_name, width = 20, height = 3, state = "disabled")
        
        self.FRM_port = ttk.Frame(self.LBF_Attributes)
        self.LBL_port = ttk.Label(self.FRM_port, text = lang["item-port"], width = 35)
        self.TXT_portActive = tk.Text(self.FRM_port, width = 20, height = 3, state = "disabled")
        
        self.FRM_area = ttk.Frame(self.LBF_Attributes)
        self.LBL_area = ttk.Label(self.FRM_area, text = lang["item-area"], width = 35)
        self.TXT_areaActive = tk.Text(self.FRM_area, width = 20, height = 3, state = "disabled")
        
        self.FRM_subarea = ttk.Frame(self.LBF_Attributes)
        self.LBL_subarea = ttk.Label(self.FRM_subarea, text = lang["item-subarea"], width = 35)
        self.TXT_subareaActive = tk.Text(self.FRM_subarea, width = 20, height = 3, state = "disabled")
        
        self.FRM_attribute = ttk.Frame(self.LBF_Attributes)
        self.LBL_attribute = ttk.Label(self.FRM_attribute, text = lang["item-attribute"], width = 35)
        self.TXT_attributeActive = tk.Text(self.FRM_attribute, width = 20, height = 3, state = "disabled")
        
        self.FRM_subattribute = ttk.Frame(self.LBF_Attributes)
        self.LBL_subattribute = ttk.Label(self.FRM_subattribute, text = lang["item-subattribute"], width = 35)
        self.TXT_subattributeActive = tk.Text(self.FRM_subattribute, width = 20, height = 3, state = "disabled")
        
        defaultItem = {"buy": "-", "sell": "-", "name": "-", "port": "-", "area": "-", "subarea": "-", "attribute": "-", "subattribute": "-"}
        
        self.setItemInfo(defaultItem)
        
        # --- Buttons Masterframe
        
        self.FRM_buttons = ttk.Frame(master)
        self.FRM_Subbuttons = ttk.Frame(self.FRM_buttons)
        
        # --- Buttons
        
        self.BTN_add = ttk.Button(self.FRM_buttons, text = lang["add"], width = 34, command = None)
        self.BTN_edit = ttk.Button(self.FRM_buttons, text = lang["edit"], width = 16, command = None)
        self.BTN_remove = ttk.Button(self.FRM_buttons, text = lang["remove"], width = 16, command = None)
        self.BTN_new = ttk.Button(self.FRM_Subbuttons, text = lang["new"], width = 34, command = None)
        self.BTN_save = ttk.Button(self.FRM_Subbuttons, text = lang["save"], width = 16, command = None)
        self.BTN_load = ttk.Button(self.FRM_Subbuttons, text = lang["load"], width = 16, command = self.loadProject)
        self.BTN_delete = ttk.Button(self.FRM_Subbuttons, text = lang["delete"], width = 34, command = None)
        self.BTN_settings = ttk.Button(self.FRM_buttons, text = lang["settings"], width = 16, command = None)
        self.BTN_quit = ttk.Button(self.FRM_buttons, text = lang["quit"], width = 16, command = self.quit)
        
        ######################################
        # --------- Allign Widgets --------- #
        ######################################
        
        # --- Master Grid
        
        self.grid(column = 0, row = 0)
        
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
        
        self.pack

    def CBB_Sorting_callback(self, event):

        lang = hand.general().getLang(settingsPath)
        
        value = self.CBB_sorting.current()

        self.LBX_stSelect.config(state = "normal")
        self.LBX_ndSelect.config(state = "normal")
        self.LBX_rdSelect.config(state = "normal")

        self.LBX_stSelect.delete(0, tk.END)
        self.LBX_ndSelect.delete(0, tk.END)
        self.LBX_rdSelect.delete(0, tk.END)
        self.TRW_offer.delete(*self.TRW_offer.get_children())
        
        if value == 0: #Item
            
            self.LBL_stSelect.config(text = lang["item"])
            self.LBL_ndSelect.config(text = "-")
            self.LBL_rdSelect.config(text = "-")
            
            self.LBX_stSelect.config(state = "normal")
            self.LBX_ndSelect.config(state = "disabled")
            self.LBX_rdSelect.config(state = "disabled")
        
        elif value == 1: #Area
            
            self.LBL_stSelect.config(text = lang["area"])
            self.LBL_ndSelect.config(text = lang["subarea"])
            self.LBL_rdSelect.config(text = lang["port"])
            
            self.LBX_stSelect.config(state = "normal")
            self.LBX_ndSelect.config(state = "normal")
            self.LBX_rdSelect.config(state = "normal")
        
        elif value == 2: #Subarea
            
            self.LBL_stSelect.config(text = lang["subarea"])
            self.LBL_ndSelect.config(text = lang["port"])
            self.LBL_rdSelect.config(text = "-")
            
            self.LBX_stSelect.config(state = "normal")
            self.LBX_ndSelect.config(state = "normal")
            self.LBX_rdSelect.config(state = "disabled")
        
        elif value == 3: #Port
            
            self.LBL_stSelect.config(text = lang["port"])
            self.LBL_ndSelect.config(text = "-")
            self.LBL_rdSelect.config(text = "-")
            
            self.LBX_stSelect.config(state = "normal")
            self.LBX_ndSelect.config(state = "disabled")
            self.LBX_rdSelect.config(state = "disabled")
        
        elif value == 4: #Attribute
            
            self.LBL_stSelect.config(text = lang["attribute"])
            self.LBL_ndSelect.config(text = lang["subattribute"])
            self.LBL_rdSelect.config(text = lang["item"])
            
            self.LBX_stSelect.config(state = "normal")
            self.LBX_ndSelect.config(state = "normal")
            self.LBX_rdSelect.config(state = "normal")
        
        elif value == 5: #Subattribute
            
            self.LBL_stSelect.config(text = lang["subattribute"])
            self.LBL_ndSelect.config(text = lang["item"])
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

            elif self.CBB_sorting.current() == 1: # - Area

                self.LBX_ndSelect.delete(0, tk.END)
                self.LBX_rdSelect.delete(0, tk.END)
                self.TRW_offer.delete(*self.TRW_offer.get_children())

                allAreas = self.LBX_stSelect.get(0, tk.END)
                selectionIndex = self.LBX_stSelect.curselection()
                selectionList = [allAreas[area] for area in selectionIndex]
                selection = selectionList[0]

                if selection == "(All)":

                    sortList = list()

                    for entry in projectData["sarea"]:

                        sortList.append(projectData["sarea"][entry]["name"])

                    sortList.sort()

                    if len(projectData["sarea"]) > 1:

                        self.LBX_ndSelect.insert(tk.END, "(All)")

                    for entry in sortList:

                        self.LBX_ndSelect.insert(tk.END, entry)

                else:

                    for entry in projectData["area"]:

                        if projectData["area"][entry]["name"] == selection:

                            areaID = entry

                    sortList = list()

                    for entry in projectData["area"][areaID]["sarea"]:

                        sortList.append(entry)

                    if len(projectData["sarea"]) > 1:

                        self.LBX_ndSelect.insert(tk.END, "(All)")

                    sortList.sort()

                    for entry in sortList:

                        self.LBX_ndSelect.insert(tk.END, entry)

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

                if selection == "(All)":

                    sortList = list()

                    for entry in projectData["port"]:

                        sortList.append(projectData["port"][entry]["name"])

                    sortList.sort()

                    for entry in sortList:

                        self.LBX_ndSelect.insert(tk.END, entry)
                
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

            elif self.CBB_sorting.current() == 4: # - Attribute

                self.LBX_ndSelect.delete(0, tk.END)
                self.LBX_rdSelect.delete(0, tk.END)
                self.TRW_offer.delete(*self.TRW_offer.get_children())

                allAttrs = self.LBX_stSelect.get(0, tk.END)
                selectionIndex = self.LBX_stSelect.curselection()
                selectionList = [allAttrs[attr] for attr in selectionIndex]
                selection = selectionList[0]

                if selection == "(All)":

                    sortList = list()

                    for entry in projectData["sattr"]:

                        sortList.append(projectData["sattr"][entry]["name"])

                    sortList.sort()

                    if len(projectData["sattr"]) > 1:

                        self.LBX_ndSelect.insert(tk.END, "(All)")
                    
                    for entry in sortList:

                        self.LBX_ndSelect.insert(tk.END, entry)

                else:

                    for entry in projectData["attr"]:

                        if projectData["attr"][entry]["name"] == selection:

                            attrID = entry

                    sortList = list()

                    for entry in projectData["attr"][attrID]["sattr"]:

                        sortList.append(entry)

                    sortList.sort()

                    if len(projectData["sattr"]) > 1:

                        self.LBX_ndSelect.insert(tk.END, "(All)")

                    for entry in sortList:

                        self.LBX_ndSelect.insert(tk.END, entry)

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

                if selection == "(All)":

                    sortList = list()

                    for entry in projectData["item"]:

                        sortList.append(projectData["item"][entry]["name"])

                    sortList.sort()

                    for entry in sortList:

                        self.LBX_ndSelect.insert(tk.END, entry)

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

                if selection == "(All)":

                    if selectionFirst == "(All)":

                        sortList = list()

                        for entry in projectData["port"]:

                            sortList.append(projectData["port"][entry]["name"])

                        sortList.sort()

                        for entry in sortList:

                            self.LBX_rdSelect.insert(tk.END, entry)

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

                if selection == "(All)":

                    if selectionFirst == "(All)":

                        sortList = list()

                        for entry in projectData["item"]:

                            sortList.append(projectData["item"][entry]["name"])

                        sortList.sort()

                        for entry in sortList:

                            self.LBX_rdSelect.insert(tk.END, entry)

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

            elif self.CBB_sorting.current() == 5: # - Subttribute - Item - None

                pass

    def loadProject(self):

        global projectData

        lang = hand.general().getLang(settingsPath)
        info = hand.general().getIniCont(infoPath)

        filePath = filedialog.askopenfilename(
            
            initialdir = (sys.path[0] + "\\save"),
            title = lang["loadProj"],
            filetypes = (

                (f"{info['name']} Database File",f"*{info['dbExtension']}"),
                ("all files","*.*")

                )

            )

        if filePath == "":

            return -1

        projectData = hand.project().load(filePath)

        self.browserSetFirstSection()
        
    def setItemInfo(self, item):
        
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
        self.TXT_subareaActive.insert(1.0, item["subarea"])
        self.TXT_subareaActive.config(state = "disabled")
        
        self.TXT_attributeActive.config(state = "normal")
        self.TXT_attributeActive.delete(1.0, "end")
        self.TXT_attributeActive.insert(1.0, item["attribute"])
        self.TXT_attributeActive.config(state = "disabled")
        
        self.TXT_subattributeActive.config(state = "normal")
        self.TXT_subattributeActive.delete(1.0, "end")
        self.TXT_subattributeActive.insert(1.0, item["subattribute"])
        self.TXT_subattributeActive.config(state = "disabled")
        
    def browserSetFirstSection(self):

        lang = hand.general().getLang(settingsPath)

        activeSorting = self.CBB_sorting.get()

        self.LBX_stSelect.delete(0, tk.END)
        self.LBX_ndSelect.delete(0, tk.END)
        self.LBX_rdSelect.delete(0, tk.END)
        self.TRW_offer.delete(*self.TRW_offer.get_children())

        if activeSorting == lang["item"]:

            sortList = list()

            for item in projectData["item"]:

                sortList.append(projectData["item"][item]["name"])

            sortList.sort()

            for entry in sortList:

                self.LBX_stSelect.insert(tk.END, entry)
            
        elif activeSorting == lang["area"]:

            sortList = list()

            for area in projectData["area"]:

                sortList.append(projectData["area"][area]["name"])

            sortList.sort()

            if len(projectData["area"]) > 1:

                self.LBX_stSelect.insert(tk.END, "(All)")

            for entry in sortList:

                self.LBX_stSelect.insert(tk.END, entry)

        elif activeSorting == lang["subarea"]:

            sortList = list()

            for sarea in projectData["sarea"]:

                sortList.append(projectData["sarea"][sarea]["name"])

            sortList.sort()

            if len(projectData["sarea"]) > 1:

                self.LBX_stSelect.insert(tk.END, "(All)")

            for entry in sortList:

                self.LBX_stSelect.insert(tk.END, entry)

        elif activeSorting == lang["port"]:

            sortList = list()

            for port in projectData["port"]:

                sortList.append(projectData["port"][port]["name"])

            sortList.sort()

            for entry in sortList:

                self.LBX_stSelect.insert(tk.END, entry)

        elif activeSorting == lang["attribute"]:

            sortList = list()

            for attr in projectData["attr"]:

                sortList.append(projectData["attr"][attr]["name"])

            sortList.sort()

            if len(projectData["attr"]) > 1:

                self.LBX_stSelect.insert(tk.END, "(All)")

            for entry in sortList:

                self.LBX_stSelect.insert(tk.END, entry)

        elif activeSorting == lang["subattribute"]:

            sortList = list()

            for sattr in projectData["sattr"]:

                sortList.append(projectData["sattr"][sattr]["name"])

            sortList.sort()

            if len(projectData["sattr"]) > 1:

                self.LBX_stSelect.insert(tk.END, "(All)")

            for entry in sortList:

                self.LBX_stSelect.insert(tk.END, entry)

######################################
# ---------------------------------- #
######################################
        
if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#end
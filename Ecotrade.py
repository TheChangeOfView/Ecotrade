######################################
# ---------------------------------- #
######################################

# --- Imports

import tkinter as tk
from tkinter import ttk
from data.scripts import utilities as util
from data.scripts import fileHandling as hand

# --- Global Variables

infoPath = "data/info.ini"
settingsPath = "data/settings.ini"
activeProject = "None"

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

        general = hand.general()
        
        info = general.getIniCont(infoPath)
        lang = general.getLang(settingsPath)
        
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
        self.LBX_stSelect = tk.Listbox(self.FRM_listboxes, height = 24, width = 30)
        self.SLB_stSelect = ttk.Scrollbar(self.FRM_listboxes, orient = tk.VERTICAL, command = self.LBX_stSelect.yview)
        self.LBX_stSelect["yscrollcommand"] = self.SLB_stSelect.set
        
        # --- Second Listbox (Upper Upper Right)
        
        self.LBL_ndSelect = ttk.Label(self.FRM_listboxes, text = activeSndSelect)
        self.LBX_ndSelect = tk.Listbox(self.FRM_listboxes, height = 12, width = 30)
        self.SLB_ndSelect = ttk.Scrollbar(self.FRM_listboxes, orient = tk.VERTICAL, command = self.LBX_ndSelect.yview)
        self.LBX_ndSelect["yscrollcommand"] = self.SLB_ndSelect.set
        
        # --- Third Listbox (Lower Upper Right)
        
        self.LBL_rdSelect = ttk.Label(self.FRM_listboxes, text = activeTrdSelect)
        self.LBX_rdSelect = tk.Listbox(self.FRM_listboxes, height = 12, width = 30)
        self.SLB_rdSelect = ttk.Scrollbar(self.FRM_listboxes, orient = tk.VERTICAL, command = self.LBX_rdSelect.yview)
        self.LBX_rdSelect["yscrollcommand"] = self.SLB_rdSelect.set
        
        # --- Offer Listbox (Lower)
        
        self.LBL_offer = ttk.Label(self.FRM_listboxes, text = activeOffer)
        self.LBX_offer = tk.Listbox(self.FRM_listboxes, height = 24)
        self.SLB_offer = ttk.Scrollbar(self.FRM_listboxes, orient = tk.VERTICAL, command = self.LBX_offer.yview)
        self.LBX_offer["yscrollcommand"] = self.SLB_offer.set
        
        # --- Sorting Combobox
        
        self.LBL_sorting = ttk.Label(master, text = lang["sort"])
        self.CBB_sorting = ttk.Combobox(master, state = "readonly", width = 25, values = sortingOptions)       
        self.CBB_sorting.current(0)
        self.CBB_sorting.bind("<<ComboboxSelected>>", self.resort)
        
        self.resort(None)
        
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
        self.TXT_nameActive = tk.Text(self.FRM_name, width = 20, height = 2, state = "disabled")
        
        self.FRM_port = ttk.Frame(self.LBF_Attributes)
        self.LBL_port = ttk.Label(self.FRM_port, text = lang["item-port"], width = 35)
        self.TXT_portActive = tk.Text(self.FRM_port, width = 20, height = 2, state = "disabled")
        
        self.FRM_area = ttk.Frame(self.LBF_Attributes)
        self.LBL_area = ttk.Label(self.FRM_area, text = lang["item-area"], width = 35)
        self.TXT_areaActive = tk.Text(self.FRM_area, width = 20, height = 2, state = "disabled")
        
        self.FRM_subarea = ttk.Frame(self.LBF_Attributes)
        self.LBL_subarea = ttk.Label(self.FRM_subarea, text = lang["item-subarea"], width = 35)
        self.TXT_subareaActive = tk.Text(self.FRM_subarea, width = 20, height = 2, state = "disabled")
        
        self.FRM_attribute = ttk.Frame(self.LBF_Attributes)
        self.LBL_attribute = ttk.Label(self.FRM_attribute, text = lang["item-attribute"], width = 35)
        self.TXT_attributeActive = tk.Text(self.FRM_attribute, width = 20, height = 2, state = "disabled")
        
        self.FRM_subattribute = ttk.Frame(self.LBF_Attributes)
        self.LBL_subattribute = ttk.Label(self.FRM_subattribute, text = lang["item-subattribute"], width = 35)
        self.TXT_subattributeActive = tk.Text(self.FRM_subattribute, width = 20, height = 2, state = "disabled")
        
        defaultItem = {"buy": "-", "sell": "-", "name": "-", "port": "-", "area": "-", "subarea": "-", "attribute": "-", "subattribute": "-"}
        
        self.setItemInfo(defaultItem)
        
        # --- Buttons Masterframe
        
        self.FRM_buttons = ttk.Frame(master)
        self.FRM_Subbuttons = ttk.Frame(self.FRM_buttons)
        
        # --- Buttons

        item = hand.item()
        
        self.BTN_add = ttk.Button(self.FRM_buttons, text = lang["add"], width = 34, command = item.get(activeProject))
        self.BTN_edit = ttk.Button(self.FRM_buttons, text = lang["edit"], width = 16, command = None)
        self.BTN_remove = ttk.Button(self.FRM_buttons, text = lang["remove"], width = 16, command = None)
        self.BTN_new = ttk.Button(self.FRM_Subbuttons, text = lang["new"], width = 34, command = None)
        self.BTN_save = ttk.Button(self.FRM_Subbuttons, text = lang["save"], width = 16, command = None)
        self.BTN_load = ttk.Button(self.FRM_Subbuttons, text = lang["load"], width = 16, command = None)
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
        
        # --- Offer Listbox (Lower)
        
        self.LBL_offer.grid(column = 0, row = 4, columnspan = 4)
        self.LBX_offer.grid(column = 0, row = 5, columnspan = 4, sticky = (tk.W, tk.E))
        self.SLB_offer.grid(column = 4, row = 5, sticky = (tk.N, tk.S))
        
        # --- Listboxes Masterframe
        
        self.FRM_listboxes.grid(column = 1, row = 1, rowspan = 3)
        
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
        
    def resort(self, event):
        
        general = hand.general()

        lang = general.getLang(settingsPath)
        
        value = self.CBB_sorting.current()
        
        if value == 0: #Item
            
            self.LBL_stSelect.config(text = lang["item"])
            self.LBL_ndSelect.config(text = "-")
            self.LBL_rdSelect.config(text = "-")
            self.LBL_offer.config(text = lang["port"])
            
            self.LBL_stSelect.config(state = "normal")
            self.LBL_ndSelect.config(state = "disabled")
            self.LBL_rdSelect.config(state = "disabled")
            self.LBL_offer.config(state = "normal")
        
        elif value == 1: #Area
            
            self.LBL_stSelect.config(text = lang["area"])
            self.LBL_ndSelect.config(text = lang["subarea"])
            self.LBL_rdSelect.config(text = lang["port"])
            self.LBL_offer.config(text = lang["item"])
            
            self.LBL_stSelect.config(state = "normal")
            self.LBL_ndSelect.config(state = "normal")
            self.LBL_rdSelect.config(state = "normal")
            self.LBL_offer.config(state = "normal")
        
        elif value == 2: #Subarea
            
            self.LBL_stSelect.config(text = lang["subarea"])
            self.LBL_ndSelect.config(text = lang["port"])
            self.LBL_rdSelect.config(text = "-")
            self.LBL_offer.config(text = lang["item"])
            
            self.LBL_stSelect.config(state = "normal")
            self.LBL_ndSelect.config(state = "normal")
            self.LBL_rdSelect.config(state = "disabled")
            self.LBL_offer.config(state = "normal")
        
        elif value == 3: #Port
            
            self.LBL_stSelect.config(text = lang["port"])
            self.LBL_ndSelect.config(text = "-")
            self.LBL_rdSelect.config(text = "-")
            self.LBL_offer.config(text = lang["item"])
            
            self.LBL_stSelect.config(state = "normal")
            self.LBL_ndSelect.config(state = "disabled")
            self.LBL_rdSelect.config(state = "disabled")
            self.LBL_offer.config(state = "normal")
        
        elif value == 4: #Attribute
            
            self.LBL_stSelect.config(text = lang["attribute"])
            self.LBL_ndSelect.config(text = lang["subattribute"])
            self.LBL_rdSelect.config(text = lang["port"])
            self.LBL_offer.config(text = lang["item"])
            
            self.LBL_stSelect.config(state = "normal")
            self.LBL_ndSelect.config(state = "normal")
            self.LBL_rdSelect.config(state = "normal")
            self.LBL_offer.config(state = "normal")
        
        elif value == 5: #Subattribute
            
            self.LBL_stSelect.config(text = lang["subattribute"])
            self.LBL_ndSelect.config(text = lang["port"])
            self.LBL_rdSelect.config(text = "-")
            self.LBL_offer.config(text = lang["item"])
            
            self.LBL_stSelect.config(state = "normal")
            self.LBL_ndSelect.config(state = "normal")
            self.LBL_rdSelect.config(state = "disabled")
            self.LBL_offer.config(state = "normal")
        
        else:
            
            pass

######################################
# ---------------------------------- #
######################################
        
if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#end
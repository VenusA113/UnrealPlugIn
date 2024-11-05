from ast import ImportFrom #Importing ImportFrom class from the ast module
import tkinter.filedialog # Importing file dialog submodule from the tkinter module for GUI file dialog 
from unreal import (ToolMenuContext, ToolMenus,
                     uclass,
                     ufunction,
                     ToolMenuEntryScript) # Importing necessary classes and functions from the Unreal module

import os  # Importing standard libraries for operating system functionalities 
import sys # Importing standard libraries for system-specific parameters and functions
import importlib # Importing the importlib module to reload modules 
import tkinter # Importing the tkinter module for creating GUI applications

srcPath = os.path.dirname(os.path.abspath(__file__)) #Gets the directory path of the current script
if srcPath not in sys.path: # Adds the script's directory to the system path if not already there
    sys.path.append(srcPath)

import UnrealUtilities # Importing the UnrealUtilities module 
importlib.reload(UnrealUtilities) # Reloading the UnrealUtilities module to ensure the latest version is used 

@uclass() # Defining a class for the Build Base Material entry script in the Unreal menu
class BuildBaseMaterialEntryScript(ToolMenuEntryScript): 
    @ufunction(override=True) # Overriding the execute function of the parent class to customize behavior
    def execute(self, context) -> None: 
        UnrealUtilities.UnrealUtility().FindorBuildBaseMaterial() #Calling the FindorBuildBaseMaterial method of UnrealUtility class

@uclass() # Defining a class for the load Mesh entry script in the Unreal menu
class LoadMeshEntryScript(ToolMenuEntryScript):
    @ufunction(override=True) # Overriding the execute function of the parent class to customize behavior
    def execute(self, context) -> None:
        window = tkinter.Tk() # Creating a hidden Tkinter window
        window.withdraw()
        importDir = tkinter.filedialog.askdirectory() # Opening a dialog to select a directory 
        window.destroy() # Destroying the Tkinter window
        UnrealUtilities.UnrealUtility()>ImportFrom(importDir) # Calling the ImportFrom method of UnrealUtility with the selected directory

class UnrealSubstancePlugin: # Defining the main plugin class for Unreal Engine 
    def __init__(self): # Initializing the plugin class
        self.submenuName="Unreal Substance Plugin" # Setting the submenu name for the plugin
        self.submenuLabel="Unreal Substance Plugin" # Setting the submenu label for the plugin
        self.CreateMenu() # Calling the method to create the menu

    def CreateMenu(self):  # Method for creating the submenu in the Unreal Editor's 
        mainMenu = ToolMenus.get().find_menu("LevelEditor.MainMenu") # Finding the main menu in Unreal Engine's Level Editor

        existing = ToolMenus.get().find_menu(f"LevelEditor.MainMenu.{self.submenuName}") # Checking if the submenu already exists and removing it if it does 
        if existing:
            print(f"deleting previous menu: {existing}") # Printing a message to indicate the removal of the existing submenu
            ToolMenus.get().remove_menu(existing.menu_name) # Removing the existing submenu 

        self.submenu = mainMenu.add_sub_menu(mainMenu.menu_name, "", "Unreal Substance Plugin", "Unreal Substance Plugin") # Adding a new submenu to the main menu 
        self.AddEntryScript("BuildBaseMaterial", "Build Base Material", BuildBaseMaterialEntryScript()) # Adding the BuildBaseMaterial to the submenu 
        ToolMenus.get().refresh_all_widgets() # Refreshing all widgets to apply changes 
    
    def AddEntryScript(self, name, label, script: ToolMenuEntryScript): # Method for adding an entry script to the submenu 
        script.init_entry(self.submenu.menu_name, self.submenu.menu_name, "", name, label) # Initializing the menu entry with the submenu details 
        script.register_menu_entry() # Registering the menu entry in Unreal Engine 

UnrealSubstancePlugin() # Creating an instance of the plugin class to initialize it and create the menu 
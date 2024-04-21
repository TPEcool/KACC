'''
GUI version of KACC.
'''

from srctools import bsp
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askyesno
from ttkbootstrap import *
import json
import os
from assetcreator import AssetCreator

win = Window('KACC (GUI version)', 'darkly')

jsonFolder = os.path.join(os.getcwd(), 'Assets')
jsonassets = []
creditlist = []

def init():
    '''
    Search for asset configs and add file paths to a list.
    '''
    jsonlist = os.listdir(jsonFolder)
    for index, item in enumerate(jsonlist):
        print(f'Indexing over JSON file "{item}" (#{index})')
        if os.path.splitext(item)[1] == '.json':
            jsonassets.append(os.path.join(jsonFolder, item))
            
    print(f'Found and indexed {len(jsonassets)} JSON files.')

def find():
    '''
    Search for assets in map.
    '''
    f = askopenfilename(defaultextension='.bsp', filetypes=[('BSP map file', '.bsp')])
    if f:
        mapf = bsp.BSP(f)
        paklist = mapf.pakfile.namelist()
        foundassets = search(paklist)
        print('Generating credits...')
        
        progressbar.config(maximum=len(foundassets))
        for index, item in enumerate(foundassets):
            progressbar.config(value=index + 1)
            
            with open(item, 'r', encoding='UTF-8') as f:
                json_obj = json.load(f)
                credit_type = json_obj['creditType']
                manualcredit = False
                if credit_type != 'none':
                    if credit_type == 'optional':
                        manualcredit = askyesno(f'Confirm credit for "{json_obj["assetName"]}"', f'"{json_obj["assetName"]}" has the credit type set to preferred.\nWould you like to credit {json_obj["assetAuthor"]}?')
                    if manualcredit or credit_type == 'required':
                        creditlist.append(json_obj)
                        
        credits = ''
    
        for file in creditlist:
            credits += f'{file["assetName"]} by {file["assetAuthor"]}\n'
                        
        credits_save_file = asksaveasfilename(confirmoverwrite=True, defaultextension='.txt', filetypes=[('Plain text file', '.txt')])
        if credits_save_file:
            with open(credits_save_file, 'w') as crfile:
                crfile.write(credits)
                
            if askyesno('Credits file is ready', 'Would you like to open the credits file in the default program?'):
                os.startfile(credits_save_file)
                
        progressbar.config(value=0)
        
isJson = lambda f: os.path.splitext(f)[1] == '.json'

progressbar = Progressbar(win, length = 200, style=(STRIPED, INFO))
progressbar.pack(side=BOTTOM, expand=True, fill=X, anchor=S, padx=5, pady=5)

assetcreator_isrunning = BooleanVar(win, False)

def add():
    if not assetcreator_isrunning.get():
        assetc = AssetCreator(assetcreator_isrunning)
    else: assetc.show()
    
def search(paklist: list[str]):
    '''
    Search for assets in asset configs and see if they're in the map.
    '''
    foundassets = []
    progressbar.config(maximum=len(jsonassets))
    for index, item in enumerate(jsonassets):
        print(item)
        progressbar.config(value=index + 1)
        with open(jsonassets[index], 'r', encoding='UTF-8') as jsfile:
            json_obj = json.load(jsfile)
            asset_paths = json_obj['assetPaths']
            
            for path in asset_paths:
                if path in paklist and item not in foundassets:
                    foundassets.append(item)
    return foundassets

button_panel = Frame(win)
button_panel.pack(side=LEFT, fill=Y, expand=True, anchor=W, padx=5, pady=5)
add_asset_button = Button(button_panel, text='Add asset', command = add)
add_asset_button.pack(side=TOP, padx=5, pady=5, expand=True)

find_asset_button = Button(button_panel, text = 'Find asset', command = find)
find_asset_button.pack(side=TOP, expand=True, padx=5, pady=5)

init()

win.mainloop()
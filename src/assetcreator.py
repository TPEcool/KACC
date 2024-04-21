from ttkbootstrap import *

class AssetCreator:
    '''
    KACC asset creator window.
    '''
    def __init__(self, var: BooleanVar):
        '''
        Create new asset creator window.
        '''
        self.var = var
        
        self.window = Toplevel('Asset creator')
        self.menu = Menu(self.window)
        self.window.configure(menu=self.menu)
        self.file_menu = Menu(self.menu)
        self.menu.add_cascade(menu=self.file_menu, label='File')
        
        
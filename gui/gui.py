from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from PySide2.QtGui import QFont
from config import definitions
import os
import src
import sys
from . import resources
from . import dialogue

class Gui:

    def __init__(self):
        self.json_file = None

        self.app = QtWidgets.QApplication(sys.argv)
        self.load_ui_file()
        self.setup_main_window()
        self.window.show()
        self.connect_toolbar_actions()
        self.connect_editor()
        self.set_font()
        self.app.exec_()

    def load_ui_file(self):
        self.ui_file = os.path.join(definitions.ROOT_DIR, "gui", "jsontool.ui")
        self.loader = QUiLoader()

    def setup_main_window(self):
        self.window = self.loader.load(self.ui_file, None)
        self.editor = src.Editor()
        self.window.setCentralWidget(self.editor)

    def update_editor_text(self, file_data):
        # Try to pretty up json
        # If not valid json, exception will print plaintext
        try:
            pretty_json = src.Validator(file_data).pretty_print_json()
            self.editor.setPlainText(pretty_json)
        except:
            # Get the data out of the File Handler
            self.editor.setPlainText(file_data)

    def set_font(self):
        font = QFont("Consolas", 11)
        self.editor.setFont(font)

    #----------------Button Actions----------------#

    def open_file_action(self):
        try:
            fh = src.FileHandler(self.window)
            self.json_file = fh.open_file_dialog()
        except FileNotFoundError:
            title = "An error occured while opening the file!"
            text = "Oh no! The file could not be found. Please make sure the file exists or creaete a new file."
            dialogue.Dialogue(title, text)
        # If file successfully open, print text to editor    
        else:
            self.update_editor_text(fh.get_data())

    def save_file_action(self):
        try:
            save_data = self.editor.toPlainText()
            fh = src.FileHandler(self.window, save_data)
            self.json_file = fh.save_file_dialog()
            
            flag = True

            if self.json_file is None:
                flag = False
                title = "Save Canceled!"
                text = "Oh no! The save action was canceled."
                dialogue.Dialogue(title, text)

        except:
            title = "Could not save file!"
            text = "Oh no! The file could not be saved."
            dialogue.Dialogue(title, text)
        else:
            if flag:
                title = "Save Successful!"
                text = "Yay! The file saved successfully."
                dialogue.Dialogue(title, text)

    def delete_file_action(self):
        try:
           
            if self.json_file is None:
                title = "Delete Content"
                question = "Are you sure you want to delete the editor content?"
                dg = dialogue.Dialogue(title, text=question, question=True)
                if dg.check_answer():
                    self.update_editor_text("")
            else:
                title = "Delete File"
                question = f"Are you sure you want to clear the editor and delete the file {self.json_file}?"
                dg = dialogue.Dialogue(title, text=question, question=True)
                if dg.check_answer():
                    fh = src.FileHandler(self.window)
                    fh.delete_file(self.json_file)
                    self.update_editor_text("")
                    self.json_file = None
        except Exception as err:
            dialogue.Dialogue("Delete Failed", "Oh no! There was a problem deleting your file.")
            print(err)
            raise
            
    #-------------Button Connections--------------#

    def connect_toolbar_actions(self):
        self.toolbar = self.window.toolBar

        open = self.window.actionOpen_File
        save = self.window.actionSave_File
        delete = self.window.actionDelete_File

        open.triggered.connect(self.open_file_action)
        save.triggered.connect(self.save_file_action)
        delete.triggered.connect(self.delete_file_action)

    #-----------------Validation--------------------#

    def validate_editor_text(self):
        e_text = self.editor.toPlainText()
        val = src.Validator(e_text)

        if not val.valid_json():
            error_line =  val.get_error_pos()[1]
            self.editor.highlight_error_line(error_line)
        else:
            self.editor.clear_all_errors()
        
    def connect_editor(self):
        self.editor.textChanged.connect(self.validate_editor_text)
import os
from PySide2.QtWidgets import QFileDialog

class FileHandler:
    def __init__(self, window, save_data=None):
        self.window = window
        self.save_data = save_data
        self.json_file = None
        self.data = None
    

    def open_file_dialog(self):
        options = QFileDialog.Options()
        init_dir = os.path.expanduser("~\Documents")
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self.window, "Select a JSON file", init_dir, "JSON Files (*.json);;All Files(*)", options=options)
        if file_path:
            print(file_path)
            self.json_file = file_path
            self.open_file()
            return self.json_file
            

    def save_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getSaveFileName(self.window,"Save your JSON file","","JSON Files (*.json);;All Files (*)", options=options)
        if file_path:
            print(file_path)
            self.json_file = file_path
            self.save_file()
            return self.json_file

    def open_file(self):
        # with open automatically closes the file when not being used
        with open(self.json_file, "r", encoding="utf-8") as f:
            self.data = f.read()

    def get_data(self):
        return self.data

    def save_file(self):
        with open(self.json_file, "w") as f:
            f.write(self.save_data)

    def delete_file(self, file_path):
        os.remove(file_path)

    def alert_editor(self):
        pass
     
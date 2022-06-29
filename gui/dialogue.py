from PySide2.QtWidgets import QMessageBox

class Dialogue(QMessageBox):
    
    def __init__(self, title, text=None, question=None):
        super(Dialogue, self).__init__()
        self.title = title
        self.text = text
        self.question = question
        self.answer = None
            
        self.setWindowTitle(self.title)
        self.setText(self.text)
        
        # Ability to create question based dialogue box
        if question is not None:
            self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            self.setDefaultButton(QMessageBox.No)

        self.answer = self.exec()

    def check_answer(self):
        if self.answer == QMessageBox.Yes:
            return True
        else:
            return False

    def get_answer(self):
        return self.answer

from PySide2.QtCore import *
from PySide2.QtGui  import *
from PySide2.QtWidgets import *


class LineNumberArea(QWidget):


    def __init__(self, editor):
        super().__init__(editor)
        self.myeditor = editor


    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)


    def paintEvent(self, event):
        self.myeditor.lineNumberAreaPaintEvent(event)


class Editor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.lineNumberArea = LineNumberArea(self)
        self.selectionTracking = []
        self.extraSelections = []
        

        self.connect(self, SIGNAL('blockCountChanged(int)'), self.updateLineNumberAreaWidth)
        self.connect(self, SIGNAL('updateRequest(QRect,int)'), self.updateLineNumberArea)
        self.connect(self, SIGNAL('cursorPositionChanged()'), self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)

    # Calculates the width base on the line numbers and font size
    def lineNumberAreaWidth(self):
        digits = 1
        count = max(1, self.blockCount())
        while count >= 10:
            count /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space


    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)


    def updateLineNumberArea(self, rect, dy):

        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(),
                       rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    # Overrides the resize to keep line number areas uniform
    def resizeEvent(self, event):
        super().resizeEvent(event)

        cr = self.contentsRect();
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(),
                    self.lineNumberAreaWidth(), cr.height()))


    # Paint event called to paint the line number block on left side of GUI gray
    def lineNumberAreaPaintEvent(self, event):
        mypainter = QPainter(self.lineNumberArea)

        mypainter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                mypainter.setPen(Qt.black)
                mypainter.drawText(0, top, self.lineNumberArea.width(), height,
                 Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1


    # Tracks the cursor and sets the line color based on cursor position
    def highlightCurrentLine(self):
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            lineColor = QColor(Qt.yellow).lighter(160)

            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()

            if "c" in self.selectionTracking:
                index = self.selectionTracking.index("c")
                self.selectionTracking.pop(index)
                self.extraSelections.pop(index)

            self.selectionTracking.append("c")
            self.extraSelections.append(selection)
        self.setExtraSelections(self.extraSelections)


    # Passed an error line and highlights the line error with red
    def highlight_error_line(self, error_line):

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            lineColor = QColor(Qt.red).lighter(160)

            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            document = self.document()
            block = document.findBlockByLineNumber(error_line - 1)
            pos = block.position()
            selection.cursor = self.textCursor()
            selection.cursor.setPosition(pos)
            selection.cursor.clearSelection()

            self.clear_all_errors()

            self.selectionTracking.append("e")
            self.extraSelections.append(selection)
        self.setExtraSelections(self.extraSelections)

    # Removes errors from highlighted selections list
    def clear_all_errors(self):
        if "e" in self.selectionTracking:
            index = self.selectionTracking.index("e")
            self.selectionTracking.pop(index)
            self.extraSelections.pop(index)



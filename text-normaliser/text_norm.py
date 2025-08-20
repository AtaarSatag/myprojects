import sys

from GUI import Ui_MainWindow
from PyQt5 import QtGui
from PyQt5.QtCore import QFile, QTimer     
from PyQt5.QtWidgets import QApplication, QMainWindow

INIT_TEXT_STAT = "Char's on/off gaps: 0/0<br>Words: 0"

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

def correct_line_gaps(line):
    try:
        i = 0
        while (line[i] == " " or line[i] == "\n" or line[i] == "\r" or line[i] == "\t") and (i < len(line)):
            i += 1
        
        line = line[i:]
        
        i = len(line) - 1
        while (line[i] == " " or line[i] == "\n" or line[i] == "\r" or line[i] == "\t") and (i < len(line)):
            i -= 1
        
        line = line[:i+1]
        
        i = 0
        while i < len(line):
            i_start = i 
            while (line[i] == " " or line[i] == "\n" or line[i] == "\r" or line[i] == "\t") and (i < len(line)):
                i += 1
                             
            i_finish = i
            
            if i_start != i_finish and i_finish - i_start == 1:
                line = line[:i_start] + " " + line[i_finish:]
                i += 1
                continue
            if i_start != i_finish and i_finish - i_start > 1:
                line = line[:i_start] + " " + line[i_finish:]
                i -= i_finish - i_start 
                continue    
            i += 1
        return line
    except IndexError:
        gui.ui.text_stat.setText(INIT_TEXT_STAT)

def count_chars_num_on_gaps():
    return len(gui.ui.text_field.toPlainText())

def count_chars_num_off_gaps():
    try:
        text = correct_line_gaps(line=gui.ui.text_field.toPlainText())
        chars_num_off_gaps = 0
        for i in text:
            if not (i == " " or i == "\n" or i == "\r" or i == "\t"):
                chars_num_off_gaps += 1
        return chars_num_off_gaps 
    except TypeError:
        gui.ui.text_stat.setText(INIT_TEXT_STAT)
        return 0        

def count_words_num():
    try:
        text = correct_line_gaps(line=gui.ui.text_field.toPlainText())
        words_num = 0
        i = 0
        while i < len(text):
            print(i)
            print(i+1)
            if text[i] == " " or text[i] == "\n" or text[i] == "\r" or text[i] == "\t":
                words_num += 1
                if i+1 < len(text) and (text[i+1] == "-" or text[i+1] == "–" or text[i+1] == "—"):
                    if  i+2 < len(text) and (text[i+2] == " " or text[i+2] == "\n" or text[i+2] == "\r" or text[i+2] == "\t"):
                        i += 3
                        continue
                    else:
                        i += 1
                        continue
                else:
                    i += 1
                    continue
            
            i += 1
        return words_num+1
    except TypeError:
        gui.ui.text_stat.setText(INIT_TEXT_STAT)
        return 0

def get_text_stat():
    try:
        chars_num_on_gaps = count_chars_num_on_gaps()
        chars_num_off_gaps = count_chars_num_off_gaps()
        
        words_num = count_words_num()
        
        gui.ui.text_stat.setText(f"Char's on/off gaps: {chars_num_on_gaps}/{chars_num_off_gaps}<br>Words: {words_num}")
    except TypeError:
        return gui.ui.text_stat.setText(INIT_TEXT_STAT)

def normalise_text():
    try:
        gui.ui.text_field.setText(correct_line_gaps(line=gui.ui.text_field.toPlainText()))
    except TypeError:
        gui.ui.text_stat.setText(INIT_TEXT_STAT)

def copy_text():
    gui.ui.text_field.selectAll()
    gui.ui.text_field.copy()
    
def del_text():
    gui.ui.text_field.clear()

def replace_gaps_with_char():
    substitute_char = gui.ui.substitute_char_line.text()
    replace_char = gui.ui.replace_char_line.text()
    text = gui.ui.text_field.toPlainText()
    new_text = ""
    i = 0
    while i < len(text):
        if text[i] == replace_char:
            new_text += substitute_char
            i += 1
        else:
            new_text += text[i]
            i += 1
    gui.ui.text_field.setText(new_text)

if __name__ == "__main__":
    application = QApplication(sys.argv)
    gui = MainWindow()
    
    myappid = 'mycompany.myproduct.subproduct.version'                          
#    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)
#    application.setWindowIcon(QtGui.QIcon("data/icon.svg"))  # When converting to exe, insert the path: data/icon.svg  
#    gui.setWindowIcon(QtGui.QIcon("data/icon.svg"))  # When converting to exe, insert the path: data/icon.svg
    
    gui.ui.norm_btn.clicked.connect(normalise_text)
    gui.ui.copy_text_btn.clicked.connect(copy_text)
    gui.ui.del_text_btn.clicked.connect(del_text)
    
    gui.ui.replace_chars_btn.clicked.connect(replace_gaps_with_char)
    
    gui.ui.text_field.textChanged.connect(get_text_stat)
    
    
    gui.show()
    
    sys.exit(application.exec())

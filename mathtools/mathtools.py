import sys
from datetime import datetime as dttm


from GUI import Ui_MainWindow
from PyQt5 import QtGui
from PyQt5.QtCore import QFile, QTimer     
from PyQt5.QtWidgets import QApplication, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

def find_evens_odds(right_edge: int) -> tuple:
    evens = []
    odds = []
    for i in range(1, right_edge+1):
        if i % 2 == 0:
            evens.append(i)
        else:
            odds.append(i)
    return (odds, evens)

def find_primes(right_edge: int) -> list:
    nums = list(range(2, right_edge+1))
    primes = []
    p = nums[0]
    while True:
        i = 0
        while i < len(nums):
            if nums[i] % p == 0:
                del(nums[i])
            i += 1
        primes.append(p)
        if len(nums) == 0:
            break
        p = nums[0]
    return primes
    
def run_search_evens_odds():
    right_edge = int(gui.ui.right_edge_odd_even.text())
    start_time = dttm.now()
    odds, evens = find_evens_odds(right_edge)
    finish_time = dttm.now()
    gui.ui.found_odds_evens.setText(f"The odd numbers are {str(odds)[1:-1]}.<br>The even numbers are {str(evens)[1:-1]}.<br>The search took (h:min:s.ms) {finish_time-start_time}.")
    
def run_search_primes():
    right_edge = int(gui.ui.right_edge_prime.text())
    start_time = dttm.now()
    primes = find_primes(right_edge)
    finish_time = dttm.now()
    gui.ui.found_primes.setText(f"The prime numbers are {str(primes)[1:-1]}.<br>The search took (h:min:s.ms) {finish_time-start_time}.")
    

if __name__ == "__main__":
    application = QApplication(sys.argv)
    gui = MainWindow()
    
    myappid = 'mycompany.myproduct.subproduct.version'                          
#    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)
#    application.setWindowIcon(QtGui.QIcon('data/icon.svg'))  # When converting to exe, insert the path: _internal/icon.png  
#    gui.setWindowIcon(QtGui.QIcon('data/icon.svg'))  # When converting to exe, insert the path: _internal/icon.png
    
    gui.ui.find_odds_evens.clicked.connect(run_search_evens_odds)
    gui.ui.find_primes.clicked.connect(run_search_primes)
    
    gui.show()
    
    sys.exit(application.exec())

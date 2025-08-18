# Built-in
import sys
import requests

# Beautiful Soup
from bs4 import BeautifulSoup

# Qt
from GUI import Ui_MainWindow
from PyQt5 import QtGui
from PyQt5.QtCore import QFile, QTimer     
#from PyQt5.QtWinExtras import QtWin
from PyQt5.QtWidgets import QApplication, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

def correct_line_gaps(line):
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

def get_app_date(soup):
    raw_app_date = correct_line_gaps(soup.find("table", id="bib").find("p").find("b").text)
    app_date = ""
    i = 0
    while i < len(raw_app_date) and raw_app_date[i] != ",":
        i += 1
    
    i += 1
    while i < len(raw_app_date): 
        app_date += raw_app_date[i]
        i += 1
    return app_date
    
def get_patent_num(raw_num):
    raw_num = raw_num.find("title").text
    i = 0
    while raw_num[i] != "№":
        i += 1
    patent_num = raw_num[i+1:]
    return patent_num 

def get_app_num(soup):
    raw_app_num = soup.find("table", id="bib").find("p").find("a").text
    app_num = ""
    
    i = 0
    while i < len(raw_app_num) and raw_app_num[i] != "/":
        app_num += raw_app_num[i]
        i += 1
    return app_num
    
def get_pub_date(soup):
    pub_date = soup.find("table", id="bib").find_all("tr")
    for tr in pub_date:
        for p in tr.find("td").find_all("p"):
            if "(45) Опубликовано:" in str(p):
                return p.find("b").find("a").text
    
def get_patent_indexes(soup):
    indexes_list = soup.find("table", {"class": "tp"}).find("table", {"class": "tp"}).find("ul", {"class": "ipc"}).find_all("a")
    
    indexes = ""
    i = 0
    for i in range(len(indexes_list)):
        if i == len(indexes_list) - 1:
            indexes += correct_line_gaps(indexes_list[i].text)
            break
        indexes += correct_line_gaps(indexes_list[i].text) + ", "
    return indexes    

def get_authors(soup):
    raw_authors = correct_line_gaps(soup.find("table", id="bib").find("td", id="bibl").find("p").find("b").text)
    authors = []
    authors.append([])
    
    i = 0
    j = 0
    l = 0
    while i < len(raw_authors):
        authors[j].append("")
        while i < len(raw_authors) and raw_authors[i] != " " and raw_authors[i] != "(":
            if l == 1 or l == 2:
                authors[j][l] += raw_authors[i] + "."
                while i < len(raw_authors) and raw_authors[i] != " " and raw_authors[i] != "(":
                    i += 1
                break

            authors[j][l] += raw_authors[i]
            i += 1
        i += 1
        l += 1
        
        if i < len(raw_authors) and raw_authors[i] == "(":
            authors.append([])
            j += 1
            l = 0
            i += 5
    
    authors.pop(-1)
    
    authors_names = ""
    i = 0
    j = 0
    while i < len(authors):
        while j < len(authors[i]):
            if i == len(authors)-1 and j == len(authors[i])-1:
                authors_names += authors[i][j]
                j += 1
                break
            if j == len(authors[i])-1:
                authors_names += authors[i][j] + ", "
                j += 1
                break
            authors_names += authors[i][j] + " "
            j += 1
            
        j = 0
        i += 1
        
    return authors_names
    
def get_applicant(soup):
    raw_applicant = correct_line_gaps(soup.find("table", id="bib").find("td", id="bibl").find_all("p")[1].find("b").text)
    applicant = raw_applicant[0].upper() + raw_applicant[1:-5]
    return applicant  

def cite_patent():
    request = requests.get(gui.ui.patent_url.text())
    soup = BeautifulSoup(request.text, "lxml")

    # Getting:
    patent_num = get_patent_num(raw_num=soup)  # The application number;
    patent_name = soup.find("p", id="B542").find("b").text  # The patent name;
    patent_reg_country = "Российская Федерация"  # The country of the patent registration;
    patent_indexes = get_patent_indexes(soup=soup)  # The application number;
    app_num = get_app_num(soup=soup)  # The application number;
    app_date = get_app_date(soup=soup)  # The date of the application;
    pub_date = get_pub_date(soup=soup)  # The publication date;
    authors = get_authors(soup=soup)  # The authors;
    applicant = get_applicant(soup=soup)  # The patent applicant.

    # Let's see if the patent is illustrated.
    ill_flag = soup.find("div", id="Abs").find_all("p")[1].text.find("ил.")  # Looking for matches to "ил." in the patent abstract. 
    if  ill_flag != -1:
        patent_citation = f"Патент № {patent_num} {patent_reg_country}, МПК {patent_indexes}. {patent_name} : № {app_num} : заявл. {app_date} : опубл. {pub_date} / {authors} ; заявитель {applicant}. - ил. - Текст : электронный."
    else:
        patent_citation = f"Патент № {patent_num} {patent_reg_country}, МПК {patent_indexes}. {patent_name} : № {app_num} : заявл. {app_date} : опубл. {pub_date} / {authors} ; заявитель {applicant}. - Текст : электронный."
    
    gui.ui.patent_citation.setText(patent_citation)

if __name__ == '__main__':
    application = QApplication(sys.argv)
    gui = MainWindow()
    
    myappid = 'mycompany.myproduct.subproduct.version'                          
#    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)
#    application.setWindowIcon(QtGui.QIcon('icon.png'))  # When converting to exe, insert the path: _internal/icon.png  
#    gui.setWindowIcon(QtGui.QIcon('icon.png'))  # When converting to exe, insert the path: _internal/icon.png
    
    gui.ui.cite_btn.clicked.connect(cite_patent)
    
    gui.show()
    
    sys.exit(application.exec())

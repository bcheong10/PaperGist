from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog
from PyQt5 import uic, QtCore
from PyQt5 import QtGui
import sys
import os
import openai
from PyPDF2 import PdfReader
from google_images_search import GoogleImagesSearch


''' API Keys '''

openai.api_key = ("")
gis = GoogleImagesSearch('')


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        self.setWindowIcon(QtGui.QIcon('logo.png'))
         # Load UI file
        uic.loadUi("draft2.ui", self)


        ''' Button Functions '''

        self.image_box.setEnabled(False)
        self.radioButton.setChecked(True)
        self.chooseFile.clicked.connect(lambda: self.choose_file())
        self.save_button.clicked.connect(lambda: self.choose_directory())
        self.generate_button.clicked.connect(lambda: self.generate())
        

        self.show()

    
    ''' Function Libraries '''

    def choose_file(self):

        # Open file dialog
        file = QFileDialog.getOpenFileName(self, "Select File")

        if file:
            self.file_dir = file
            self.file_dir_txt.setText(self.file_dir[0])

        
    def choose_directory(self):

        directory = QFileDialog.getExistingDirectory(self, "Select Folder")

        if directory:
            self.save_dir = directory
            self.save_dir_txt.setText(self.save_dir)
            
            if self.save_dir:
                self.image_box.setEnabled(True)


    def generate(self):

        isSummaryChecked = self.summary_box.isChecked()
        isBulletChecked = self.bullet_box.isChecked()
        isKeywordChecked = self.keyword_box.isChecked()
        isImageChecked = self.image_box.isChecked()


        if self.radioButton.isChecked():
            
            reader = PdfReader(self.file_dir_txt.text())
            page_summary = ""
            

            for page_number in range(len(reader.pages)):
                page = reader.pages[page_number]
                text = page.extract_text(0) + "\n"

                get_summary = f"summarise {text} into a paragraph"
                summary_response = openai.Completion.create(model="text-davinci-003", prompt = get_summary, 
                                        temperature=0, max_tokens=1000)

                page_summary += summary_response.choices[0]["text"] + "\n"
            

        elif self.radioButton_2.isChecked():
            
            page_summary = self.file_dir_txt.text()
            


        if isSummaryChecked:
            

            # Prompt to get summary of whole article

            get_summary_article = f"summarise {page_summary} into a paragraph"
            article_summary_response = openai.Completion.create(model="text-davinci-003", prompt = get_summary_article, 
                                                temperature=0, max_tokens=1000)

            summary = article_summary_response.choices[0]["text"]
                
            self.textBrowser_4.setText(summary)


        if isBulletChecked:
            

            # Prompt to get bullet points from article summary

            get_bullet = f"summarise {page_summary} into bullet points"
            bullet_response = openai.Completion.create(model="text-davinci-003", prompt = get_bullet, 
                                                temperature=0, max_tokens=1000)

            bullet = bullet_response.choices[0]["text"]
            self.textBrowser_2.setText(bullet)


        if isKeywordChecked:
            
            

            # Prompt to get key words from summary

            get_keywords = f"list keywords from {page_summary}"
            kw_response = openai.Completion.create(model="text-davinci-003", prompt = get_keywords, 
                                                temperature=0, max_tokens=1000)

            keywords = kw_response.choices[0]["text"]
            self.textBrowser_3.setText(keywords)

            keyword_list = keywords.split(" ")
            print(keyword_list)
        

        if isImageChecked:
            
            pathz = self.save_dir

            for key in keyword_list:

                _search_params = {
                    'q': key,
                    'num': 2,
                    'fileType': 'jpg|gif|png',
                    'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived',
                    'safe': 'active', ##
                    'imgType': 'imgTypeUndefined', ##
                    'imgSize': 'imgSizeUndefined', ##
                    'imgDominantColor': 'imgDominantColorUndefined', ##
                    'imgColorType': 'color'
                    }           

                gis.search(search_params=_search_params, path_to_dir=pathz)
        
        
    


        

# Initialize app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
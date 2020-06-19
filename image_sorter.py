from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImageReader
from PyQt5.Qt import Qt
import sys
import json
import os
import pathlib
import shutil
from pathlib import Path
class Menu(QMainWindow):

    def set_save_dir(self):
        print('x')

    def func_load_image(self):
        self.filename = self.image_filename_list[self.image_index]
        
        #skip non image files
        print('open', self.filename, 'suffix', self.filename.suffix)
        if self.filename.suffix not in self.allowed_extensions:
            print('non image, go to next')
            self.image_index += 1
            self.func_load_image() # recursion, will crash

            return

        self.current_file_label.setText(str(self.filename)[-15:])


        #self.self.image_directory / self.filename
        self.image_uid = self.filename.stem
        print('opening:', str(self.filename))
        self.pixmap = QPixmap(str(self.filename))
        self.pixmap = self.pixmap.scaledToWidth(256)
        self.image_preview.setPixmap(self.pixmap)

        self.image_preview.repaint()

    def func_debug(self):
        print(self.database)


    def func_open(self):
        with open(self.save_file, 'r', encoding='utf8') as file:
            self.database = json.loads(file.read())
            
            print(self.database)
            print('loaded')
        self.image_index = self.database['image_index']

    def func_save(self):
        self.database['image_index'] = self.image_index

        #make a backup
        shutil.copy(self.save_file, self.save_file + '_copy')

        with open(self.save_file, 'w+', encoding='utf8') as file:
            file.write(json.dumps(self.database))

        
        print('saved')

    def func_next(self):
        self.image_index += 1
        self.func_load_image()
    
    def func_prev(self):
        self.image_index -= 1
        self.func_load_image()

    def func_good(self):
        self.database['ids'][self.image_uid] = 'good'
        self.func_next()
        pass

    def func_bad(self):
        self.database['ids'][self.image_uid] = 'bad'

        self.func_next()
        pass

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            print('ok')

    def __init__(self):
        super().__init__()
        self.database = {'ids': {}, 'image_index': 0}

        # config -------
        self.image_directory = Path.cwd() / '../256_imgs/'
        self.save_file = 'database.json'
        self.allowed_extensions = ['.jpg', '.jpeg', '.png']
        self.image_index = 0
        self.image_uid = 0 # filename without extensions (derpi id)

        self.image_filename_list = [file for file in self.image_directory.iterdir()]#os.listdir(image_directory)

        self.setWindowTitle("Pony s2 sorter (version 1a)")

        self.central_widget = QWidget()               
        self.setCentralWidget(self.central_widget)    
        lay = QGridLayout(self.central_widget)

        self.c_debug = QPushButton("debug info")
        self.c_debug.clicked.connect(self.func_debug)

        self.c_open = QPushButton("open")
        self.c_open.clicked.connect(self.func_open)
        self.c_save = QPushButton("save to database.json")
        self.c_save.clicked.connect(self.func_save)



        self.c_good = QPushButton("Good : (a)ccept")
        self.c_good.clicked.connect(self.func_good)

        self.c_bad = QPushButton("Bad : (d)eny")
        self.c_bad.clicked.connect(self.func_bad)

        self.c_prev = QPushButton("Prev")
        self.c_prev.clicked.connect(self.func_prev)
        self.c_next = QPushButton("Next")
        self.c_next.clicked.connect(self.func_next)

        self.current_file_label = QLabel("Current image")
        self.current_file_label.setFixedWidth(100)


        lay.addWidget(self.current_file_label)
        lay.addWidget(self.c_debug, 0, 0)
        lay.addWidget(self.c_open, 1, 0)
        lay.addWidget(self.c_save, 1, 1)
        lay.addWidget(self.c_good, 4, 0)
        lay.addWidget(self.c_bad, 5, 0)
        lay.addWidget(self.c_prev, 4, 1)
        lay.addWidget(self.c_next, 5, 1)
        self.current_file_label.setText('test')
        
        self.image_preview = QLabel(self)
        self.image_preview.setFixedSize(256,256)

        lay.addWidget(self.image_preview, 3, 0, 1, 2)

        self.setGeometry(50,50,450,450)
        

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    sys.exit(app.exec_())
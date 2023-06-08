import os, sys, shutil, encryption, subprocess
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow, 
    QPushButton, 
    QLineEdit, 
    QFileDialog, 
    QMessageBox, 
    QComboBox, 
    QListWidget,
    QVBoxLayout,
    QWidget,
    QInputDialog,
    QLabel,
    QTabWidget,
    QPlainTextEdit,
    QAbstractItemView
    )
from PyQt5.QtCore import QRect, QSize
from PyQt5.QtGui import QFont, QIcon
from fabfile import RemoteConnect
from inputs import InputDialog
import pandas as pd

LABEL_GEOMETRY = QRect(25, 13, 350, 20)
FONT = QFont('Helvetica', 9, 1)
ADD_GEOMETRY = QRect(320, 97, 130, 40)
COPY_GEOMETRY = QRect(25, 150, 200, 50)
ENCRYPT_GEOMETRY = QRect(250, 150, 200, 50)
FILE_LINE_GEOMETRY = QRect(25, 100, 290, 35)
IP_LINE_GEOMETRY = QRect(25, 25, 425, 35)
TEXTBOX_GEOMETRY = QRect(35, 150, 425, 150)
COMP_LINE_GEOMETRY = QRect(25, 25, 275, 35)
COMP_LIST_GEOMETRY = QRect(320, 25, 140, 150)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        #Setup the GUI
        self.setupUI()

    def setupUI(self):
        self.setFixedSize(500, 500)
        self.setWindowTitle("SysAutomate")

        self.destination = f"C:\\Users\\{os.getlogin()}\\Desktop"
        self.layout = QVBoxLayout(self)

        #Store File and Folder paths in a list
        self.files_list = []
        self.computers = []

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.resize(400,400)

        self.tabs.addTab(self.tab1, "This PC")
        self.tabs.addTab(self.tab2, "Commands")
        self.tabs.addTab(self.tab3, "Remote PC")

        #Create Label for destination
        self.label = QLabel(f"Destination: {self.destination}", self.tab1)
        self.label.setGeometry(LABEL_GEOMETRY)
        self.label.setFont(FONT)

        #Create Button to change destination
        self.change_button = QPushButton('Change...', self.tab1)
        self.change_button.move(350, 10)
        self.change_button.clicked.connect(self.change_dir)
        
        #Create Combobox to choose between files or folder
        self.combobox = QComboBox(self.tab1)
        self.combobox.addItems(['Folder', 'Files'])
        self.combobox.move(25, 50)
        self.combobox.setFixedSize(425, 30)
        self.combobox.currentIndexChanged.connect(self.index_changed)

        #Create QLineEdit to show selected files
        self.file_line = QLineEdit(self.tab1)
        self.file_line.setReadOnly(True)
        self.file_line.setGeometry(FILE_LINE_GEOMETRY)

        #Create Button to add files/folders
        self.file_button = QPushButton(self.tab1)
        self.file_button.setIcon(QIcon('add-folder.png'))
        self.file_button.setIconSize(QSize(30,30))
        self.file_button.setText('Browse')
        self.file_button.setToolTip('Add Folder')
        self.file_button.setGeometry(ADD_GEOMETRY)
        self.file_button.clicked.connect(self.add_file)
        
        #Create Button to copy files/folder to destination
        self.copy_button = QPushButton(self.tab1)
        self.copy_button.setGeometry(COPY_GEOMETRY)
        self.copy_button.setIcon(QIcon('copy.png'))
        self.copy_button.setIconSize(QSize(30,30))
        self.copy_button.setText("Copy")
        self.copy_button.setToolTip('Copy')
        self.copy_button.clicked.connect(self.copy_file)

        self.encrypt_button = QPushButton(self.tab1)
        self.encrypt_button.setGeometry(ENCRYPT_GEOMETRY)
        self.encrypt_button.setIcon(QIcon('data-encryption.png'))
        self.encrypt_button.setText("Encrypt")
        self.encrypt_button.setToolTip("Archive and Encrypt")
        self.encrypt_button.setIconSize(QSize(30,30))
        self.encrypt_button.clicked.connect(self.encrypt_files)

        self.ip_line = QLineEdit(self.tab2)
        self.ip_line.setGeometry(IP_LINE_GEOMETRY)
        self.ip_line.setPlaceholderText("Enter IP address")

        self.status_button = QPushButton(self.tab2, text='Status')
        self.status_button.move(30, 70)
        self.status_button.setFixedWidth(200)
        self.status_button.clicked.connect(self.check_status)

        self.lookup_button = QPushButton(self.tab2, text='Lookup')
        self.lookup_button.move(240, 70)
        self.lookup_button.setFixedWidth(200)
        self.lookup_button.clicked.connect(self.dns_lookup)

        self.ipconfig_button = QPushButton(self.tab2, text="IP Config")
        self.ipconfig_button.move(30, 100)
        self.ipconfig_button.setFixedWidth(200)
        self.ipconfig_button.clicked.connect(self.get_ip)

        self.policy_button = QPushButton(self.tab2, text="Update Policy")
        self.policy_button.move(240, 100)
        self.policy_button.setFixedWidth(200)
        self.policy_button.clicked.connect(self.update_gp)

        self.textbox = QPlainTextEdit(self.tab2)
        self.textbox.setGeometry(TEXTBOX_GEOMETRY)

        self.comp_line = QLineEdit(self.tab3)
        self.comp_line.setGeometry(COMP_LINE_GEOMETRY)
        self.comp_line.setPlaceholderText("Enter IP address or hostname of remote PC")

        self.comps_list = QListWidget(self.tab3)
        self.comps_list.setGeometry(COMP_LIST_GEOMETRY)
        self.comps_list.setSelectionMode(QAbstractItemView.MultiSelection)
        self.comps_list.setStyleSheet("border: 1px solid black; font-size: 9pt; font-family: Helvetica;")

        self.add_button = QPushButton(self.tab3, text="Add")
        self.add_button.move(30, 70)
        self.add_button.setFixedWidth(130)
        self.add_button.clicked.connect(lambda x: self.add_computer(self.comp_line.text()))

        self.read_button = QPushButton(self.tab3, text="Read from CSV")
        self.read_button.move(160, 70)
        self.read_button.setFixedWidth(130)
        self.read_button.clicked.connect(self.read_from_csv)

        self.remove_button = QPushButton(self.tab3, text="Remove")
        self.remove_button.move(325, 180)
        self.remove_button.setFixedWidth(130)
        self.remove_button.clicked.connect(self.remove_computer)

        self.update_button = QPushButton(self.tab3, text="Update All")
        self.update_button.move(30, 100)
        self.update_button.setFixedWidth(260)
        self.update_button.clicked.connect(self.update_computer)

        self.remote_copy_button = QPushButton(self.tab3, text="Copy Files")
        self.remote_copy_button.setToolTip("Copy files to remote hosts")
        self.remote_copy_button.move(30, 130)
        self.remote_copy_button.setFixedWidth(260)
        self.remote_copy_button.clicked.connect(self.remote_copy)

        self.archive_button = QPushButton(self.tab3, text="Archive and Send")
        self.archive_button.setToolTip("Archive folder and send to remote hosts")
        self.archive_button.move(30, 160)
        self.archive_button.setFixedWidth(260)
        self.archive_button.clicked.connect(self.archive_transfer)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        

    def change_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.destination = dir_path
        self.label.setText(f"Destination: {self.destination}")
    
    #When different combobox item is chosen clear list of paths
    def index_changed(self):

        if self.combobox.currentIndex() == 1:
            self.encrypt_button.setToolTip("Encrypt")
            self.file_button.setToolTip("Add Files")
        else:
            self.encrypt_button.setToolTip("Archive and Encrypt")
            self.file_button.setToolTip("Add Folder")

        self.files_list.clear()

    def add_file(self):
        if self.combobox.currentIndex() == 0:
            dir_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
            self.files_list.append(dir_path)
            self.file_line.setText(dir_path)
        
        elif self.combobox.currentIndex() == 1:
            file_paths = QFileDialog.getOpenFileNames(self, 'Select Files')[0]
            self.files_list.extend(file_paths)
            file_string = ""
            for f in file_paths:
                file_name = os.path.split(f)[1]
                file_string += f"{file_name};"
            self.file_line.setText(file_string)

    def copy_file(self):
        if len(self.files_list) != 0:
            #Loop through saved paths and copy them to destination
            for src in self.files_list:
                #If path leads to a directory, copy it to destination with copytree method
                if os.path.isdir(src):
                    shutil.copytree(src, f"{self.destination}\\{os.path.split(src)[1]}")
                    self.file_line.clear()

                #If path leads to a file, copy it to destination with copyfile method
                if os.path.isfile(src):
                    shutil.copy2(src, self.destination)
                    self.file_line.clear()
            self.files_list.clear()

    def check_status(self):
        self.textbox.clear()
        ip = self.ip_line.text()
        if os.system("ping /n 1 " + ip) == 0:
            self.textbox.insertPlainText(f'{ip} is online.')
        
    def dns_lookup(self):
        self.textbox.clear()
        p = subprocess.check_output(['nslookup', self.ip_line.text()]).decode()
        self.textbox.insertPlainText(p)
    
    def get_ip(self):
        self.textbox.clear()
        p = subprocess.check_output(['ipconfig']).decode()
        print(p)
        self.textbox.insertPlainText(p)
    
    def update_gp(self):
        self.textbox.clear()
        p = subprocess.check_output(['gpupdate', '/force']).decode()
        self.textbox.insertPlainText(p)

    
    def add_computer(self, host):
        if host != '':
            self.comp_line.clear()
            if host in self.computers:
                print("This IP Address/Host is already in the list")
                return None
            
            self.computers.append(host)
            self.comps_list.addItem(host)
    
    def read_from_csv(self):
        fileName = QFileDialog.getOpenFileName(self, filter="Comma-Delimited (*.csv)")
        if fileName[0] != '':
            df = pd.read_csv(fileName[0])
            df['IP'].apply(lambda x: self.add_computer(x))
            
    
    def remove_computer(self):
        selected = self.comps_list.selectedIndexes()
        for i in range (len(selected)):
            if selected[i].data() in self.computers:
                self.computers.remove(selected[i].data())

            self.comps_list.takeItem(selected[i].row())
        print(self.computers)
            
    
    def update_computer(self):
        dialog = InputDialog()
        if dialog.exec():
            username, password = dialog.getInputs()
            print(username, password)
            conn = RemoteConnect(hosts=self.computers, username=username, password=password)
            conn.update_all()
            

    def remote_copy(self):
        dialog = InputDialog()
        if dialog.exec():
            username, password = dialog.getInputs()
            print(username, password)
            conn = RemoteConnect(hosts=self.computers, username=username, password=password)
            file_paths = QFileDialog.getOpenFileNames(self, 'Select Files')[0]
            conn.file_transfer(file_paths, f'/home/{username}/Desktop')

        #If list of paths is empty show an error message and ask user to select files or folders
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setText("No Files or Folders Selected")
            msg.setInformativeText('Please Select Folder or Files')
            msg.setWindowTitle("Error")
            msg.exec_()

    def archive_transfer(self):
        dialog = InputDialog()
        if dialog.exec():
            username, password = dialog.getInputs()
            print(username, password)
            conn = RemoteConnect(hosts=self.computers, username=username, password=password)

            dir_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
            out_path = f"{self.destination}\\{os.path.basename(dir_path)}"
            shutil.make_archive(out_path, 'gztar', dir_path)

            conn.send_and_unzip(out_path)
        

    def encrypt_files(self):
        if len(self.files_list) == 0:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setText("No Files or Folders Selected")
            msg.setInformativeText('Please Select Folder or Files')
            msg.setWindowTitle("Error")
            msg.exec_()
            return None
        
        password, ok = QInputDialog.getText(self, "Password Required", "Please enter password:", QLineEdit.EchoMode.Password)
        if password and ok :
            print(password)
            for src in self.files_list:
                if src[-4:] == ".aes":
                    encryption.decrypt(src, self.destination, password)

                elif os.path.isdir(src):
                    out_path = f"{self.destination}\\{os.path.basename(src)}"
                    shutil.make_archive(out_path, "zip", src)
                    encryption.encrypt(f"{out_path}.zip", self.destination, password)
                    
                elif os.path.isfile(src):
                    encryption.encrypt(src, self.destination, password)
    
    



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


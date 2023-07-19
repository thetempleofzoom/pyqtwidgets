from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QWidget, \
    QGridLayout, QLineEdit, QPushButton, QComboBox, QTableWidget, \
    QTableWidgetItem, QDialog, QVBoxLayout, QToolBar, QStatusBar, \
    QMessageBox
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management Portal")
        self.setMinimumSize(600,400)
        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&Help")
        edit_menu = self.menuBar().addMenu("&Edit")

        #add menu item
        add_student = QAction(QIcon("icons/add.png"), "Add Student", self)
        #when add_student chosen
        add_student.triggered.connect(self.insert)
        about = QAction("About", self)
        #??
        about.setMenuRole(QAction.MenuRole.NoRole)
        search_student = QAction(QIcon("icons/search.png"), "Search for Student", self)
        search_student.triggered.connect(self.search)

        file_menu.addAction(add_student)
        help_menu.addAction(about)
        edit_menu.addAction(search_student)

        #add toolbar and elements
        toolbar = QToolBar()
        #toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student)
        toolbar.addAction(search_student)


        
        #add student table to main window. add 'self' to be able to connect to other
        #functions in class
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Mobile" ))
        #remove column numbers
        self.table.verticalHeader().setVisible(False)

        # add status bar and elements. n/b adding 'self' to statusbar variable
        # allows it to be called in the edit student function
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        # add buttons to statusbar when cell clicked
        self.table.cellClicked.connect(self.add_buttons)

        #specify central widget for window
        self.setCentralWidget(self.table)
        
    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        #always puts cursor at 0 to avoid dups
        self.table.setRowCount(0)
        for index, row_data in enumerate(result):
            self.table.insertRow(index)
            for column, data in enumerate(row_data):
                self.table.setItem(index, column, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        #call insertdialog class
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        #call searchdialog class
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def add_buttons(self):
        edit = QPushButton("Edit Record")
        edit.clicked.connect(self.edit)

        delete = QPushButton("Delete Record")
        delete.clicked.connect(self.delete)

        # buttons are not removed once a cell is clicked. therefore remove all buttons
        # everytime cell is clicked
        children = self.statusbar.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        # now that old buttons are removed, we can safely add new ones
        self.statusbar.addWidget(edit)
        self.statusbar.addWidget(delete)


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert New Student Data")
        #gd practice for dialog window
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("name")
        layout.addWidget(self.student_name)

        self.student_class = QComboBox()
        classes = ["Biology", "Math", "Literature", "English", "Physics"]
        self.student_class.addItems(classes)
        layout.addWidget(self.student_class)

        self.student_mobile = QLineEdit()
        self.student_mobile.setPlaceholderText("mobile")
        layout.addWidget(self.student_mobile)

        submit = QPushButton("Submit")
        submit.clicked.connect(self.add_student)
        layout.addWidget(submit)

        self.setLayout(layout)

    def add_student(self):
        #import variable values
        name = self.student_name.text()
        course = self.student_class.currentText()
        mobile = int(self.student_mobile.text())
        #add entry into sql database
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?,?,?)",
                       (name, course, mobile))
        connection.commit()
        count = cursor.execute("SELECT COUNT(id) FROM students")
        count = count.fetchall()[0][0]
        cursor.close()
        connection.close()
        #refresh table
        mainwindow.load_data()
        print(f'{count} students in database')
        

class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student Database")
        #gd practice for dialog window
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.search_student = QLineEdit()
        self.search_student.setPlaceholderText("search by name")
        layout.addWidget(self.search_student)

        submit = QPushButton("Search")
        submit.clicked.connect(self.find_student)
        layout.addWidget(submit)

        self.setLayout(layout)
    def find_student(self):
        #erase any highlighted items
        mainwindow.table.setCurrentItem(None)
        #no need to call up database. search in table itself. alternate code with SQL
        #query in test.py

        hits = mainwindow.table.findItems(self.search_student.text(), Qt.MatchFlag.MatchContains)
        if hits:
            for hit in hits:
                hit.setSelected(True)


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        #gd practice for dialog window
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        index = mainwindow.table.currentRow()
        self.id = mainwindow.table.item(index, 0).text()
        student_selected = mainwindow.table.item(index, 1).text()
        subject = mainwindow.table.item(index, 2).text()
        mobile_selected = mainwindow.table.item(index, 3).text()
        self.student_name = QLineEdit(student_selected)
        self.student_name.setPlaceholderText("name")
        layout.addWidget(self.student_name)

        self.student_class = QComboBox()
        classes = ["Biology", "Math", "Literature", "English", "Physics"]
        if subject not in classes:
            classes.append(subject)
        self.student_class.addItems(classes)
        self.student_class.setCurrentText(subject)
        layout.addWidget(self.student_class)

        self.student_mobile = QLineEdit(mobile_selected)
        self.student_mobile.setPlaceholderText("mobile")
        layout.addWidget(self.student_mobile)

        submit = QPushButton("Update")
        submit.clicked.connect(self.edit_student)
        layout.addWidget(submit)

        self.setLayout(layout)

    def edit_student(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (self.student_name.text(), self.student_class.currentText(), self.student_mobile.text(),
                        self.id))
        connection.commit()
        cursor.close()
        connection.close()
        # refresh table
        mainwindow.load_data()


#this class is a messagebox unlike the others which are dialogs
class DeleteDialog(QMessageBox):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Delete Student Record")

        index = mainwindow.table.currentRow()
        self.id = mainwindow.table.item(index, 0).text()
        tbd = mainwindow.table.item(index, 1).text()

        self.setText(f"Delete {tbd}'s record?")
        self.setStandardButtons(self.StandardButton.Ok | self.StandardButton.Cancel)

        self.buttonClicked.connect(self.delete_record)


    def delete_record(self, i):
        if i.text() == "OK":
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            cursor.execute("DELETE FROM students WHERE id = ?", (int(self.id), ))
            connection.commit()
            cursor.close()
            connection.close()
            # refresh table
            mainwindow.load_data()
        else:
            self.close()


app = QApplication(sys.argv)
mainwindow = MainWindow()
mainwindow.show()
mainwindow.load_data()
#insert = InsertDialog()
#insert.show()
sys.exit(app.exec())

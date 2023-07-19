from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton
import sys
from datetime import datetime


class AgeCalc(QWidget):
    def __init__(self):
        #The super() function is a useful tool for accessing and reusing the
        # attributes and methods of a parent class (QWidget) in the child class.
        super().__init__()
        self.setWindowTitle("Age Calculator")
        grid = QGridLayout()

        #title
        name_label = QLabel("Name:")
        #we need the qlineedit responses, but name_input and dob_input are local
        #to the init method. to make them accessible class-wide, add 'self' to
        #get instance
        self.name_input = QLineEdit()
        dob_label = QLabel("Date of Birth (dd/mm/yyyy):")
        self.dob_input = QLineEdit()
        calc_button = QPushButton("Calculate Age")
        calc_button.clicked.connect(self.calc_age)
        #initial label
        self.output = QLabel("{answer}")

        #add widgets to grid, RC style
        grid.addWidget(name_label, 0,0)
        grid.addWidget(self.name_input, 0, 1)
        grid.addWidget(dob_label, 1, 0)
        grid.addWidget(self.dob_input, 1, 1)
        #span across 1R2C
        grid.addWidget(calc_button, 2, 0, 1,2)
        grid.addWidget(self.output, 3, 0, 1, 2)

        #tie grid to Qwidget
        self.setLayout(grid)

    def calc_age(self):
        current_year = datetime.now().year
        #text() extracts the data
        dob = self.dob_input.text()
        birth_year = datetime.strptime(dob, "%d/%m/%Y").date().year
        age = current_year - birth_year
        #overrides initial text output
        self.output.setText(f'{self.name_input.text()} is {age} years old')
    
#The QApplication object is the core of every Qt Widgets application.
# Every application needs one and only one QApplication object to function.
# This object starts and holds the main event loop of your application which
# governs all user interaction with the GUI.
#When we pass sys.argv to QApplication we are passing the command-line arguments
# to Qt. This allows us to pass any configuration settings to Qt at the startup of an application.
# eg run scratch.py
app = QApplication(sys.argv)
#instantiating instance of class
agecalc = AgeCalc()
agecalc.show()
#closes program after app is finished executing
sys.exit(app.exec())

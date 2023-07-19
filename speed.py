from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QComboBox
import sys



class SpeedCalc(QWidget):
    def __init__(self):
        #The super() function is a useful tool for accessing and reusing the
        # attributes and methods of a parent class (QWidget) in the child class.
        super().__init__()
        self.setWindowTitle("Average Speed Calculator")
        grid = QGridLayout()

        #title
        distance_label = QLabel("Distance:")
        #we need the qlineedit responses, but name_input and dob_input are local
        #to the init method. to make them accessible class-wide, add 'self' to
        #get instance
        self.distance_input = QLineEdit()
        self.distance_type = QComboBox()
        self.distance_type.addItems(["Metric (km)", "Imperial (miles)"])
        time_label = QLabel("Time (hours):")
        self.time_input = QLineEdit()
        calc_button = QPushButton("Calculate Avg Speed")
        calc_button.clicked.connect(self.calc_speed)
        #initial label
        self.output = QLabel("answer")

        #add widgets to grid, RC style
        grid.addWidget(distance_label, 0,0)
        grid.addWidget(self.distance_input, 0, 1)
        grid.addWidget(self.distance_type, 0, 2)
        grid.addWidget(time_label, 1, 0)
        grid.addWidget(self.time_input, 1, 1)
        #span across 1R3C
        grid.addWidget(calc_button, 2, 0, 1,3)
        grid.addWidget(self.output, 3, 0, 1, 3)

        #tie grid to Qwidget
        self.setLayout(grid)

    def calc_speed(self):
        #text() extracts the data
        distance = self.distance_input.text()
        time = self.time_input.text()
        speed = float(distance) / float(time)
        print(self.distance_type.currentText())
        if self.distance_type.currentText() == "Metric (km)":
            t = "kph"
            print(t)
        else:
            t = "mph"
            print(t)
        #overrides initial text output
        self.output.setText(f'Average speed is {speed} {t}')


#The QApplication object is the core of every Qt Widgets application.
# Every application needs one and only one QApplication object to function.
# This object starts and holds the main event loop of your application which
# governs all user interaction with the GUI.
#When we pass sys.argv to QApplication we are passing the command-line arguments
# to Qt. This allows us to pass any configuration settings to Qt at the startup of an application.
# eg run scratch.py
app = QApplication(sys.argv)
#instantiating instance of class
speedcalc = SpeedCalc()
speedcalc.show()
#closes program after app is finished executing
sys.exit(app.exec())

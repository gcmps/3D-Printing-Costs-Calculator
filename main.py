import configparser
import sys
import csv
from configparser import ConfigParser
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

config = configparser.ConfigParser()
config.read('config.ini')
filqty = float(config.get('settings', 'Filament_Qty'))
filcost = float(config.get('settings', 'Filament_Cost'))
elecost = float(config.get('settings', 'Electricity_Cost'))
laborcost = float(config.get('settings', 'Labor_Cost'))

class AnotherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Configuration')
        layout = QVBoxLayout()
        self.label1 = QLabel("Filament Qty (gr):")
        layout.addWidget(self.label1)
        self.edit1 = QLineEdit(str(filqty))
        layout.addWidget(self.edit1)
        self.label2 = QLabel("Filament Cost ($):")
        layout.addWidget(self.label2)
        self.edit2 = QLineEdit(str(filcost))
        layout.addWidget(self.edit2)
        self.setLayout(layout)
        self.label3 = QLabel("Electricity Kw/h Cost ($):")
        layout.addWidget(self.label3)
        self.edit3 = QLineEdit(str(elecost))
        layout.addWidget(self.edit3)
        self.label4 = QLabel("Labor Cost ($):")
        layout.addWidget(self.label4)
        self.edit4 = QLineEdit(str(laborcost))
        layout.addWidget(self.edit4)
        self.setLayout(layout)
        button1 = QPushButton("Accept")
        button1.clicked.connect(self.config)
        layout.addWidget(button1)

    def config(self, checked):
        config = ConfigParser()

        config['settings'] = {
            'Filament_Qty': float(self.edit1.text()),
            'Filament_Cost': float(self.edit2.text()),
            'Electricity_Cost': float(self.edit3.text()),
            'Labor_Cost': float(self.edit4.text()),
        }

        with open('./config.ini', 'w') as f:
            config.write(f)
        self.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window1 = AnotherWindow()
        self.setWindowTitle('3D Printing Costs Calculator')

        l = QVBoxLayout()
        label5 = QLabel("Estimated Filament Used (gr):")
        l.addWidget(label5)
        self.edit5 = QLineEdit('0')
        l.addWidget(self.edit5)
        self.edit8 = QLineEdit('$')
        self.edit8.setDisabled(True)
        l.addWidget(self.edit8)
        label6 = QLabel("Estimated Print Time (hr):")
        l.addWidget(label6)
        self.edit6 = QLineEdit('0')
        l.addWidget(self.edit6)
        self.edit9 = QLineEdit('$')
        self.edit9.setDisabled(True)
        l.addWidget(self.edit9)
        label7 = QLabel("Estimated Labor Time (hr):")
        l.addWidget(label7)
        self.edit7 = QLineEdit('0')
        l.addWidget(self.edit7)
        self.edit10 = QLineEdit('$')
        self.edit10.setDisabled(True)
        l.addWidget(self.edit10)
        label7 = QLabel("Total Cost:")
        l.addWidget(label7)
        self.edit11 = QLineEdit('$')
        self.edit11.setReadOnly(True)
        l.addWidget(self.edit11)
        button2 = QPushButton("Calculate")
        button2.clicked.connect(self.calculate)
        l.addWidget(button2)
        button3 = QPushButton("Erase")
        button3.clicked.connect(self.erase)
        l.addWidget(button3)
        button4 = QPushButton("Config")
        button4.clicked.connect(self.open_window)
        l.addWidget(button4)

        w = QWidget()
        w.setLayout(l)
        self.setCentralWidget(w)

    def open_window(self, checked):
        if self.window1.isVisible():
            self.window1.hide()

        else:
            self.window1.show()
    
    def calculate(self, checked):
        inputFil = float(self.edit5.text())
        filgr = filcost/filqty
        fil = round(filgr*inputFil, 2)
        inputElec = float(self.edit6.text())
        elec = round(inputElec*elecost, 2)
        inputLabor =  float(self.edit7.text())
        labor = round(inputLabor*laborcost, 2)
        total = round(fil+elec+labor, 2)
        self.edit8.setText('$ {0}'.format(fil))
        self.edit9.setText('$ {0}'.format(elec))
        self.edit10.setText('$ {0}'.format(labor))
        self.edit11.setText('$ {0}'.format(total))

        #CSV Save
        header = ['Filament Cost', 'Electricity Cost', 'Operation Cost', 'Total Cost']
        data = [fil, elec, labor, total]

        with open('3D Printing Costs.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
        # write the header
            writer.writerow(header)
        # write the data
            writer.writerow(data)
    
    def erase(self, checked):
        self.edit5.setText('0')
        self.edit6.setText('0')
        self.edit7.setText('0')
        self.edit8.setText('$ 0')
        self.edit9.setText('$ 0')
        self.edit10.setText('$ 0')
        self.edit11.setText('$ 0')

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
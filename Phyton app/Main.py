from msilib.schema import Font
import sys
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QIODevice 
from PyQt5.QtCore import Qt
from PyQt5.QtGui import * 
 
global serial
serial = QSerialPort()
portList = []
ports = QSerialPortInfo.availablePorts()
baudRate = ["1200", "2400", "4800", "9600", "19200", "38400", "57600", "115200"]
dataBits = ["5", "6", "7", "8"]
parity = ["none", "even", "odd", "space", "mark"]
parityValue = [serial.Parity.NoParity, serial.Parity.EvenParity, serial.Parity.OddParity, serial.Parity.SpaceParity, serial.Parity.MarkParity]
stopBits = ["1", "3", "2"]
receivedDataString = ""

 
class SecondWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, QtCore.Qt.Window)
        self.setWindowTitle("Port settings")
        self.setFixedWidth(250)
        self.setFixedHeight(180)
        self.build()

    def build(self):
        self.baudRateLabel = QtWidgets.QLabel("Baud rate", self) 
        self.baudRateLabel.setFont(QFont("Arial", 10))
        self.baudRateLabel.setStyleSheet("color: black;")      
        self.baudRateLabel.move(47, 5)  

        self.baudRateBox = QtWidgets.QComboBox(self)        
        self.baudRateBox.addItems(baudRate)
        self.baudRateBox.setCurrentIndex(3)
        self.baudRateBox.setFixedWidth(80)
        self.baudRateBox.setFont(QFont("Ink Free", 12))
        self.baudRateBox.setStyleSheet("font-weight: bold")         
        self.baudRateBox.move(35, 20)

        self.dataBitsLabel = QtWidgets.QLabel("Data Bits", self) 
        self.dataBitsLabel.setFont(QFont("Arial", 10))
        self.dataBitsLabel.setStyleSheet("color: black;")       
        self.dataBitsLabel.move(147, 5) 

        self.dataBitsBox = QtWidgets.QComboBox(self)        
        self.dataBitsBox.addItems(dataBits)
        self.dataBitsBox.setCurrentIndex(3)
        self.dataBitsBox.setFixedWidth(80)
        self.dataBitsBox.setFont(QFont("Ink Free", 12))
        self.dataBitsBox.setStyleSheet("font-weight: bold")          
        self.dataBitsBox.move(135, 20)

        self.portLabel = QtWidgets.QLabel("Port", self) 
        self.portLabel.setFont(QFont("Arial", 10))
        self.portLabel.setStyleSheet("color: black;")       
        self.portLabel.move(60, 115)  

        self.comPortBox = QtWidgets.QComboBox(self)
        self.comPortBox.setFixedWidth(80)
        self.comPortBox.move(35, 130)  
        self.comPortBox.setFont(QFont("Ink Free", 12))
        self.comPortBox.setStyleSheet("font-weight: bold")        
        for port in ports:
            portList.append(port.portName())
        self.comPortBox.addItems(portList)

        self.parityLabel = QtWidgets.QLabel("Parity", self) 
        self.parityLabel.setFont(QFont("Arial", 10))
        self.parityLabel.setStyleSheet("color: black;")       
        self.parityLabel.move(157, 60)

        self.parityBox = QtWidgets.QComboBox(self)        
        self.parityBox.addItems(parity)
        self.parityBox.setCurrentIndex(0)
        self.parityBox.setFixedWidth(80)
        self.parityBox.setFont(QFont("Ink Free", 12))
        self.parityBox.setStyleSheet("font-weight: bold")         
        self.parityBox.move(135, 75)  

        self.stopBitsLabel = QtWidgets.QLabel("Stop bits", self) 
        self.stopBitsLabel.setFont(QFont("Arial", 10))
        self.stopBitsLabel.setStyleSheet("color: black;")       
        self.stopBitsLabel.move(47, 60) 

        self.stopBitsBox = QtWidgets.QComboBox(self)        
        self.stopBitsBox.addItems(stopBits)
        self.stopBitsBox.setCurrentIndex(0)
        self.stopBitsBox.setFixedWidth(80)
        self.stopBitsBox.setFont(QFont("Ink Free", 12))
        self.stopBitsBox.setStyleSheet("font-weight: bold") 
        self.stopBitsBox.move(35, 75)
 
        self.connectButton = QtWidgets.QPushButton('Connect', self)
        self.connectButton.move(134, 130)
        self.connectButton.setFixedWidth(82)
        self.connectButton.setFont(QFont("Ink Free", 12))
        self.connectButton.setStyleSheet("font-weight: bold")        
        self.connectButton.clicked.connect(self.connect)     

    def connect(self):
        def temperatureControl():
            rxData = serial.readLine()       
            if len(rxData) == 5:
                global receivedDataString 
                if(rxData[0] == b't'):
                    if rxData[1] == b'1':
                        receivedDataString = '-'
                    elif rxData[1] == b'0': 
                        receivedDataString = '+'    
                    receivedDataString += str(rxData[2], 'utf-8')
                    receivedDataString += str(rxData[3], 'utf-8')
                    receivedDataString += '.'
                    receivedDataString += str(rxData[4], 'utf-8')
                    receivedDataString += "\u00B0" + "C"
                    self.parent().temperatureLabel.setText(receivedDataString)
                    receivedDataString = "" 
                elif(rxData[0] == b'a'):
                    self.parent().progressBar.setValue(int.from_bytes(rxData[1], "big"))

        self.close()
        self.parent().serialSettingsEdit.setText(self.comPortBox.currentText() + " " + self.baudRateBox.currentText() + " bps, " + " " + self.dataBitsBox.currentText() + " " + self.parityBox.currentText() + " " + self.stopBitsBox.currentText())
        serial.setPortName(self.comPortBox.currentText())
        serial.setBaudRate((int)(baudRate[self.baudRateBox.currentIndex()]))
        serial.setDataBits((int)(dataBits[self.dataBitsBox.currentIndex()]))
        serial.setStopBits((int)(stopBits[self.stopBitsBox.currentIndex()]))
        serial.setParity(parityValue[self.parityBox.currentIndex()])
        serial.open(QIODevice.ReadWrite)
        serial.readyRead.connect(temperatureControl)

class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.secondWin = None
        self.setFixedWidth(330)
        self.setFixedHeight(270)
        self.build()
 
    def build(self):
        self.serialSettingsEdit = QtWidgets.QLineEdit(self)
        self.serialSettingsEdit.setFixedWidth(190)
        self.serialSettingsEdit.setFixedHeight(27)
        self.serialSettingsEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.serialSettingsEdit.setFont(QFont("Ink Free", 12))
        self.serialSettingsEdit.setStyleSheet("color: blue;")
        self.serialSettingsEdit.move(25, 5)
        self.serialSettingsEdit.setReadOnly(True)

        self.temperatureLabel = QtWidgets.QLabel("+00.0\u00B0" + "C", self) 
        self.temperatureLabel.setFixedWidth(110)
        self.temperatureLabel.setFont(QFont("Ink Free", 20))
        self.temperatureLabel.setStyleSheet("color: red;")       
        self.temperatureLabel.move(110, 230)

        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(255)
        self.progressBar.setFixedWidth(320)
        self.progressBar.setFormat("")
        self.progressBar.move(25, 200)

        self.settingsButton = QtWidgets.QPushButton('Settings', self)
        self.settingsButton.setFont(QFont("Ink Free", 12))
        self.settingsButton.setStyleSheet("font-weight: bold")
        self.settingsButton.clicked.connect(self.open_win)
        self.settingsButton.move(235, 5)

        self.redColorLabel = QtWidgets.QLabel("Red", self) 
        self.redColorLabel.setFont(QFont("Arial", 10))
        self.redColorLabel.setStyleSheet("color: red;")       
        self.redColorLabel.move(28, 55)     

        self.redColorSlider = QtWidgets.QSlider(Qt.Horizontal, self)
        self.redColorSlider.setGeometry(30, 40, 200, 30)
        self.redColorSlider.setMaximum(255)
        self.redColorSlider.move(60, 50)
        self.redColorSlider.valueChanged[int].connect(self.redSlider)            

        self.yellowColorLabel = QtWidgets.QLabel("Yellow", self) 
        self.yellowColorLabel.setFont(QFont("Arial", 10))
        self.yellowColorLabel.setStyleSheet("color: rgb(204, 204, 0)")       
        self.yellowColorLabel.move(15, 105) 

        self.yellowColorSlider = QtWidgets.QSlider(Qt.Horizontal, self)
        self.yellowColorSlider.setGeometry(30, 40, 200, 30)
        self.yellowColorSlider.setMaximum(255)
        self.yellowColorSlider.move(60, 100)
        self.yellowColorSlider.valueChanged[int].connect(self.yellowSlider)  

        self.greenColorLabel = QtWidgets.QLabel("Green", self) 
        self.greenColorLabel.setFont(QFont("Arial", 10))
        self.greenColorLabel.setStyleSheet("color: green")       
        self.greenColorLabel.move(15, 155)

        self.greenColorSlider = QtWidgets.QSlider(Qt.Horizontal, self)
        self.greenColorSlider.setGeometry(30, 40, 200, 30)
        self.greenColorSlider.setMaximum(255)
        self.greenColorSlider.move(60, 150)
        self.greenColorSlider.valueChanged[int].connect(self.greenSlider)      

    def open_win(self):
        if not self.secondWin:
            self.secondWin = SecondWindow(self)
        self.secondWin.show()

    def redSlider(self, value):
        serial.write(b'2')
        serial.write(value.to_bytes(1, 'big'))

    def greenSlider(self, value):
        serial.write(b'0')
        serial.write(value.to_bytes(1, 'big')) 
           
    def yellowSlider(self, value):
        serial.write(b'1')
        serial.write(value.to_bytes(1, 'big'))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
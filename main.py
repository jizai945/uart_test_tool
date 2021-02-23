import sys
import serial
import serial.tools.list_ports
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer
from ui_demo_1 import Ui_Form


class Pyqt5_Serial(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(Pyqt5_Serial, self).__init__()
        self.setupUi(self)
        self.init()
        self.setWindowTitle("普渡测试小工具")
        self.ser = serial.Serial()
        self.port_check()


    def init(self):
        # 串口检测按钮
        self.s1__box_1.clicked.connect(self.port_check)

        # 串口信息显示
        self.s1__box_2.currentTextChanged.connect(self.port_imf)

        # 打开串口按钮
        self.open_button.clicked.connect(self.port_open)

        # 关闭串口按钮
        self.close_button.clicked.connect(self.port_close)

        # 清除接收窗口
        self.clear_button.clicked.connect(self.receive_data_clear)

        # BTN
        self.btn1.clicked.connect(lambda: self.btn_func(1))
        self.btn2.clicked.connect(lambda: self.btn_func(2))
        self.btn3.clicked.connect(lambda: self.btn_func(3))
        self.btn4.clicked.connect(lambda: self.btn_func(4))
        self.btn5.clicked.connect(lambda: self.btn_func(5))
        self.btn6.clicked.connect(lambda: self.btn_func(6))
        self.btn7.clicked.connect(lambda: self.btn_func(7))
        self.btn8.clicked.connect(lambda: self.btn_func(8))

        # 定时器接收数据
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.data_receive)

    # 串口检测
    def port_check(self):
        # 检测所有存在的串口，将信息存储在字典中
        self.Com_Dict = {}
        port_list = list(serial.tools.list_ports.comports())
        self.s1__box_2.clear()
        for port in port_list:
            self.Com_Dict["%s" % port[0]] = "%s" % port[1]
            self.s1__box_2.addItem(port[0])
        if len(self.Com_Dict) == 0:
            self.state_label.setText(" 无串口")

    # 串口信息
    def port_imf(self):
        # 显示选定的串口的详细信息
        imf_s = self.s1__box_2.currentText()
        if imf_s != "":
            self.state_label.setText(
                self.Com_Dict[self.s1__box_2.currentText()])

    # 打开串口
    def port_open(self):
        self.ser.port = self.s1__box_2.currentText()
        self.ser.baudrate = 115200
        self.ser.bytesize = 8
        self.ser.stopbits = 1
        self.ser.parity = 'N'

        try:
            self.ser.open()
        except:
            QMessageBox.critical(self, "Port Error", "此串口不能被打开！")
            return None

        # 打开串口接收定时器，周期为2ms
        self.timer.start(2)

        if self.ser.isOpen():
            self.open_button.setEnabled(False)
            self.close_button.setEnabled(True)

    # 关闭串口
    def port_close(self):

        self.timer.stop()

        try:
            self.ser.close()
        except:
            pass
        self.open_button.setEnabled(True)
        self.close_button.setEnabled(False)
  
     # 接收数据
    def data_receive(self):
        try:
            num = self.ser.inWaiting()
        except:
            self.port_close()
            return None
        if num > 0:
            data = self.ser.read(num)
            num = len(data)
            # hex显示
            if self.hex_receive.checkState():
                out_s = ''
                for i in range(0, len(data)):
                    out_s = out_s + '{:02X}'.format(data[i]) + ' '
                self.receive_text.insertPlainText(out_s)
            else:
                # 串口接收到的字符串为b'123',要转化成unicode字符串才能输出到窗口中去
                self.receive_text.insertPlainText(data.decode('iso-8859-1'))


            # 获取到text光标
            textCursor = self.receive_text.textCursor()
            # 滚动到底部
            textCursor.movePosition(textCursor.End)
            # 设置光标到text中去
            self.receive_text.setTextCursor(textCursor)
        else:
            pass

    # 清除显示
    def receive_data_clear(self):
        self.receive_text.setText("")

    # btn1
    def btn_func(self, n):
        print(f'btn{n} clicked')   

        if self.ser.isOpen():  
            if n==1:
                src = '40 06 00 01 00 01 DB 16'
            elif n==2:
                src = '40 06 00 01 00 02 DA 56'
            elif n==3:
                src = '40 06 00 02 00 01 DB E6'
            elif n==4:
                src = '40 06 00 02 00 02 DA A6'
            elif n==5:
                src = '41 06 00 01 00 01 0A 17'
            elif n==6:
                src = '41 06 00 01 00 02 0B 57'
            elif n==7:
                src = '41 06 00 02 00 01 0A E7'
            elif n==8:
                src = '41 06 00 02 00 02 0B A7'               
            else:
                return

            input_s=bytes.fromhex(src) 

            self.ser.write(input_s)
            self.s3__send_text.setText(src)
        else:
            QMessageBox.critical(self, 'wrong data', '发送错误，请打开串口')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myshow = Pyqt5_Serial()
    myshow.show()
    sys.exit(app.exec_())

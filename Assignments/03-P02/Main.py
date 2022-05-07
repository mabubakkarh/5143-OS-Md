'''
 Importing all necessary modules and packages .
 For GUI using PyQt5
'''


"""
File uploading imports
"""
from Process_file import Process_file
from FCFS_file import FCFS_ALGO
from SJF_file import SJF_ALGO
from Priority_file import Priority_ALGO
from RoundRobbin import RR_ALGO
from SRTF_file import SRTF_ALGO
"""
End of file upload imports
"""

import random
import sys
import copy
from subprocess import Popen
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from process import Process

from rr import RR
from fcfs import FCFS
from pb import PB
from sjf import SJF
from srtf import SRTF



class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.change_font()
        self.proc_list = []
        self.history = []
        self.algo_list = ["FCFS", "RR", "SJF", "SRTF", "PB"]

        self.column_count = 3
        self.cur_algo = "FCFS"
        self.process_count = 0

        self.init_ui()

   # setting font style
    def change_font(self):
        font = QtGui.QFont()


        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(True)
        self.setFont(font)
    # initialisation of UI
    def init_ui(self):
        self.resize(1200, 700)
        self.center()

        # Algorithm selection
        self.alg_select = QComboBox(self)
        for algo in self.algo_list:
            self.alg_select.addItem(algo)
        self.alg_select.activated.connect(self.enable_slot)
        self.process_name = QLineEdit()
        self.process_name.setMaxLength(10)

        # at for arrival time
        self.at_label = QLabel("AT")
        self.at = QSpinBox()
        self.at.setRange(0, 65535)
        
        # bt for  burst  time
        self.bt = QSpinBox()
        self.bt.setRange(1, 65535)
       
        

        # CPU count
        self.cpu_count = QComboBox(self)
        for cpu_idx in range(1, 5):
            self.cpu_count.addItem(str(cpu_idx))
        self.cpu_count.activated.connect(self.set_cpu_slot)
        self.cpu_label = QLabel("CPU")

        # quantum time
        self.tq = QSpinBox()
        self.tq.setRange(1, 65535)
        self.tq.setDisabled(True)
        self.tq_label = QLabel("Quantum")

        # priority List
        self.priority_list = QLabel("Priority")
        self.priority_list = QSpinBox()
        self.priority_list.setRange(1, 65535)
        self.priority_list.setDisabled(True)

        # I/O Burst
        self.io=QLabel("I/O burst")
        self.io=QSpinBox()
        self.io.setRange(0,65535)
        self.proc_table = QTableWidget(self)

        # add_button
        self.add_button = QPushButton("Add", self)
        self.add_button.clicked.connect(self.add)

        # add file button
        self.add_file_button = QPushButton("Add File", self)
        self.add_file_button.clicked.connect(self.add_file)

        #  Reset the whole process
        reset_button = QPushButton("Reset", self)
        reset_button.clicked.connect(self.reset)

        # Run the process
        self.run_alg = QPushButton("Run", self)
        self.run_alg.clicked.connect(self.run_algorithm)
        self.run_alg.setDisabled(True)
        self.run_alg.setFixedHeight(65)

        # setting The columns
        self.proc_table.setColumnCount(5)
        self.proc_table.setHorizontalHeaderLabels(["Process Name", "Arrival Time","Total BT for a process" ,"Priority","I/O Burst"])
        self.proc_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.proc_table.verticalHeader().setVisible(False)
        header = self.proc_table.horizontalHeader()
        for column_idx in range(self.column_count):
            header.setSectionResizeMode(column_idx, QHeaderView.Stretch)

        # Ready queue
        self.ready_table = QTableWidget(self)
        self.ready_table.setRowCount(1)
        self.ready_table.verticalHeader().setVisible(False)
        self.ready_table.setMaximumHeight(50)
        self.ready_table.verticalHeader().setDefaultSectionSize(50)
        self.ready_table.horizontalHeader().setVisible(False)
        self.ready_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Gantt_table
        self.gantt_table = QTableWidget(self)
        self.gantt_table.setRowCount(1)
        self.gantt_table.setVerticalHeaderLabels(["CPU 1"])
        header = self.gantt_table.verticalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        self.gantt_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.real_time_label = QLabel("Real Time = 0 sec")


        # Result table column
        self.result_table = QTableWidget(self)
        self.result_table.setColumnCount(6)
        self.result_table.setHorizontalHeaderLabels(
            ["Process Name", "Arrival Time", "Burst Time", "Waiting Time", "Turnaround Time", "Normalized TT"]
        )
        self.result_table.verticalHeader().setVisible(False)
        header = self.result_table.horizontalHeader()
        for time_table_col in range(6):
            header.setSectionResizeMode(time_table_col, QHeaderView.Stretch)
        self.result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        
        # Realtime history slideer
        self.history_slider = QSlider(Qt.Horizontal, self)
        self.history_slider.setDisabled(True)
        self.history_slider.valueChanged.connect(self.slider_control)
        # taking a grid layout for all necessary process
        grid_line = QGridLayout()
        grid_line.addWidget(QLabel("Algorithm"), 0, 0)
        grid_line.addWidget(self.at_label, 0, 1)
        grid_line.addWidget(QLabel("BT For A process "), 0, 2)
        grid_line.addWidget(self.alg_select, 1, 0)
        grid_line.addWidget(self.at, 1, 1)
        grid_line.addWidget(self.bt, 1, 2)
        grid_line.addWidget(self.cpu_label, 0, 3)
        grid_line.addWidget(self.cpu_count, 1, 3)
        grid_line.addWidget(self.tq_label, 0, 4)
        grid_line.addWidget(self.tq, 1, 4)
        # priority adding only for pb
        grid_line.addWidget(QLabel("Priority"), 0, 5)
        grid_line.addWidget(self.priority_list, 1, 5)
        grid_line.addWidget(QLabel("I/O Burst"),0,6)
        grid_line.addWidget(self.io,1,6)
        grid_line.addWidget(self.add_button, 0, 7)
        grid_line.addWidget(self.add_file_button, 1, 7)
        grid_line.addWidget(reset_button, 2, 7)
        grid_line.addWidget(self.run_alg, 0, 8, 2, 1)
        vbox_line2 = QVBoxLayout()
        ready_name = QLabel("Ready Queue")
        ready_name.setMaximumHeight(25)
        vbox_line2.addWidget(ready_name)
        vbox_line2.addWidget(self.ready_table)
        # Widgets for Gant Chart
        hbox_line3 = QHBoxLayout()
        hbox_line3.addWidget(QLabel("Gantt Chart"))
        hbox_line3.addWidget(self.real_time_label)

        # vbox layout for whole process
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)
        vbox_main.addLayout(grid_line)
        vbox_main.addWidget(self.proc_table)
        vbox_main.addWidget(self.history_slider)
        vbox_main.addLayout(vbox_line2)
        vbox_main.addLayout(hbox_line3)
        vbox_main.addWidget(self.gantt_table)
        vbox_main.addWidget(self.result_table)
        # vbox_main.addStretch(3)
        self.setWindowTitle("Process Simulator ")

        # self.setGeometry(0, 0, 800, 600)
        self.center()
        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    # enables slot when select an algorithm
    def enable_slot(self):
        if self.alg_select.currentText() != "Y":

            if self.cur_algo == "Y":
                self.reset()

                self.default_setting()
            if self.alg_select.currentText() == "RR":
                self.tq.setEnabled(True)
            elif self.alg_select.currentText()=="PB":
                self.priority_list.setEnabled(True)
            else:
                self.priority_list.setDisabled(True)
                self.tq.setDisabled(True)
        else:
            self.reset()

            self.yosa_setting()
        self.cur_algo = self.alg_select.currentText()

    def set_cpu_slot(self):
        name_header = []
        cpu_select = int(self.cpu_count.currentText())
        self.gantt_table.setRowCount(cpu_select)
        if self.alg_select.currentText() != "Y":
            for i in range(1, cpu_select + 1):
                name_header.append("CPU " + str(i))
        else:


            self.result_table.setRowCount(cpu_select)
            self.result_table.verticalHeader().setVisible(True)
            self.result_table.setVerticalHeaderLabels(name_header)

            if cpu_select > 1:
                self.result_table.setSpan(0, 10, cpu_select, 1)
                self.result_table.setSpan(0, 12, cpu_select, 1)
            header = self.result_table.verticalHeader()
            for i in range(len(name_header)):
                header.setSectionResizeMode(i, QHeaderView.Stretch)
            self.student_list.clear()


        self.gantt_table.setVerticalHeaderLabels(name_header)
        header = self.gantt_table.verticalHeader()
        for i in range(len(name_header)):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

        self.history_slider.setDisabled(True)

    # For testing
    def test(self):
        self.run_alg.setEnabled(True)

        for process_id in range(random.randrange(1, 16)):
            self.proc_list.append(
                Process("p" + str(process_id), random.randrange(0, 10), random.randrange(1, 8), process_id)
            )

        self.proc_list = [
            Process("p0", 1, 4, 0),
            Process("p1", 2, 3, 1),
            Process("p2", 2, 3, 2),
            Process("p3", 2, 3, 3),
            Process("p4", 2, 3, 4),
            Process("p5", 0, 2, 5),
            Process("p6", 0, 2, 6),
            Process("p7", 0, 2, 7),
            Process("p8", 1, 4, 8),
            Process("p9", 1, 4, 9),
        ]


        # -------------------------------
        # showing Results in console
        print("[self.proc_list]")
        print("[", end="")
        for idx, process in enumerate(self.proc_list):
            print("Process('{0}', {1}, {2}, {3}),".format(process.id, process.at, process.at, idx), end="")
        print("]")


        self.proc_table.setRowCount(len(self.proc_list))
        for i in range(len(self.proc_list)):
            self.proc_table.setItem(i, 0, QTableWidgetItem(self.proc_list[i].id))
            self.proc_table.item(i, 0).setBackground(
                QtGui.QColor(self.proc_list[i].color[0], self.proc_list[i].color[1], self.proc_list[i].color[2])
            )

            self.proc_table.setItem(i, 1, QTableWidgetItem(str(self.proc_list[i].at)))
            self.proc_table.setItem(i, 2, QTableWidgetItem(str(self.proc_list[i].bt)))

        self.process_name.clear()
        self.at.setValue(0)
        self.bt.setValue(0)

    # taking values from file
    def add_file(self):
      path = QFileDialog.getOpenFileName(self, 'Open a file', '', "All files (*)")
      if path != ('',''):
        print("File path:", path[0])

    # Taking values for processing and algorithm to execute
    def add(self):
        self.run_alg.setEnabled(True)
        if self.cur_algo=="PB":
            proc_name="p"+str(self.process_count+1)
            self.proc_list.append(Process(proc_name, self.at.value(), self.bt.value(), self.process_count,self.priority_list.value(),self.io.value()))
            self.process_count += 1
            if self.process_count == 15:
                self.add_button.setDisabled(True)

        elif self.cur_algo != "Y":
            proc_name = "P" + str(self.process_count + 1)

            self.proc_list.append(Process(proc_name, self.at.value(), self.bt.value(), self.process_count,self.priority_list.value(),self.io.value()))
            self.process_count += 1
            if self.process_count == 15:
                self.add_button.setDisabled(True)




       # self.process_count += 1

        self.proc_table.setRowCount(len(self.proc_list))
        for proc_idx, process in enumerate(self.proc_list):
            self.proc_table.setItem(proc_idx, 0, QTableWidgetItem(process.id))
            self.proc_table.item(proc_idx, 0).setBackground(
                QtGui.QColor(process.color[0], process.color[1], process.color[2])
            )
            self.proc_table.setItem(proc_idx, 2, QTableWidgetItem(str(process.bt)))
            self.proc_table.setItem(proc_idx,4,QTableWidgetItem(str(process.io)))
            if self.cur_algo=="PB":
                self.proc_table.setItem(proc_idx,3,QTableWidgetItem(str(process.priority_list)))
            if self.cur_algo != "YOSA":

                self.proc_table.setItem(proc_idx, 1, QTableWidgetItem(str(process.at)))




        self.process_name.clear()
        self.at.setValue(0)
        self.bt.setValue(1)
    # Reset the whole process
    def reset(self):

        self.proc_table.setRowCount(0)


        self.ready_table.clear()
        self.ready_table.setColumnCount(0)
        self.gantt_table.setColumnCount(0)
        self.result_table.setRowCount(0)
        self.run_alg.setDisabled(True)
        self.proc_list.clear()
        self.history.clear()
        self.history_slider.setDisabled(True)
        self.add_button.setEnabled(True)

        self.set_cpu_slot()
        self.cpu_count.setEnabled(True)

        self.cpu_count.clear()
        for cpu_idx in range(1, 5):
            self.cpu_count.addItem(str(cpu_idx))
        self.subject_count = [0, 0, 0, 0]
        self.process_count = 0
        self.ready_table.setEnabled(True)

    # Function for Running different algorithm
    def run_algorithm(self):

        proc_copy_list = copy.deepcopy(self.proc_list)
        if self.cur_algo == "FCFS":
            scheduler = FCFS(proc_copy_list, int(self.cpu_count.currentText()))
        elif self.cur_algo == "RR":
            scheduler = RR(proc_copy_list, int(self.cpu_count.currentText()), self.tq.value())
        elif self.cur_algo == "SJF":
            scheduler = SJF(proc_copy_list, int(self.cpu_count.currentText()))
        elif self.cur_algo == "SRTF":
            scheduler = SRTF(proc_copy_list, int(self.cpu_count.currentText()))
        elif self.cur_algo == "PB":
            scheduler = PB(proc_copy_list, int(self.cpu_count.currentText()),int(self.priority_list.value()))


        scheduler.run()
        self.history_slider.setEnabled(True)


        if self.cur_algo != "Y":
            self.history = scheduler.history

            self.history_slider.setRange(0, len(self.history) - 1)
            self.history_slider.setValue(0)
            self.ready_table.setColumnCount(len(self.history[0][0]))
            self.gantt_table.setColumnCount(0)
            self.result_table.setRowCount(len(self.history[0][2]))

            for q_proc_idx, q_process in enumerate(self.history[0][0]):
                self.ready_table.setItem(0, q_proc_idx, QTableWidgetItem(q_process.id))
                self.ready_table.item(0, q_proc_idx).setBackground(
                    QtGui.QColor(
                        q_process.color[0],
                        q_process.color[1],
                        q_process.color[2],
                    )
                )
            # DEBUG
            # print("queue:", self.history[0][0][queue_process_idx].id)
            for proc_idx, process in enumerate(self.history[0][2]):
                self.result_table.setItem(proc_idx, 0, QTableWidgetItem(process.id))
                self.result_table.setItem(proc_idx, 1, QTableWidgetItem(str(process.at)))
                self.result_table.setItem(proc_idx, 2, QTableWidgetItem(str(process.bt)))
                self.result_table.setItem(proc_idx, 3, QTableWidgetItem(str(process.wt)))
                self.result_table.setItem(proc_idx, 4, QTableWidgetItem(str(process.tt)))
                self.result_table.setItem(proc_idx, 5, QTableWidgetItem(str(process.ntt)))
                self.result_table.item(proc_idx, 0).setBackground(
                    QtGui.QColor(
                        process.color[0],
                        process.color[1],
                        process.color[2],
                    )
                )


    def slider_control(self):

        second = self.history_slider.value()

        if self.cur_algo != "Y":
            cpu_count = len(self.history[0][1])
            self.ready_table.setColumnCount(len(self.history[second][0]))
            self.gantt_table.setColumnCount(second)
            for q_proc_idx, q_process in enumerate(self.history[second][0]):
                self.ready_table.setItem(0, q_proc_idx, QTableWidgetItem(q_process.id))
                self.ready_table.item(0, q_proc_idx).setBackground(
                    QtGui.QColor(
                        q_process.color[0],
                        q_process.color[1],
                        q_process.color[2],
                    )
                )
            max_len_cpu = 0
            for seconds in range(second):
                for cpu in range(cpu_count):

                    if self.history[seconds + 1][1][cpu]:
                        max_len_cpu = cpu
                        self.gantt_table.setItem(cpu, seconds, QTableWidgetItem(self.history[seconds + 1][1][cpu].id))
                        self.gantt_table.item(cpu, seconds).setBackground(
                            QtGui.QColor(
                                self.history[seconds + 1][1][cpu].color[0],
                                self.history[seconds + 1][1][cpu].color[1],
                                self.history[seconds + 1][1][cpu].color[2],
                            )
                        )

            self.gantt_table.scrollToItem(self.gantt_table.item(max_len_cpu, second - 1))
            fortext = "Real Time = " + str(second) + " sec"
            self.real_time_label.setText(fortext)



    def default_setting(self):

        self.at.setRange(0, 65535)
        self.at_label.setText("AT")
        self.bt.setRange(1, 65535)
        self.cpu_label.setText("CPU")
        self.tq.setRange(1, 65535)
        self.tq_label.setText("Quantum")


        self.proc_table.setColumnCount(3)
        self.proc_table.setHorizontalHeaderLabels(["Process Name", "Arrival Time", "Burst Time"])
        header = self.proc_table.horizontalHeader()
        for column_idx in range(self.column_count):
            header.setSectionResizeMode(column_idx, QHeaderView.Stretch)

        self.set_cpu_slot()

        self.result_table.setColumnCount(6)
        self.result_table.setHorizontalHeaderLabels(
            ["Process Name", "Arrival Time", "Burst Time", "Waiting Time", "Turnaround Time", "Normalized TT"]
        )
        self.result_table.verticalHeader().setVisible(False)
        header = self.result_table.horizontalHeader()
        self.result_table.horizontalHeader().setFixedHeight(25)
        for time_table_col in range(6):
            header.setSectionResizeMode(time_table_col, QHeaderView.Stretch)
        self.real_time_label.setText("Real Time = 0 sec")
        self.student_list.setDisabled(True)

"""
CODE FOR READING FROM FILES
"""
words = []
processes = list()
processesSJF = list()

with open('process', 'r') as file:
    for line in file:
        words.append(line.split())



        
def menu():
    print("\nWhat algorithm you want to launch?")
    print('1. FCFS')
    print('2. SJF')
    print('3. Priority')
    print('4. Round Robin')
    print('5. SRTF')
    print('6. End')
    z = int(input('(1-4):'))
    if z == 1:
        fcfs = FCFS_ALGO(words)
        fcfs.run()
        menu()
    elif z == 2:
        sjf = SJF_ALGO(words)
        sjf.run()
        menu()
    elif z == 3:
        pr = Priority_ALGO(words)
        pr.run()
        menu()
    elif z == 4:
        rr = RR_ALGO()
        rr.getData()
        rr.RoundRobin()
        menu()
    elif z == 5:
        """
        code for reading data from srtf file
        """
        proc = []
        with open('srtf_process', 'r') as file:
            for line in file:
                intList = []
                ll = line.split()
                for i in ll:
                    intList.append(int(i))
                proc.append(intList)
        n = len(proc)
        srtf = SRTF_ALGO()
        srtf.findavgTime(proc, n)
        menu()
    elif z == 6:
        print("System is exiting...")
        sys.exit()
    else:
        print("Wrong input")
        sys.exit()


if __name__ == "__main__":
    print("Choose an option:")
    print("1. python GUI with manual input")
    print("2. console GUI with File input")
    print("3. Exit")
    option = int(input())
    if option == 1:
      app = QApplication(sys.argv)
      ex = MyApp()
      sys.exit(app.exec_())
    elif option == 2:
      menu()
    else:
      print("System is exiting...")
      sys.exit()






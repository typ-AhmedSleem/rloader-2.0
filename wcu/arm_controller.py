from PyQt5 import QtGui, QtWidgets


class Joints:
    Joint_1 = ('joint_1', 1)
    Joint_2 = ('joint_2', 2)
    Joint_3 = ('joint_3', 3)
    Joint_4 = ('joint_4', 4)
    Joint_5 = ('joint_5', 5)
    Joint_6 = ('joint_6', 6)


class Operation:
    INC = 1
    DEC = 2


class ArmControllerWindow(QtWidgets.QWidget):
    def __init__(self, handle_arm_cmd):
        super(ArmControllerWindow, self).__init__()

        self.tag = "ArmController"

        self.joints = [0] * 6

        W_WIDTH, W_HEIGHT, PADDING, = 400, 800, 15
        B_WIDTH, B_HEIGHT = (W_WIDTH - 2 * PADDING) // 2, 50

        self.setFixedWidth(W_WIDTH)
        self.setWindowTitle('Arm Controller')

        lbl_joint1 = QtWidgets.QLabel(parent=self, text=f'Joint 1:\t Angle= {self.joints[0]}')
        lbl_joint1.setFont(QtGui.QFont('monospace', 16))
        lbl_joint1.setGeometry(PADDING, PADDING // 2, W_WIDTH - 2 * PADDING, 50)

        btn_sm1_p = QtWidgets.QPushButton(parent=self, text='+')
        btn_sm1_p.clicked.connect(lambda: handle_arm_cmd(Joints.Joint_1,  self.joints[0],  Operation.INC))
        btn_sm1_p.setFont(QtGui.QFont("monospace", 20))
        btn_sm1_p.setStyleSheet("color: #0B9600;")
        btn_sm1_p.setGeometry(PADDING, lbl_joint1.geometry().y() + 50, B_WIDTH - PADDING // 2, B_HEIGHT)

        btn_sm1_n = QtWidgets.QPushButton(parent=self, text="-")
        btn_sm1_n.clicked.connect(lambda: handle_arm_cmd(Joints.Joint_1, self.joints[0], Operation.DEC))
        btn_sm1_n.setFont(QtGui.QFont("monospace", 20))
        btn_sm1_n.setStyleSheet("color: #F0391B;")
        btn_sm1_n.setGeometry(btn_sm1_p.geometry().x() + btn_sm1_p.geometry().width() + PADDING // 2,
                              btn_sm1_p.geometry().y(),
                              B_WIDTH,
                              B_HEIGHT)

        lbl_joint2 = QtWidgets.QLabel(parent=self, text=f'Joint 2:\t Angle= {self.joints[1]}')
        lbl_joint2.setFont(QtGui.QFont('monospace', 16))
        lbl_joint2.setGeometry(PADDING, btn_sm1_n.geometry().y() + B_HEIGHT, W_WIDTH - 2 * PADDING, 50)

        btn_sm2_p = QtWidgets.QPushButton(parent=self, text='+')
        btn_sm2_p.clicked.connect(lambda: handle_arm_cmd(Joints.Joint_2,  self.joints[1],  Operation.INC))
        btn_sm2_p.setFont(QtGui.QFont("monospace", 20))
        btn_sm2_p.setStyleSheet("color: #0B9600;")
        btn_sm2_p.setGeometry(PADDING, lbl_joint2.geometry().y() + 50, B_WIDTH - PADDING // 2, B_HEIGHT)

        btn_sm2_n = QtWidgets.QPushButton(parent=self, text="-")
        btn_sm2_n.clicked.connect(lambda: handle_arm_cmd(Joints.Joint_2,  self.joints[1],  Operation.DEC))
        btn_sm2_n.setFont(QtGui.QFont("monospace", 20))
        btn_sm2_n.setStyleSheet("color: #F0391B;")
        btn_sm2_n.setGeometry(btn_sm2_p.geometry().x() + btn_sm2_p.geometry().width() + PADDING // 2,
                              btn_sm2_p.geometry().y(),
                              B_WIDTH,
                              B_HEIGHT)

        lbl_joint3 = QtWidgets.QLabel(parent=self, text=f'Joint 3:\t Angle= {self.joints[2]}')
        lbl_joint3.setFont(QtGui.QFont('monospace', 16))
        lbl_joint3.setGeometry(PADDING, btn_sm2_n.geometry().y() + B_HEIGHT, W_WIDTH - 2 * PADDING, 50)

        btn_sm3_p = QtWidgets.QPushButton(parent=self, text='+')
        btn_sm3_p.clicked.connect(lambda: handle_arm_cmd(Joints.Joint_3,  self.joints[2],  Operation.INC))
        btn_sm3_p.setFont(QtGui.QFont("monospace", 20))
        btn_sm3_p.setStyleSheet("color: #0B9600;")
        btn_sm3_p.setGeometry(PADDING, lbl_joint3.geometry().y() + 50, B_WIDTH - PADDING // 2, B_HEIGHT)

        btn_sm3_n = QtWidgets.QPushButton(parent=self, text="-")
        btn_sm3_n.clicked.connect(lambda: handle_arm_cmd(Joints.Joint_3,  self.joints[2],  Operation.DEC))
        btn_sm3_n.setFont(QtGui.QFont("monospace", 20))
        btn_sm3_n.setStyleSheet("color: #F0391B;")
        btn_sm3_n.setGeometry(btn_sm3_p.geometry().x() + btn_sm3_p.geometry().width() + PADDING // 2,
                              btn_sm3_p.geometry().y(),
                              B_WIDTH,
                              B_HEIGHT)

        lbl_joint4 = QtWidgets.QLabel(parent=self, text=f'Joint 4:\t Angle= {self.joints[3]}')
        lbl_joint4.setFont(QtGui.QFont('monospace', 16))
        lbl_joint4.setGeometry(PADDING, btn_sm3_n.geometry().y() + B_HEIGHT, W_WIDTH - 2 * PADDING, 50)

        btn_sm4_p = QtWidgets.QPushButton(parent=self, text='+')
        btn_sm4_p.clicked.connect(lambda: handle_arm_cmd(Joints.Joint_4,  self.joints[3],  Operation.INC))
        btn_sm4_p.setFont(QtGui.QFont("monospace", 20))
        btn_sm4_p.setStyleSheet("color: #0B9600;")
        btn_sm4_p.setGeometry(PADDING, lbl_joint4.geometry().y() + 50, B_WIDTH - PADDING // 2, B_HEIGHT)

        btn_sm4_n = QtWidgets.QPushButton(parent=self, text="-")
        btn_sm4_n.clicked.connect(lambda: handle_arm_cmd(Joints.Joint_4,  self.joints[3],  Operation.DEC))
        btn_sm4_n.setFont(QtGui.QFont("monospace", 20))
        btn_sm4_n.setStyleSheet("color: #F0391B;")
        btn_sm4_n.setGeometry(btn_sm4_p.geometry().x() + btn_sm4_p.geometry().width() + PADDING // 2,
                              btn_sm4_p.geometry().y(),
                              B_WIDTH,
                              B_HEIGHT)

        lbl_joint5 = QtWidgets.QLabel(parent=self, text=f'Joint 5:\t Angle= {self.joints[4]}')
        lbl_joint5.setFont(QtGui.QFont('monospace', 16))
        lbl_joint5.setGeometry(PADDING, btn_sm4_n.geometry().y() + B_HEIGHT, W_WIDTH - 2 * PADDING, 50)

        btn_sm5_p = QtWidgets.QPushButton(parent=self, text='+')
        btn_sm5_p.clicked.connect(lambda: handle_arm_cmd(Joints.Joint_5,  self.joints[4],  Operation.INC))
        btn_sm5_p.setFont(QtGui.QFont("monospace", 20))
        btn_sm5_p.setStyleSheet("color: #0B9600;")
        btn_sm5_p.setGeometry(PADDING, lbl_joint5.geometry().y() + 50, B_WIDTH - PADDING // 2, B_HEIGHT)

        btn_sm5_n = QtWidgets.QPushButton(parent=self, text="-")
        btn_sm5_n.clicked.connect(lambda: handle_arm_cmd(Joints.Joint_5,  self.joints[4],  Operation.DEC))
        btn_sm5_n.setFont(QtGui.QFont("monospace", 20))
        btn_sm5_n.setStyleSheet("color: #F0391B;")
        btn_sm5_n.setGeometry(btn_sm5_p.geometry().x() + btn_sm5_p.geometry().width() + PADDING // 2,
                              btn_sm5_p.geometry().y(),
                              B_WIDTH,
                              B_HEIGHT)

        lbl_joint6 = QtWidgets.QLabel(parent=self, text=f'Joint 6:\t Angle= {self.joints[5]}')
        lbl_joint6.setFont(QtGui.QFont('monospace', 16))
        lbl_joint6.setGeometry(PADDING, btn_sm5_n.geometry().y() + B_HEIGHT, W_WIDTH - 2 * PADDING, 50)

        btn_sm6_p = QtWidgets.QPushButton(parent=self, text='+')
        btn_sm6_p.clicked.connect(lambda: handle_arm_cmd(Joints.Joint_6,  self.joints[5],  Operation.INC))
        btn_sm6_p.setFont(QtGui.QFont("monospace", 20))
        btn_sm6_p.setStyleSheet("color: #0B9600;")
        btn_sm6_p.setGeometry(PADDING, lbl_joint6.geometry().y() + 50, B_WIDTH - PADDING // 2, B_HEIGHT)

        btn_sm6_n = QtWidgets.QPushButton(parent=self, text="-")
        btn_sm6_n.clicked.connect(lambda: handle_arm_cmd(Joints.Joint_6,  self.joints[5],  Operation.DEC))
        btn_sm6_n.setFont(QtGui.QFont("monospace", 20))
        btn_sm6_n.setStyleSheet("color: #F0391B;")
        btn_sm6_n.setGeometry(btn_sm6_p.geometry().x() + btn_sm6_p.geometry().width() + PADDING // 2,
                              btn_sm6_p.geometry().y(),
                              B_WIDTH,
                              B_HEIGHT)

        self.setFixedHeight(max(btn_sm6_p.geometry().y() + B_HEIGHT + PADDING, W_WIDTH))

        self.lbls = [lbl_joint1, lbl_joint2, lbl_joint3, lbl_joint4, lbl_joint5, lbl_joint6]

    def ujr(self, j: int, na: int):
        self.joints[j - 1] = na
        self.lbls[j - 1].setText(f"Joint {j}:\t Angle={self.joints[j - 1]}")
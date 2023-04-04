from PyQt5 import QtGui, QtWidgets


class Joints:
    Joint_1 = ('joint_1', 1)
    Joint_2 = ('joint_2', 2)
    Joint_3 = ('joint_3', 3)
    Joint_4 = ('joint_4', 4)
    Joint_5 = ('joint_5', 5)
    Joint_6 = ('joint_6', 6)


class Operation:
    UP = 1
    DOWN = -1


class ArmControllerWindow(QtWidgets.QWidget):
    def __init__(self, handle_arm_cmd):
        super(ArmControllerWindow, self).__init__()

        self.tag = "ArmController"

        self.joints = {
            Joints.Joint_1[0]: 0,
            Joints.Joint_2[0]: 0,
            Joints.Joint_3[0]: 0,
            Joints.Joint_4[0]: 0,
            Joints.Joint_5[0]: 0,
            Joints.Joint_6[0]: 0
        }

        W_WIDTH, W_HEIGHT, PADDING, = 400, 800, 15
        B_WIDTH, B_HEIGHT = (W_WIDTH - 2 * PADDING) // 2, 50

        self.setFixedWidth(W_WIDTH)
        self.setWindowTitle('Arm Controller')

        lbl_joint1 = QtWidgets.QLabel(parent=self, text='Joint 1')
        lbl_joint1.setFont(QtGui.QFont('monospace', 16))
        lbl_joint1.setGeometry(PADDING, PADDING // 2, W_WIDTH - 2 * PADDING, 50)

        btn_sm1_p = QtWidgets.QPushButton(parent=self, text='+')
        btn_sm1_p.clicked.connect(lambda: handle_arm_cmd(Joints.Joint_1, Operation.UP))
        btn_sm1_p.setFont(QtGui.QFont("monospace", 20))
        btn_sm1_p.setStyleSheet("color: #0B9600;")
        btn_sm1_p.setGeometry(PADDING, lbl_joint1.geometry().y() + 50, B_WIDTH - PADDING // 2, B_HEIGHT)

        btn_sm1_n = QtWidgets.QPushButton(parent=self, text="-")
        btn_sm1_n.clicked.connect(lambda: handle_arm_cmd(Joints.Joint_1, Operation.DOWN))
        btn_sm1_n.setFont(QtGui.QFont("monospace", 20))
        btn_sm1_n.setStyleSheet("color: #F0391B;")
        btn_sm1_n.setGeometry(btn_sm1_p.geometry().x() + btn_sm1_p.geometry().width() + PADDING // 2,
                              btn_sm1_p.geometry().y(),
                              B_WIDTH,
                              B_HEIGHT)

        lbl_joint2 = QtWidgets.QLabel(parent=self, text="Joint 2")
        lbl_joint2.setFont(QtGui.QFont('monospace', 16))
        lbl_joint2.setGeometry(PADDING, btn_sm1_n.geometry().y() + B_HEIGHT, W_WIDTH - 2 * PADDING, 50)

        btn_sm2_p = QtWidgets.QPushButton(parent=self, text='+')
        btn_sm2_p.clicked.connect(lambda: handle_arm_cmd(Joints.Joint_2, Operation.UP))
        btn_sm2_p.setFont(QtGui.QFont("monospace", 20))
        btn_sm2_p.setStyleSheet("color: #0B9600;")
        btn_sm2_p.setGeometry(PADDING, lbl_joint2.geometry().y() + 50, B_WIDTH - PADDING // 2, B_HEIGHT)

        btn_sm2_n = QtWidgets.QPushButton(parent=self, text="-")
        btn_sm2_n.clicked.connect(lambda: handle_arm_cmd(Joints.Joint_2, Operation.DOWN))
        btn_sm2_n.setFont(QtGui.QFont("monospace", 20))
        btn_sm2_n.setStyleSheet("color: #F0391B;")
        btn_sm2_n.setGeometry(btn_sm2_p.geometry().x() + btn_sm2_p.geometry().width() + PADDING // 2,
                              btn_sm2_p.geometry().y(),
                              B_WIDTH,
                              B_HEIGHT)

        lbl_joint3 = QtWidgets.QLabel(parent=self, text="Joint 3")
        lbl_joint3.setFont(QtGui.QFont('monospace', 16))
        lbl_joint3.setGeometry(PADDING, btn_sm2_n.geometry().y() + B_HEIGHT, W_WIDTH - 2 * PADDING, 50)

        btn_sm3_p = QtWidgets.QPushButton(parent=self, text='+')
        btn_sm3_p.clicked.connect(lambda: handle_arm_cmd(Joints.Joint_3, Operation.UP))
        btn_sm3_p.setFont(QtGui.QFont("monospace", 20))
        btn_sm3_p.setStyleSheet("color: #0B9600;")
        btn_sm3_p.setGeometry(PADDING, lbl_joint3.geometry().y() + 50, B_WIDTH - PADDING // 2, B_HEIGHT)

        btn_sm3_n = QtWidgets.QPushButton(parent=self, text="-")
        btn_sm3_n.clicked.connect(lambda: handle_arm_cmd(Joints.Joint_3, Operation.DOWN))
        btn_sm3_n.setFont(QtGui.QFont("monospace", 20))
        btn_sm3_n.setStyleSheet("color: #F0391B;")
        btn_sm3_n.setGeometry(btn_sm3_p.geometry().x() + btn_sm3_p.geometry().width() + PADDING // 2,
                              btn_sm3_p.geometry().y(),
                              B_WIDTH,
                              B_HEIGHT)

        lbl_joint4 = QtWidgets.QLabel(parent=self, text="Joint 5")
        lbl_joint4.setFont(QtGui.QFont('monospace', 16))
        lbl_joint4.setGeometry(PADDING, btn_sm3_n.geometry().y() + B_HEIGHT, W_WIDTH - 2 * PADDING, 50)

        btn_sm4_p = QtWidgets.QPushButton(parent=self, text='+')
        btn_sm4_p.clicked.connect(lambda: handle_arm_cmd(Joints.Joint_4, Operation.UP))
        btn_sm4_p.setFont(QtGui.QFont("monospace", 20))
        btn_sm4_p.setStyleSheet("color: #0B9600;")
        btn_sm4_p.setGeometry(PADDING, lbl_joint4.geometry().y() + 50, B_WIDTH - PADDING // 2, B_HEIGHT)

        btn_sm4_n = QtWidgets.QPushButton(parent=self, text="-")
        btn_sm4_n.clicked.connect(lambda: handle_arm_cmd(Joints.Joint_4, Operation.DOWN))
        btn_sm4_n.setFont(QtGui.QFont("monospace", 20))
        btn_sm4_n.setStyleSheet("color: #F0391B;")
        btn_sm4_n.setGeometry(btn_sm4_p.geometry().x() + btn_sm4_p.geometry().width() + PADDING // 2,
                              btn_sm4_p.geometry().y(),
                              B_WIDTH,
                              B_HEIGHT)

        lbl_joint5 = QtWidgets.QLabel(parent=self, text="Joint 5")
        lbl_joint5.setFont(QtGui.QFont('monospace', 16))
        lbl_joint5.setGeometry(PADDING, btn_sm4_n.geometry().y() + B_HEIGHT, W_WIDTH - 2 * PADDING, 50)

        btn_sm5_p = QtWidgets.QPushButton(parent=self, text='+')
        btn_sm5_p.clicked.connect(lambda: handle_arm_cmd(Joints.Joint_5, Operation.UP))
        btn_sm5_p.setFont(QtGui.QFont("monospace", 20))
        btn_sm5_p.setStyleSheet("color: #0B9600;")
        btn_sm5_p.setGeometry(PADDING, lbl_joint5.geometry().y() + 50, B_WIDTH - PADDING // 2, B_HEIGHT)

        btn_sm5_n = QtWidgets.QPushButton(parent=self, text="-")
        btn_sm5_n.clicked.connect(lambda: handle_arm_cmd(Joints.Joint_5, Operation.DOWN))
        btn_sm5_n.setFont(QtGui.QFont("monospace", 20))
        btn_sm5_n.setStyleSheet("color: #F0391B;")
        btn_sm5_n.setGeometry(btn_sm5_p.geometry().x() + btn_sm5_p.geometry().width() + PADDING // 2,
                              btn_sm5_p.geometry().y(),
                              B_WIDTH,
                              B_HEIGHT)

        lbl_joint6 = QtWidgets.QLabel(parent=self, text=f'Arm Hand')
        lbl_joint6.setFont(QtGui.QFont('monospace', 16))
        lbl_joint6.setGeometry(PADDING, btn_sm5_n.geometry().y() + B_HEIGHT, W_WIDTH - 2 * PADDING, 50)

        btn_arm_hand = QtWidgets.QPushButton(parent=self, text='Open Hand')
        btn_arm_hand.clicked.connect(lambda: handle_arm_cmd(Joints.Joint_6, Operation.UP if self.joints[Joints.Joint_6[0]] == Operation.DOWN else Operation.DOWN))
        btn_arm_hand.setFont(QtGui.QFont("monospace", 17))
        btn_arm_hand.setGeometry(PADDING, lbl_joint6.geometry().y() + 50, lbl_joint6.geometry().width(), B_HEIGHT)

        self.setFixedHeight(max(btn_arm_hand.geometry().y() + B_HEIGHT + PADDING, W_WIDTH))

        self.lbls = {
            Joints.Joint_1[0]: lbl_joint1,
            Joints.Joint_2[0]: lbl_joint2,
            Joints.Joint_3[0]: lbl_joint3,
            Joints.Joint_4[0]: lbl_joint4,
            Joints.Joint_5[0]: lbl_joint5,
            Joints.Joint_6[0]: btn_arm_hand
        }

    def ujr(self, joint: str, new_pos: int):
        self.joints[joint] = new_pos
        if joint == Joints.Joint_6[0]:
            self.lbls[Joints.Joint_6[0]].setText("Open hand" if new_pos == Operation.UP else 'Close hand')
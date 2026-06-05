<<<<<<< HEAD
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 757)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.main_layout = QVBoxLayout(self.centralwidget)
        self.main_layout.setSpacing(15)
        self.main_layout.setObjectName(u"main_layout")
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.header_frame = QFrame(self.centralwidget)
        self.header_frame.setObjectName(u"header_frame")
        self.header_frame.setMinimumSize(QSize(0, 60))
        self.header_layout = QHBoxLayout(self.header_frame)
        self.header_layout.setObjectName(u"header_layout")
        self.header_layout.setContentsMargins(20, -1, 20, -1)
        self.title_label = QLabel(self.header_frame)
        self.title_label.setObjectName(u"title_label")

        self.header_layout.addWidget(self.title_label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header_layout.addItem(self.horizontalSpacer)

        self.btn_play = QPushButton(self.header_frame)
        self.btn_play.setObjectName(u"btn_play")
        self.btn_play.setMinimumSize(QSize(110, 36))

        self.header_layout.addWidget(self.btn_play)


        self.main_layout.addWidget(self.header_frame)

        self.video_layout = QHBoxLayout()
        self.video_layout.setSpacing(15)
        self.video_layout.setObjectName(u"video_layout")
        self.screen_main = QLabel(self.centralwidget)
        self.screen_main.setObjectName(u"screen_main")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(7)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.screen_main.sizePolicy().hasHeightForWidth())
        self.screen_main.setSizePolicy(sizePolicy)
        self.screen_main.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.video_layout.addWidget(self.screen_main)

        self.side_layout = QVBoxLayout()
        self.side_layout.setSpacing(10)
        self.side_layout.setObjectName(u"side_layout")
        self.label_thresh_title = QLabel(self.centralwidget)
        self.label_thresh_title.setObjectName(u"label_thresh_title")

        self.side_layout.addWidget(self.label_thresh_title)

        self.screen_thresh = QLabel(self.centralwidget)
        self.screen_thresh.setObjectName(u"screen_thresh")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(3)
        sizePolicy1.setVerticalStretch(3)
        sizePolicy1.setHeightForWidth(self.screen_thresh.sizePolicy().hasHeightForWidth())
        self.screen_thresh.setSizePolicy(sizePolicy1)
        self.screen_thresh.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.side_layout.addWidget(self.screen_thresh)

        self.label_crop_title = QLabel(self.centralwidget)
        self.label_crop_title.setObjectName(u"label_crop_title")

        self.side_layout.addWidget(self.label_crop_title)

        self.screen_crop = QLabel(self.centralwidget)
        self.screen_crop.setObjectName(u"screen_crop")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(3)
        sizePolicy2.setVerticalStretch(2)
        sizePolicy2.setHeightForWidth(self.screen_crop.sizePolicy().hasHeightForWidth())
        self.screen_crop.setSizePolicy(sizePolicy2)
        self.screen_crop.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.side_layout.addWidget(self.screen_crop)


        self.video_layout.addLayout(self.side_layout)


        self.main_layout.addLayout(self.video_layout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"NEXT FRAME - Intelligent License Plate Recognition System", None))
        MainWindow.setStyleSheet(QCoreApplication.translate("MainWindow", u"\n"
"    QMainWindow {\n"
"        background-color: #121214;\n"
"    }\n"
"    QWidget #centralwidget {\n"
"        background-color: #121214;\n"
"    }\n"
"    QLabel {\n"
"        color: #E2E8F0;\n"
"        font-family: 'Segoe UI', 'Malgun Gothic', sans-serif;\n"
"    }\n"
"   ", None))
        self.header_frame.setStyleSheet(QCoreApplication.translate("MainWindow", u"\n"
"        QFrame #header_frame {\n"
"            background-color: #1A1A1E;\n"
"            border-radius: 8px;\n"
"            border: 1px solid #2A2A32;\n"
"        }\n"
"       ", None))
        self.title_label.setStyleSheet(QCoreApplication.translate("MainWindow", u"font-size: 18px; font-weight: 700; color: #FFFFFF;", None))
        self.title_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\U0001f697 NEXT FRAME <span style=\" color:#10b981;\">| \U0000cc28\U0000b7c9 \U0000bc88\U0000d638\U0000d310 \U0000ac80\U0000cd9c \U0000c2dc\U0000c2a4\U0000d15c</span></p></body></html>", None))
        self.btn_play.setStyleSheet(QCoreApplication.translate("MainWindow", u"\n"
"           QPushButton {\n"
"               background-color: #27272A;\n"
"               color: #E4E4E7;\n"
"               border: 1px solid #3F3F46;\n"
"               border-radius: 6px;\n"
"               font-weight: 600;\n"
"               font-size: 13px;\n"
"           }\n"
"           QPushButton:hover {\n"
"               background-color: #3F3F46;\n"
"               border: 1px solid #52525B;\n"
"           }\n"
"           QPushButton:pressed {\n"
"               background-color: #18181B;\n"
"           }\n"
"          ", None))
        self.btn_play.setText(QCoreApplication.translate("MainWindow", u"\uc77c\uc2dc\uc815\uc9c0", None))
        self.screen_main.setStyleSheet(QCoreApplication.translate("MainWindow", u"\n"
"          QLabel #screen_main {\n"
"              border: 1px solid #2A2A32;\n"
"              background-color: #09090B;\n"
"              border-radius: 10px;\n"
"              font-size: 14px;\n"
"              letter-spacing: 1px;\n"
"              color: #71717A;\n"
"          }\n"
"         ", None))
        self.screen_main.setText(QCoreApplication.translate("MainWindow", u"SYSTEM INITIALIZING...", None))
        self.label_thresh_title.setStyleSheet(QCoreApplication.translate("MainWindow", u"font-size: 13px; font-weight: 600; color: #A1A1AA; margin-top: 5px;", None))
        self.label_thresh_title.setText(QCoreApplication.translate("MainWindow", u"\u2699\ufe0f \uc774\uc9c4\ud654 \uc601\uc0c1 \ubd84\uc11d (Advanced Thresh)", None))
        self.screen_thresh.setStyleSheet(QCoreApplication.translate("MainWindow", u"\n"
"            QLabel #screen_thresh {\n"
"                border: 1px solid #2A2A32;\n"
"                background-color: #09090B;\n"
"                border-radius: 8px;\n"
"                color: #52525B;\n"
"            }\n"
"           ", None))
        self.screen_thresh.setText(QCoreApplication.translate("MainWindow", u"BINARY FEED", None))
        self.label_crop_title.setStyleSheet(QCoreApplication.translate("MainWindow", u"font-size: 13px; font-weight: 600; color: #A1A1AA; margin-top: 10px;", None))
        self.label_crop_title.setText(QCoreApplication.translate("MainWindow", u"\U0001f50d \U0000c2e4\U0000c2dc\U0000ac04 \U0000bc88\U0000d638\U0000d310 \U0000cd94\U0000cd9c (ROI Crop)", None))
        self.screen_crop.setStyleSheet(QCoreApplication.translate("MainWindow", u"\n"
"            QLabel #screen_crop {\n"
"                border: 1px dashed #10B981;\n"
"                background-color: #14241F;\n"
"                border-radius: 8px;\n"
"                color: #10B981;\n"
"                font-weight: 600;\n"
"                font-size: 12px;\n"
"            }\n"
"           ", None))
        self.screen_crop.setText(QCoreApplication.translate("MainWindow", u"WAITING FOR DETECTION...", None))
    # retranslateUi

=======
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 757)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.main_layout = QVBoxLayout(self.centralwidget)
        self.main_layout.setSpacing(15)
        self.main_layout.setObjectName(u"main_layout")
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.header_frame = QFrame(self.centralwidget)
        self.header_frame.setObjectName(u"header_frame")
        self.header_frame.setMinimumSize(QSize(0, 60))
        self.header_layout = QHBoxLayout(self.header_frame)
        self.header_layout.setObjectName(u"header_layout")
        self.header_layout.setContentsMargins(20, -1, 20, -1)
        self.title_label = QLabel(self.header_frame)
        self.title_label.setObjectName(u"title_label")

        self.header_layout.addWidget(self.title_label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header_layout.addItem(self.horizontalSpacer)

        self.btn_play = QPushButton(self.header_frame)
        self.btn_play.setObjectName(u"btn_play")
        self.btn_play.setMinimumSize(QSize(110, 36))

        self.header_layout.addWidget(self.btn_play)


        self.main_layout.addWidget(self.header_frame)

        self.video_layout = QHBoxLayout()
        self.video_layout.setSpacing(15)
        self.video_layout.setObjectName(u"video_layout")
        self.screen_main = QLabel(self.centralwidget)
        self.screen_main.setObjectName(u"screen_main")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(7)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.screen_main.sizePolicy().hasHeightForWidth())
        self.screen_main.setSizePolicy(sizePolicy)
        self.screen_main.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.video_layout.addWidget(self.screen_main)

        self.side_layout = QVBoxLayout()
        self.side_layout.setSpacing(10)
        self.side_layout.setObjectName(u"side_layout")
        self.label_thresh_title = QLabel(self.centralwidget)
        self.label_thresh_title.setObjectName(u"label_thresh_title")

        self.side_layout.addWidget(self.label_thresh_title)

        self.screen_thresh = QLabel(self.centralwidget)
        self.screen_thresh.setObjectName(u"screen_thresh")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(3)
        sizePolicy1.setVerticalStretch(3)
        sizePolicy1.setHeightForWidth(self.screen_thresh.sizePolicy().hasHeightForWidth())
        self.screen_thresh.setSizePolicy(sizePolicy1)
        self.screen_thresh.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.side_layout.addWidget(self.screen_thresh)

        self.label_crop_title = QLabel(self.centralwidget)
        self.label_crop_title.setObjectName(u"label_crop_title")

        self.side_layout.addWidget(self.label_crop_title)

        self.screen_crop = QLabel(self.centralwidget)
        self.screen_crop.setObjectName(u"screen_crop")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(3)
        sizePolicy2.setVerticalStretch(2)
        sizePolicy2.setHeightForWidth(self.screen_crop.sizePolicy().hasHeightForWidth())
        self.screen_crop.setSizePolicy(sizePolicy2)
        self.screen_crop.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.side_layout.addWidget(self.screen_crop)


        self.video_layout.addLayout(self.side_layout)


        self.main_layout.addLayout(self.video_layout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"NEXT FRAME - Intelligent License Plate Recognition System", None))
        MainWindow.setStyleSheet(QCoreApplication.translate("MainWindow", u"\n"
"    QMainWindow {\n"
"        background-color: #121214;\n"
"    }\n"
"    QWidget #centralwidget {\n"
"        background-color: #121214;\n"
"    }\n"
"    QLabel {\n"
"        color: #E2E8F0;\n"
"        font-family: 'Segoe UI', 'Malgun Gothic', sans-serif;\n"
"    }\n"
"   ", None))
        self.header_frame.setStyleSheet(QCoreApplication.translate("MainWindow", u"\n"
"        QFrame #header_frame {\n"
"            background-color: #1A1A1E;\n"
"            border-radius: 8px;\n"
"            border: 1px solid #2A2A32;\n"
"        }\n"
"       ", None))
        self.title_label.setStyleSheet(QCoreApplication.translate("MainWindow", u"font-size: 18px; font-weight: 700; color: #FFFFFF;", None))
        self.title_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\U0001f697 NEXT FRAME <span style=\" color:#10b981;\">| \U0000cc28\U0000b7c9 \U0000bc88\U0000d638\U0000d310 \U0000ac80\U0000cd9c \U0000c2dc\U0000c2a4\U0000d15c</span></p></body></html>", None))
        self.btn_play.setStyleSheet(QCoreApplication.translate("MainWindow", u"\n"
"           QPushButton {\n"
"               background-color: #27272A;\n"
"               color: #E4E4E7;\n"
"               border: 1px solid #3F3F46;\n"
"               border-radius: 6px;\n"
"               font-weight: 600;\n"
"               font-size: 13px;\n"
"           }\n"
"           QPushButton:hover {\n"
"               background-color: #3F3F46;\n"
"               border: 1px solid #52525B;\n"
"           }\n"
"           QPushButton:pressed {\n"
"               background-color: #18181B;\n"
"           }\n"
"          ", None))
        self.btn_play.setText(QCoreApplication.translate("MainWindow", u"\uc77c\uc2dc\uc815\uc9c0", None))
        self.screen_main.setStyleSheet(QCoreApplication.translate("MainWindow", u"\n"
"          QLabel #screen_main {\n"
"              border: 1px solid #2A2A32;\n"
"              background-color: #09090B;\n"
"              border-radius: 10px;\n"
"              font-size: 14px;\n"
"              letter-spacing: 1px;\n"
"              color: #71717A;\n"
"          }\n"
"         ", None))
        self.screen_main.setText(QCoreApplication.translate("MainWindow", u"SYSTEM INITIALIZING...", None))
        self.label_thresh_title.setStyleSheet(QCoreApplication.translate("MainWindow", u"font-size: 13px; font-weight: 600; color: #A1A1AA; margin-top: 5px;", None))
        self.label_thresh_title.setText(QCoreApplication.translate("MainWindow", u"\u2699\ufe0f \uc774\uc9c4\ud654 \uc601\uc0c1 \ubd84\uc11d (Advanced Thresh)", None))
        self.screen_thresh.setStyleSheet(QCoreApplication.translate("MainWindow", u"\n"
"            QLabel #screen_thresh {\n"
"                border: 1px solid #2A2A32;\n"
"                background-color: #09090B;\n"
"                border-radius: 8px;\n"
"                color: #52525B;\n"
"            }\n"
"           ", None))
        self.screen_thresh.setText(QCoreApplication.translate("MainWindow", u"BINARY FEED", None))
        self.label_crop_title.setStyleSheet(QCoreApplication.translate("MainWindow", u"font-size: 13px; font-weight: 600; color: #A1A1AA; margin-top: 10px;", None))
        self.label_crop_title.setText(QCoreApplication.translate("MainWindow", u"\U0001f50d \U0000c2e4\U0000c2dc\U0000ac04 \U0000bc88\U0000d638\U0000d310 \U0000cd94\U0000cd9c (ROI Crop)", None))
        self.screen_crop.setStyleSheet(QCoreApplication.translate("MainWindow", u"\n"
"            QLabel #screen_crop {\n"
"                border: 1px dashed #10B981;\n"
"                background-color: #14241F;\n"
"                border-radius: 8px;\n"
"                color: #10B981;\n"
"                font-weight: 600;\n"
"                font-size: 12px;\n"
"            }\n"
"           ", None))
        self.screen_crop.setText(QCoreApplication.translate("MainWindow", u"WAITING FOR DETECTION...", None))
    # retranslateUi

>>>>>>> main

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QMenu
import conexion, var


class WidgetHistorial(QWidget):
    def __init__(self, nav):
        super(WidgetHistorial, self).__init__()

        self.nav = nav
        self.verticalLayout = QtWidgets.QVBoxLayout(self)

        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)

        self.tableWidget = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)

        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setText("Título")
        self.tableWidget.setHorizontalHeaderItem(0, item)

        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setText("Fecha")
        self.tableWidget.setHorizontalHeaderItem(1, item)

        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setText("Hora")
        self.tableWidget.setHorizontalHeaderItem(2, item)

        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setText("URL")
        self.tableWidget.setHorizontalHeaderItem(3, item)

        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setVisible(False)
        self.verticalLayout_2.addWidget(self.tableWidget)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.horizontalLayout = QtWidgets.QHBoxLayout()

        self.btnBorrarFecha = QtWidgets.QPushButton(self)

        self.horizontalLayout.addWidget(self.btnBorrarFecha)
        self.btnBorrarSel = QtWidgets.QPushButton(self)

        self.horizontalLayout.addWidget(self.btnBorrarSel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.btnBorrarFecha.setText("Borrar por fecha")
        self.btnBorrarSel.setText("Borrar selección")

        self.tableWidget.viewport().installEventFilter(self)
        self.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.generateMenu)

    def eventFilter(self, source, event):
        try:
            if (event.type() == QtCore.QEvent.MouseButtonPress and
                    event.buttons() == QtCore.Qt.RightButton and
                    source is self.tableWidget.viewport()):
                item = self.tableWidget.itemAt(event.pos())

                if item:
                    self.menu = QMenu(self)
                    self.tableWidget.selectRow(item.row())
                    if self.nav:
                        self.menu.addAction("Ir a sitio", lambda i=item: var.nav.nueva_pestana(
                            self.tableWidget.selectedItems()[3].text()))
                    self.menu.addAction("Borrar entrada", lambda i=item: self.borrar_entrada(i.row().numerator))
        except Exception as error:
            print("Error en event filter de historial: %s" % str(error))
        return super(WidgetHistorial, self).eventFilter(source, event)

    def generateMenu(self, pos):
        self.menu.exec_(self.tableWidget.mapToGlobal(pos))

    def borrar_entrada(self, idx=0):
        try:
            conexion.borrar_entrada_historial(conexion.ultima_entrada_historial() - idx)
            conexion.cargar_historial(self)
        except Exception as error:
            print("Error al borrar entrada: %s" % str(error))
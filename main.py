import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi
from conexion_sqlite import Comunicacion
import pyodbc

class VentanaPrincipal(QMainWindow):
    #Intercomunicar los botones de QTDesigner a Pycharm
    def __init__(self):
        super(VentanaPrincipal, self).__init__()
        loadUi("diseño.ui", self)
        self.bt_menu.clicked.connect(self.mover_menu)
        self.base_de_datos_tecnologias = Comunicacion()
        self.bt_restaurar.hide()
        self.bt_refrescar.clicked.connect(self.mostrar_productos)
        self.bt_agregar.clicked.connect(self.registrar_productos)
        self.bt_borrar.clicked.connect(self.eliminar_productos)
        self.bt_actualizar_tabla.clicked.connect(self.modificar_productos)
        self.bt_actualiza_buscar.clicked.connect(self.buscar_por_nombre_actualiza)
        self.bt_buscar_borrar.clicked.connect(self.buscar_por_nombre_eliminar)

        self.bt_minimizar.clicked.connect(self.control_bt_minimizar)
        self.bt_restaurar.clicked.connect(self.control_bt_normal)
        self.bt_maximizar.clicked.connect(self.control_bt_maximizar)
        self.bt_cerrar.clicked.connect(lambda: self.close())

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)

        self.frame_superior.mouseMoveEvent = self.mover_ventana

        self.bt_datos.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_datos))
        self.bt_registrar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_registrar))
        self.bt_actualizar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_actualizar))
        self.bt_eliminar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_eliminar))

        self.tabla_borrar.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_productos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def control_bt_minimizar(self):
        self.showMinimized()

    def control_bt_normal(self):
        self.showNormal()
        self.bt_restaurar.hide()
        self.bt_maximizar.show()

    def control_bt_maximizar(self):
        self.showMaximized()
        self.bt_maximizar.hide()
        self.bt_restaurar.show()

    def resizeEvent(self, event):
        rect =  self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)

    def mousePressEvent(self, event):
        self.click_position = event.globalPos()

    def mover_ventana(self, event):
        if self.isMaximized() == False:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.click_position)
                self.click_position = event.globalPos()
                event.accept()
        if event.globalPos().y() <= 10:
            self.showMaximized()
            self.bt_maximizar.hide()
            self.bt_restaurar.show()
        else:
            self.showNormal()
            self.bt_restaurar.hide()
            self.bt_maximizar.show()

    def mover_menu(self):
        if True:
            width = self.frame_control.width()
            normal = 0
            if width == 0:
                extender = 200
            else:
                extender = normal
            self.animacion = QPropertyAnimation(self.frame_control, b'minimumWidth')
            self.animacion.setDuration(300)
            self.animacion.setStartValue(width)
            self.animacion.setEndValue(extender)
            self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animacion.start()
        # FIN DE INTERCOMUNICACION DEL QT DESIGNER (INTERFAZ) A PYCHARM
    def mostrar_productos(self):
        datos = self.base_de_datos_tecnologias.mostrar_productos()
        i = len(datos)
        print(datos)
        self.tabla_productos.setRowCount(i)
        tablerow = 0
        for row in datos:
            print(row)  # Imprimir la fila para verificar su contenido
            self.tabla_productos.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.tabla_productos.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.tabla_productos.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.tabla_productos.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
            self.tabla_productos.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(row[4]))
            self.tabla_productos.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(row[5]))
            self.tabla_productos.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(row[6]))
            self.tabla_productos.setItem(tablerow, 7, QtWidgets.QTableWidgetItem(str(row[7])))
            self.tabla_productos.setItem(tablerow, 8, QtWidgets.QTableWidgetItem(str(row[8])))
            tablerow += 1
        self.signal_actualizar.setText("")
        self.signal_registrar.setText("")
        self.signal_eliminacion.setText("")

    def registrar_productos(self):
        id = self.reg_id.text().upper()
        #codigo = self.reg_codigo.text().upper() a eliminar
        nombre = self.reg_nombre.text().upper()
        modelo = self.reg_modelo.text().upper()
        proveedor = self.reg_proveedor.text().upper()
        categoria = self.reg_categoria.text().upper()
        sector = self.reg_sector.text().upper()
        fechaing = self.reg_fechaing.text().upper()
        cantidad = self.reg_cantidad.text().upper()
        precio = self.reg_precio.text().upper()
        #print(codigo) a eliminar
        print(nombre)
        print(modelo)
        print(precio)
        print(cantidad)


        if id != '' and nombre != '' and modelo != '' and proveedor != '' and categoria != '' and sector != '' and fechaing != '' and precio != '' and cantidad != '':
            self.base_de_datos_tecnologias.inserta_producto(id,nombre,modelo,proveedor, categoria, sector, fechaing, cantidad,precio)
            print(self.base_de_datos_tecnologias)
            self.signal_registrar.setText('Productos Registrados')
            self.reg_id.clear()
            self.reg_nombre.clear()
            self.reg_modelo.clear()
            self.reg_precio.clear()
            self.reg_cantidad.clear()
            self.reg_proveedor.clear()
            self.reg_categoria.clear()
            self.reg_sector.clear()
            self.reg_fechaing.clear()
        else:
            self.signal_registrar.setText('Hay espacios vacíos')

    def buscar_por_nombre_actualiza(self):
        id_producto = self.act_buscar.text().upper()
        #id_producto = str("'"+ id_producto + "'")
        self.producto = self.base_de_datos_tecnologias.busca_productos(id_producto)
        print(id_producto)
        print(self.producto)
        if len(self.producto) != 0:
            self.act_id.setText(str(self.producto[0][0]))
            #self.act_codigo.setText(self.producto[0][1]) a eliminar el código
            self.act_nombre.setText(self.producto[0][1])
            self.act_modelo.setText(self.producto[0][2])
            self.act_proveedor.setText(self.producto[0][3])
            self.act_categoria.setText(self.producto[0][4])
            self.act_sector.setText(self.producto[0][5])
            self.act_frechaing.setText(self.producto[0][6])
            #self.act_modelo.setText(self.producto[0][2])
            self.act_precio.setText(str(self.producto[0][8]))
            self.act_cantidad.setText(str(self.producto[0][7]))
        else:
            self.signal_actualizar.setText("NO EXISTE EL PRODUCTO")

    def modificar_productos(self):
        if self.producto != '':
            id = self.act_id.text().upper()
            nombre = self.act_nombre.text().upper()
            modelo = self.act_modelo.text().upper()
            proveedor = self.act_proveedor.text().upper()
            categoria = self.act_categoria.text().upper()
            sector = self.act_sector.text().upper()
            fechaing = self.act_frechaing.text().upper()
            cantidad = self.act_cantidad.text().upper()
            precio = self.act_precio.text().upper()
            act = self.base_de_datos_tecnologias.actualiza_productos(id,nombre,modelo,proveedor,categoria,sector, fechaing, cantidad,precio)
            if act == 1:
                self.signal_actualizar.setText("Producto actualizado")
                self.act_id.clear()
                self.act_nombre.clear()
                self.act_modelo.clear()
                self.act_precio.clear()
                self.act_cantidad.clear()
                self.act_frechaing.clear()
                self.act_proveedor.clear()
                self.act_categoria.clear()
                self.act_sector.clear()
                self.act_buscar.setText('') 
            elif act == 0:
                self.signal_actualizar.setText("Error")
            else:   
                self.signal_actualizar.setText("Incorrecto")


    def buscar_por_nombre_eliminar(self):
        nombre_producto = self.eliminar_buscar.text().upper()
        self.productoawa = self.base_de_datos_tecnologias.busca_productos(nombre_producto)
        self.tabla_borrar.setRowCount(len(self.productoawa))
        if len(self.productoawa) != 0:
            self.signal_eliminacion.setText('Producto seleccionado')
        else:
            self.signal_eliminacion.setText('No existe')
        tablerow= 0
        for row in self.productoawa: #cambié tablerow por productoawa
            self.producto_a_borrar = row[0]
            self.tabla_borrar.setItem(tablerow,0,QtWidgets.QTableWidgetItem(str(row[0])))
            self.tabla_borrar.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.tabla_borrar.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.tabla_borrar.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
            self.tabla_borrar.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(row[4]))
            self.tabla_borrar.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(row[5]))
            self.tabla_borrar.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(row[6]))
            self.tabla_borrar.setItem(tablerow, 7, QtWidgets.QTableWidgetItem(str(row[7])))
            self.tabla_borrar.setItem(tablerow, 8, QtWidgets.QTableWidgetItem(str(row[8])))
            #self.tabla_borrar.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(row[5])) a eliminar
            tablerow +=1


    def eliminar_productos(self):
        self.row_flag = self.tabla_borrar.currentRow()
        if self.row_flag == 0:
            self.tabla_borrar.removeRow(0)
            id_producto = int(self.producto_a_borrar)  # Convert to integer
            self.base_de_datos_tecnologias.elimina_producto(id_producto)
            self.signal_eliminacion.setText('Producto Eliminado')
            self.eliminar_buscar.setText('')
        else:
            self.signal_eliminacion.setText('Seleccione')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())

import sqlite3
import pyodbc


class Comunicacion():
    #CONEXIÓN CON SQL SERVER
    def __init__(self):
        self.conexion = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-LEQ5LOGA\SQLEXPRESS;DATABASE=Inventario')
    #CONEXIÓN CON SQL SERVER

    #INGRESAR PRODUCTO
    def inserta_producto(self,id, nombre, modelo,proveedor, categoria, sector, fechaing, cantidad, precio):
        cursor = self.conexion.cursor()
        query = "INSERT INTO Producto (ID_PRODUCTO, NOMB_PRODUCTO, DESC_PRODUCTO, PROVEEDOR  , CATEGORIA , SECTOR , FECHA_INGRESO , STOCK , CU ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        values = (id, nombre, modelo,proveedor, categoria, sector, fechaing, cantidad, precio)
        cursor.execute(query, values)
        self.conexion.commit() #HACER QUERY
        cursor.close()
    # INGRESAR PRODUCTO

    #MOSTRAR TODOS LOS PRODUCTOS
    def mostrar_productos(self):
        cursor = self.conexion.cursor()
        #query = "SELECT * FROM Datos"
        query = "SELECT * FROM Producto"
        cursor.execute(query)
        registros = cursor.fetchall()
        return registros
    # MOSTRAR TODOS LOS PRODUCTOS


    #BUSCAR PRODUCTO
    def busca_productos(self, nombre_producto):
        cursor = self.conexion.cursor()
        query = "SELECT * FROM Producto WHERE ID_PRODUCTO= ?"
        cursor.execute(query, (nombre_producto,))
        nombreX = cursor.fetchall()
        cursor.close()
        return nombreX

    # BUSCAR PRODUCTO

    # ELIMINAR PRODUCTO
    def elimina_producto(self, nombre):
        cursor = self.conexion.cursor()
        query3 = "INSERT INTO [BACKUP] (ID_PRODUCTO, DNI_TRABAJADOR, STOCK, CU) SELECT ID_PRODUCTO, 73050787, STOCK, CU FROM Producto WHERE ID_PRODUCTO = ?"
        query2 = "INSERT INTO Venta (ID_PRODUCTO, STOCK, CU, FECHA_INGRESO, FECHA_SALIDA) SELECT ID_PRODUCTO, STOCK, CU, FECHA_INGRESO, CONVERT(DATE, GETDATE()) FROM Producto WHERE ID_PRODUCTO = ?"
        query = "DELETE FROM Producto WHERE ID_PRODUCTO = ?"

        cursor.execute(query3, (nombre,))
        self.conexion.commit()

        cursor.execute(query2, (nombre,))
        self.conexion.commit()

        cursor.execute(query, (nombre,))
        self.conexion.commit()

        cursor.close()

    # ELIMINAR PRODUCTO


    #ACTUALIZAR PRODUCTO
    def actualiza_productos(self, id, nombre, modelo,proveedor, categoria, sector, fechaing, cantidad, precio):
        cursor = self.conexion.cursor()
        query = "UPDATE Producto SET NOMB_PRODUCTO = ?, DESC_PRODUCTO = ?, PROVEEDOR = ?, CATEGORIA = ?, SECTOR = ?, FECHA_INGRESO = ?, STOCK = ?, CU = ? WHERE ID_PRODUCTO = ?"
        values = (nombre, modelo,proveedor, categoria, sector, fechaing, cantidad, precio, id)
        cursor.execute(query, values)
        affected_rows = cursor.rowcount
        self.conexion.commit()
        cursor.close()
        return affected_rows
    # ACTUALIZAR PRODUCTO


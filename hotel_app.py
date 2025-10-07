#!/usr/bin/env python3
"""
hotel_app.py
Ejemplo OOP + SQLite para el modelo entidad-relación del hotel:
Huesped, Empleado, Habitacion, ServicioAdicional, Reserva, Factura,
y tabla intermedia reserva_servicio (many-to-many).
"""

import sqlite3
from datetime import date, datetime
from decimal import Decimal

# -------------------------
# Helper: conexión y tablas
# -------------------------
class Database:
    def __init__(self, path='hotel.db'):
        # detect_types no obligatorio aquí; usamos strings ISO para fechas
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        # activar claves foráneas en SQLite
        self.conn.execute("PRAGMA foreign_keys = ON;")

    def create_tables(self):
        sqls = [
            # Huesped
            """
            CREATE TABLE IF NOT EXISTS huesped (
                id_huesped INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                documento TEXT,
                fecha_nacimiento TEXT,
                nacionalidad TEXT,
                direccion TEXT
            );
            """,
            # Empleado
            """
            CREATE TABLE IF NOT EXISTS empleado (
                id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                cargo TEXT,
                area TEXT
            );
            """,
            # Habitacion
            """
            CREATE TABLE IF NOT EXISTS habitacion (
                id_habitacion INTEGER PRIMARY KEY AUTOINCREMENT,
                numero INTEGER NOT NULL UNIQUE,
                tipo TEXT,
                precio REAL,
                estado TEXT
            );
            """,
            # Servicio adicional
            """
            CREATE TABLE IF NOT EXISTS servicio_adicional (
                id_servicio INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_servicio TEXT,
                descripcion TEXT,
                costo REAL
            );
            """,
            # Reserva
            """
            CREATE TABLE IF NOT EXISTS reserva (
                id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_ingreso TEXT,
                fecha_salida TEXT,
                estado TEXT,
                id_huesped INTEGER,
                id_habitacion INTEGER,
                id_empleado INTEGER,
                FOREIGN KEY(id_huesped) REFERENCES huesped(id_huesped),
                FOREIGN KEY(id_habitacion) REFERENCES habitacion(id_habitacion),
                FOREIGN KEY(id_empleado) REFERENCES empleado(id_empleado)
            );
            """,
            # Tabla intermedia Reserva-Servicio (many-to-many)
            """
            CREATE TABLE IF NOT EXISTS reserva_servicio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_reserva INTEGER,
                id_servicio INTEGER,
                cantidad INTEGER DEFAULT 1,
                FOREIGN KEY(id_reserva) REFERENCES reserva(id_reserva) ON DELETE CASCADE,
                FOREIGN KEY(id_servicio) REFERENCES servicio_adicional(id_servicio)
            );
            """,
            # Factura
            """
            CREATE TABLE IF NOT EXISTS factura (
                id_factura INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_emision TEXT,
                monto_total REAL,
                id_reserva INTEGER,
                FOREIGN KEY(id_reserva) REFERENCES reserva(id_reserva)
            );
            """
        ]
        cur = self.conn.cursor()
        for s in sqls:
            cur.execute(s)
        self.conn.commit()

    def close(self):
        self.conn.close()


# -------------------------
# Modelos OOP (mínimos CRUD)
# -------------------------
class Huesped:
    def __init__(self, nombre, documento=None, fecha_nacimiento=None, nacionalidad=None, direccion=None, id_huesped=None):
        self.id = id_huesped
        self.nombre = nombre
        self.documento = documento
        self.fecha_nacimiento = fecha_nacimiento  # 'YYYY-MM-DD' or None
        self.nacionalidad = nacionalidad
        self.direccion = direccion

    def save(self, db: Database):
        if self.id is None:
            cur = db.conn.execute(
                "INSERT INTO huesped (nombre, documento, fecha_nacimiento, nacionalidad, direccion) VALUES (?,?,?,?,?)",
                (self.nombre, self.documento, self.fecha_nacimiento, self.nacionalidad, self.direccion)
            )
            db.conn.commit()
            self.id = cur.lastrowid
        else:
            db.conn.execute(
                "UPDATE huesped SET nombre=?, documento=?, fecha_nacimiento=?, nacionalidad=?, direccion=? WHERE id_huesped=?",
                (self.nombre, self.documento, self.fecha_nacimiento, self.nacionalidad, self.direccion, self.id)
            )
            db.conn.commit()
        return self.id

    @staticmethod
    def get(db: Database, id_huesped):
        row = db.conn.execute("SELECT * FROM huesped WHERE id_huesped = ?", (id_huesped,)).fetchone()
        if not row:
            return None
        return Huesped(row['nombre'], row['documento'], row['fecha_nacimiento'], row['nacionalidad'], row['direccion'], row['id_huesped'])

    def __repr__(self):
        return f"<Huesped id={self.id} nombre={self.nombre}>"


class Empleado:
    def __init__(self, nombre, cargo=None, area=None, id_empleado=None):
        self.id = id_empleado
        self.nombre = nombre
        self.cargo = cargo
        self.area = area

    def save(self, db: Database):
        if self.id is None:
            cur = db.conn.execute(
                "INSERT INTO empleado (nombre, cargo, area) VALUES (?,?,?)",
                (self.nombre, self.cargo, self.area)
            )
            db.conn.commit()
            self.id = cur.lastrowid
        else:
            db.conn.execute(
                "UPDATE empleado SET nombre=?, cargo=?, area=? WHERE id_empleado=?",
                (self.nombre, self.cargo, self.area, self.id)
            )
            db.conn.commit()
        return self.id

    @staticmethod
    def get(db: Database, id_empleado):
        row = db.conn.execute("SELECT * FROM empleado WHERE id_empleado = ?", (id_empleado,)).fetchone()
        if not row:
            return None
        return Empleado(row['nombre'], row['cargo'], row['area'], row['id_empleado'])

    def __repr__(self):
        return f"<Empleado id={self.id} nombre={self.nombre}>"


class Habitacion:
    def __init__(self, numero, tipo=None, precio=0.0, estado='disponible', id_habitacion=None):
        self.id = id_habitacion
        self.numero = numero
        self.tipo = tipo
        self.precio = float(precio)
        self.estado = estado

    def save(self, db: Database):
        if self.id is None:
            cur = db.conn.execute(
                "INSERT INTO habitacion (numero, tipo, precio, estado) VALUES (?,?,?,?)",
                (self.numero, self.tipo, self.precio, self.estado)
            )
            db.conn.commit()
            self.id = cur.lastrowid
        else:
            db.conn.execute(
                "UPDATE habitacion SET numero=?, tipo=?, precio=?, estado=? WHERE id_habitacion=?",
                (self.numero, self.tipo, self.precio, self.estado, self.id)
            )
            db.conn.commit()
        return self.id

    @staticmethod
    def get(db: Database, id_habitacion):
        row = db.conn.execute("SELECT * FROM habitacion WHERE id_habitacion = ?", (id_habitacion,)).fetchone()
        if not row:
            return None
        return Habitacion(row['numero'], row['tipo'], row['precio'], row['estado'], row['id_habitacion'])

    def __repr__(self):
        return f"<Habitacion id={self.id} numero={self.numero} precio={self.precio}>"


class ServicioAdicional:
    def __init__(self, nombre_servicio, descripcion=None, costo=0.0, id_servicio=None):
        self.id = id_servicio
        self.nombre_servicio = nombre_servicio
        self.descripcion = descripcion
        self.costo = float(costo)

    def save(self, db: Database):
        if self.id is None:
            cur = db.conn.execute(
                "INSERT INTO servicio_adicional (nombre_servicio, descripcion, costo) VALUES (?,?,?)",
                (self.nombre_servicio, self.descripcion, self.costo)
            )
            db.conn.commit()
            self.id = cur.lastrowid
        else:
            db.conn.execute(
                "UPDATE servicio_adicional SET nombre_servicio=?, descripcion=?, costo=? WHERE id_servicio=?",
                (self.nombre_servicio, self.descripcion, self.costo, self.id)
            )
            db.conn.commit()
        return self.id

    @staticmethod
    def get(db: Database, id_servicio):
        row = db.conn.execute("SELECT * FROM servicio_adicional WHERE id_servicio = ?", (id_servicio,)).fetchone()
        if not row:
            return None
        return ServicioAdicional(row['nombre_servicio'], row['descripcion'], row['costo'], row['id_servicio'])

    def __repr__(self):
        return f"<Servicio id={self.id} nombre={self.nombre_servicio} costo={self.costo}>"


class Reserva:
    def __init__(self, fecha_ingreso, fecha_salida, estado, id_huesped, id_habitacion, id_empleado=None, id_reserva=None):
        self.id = id_reserva
        # aceptar date o string 'YYYY-MM-DD' -> normalizamos a 'YYYY-MM-DD'
        self.fecha_ingreso = fecha_ingreso if isinstance(fecha_ingreso, str) else fecha_ingreso.isoformat()
        self.fecha_salida = fecha_salida if isinstance(fecha_salida, str) else fecha_salida.isoformat()
        self.estado = estado
        self.id_huesped = id_huesped
        self.id_habitacion = id_habitacion
        self.id_empleado = id_empleado

    def save(self, db: Database):
        if self.id is None:
            cur = db.conn.execute(
                "INSERT INTO reserva (fecha_ingreso, fecha_salida, estado, id_huesped, id_habitacion, id_empleado) VALUES (?,?,?,?,?,?)",
                (self.fecha_ingreso, self.fecha_salida, self.estado, self.id_huesped, self.id_habitacion, self.id_empleado)
            )
            db.conn.commit()
            self.id = cur.lastrowid
        else:
            db.conn.execute(
                "UPDATE reserva SET fecha_ingreso=?, fecha_salida=?, estado=?, id_huesped=?, id_habitacion=?, id_empleado=? WHERE id_reserva=?",
                (self.fecha_ingreso, self.fecha_salida, self.estado, self.id_huesped, self.id_habitacion, self.id_empleado, self.id)
            )
            db.conn.commit()
        return self.id

    def add_service(self, db: Database, id_servicio, cantidad=1):
        if self.id is None:
            raise ValueError("Guarda la reserva antes de asignar servicios.")
        db.conn.execute(
            "INSERT INTO reserva_servicio (id_reserva, id_servicio, cantidad) VALUES (?,?,?)",
            (self.id, id_servicio, cantidad)
        )
        db.conn.commit()

    def services(self, db: Database):
        q = """
        SELECT rs.cantidad, s.id_servicio, s.nombre_servicio, s.descripcion, s.costo
        FROM reserva_servicio rs
        JOIN servicio_adicional s ON rs.id_servicio = s.id_servicio
        WHERE rs.id_reserva = ?
        """
        rows = db.conn.execute(q, (self.id,)).fetchall()
        return [dict(row) for row in rows]

    def nights(self):
        d1 = datetime.fromisoformat(self.fecha_ingreso).date()
        d2 = datetime.fromisoformat(self.fecha_salida).date()
        ndays = (d2 - d1).days
        return max(0, ndays)

    def calculate_total(self, db: Database):
        # precio habitación
        row = db.conn.execute("SELECT precio FROM habitacion WHERE id_habitacion = ?", (self.id_habitacion,)).fetchone()
        if not row:
            raise ValueError("Habitación no encontrada")
        precio = Decimal(str(row['precio'] or 0.0))
        noches = Decimal(str(self.nights()))
        total_habitacion = precio * noches

        # servicios
        servicio_rows = db.conn.execute("""
            SELECT s.costo, rs.cantidad
            FROM reserva_servicio rs
            JOIN servicio_adicional s ON rs.id_servicio = s.id_servicio
            WHERE rs.id_reserva = ?
        """, (self.id,)).fetchall()

        total_servicios = Decimal('0.0')
        for r in servicio_rows:
            costo = Decimal(str(r['costo'] or 0.0))
            cantidad = Decimal(str(r['cantidad'] or 1))
            total_servicios += costo * cantidad

        total = total_habitacion + total_servicios
        return float(total)  # devolvemos float para insertar en BD; para mostrar usar Decimal si quieres

    def generate_invoice(self, db: Database):
        if self.id is None:
            raise ValueError("Reserva no registrada")
        monto = self.calculate_total(db)
        fecha_emision = date.today().isoformat()
        cur = db.conn.execute(
            "INSERT INTO factura (fecha_emision, monto_total, id_reserva) VALUES (?,?,?)",
            (fecha_emision, monto, self.id)
        )
        db.conn.commit()
        return cur.lastrowid

    @staticmethod
    def get(db: Database, id_reserva):
        row = db.conn.execute("SELECT * FROM reserva WHERE id_reserva = ?", (id_reserva,)).fetchone()
        if not row:
            return None
        return Reserva(row['fecha_ingreso'], row['fecha_salida'], row['estado'], row['id_huesped'], row['id_habitacion'], row['id_empleado'], row['id_reserva'])

    def __repr__(self):
        return f"<Reserva id={self.id} huesped={self.id_huesped} habitacion={self.id_habitacion} {self.fecha_ingreso}->{self.fecha_salida}>"




def menu():
    db = Database("hotel.db")
    db.create_tables()
    print("=== SISTEMA DE GESTIÓN HOTELERA ===")

    while True:
        print("""
        ----- MENÚ PRINCIPAL -----
        1. Gestionar Huéspedes
        2. Gestionar Empleados
        3. Gestionar Habitaciones
        4. Gestionar Servicios Adicionales
        5. Gestionar Reservas
        6. Generar Factura
        0. Salir
        """)
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_huesped(db)
        elif opcion == "2":
            menu_empleado(db)
        elif opcion == "3":
            menu_habitacion(db)
        elif opcion == "4":
            menu_servicio(db)
        elif opcion == "5":
            menu_reserva(db)
        elif opcion == "6":
            menu_factura(db)
        elif opcion == "0":
            print("Saliendo del sistema...")
            db.close()
            break
        else:
            print("Opción no válida. Intente de nuevo.")


# -------------------------------
# Submenús de cada entidad
# -------------------------------
def menu_huesped(db):
    while True:
        print("""
        --- Gestión de Huéspedes ---
        1. Agregar huésped
        2. Ver huéspedes
        0. Volver
        """)
        op = input("Elija una opción: ")

        if op == "1":
            nombre = input("Nombre completo: ")
            documento = input("Documento: ")
            fecha_nacimiento = input("Fecha nacimiento (YYYY-MM-DD): ")
            nacionalidad = input("Nacionalidad: ")
            direccion = input("Dirección: ")
            h = Huesped(nombre, documento, fecha_nacimiento, nacionalidad, direccion)
            h.save(db)
            print("✅ Huésped agregado con ID:", h.id)
        elif op == "2":
            rows = db.conn.execute("SELECT * FROM huesped").fetchall()
            for r in rows:
                print(dict(r))
        elif op == "0":
            break


def menu_empleado(db):
    while True:
        print("""
        --- Gestión de Empleados ---
        1. Agregar empleado
        2. Ver empleados
        0. Volver
        """)
        op = input("Elija una opción: ")

        if op == "1":
            nombre = input("Nombre: ")
            cargo = input("Cargo: ")
            area = input("Área: ")
            e = Empleado(nombre, cargo, area)
            e.save(db)
            print("✅ Empleado agregado con ID:", e.id)
        elif op == "2":
            rows = db.conn.execute("SELECT * FROM empleado").fetchall()
            for r in rows:
                print(dict(r))
        elif op == "0":
            break


def menu_habitacion(db):
    while True:
        print("""
        --- Gestión de Habitaciones ---
        1. Agregar habitación
        2. Ver habitaciones
        0. Volver
        """)
        op = input("Elija una opción: ")

        if op == "1":
            numero = int(input("Número: "))
            tipo = input("Tipo (simple, doble, suite): ")
            precio = float(input("Precio por noche: "))
            estado = input("Estado (disponible/ocupada): ")
            hab = Habitacion(numero, tipo, precio, estado)
            hab.save(db)
            print("✅ Habitación agregada con ID:", hab.id)
        elif op == "2":
            rows = db.conn.execute("SELECT * FROM habitacion").fetchall()
            for r in rows:
                print(dict(r))
        elif op == "0":
            break


def menu_servicio(db):
    while True:
        print("""
        --- Gestión de Servicios ---
        1. Agregar servicio adicional
        2. Ver servicios
        0. Volver
        """)
        op = input("Elija una opción: ")

        if op == "1":
            nombre = input("Nombre del servicio: ")
            descripcion = input("Descripción: ")
            costo = float(input("Costo: "))
            s = ServicioAdicional(nombre, descripcion, costo)
            s.save(db)
            print("✅ Servicio agregado con ID:", s.id)
        elif op == "2":
            rows = db.conn.execute("SELECT * FROM servicio_adicional").fetchall()
            for r in rows:
                print(dict(r))
        elif op == "0":
            break


def menu_reserva(db):
    while True:
        print("""
        --- Gestión de Reservas ---
        1. Crear reserva
        2. Asignar servicio a reserva
        3. Ver reservas
        0. Volver
        """)
        op = input("Elija una opción: ")

        if op == "1":
            id_huesped = int(input("ID del huésped: "))
            id_habitacion = int(input("ID de la habitación: "))
            id_empleado = int(input("ID del empleado que gestiona: "))
            fecha_ingreso = input("Fecha ingreso (YYYY-MM-DD): ")
            fecha_salida = input("Fecha salida (YYYY-MM-DD): ")
            estado = "confirmada"
            r = Reserva(fecha_ingreso, fecha_salida, estado, id_huesped, id_habitacion, id_empleado)
            r.save(db)
            print("✅ Reserva creada con ID:", r.id)
        elif op == "2":
            id_reserva = int(input("ID de la reserva: "))
            id_servicio = int(input("ID del servicio: "))
            cantidad = int(input("Cantidad: "))
            r = Reserva.get(db, id_reserva)
            if r:
                r.add_service(db, id_servicio, cantidad)
                print("✅ Servicio agregado a la reserva.")
            else:
                print("❌ Reserva no encontrada.")
        elif op == "3":
            rows = db.conn.execute("SELECT * FROM reserva").fetchall()
            for r in rows:
                print(dict(r))
        elif op == "0":
            break


def menu_factura(db):
    while True:
        print("""
        --- Generación de Facturas ---
        1. Generar factura de reserva
        2. Ver facturas
        0. Volver
        """)
        op = input("Elija una opción: ")

        if op == "1":
            id_reserva = int(input("ID de la reserva: "))
            r = Reserva.get(db, id_reserva)
            if r:
                factura_id = r.generate_invoice(db)
                print(f"✅ Factura generada con ID: {factura_id}")
            else:
                print("❌ Reserva no encontrada.")
        elif op == "2":
            rows = db.conn.execute("SELECT * FROM factura").fetchall()
            for r in rows:
                print(dict(r))
        elif op == "0":
            break


# -------------------------------
# Iniciar programa
# -------------------------------
if __name__ == "__main__":
    menu()

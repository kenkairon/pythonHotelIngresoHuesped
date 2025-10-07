```python
# -------------------------
# Ejemplo / flujo
# -------------------------
def ejemplo_flujo():
    db = Database(':memory:')  # usa ':memory:' para ejemplo en RAM; cambia a 'hotel.db' para persistencia
    db.create_tables()

    # 1) crear huésped
    h = Huesped("Juan Perez", "12345678", "1990-05-10", "Argentina", "Calle Falsa 123")
    h.save(db)
    print("Huésped creado:", h)

    # 2) crear empleado
    e = Empleado("María Gomez", "Recepcionista", "Recepción")
    e.save(db)
    print("Empleado creado:", e)

    # 3) crear habitación
    hab = Habitacion(numero=101, tipo="Doble", precio=50.0, estado="disponible")
    hab.save(db)
    print("Habitación creada:", hab)

    # 4) crear servicios
    s1 = ServicioAdicional("Desayuno", "Buffet diario", 8.5)
    s1.save(db)
    s2 = ServicioAdicional("Lavandería", "Lavado por prenda", 3.0)
    s2.save(db)
    print("Servicios creados:", s1, s2)

    # 5) crear reserva
    reserva = Reserva("2025-10-10", "2025-10-13", "confirmada", h.id, hab.id, e.id)
    reserva.save(db)
    print("Reserva creada:", reserva)

    # 6) asignar servicios a la reserva
    reserva.add_service(db, s1.id, cantidad=3)  # 3 desayunos
    reserva.add_service(db, s2.id, cantidad=2)  # 2 prendas lavandería
    print("Servicios asignados a la reserva:", reserva.services(db))

    # 7) calcular total y generar factura
    total = reserva.calculate_total(db)
    print(f"Total reserva (habitación + servicios): {total:.2f}")

    id_factura = reserva.generate_invoice(db)
    print("Factura generada con id:", id_factura)
    factura_row = db.conn.execute("SELECT * FROM factura WHERE id_factura = ?", (id_factura,)).fetchone()
    print(dict(factura_row))
```
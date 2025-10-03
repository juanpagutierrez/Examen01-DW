class Prestamo:
    def __init__(self, id, libro_id, usuario, fecha):
        self.id = id
        self.libro_id = libro_id
        self.usuario = usuario
        self.fecha = fecha
        self.devuelto = False
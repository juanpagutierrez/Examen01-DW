# ejercicio02.py
from datetime import datetime
from typing import List, Optional
from libro import Libro
from prestamo import Prestamo


class ValidadorBiblioteca:
    """Clase dedicada exclusivamente a la validación de datos"""
    
    @staticmethod
    def validar_libro(titulo: str, autor: str, isbn: str) -> List[str]:
        """Valida los datos de un libro y retorna lista de errores"""
        errores = []
        
        if not titulo or len(titulo.strip()) < 2:
            errores.append("Error: Título inválido - debe tener al menos 2 caracteres")
        
        if not autor or len(autor.strip()) < 3:
            errores.append("Error: Autor inválido - debe tener al menos 3 caracteres")
        
        if not isbn or len(isbn.strip()) < 10:
            errores.append("Error: ISBN inválido - debe tener al menos 10 caracteres")
        
        return errores
    
    @staticmethod
    def validar_usuario(usuario: str) -> List[str]:
        """Valida el nombre de usuario"""
        errores = []
        
        if not usuario or len(usuario.strip()) < 3:
            errores.append("Error: Nombre de usuario inválido - debe tener al menos 3 caracteres")
        
        return errores
    
    @staticmethod
    def validar_prestamo_existente(prestamo: Optional[Prestamo]) -> List[str]:
        """Valida si un préstamo existe y no está devuelto"""
        errores = []
        
        if not prestamo:
            errores.append("Error: Préstamo no encontrado")
        elif prestamo.devuelto:
            errores.append("Error: Libro ya devuelto")
        
        return errores
    
    @staticmethod
    def validar_libro_disponible(libro: Optional[Libro]) -> List[str]:
        """Valida si un libro existe y está disponible"""
        errores = []
        
        if not libro:
            errores.append("Error: Libro no encontrado")
        elif libro and not libro.disponible:
            errores.append("Error: Libro no disponible")
        
        return errores


class RepositorioBiblioteca:
    """Clase dedicada exclusivamente a la persistencia de datos"""
    
    def __init__(self, archivo: str = "biblioteca.txt"):
        self.archivo = archivo
        self.libros: List[Libro] = []
        self.prestamos: List[Prestamo] = []
        self.contador_libro = 1
        self.contador_prestamo = 1
    
    # Operaciones de Libros
    def agregar_libro(self, libro: Libro) -> Libro:
        """Agrega un libro al repositorio"""
        libro.id = self.contador_libro
        self.libros.append(libro)
        self.contador_libro += 1
        self._guardar_en_archivo()
        return libro
    
    def obtener_libro_por_id(self, libro_id: int) -> Optional[Libro]:
        """Busca un libro por su ID"""
        for libro in self.libros:
            if libro.id == libro_id:
                return libro
        return None
    
    def obtener_todos_libros(self) -> List[Libro]:
        """Retorna todos los libros"""
        return self.libros.copy()
    
    def obtener_libros_disponibles(self) -> List[Libro]:
        """Retorna solo los libros disponibles"""
        return [libro for libro in self.libros if libro.disponible]
    
    def actualizar_libro(self, libro: Libro) -> None:
        """Actualiza el estado de un libro"""
        for i, l in enumerate(self.libros):
            if l.id == libro.id:
                self.libros[i] = libro
                break
        self._guardar_en_archivo()
    
    # Operaciones de Préstamos
    def agregar_prestamo(self, prestamo: Prestamo) -> Prestamo:
        """Agrega un préstamo al repositorio"""
        prestamo.id = self.contador_prestamo
        self.prestamos.append(prestamo)
        self.contador_prestamo += 1
        self._guardar_en_archivo()
        return prestamo
    
    def obtener_prestamo_por_id(self, prestamo_id: int) -> Optional[Prestamo]:
        """Busca un préstamo por su ID"""
        for prestamo in self.prestamos:
            if prestamo.id == prestamo_id:
                return prestamo
        return None
    
    def obtener_prestamos_activos(self) -> List[Prestamo]:
        """Retorna los préstamos activos"""
        return [p for p in self.prestamos if not p.devuelto]
    
    def actualizar_prestamo(self, prestamo: Prestamo) -> None:
        """Actualiza el estado de un préstamo"""
        for i, p in enumerate(self.prestamos):
            if p.id == prestamo.id:
                self.prestamos[i] = prestamo
                break
        self._guardar_en_archivo()
    
    # Persistencia en archivo
    def _guardar_en_archivo(self):
        """Guarda el estado actual en archivo (versión simplificada)"""
        with open(self.archivo, 'w') as f:
            f.write(f"Libros: {len(self.libros)}\n")
            f.write(f"Préstamos: {len(self.prestamos)}\n")
    
    def cargar_desde_archivo(self) -> bool:
        """Carga datos desde archivo (versión simplificada)"""
        try:
            with open(self.archivo, 'r') as f:
                data = f.read()
            return True
        except:
            return False


class ServicioNotificaciones:
    """Clase dedicada exclusivamente al envío de notificaciones"""
    
    @staticmethod
    def enviar_notificacion_prestamo(usuario: str, titulo_libro: str):
        """Envía notificación cuando se realiza un préstamo"""
        print(f"[NOTIFICACIÓN] {usuario}: Préstamo de '{titulo_libro}' realizado exitosamente")
    
    @staticmethod
    def enviar_notificacion_devolucion(usuario: str, titulo_libro: str):
        """Envía notificación cuando se devuelve un libro"""
        print(f"[NOTIFICACIÓN] {usuario}: Devolución de '{titulo_libro}' realizada exitosamente")
    
    @staticmethod
    def enviar_recordatorio_prestamo(usuario: str, titulo_libro: str, dias_retraso: int):
        """Envía recordatorio de préstamo vencido"""
        print(f"[RECORDATORIO] {usuario}: El libro '{titulo_libro}' tiene {dias_retraso} días de retraso")


class SistemaBibliotecaRefactorizado:
    """
    Clase refactorizada que delega responsabilidades específicas
    Ahora se enfoca solo en la lógica de negocio principal
    """
    
    def __init__(self):
        self.validador = ValidadorBiblioteca()
        self.repositorio = RepositorioBiblioteca()
        self.notificador = ServicioNotificaciones()
    
    # Operaciones de Libros
    def agregar_libro(self, titulo: str, autor: str, isbn: str) -> str:
        """Agrega un libro validando datos y delegando persistencia"""
        # Validación
        errores = self.validador.validar_libro(titulo, autor, isbn)
        if errores:
            return "\n".join(errores)
        
        # Lógica de negocio
        libro = Libro(None, titulo, autor, isbn, True)
        libro_guardado = self.repositorio.agregar_libro(libro)
        
        return f"Libro '{titulo}' agregado exitosamente (ID: {libro_guardado.id})"
    
    def buscar_libro(self, criterio: str, valor: str) -> List[Libro]:
        """
        Busca libros por criterio (manteniendo compatibilidad con ejercicio anterior)
        En una implementación real, esto usaría las estrategias del Ejercicio 1
        """
        libros = self.repositorio.obtener_todos_libros()
        resultados = []
        
        if criterio == "titulo":
            for libro in libros:
                if valor.lower() in libro.titulo.lower():
                    resultados.append(libro)
        
        elif criterio == "autor":
            for libro in libros:
                if valor.lower() in libro.autor.lower():
                    resultados.append(libro)
        
        elif criterio == "isbn":
            for libro in libros:
                if libro.isbn == valor:
                    resultados.append(libro)
        
        elif criterio == "disponible":
            disponible = valor.lower() == "true"
            for libro in libros:
                if libro.disponible == disponible:
                    resultados.append(libro)
        
        return resultados
    
    # Operaciones de Préstamos
    def realizar_prestamo(self, libro_id: int, usuario: str) -> str:
        """Realiza un préstamo validando y delegando responsabilidades"""
        # Validaciones
        errores_usuario = self.validador.validar_usuario(usuario)
        if errores_usuario:
            return "\n".join(errores_usuario)
        
        libro = self.repositorio.obtener_libro_por_id(libro_id)
        errores_libro = self.validador.validar_libro_disponible(libro)
        if errores_libro:
            return "\n".join(errores_libro)
        
        # Lógica de negocio
        prestamo = Prestamo(
            id=None,
            libro_id=libro_id,
            usuario=usuario,
            fecha=datetime.now().strftime("%Y-%m-%d")
        )
        
        prestamo_guardado = self.repositorio.agregar_prestamo(prestamo)
        libro.disponible = False
        self.repositorio.actualizar_libro(libro)
        
        # Notificación
        self.notificador.enviar_notificacion_prestamo(usuario, libro.titulo)
        
        return f"Préstamo realizado a {usuario} (ID Préstamo: {prestamo_guardado.id})"
    
    def devolver_libro(self, prestamo_id: int) -> str:
        """Devuelve un libro validando y delegando responsabilidades"""
        prestamo = self.repositorio.obtener_prestamo_por_id(prestamo_id)
        
        errores = self.validador.validar_prestamo_existente(prestamo)
        if errores:
            return "\n".join(errores)
        
        # Lógica de negocio
        libro = self.repositorio.obtener_libro_por_id(prestamo.libro_id)
        if libro:
            libro.disponible = True
            self.repositorio.actualizar_libro(libro)
        
        prestamo.devuelto = True
        self.repositorio.actualizar_prestamo(prestamo)
        
        # Notificación
        if libro:
            self.notificador.enviar_notificacion_devolucion(prestamo.usuario, libro.titulo)
        
        return "Libro devuelto exitosamente"
    
    # Métodos de consulta (delegados al repositorio)
    def obtener_todos_libros(self) -> List[Libro]:
        return self.repositorio.obtener_todos_libros()
    
    def obtener_libros_disponibles(self) -> List[Libro]:
        return self.repositorio.obtener_libros_disponibles()
    
    def obtener_prestamos_activos(self) -> List[Prestamo]:
        return self.repositorio.obtener_prestamos_activos()


# Función main actualizada para demostrar el funcionamiento
def main():
    """Función principal que demuestra el funcionamiento del sistema refactorizado"""
    
    print("=== EJERCICIO 2: SINGLE RESPONSIBILITY PRINCIPLE ===\n")
    
    sistema = SistemaBibliotecaRefactorizado()
    
    print("=== AGREGANDO LIBROS ===")
    print(sistema.agregar_libro("Cien Años de Soledad", "Gabriel García Márquez", "9780060883287"))
    print(sistema.agregar_libro("El Principito", "Antoine de Saint-Exupéry", "9780156012195"))
    print(sistema.agregar_libro("1984", "George Orwell", "9780451524935"))
    
    # Prueba de validación
    print("\n=== PRUEBA DE VALIDACIÓN ===")
    print("Intentando agregar libro inválido:")
    print(sistema.agregar_libro("A", "B", "123"))
    
    print("\n=== BÚSQUEDA POR AUTOR ===")
    resultados = sistema.buscar_libro("autor", "Garcia")
    for libro in resultados:
        print(f"- {libro.titulo} por {libro.autor}")
    
    print("\n=== REALIZAR PRÉSTAMO ===")
    print(sistema.realizar_prestamo(1, "Juan Pérez"))
    
    # Prueba de validación de usuario
    print("\n=== PRUEBA VALIDACIÓN USUARIO ===")
    print("Intentando préstamo con usuario inválido:")
    print(sistema.realizar_prestamo(2, "Jo"))
    
    print("\n=== LIBROS DISPONIBLES ===")
    disponibles = sistema.obtener_libros_disponibles()
    for libro in disponibles:
        print(f"- {libro.titulo}")
    
    print("\n=== DEVOLVER LIBRO ===")
    print(sistema.devolver_libro(1))
    
    print("\n=== PRÉSTAMOS ACTIVOS ===")
    activos = sistema.obtener_prestamos_activos()
    print(f"Total de préstamos activos: {len(activos)}")
    
    print("\n=== ESTADO FINAL DEL SISTEMA ===")
    print(f"Total libros: {len(sistema.obtener_todos_libros())}")
    print(f"Libros disponibles: {len(sistema.obtener_libros_disponibles())}")
    print(f"Préstamos activos: {len(sistema.obtener_prestamos_activos())}")


if __name__ == "__main__":
    main()

'''
Esto es lo que te tiene que dar

=== AGREGANDO LIBROS ===
Libro 'Cien Años de Soledad' agregado exitosamente (ID: 1)
Libro 'El Principito' agregado exitosamente (ID: 2)
Libro '1984' agregado exitosamente (ID: 3)

=== PRUEBA DE VALIDACIÓN ===
Intentando agregar libro inválido:
Error: Título inválido - debe tener al menos 2 caracteres
Error: Autor inválido - debe tener al menos 3 caracteres
Error: ISBN inválido - debe tener al menos 10 caracteres

=== BÚSQUEDA POR AUTOR ===
- Cien Años de Soledad por Gabriel García Márquez

=== REALIZAR PRÉSTAMO ===
[NOTIFICACIÓN] Juan Pérez: Préstamo de 'Cien Años de Soledad' realizado exitosamente
Préstamo realizado a Juan Pérez (ID Préstamo: 1)

=== PRUEBA VALIDACIÓN USUARIO ===
Intentando préstamo con usuario inválido:
Error: Nombre de usuario inválido - debe tener al menos 3 caracteres

=== LIBROS DISPONIBLES ===
- El Principito
- 1984

=== DEVOLVER LIBRO ===
[NOTIFICACIÓN] Juan Pérez: Devolución de 'Cien Años de Soledad' realizada exitosamente
Libro devuelto exitosamente

=== PRÉSTAMOS ACTIVOS ===
Total de préstamos activos: 0

=== ESTADO FINAL DEL SISTEMA ===
Total libros: 3
Libros disponibles: 3
Préstamos activos: 0
'''
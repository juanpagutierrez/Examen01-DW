from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from libro import Libro
from prestamo import Prestamo


# 1. Interfaz para el repositorio (clase abstracta)
class IRepositorioBiblioteca(ABC):
    """Interfaz abstracta que define el contrato para todos los repositorios"""
    
    @abstractmethod
    def agregar_libro(self, libro: Libro) -> Libro:
        pass
    
    @abstractmethod
    def obtener_libro_por_id(self, libro_id: int) -> Optional[Libro]:
        pass
    
    @abstractmethod
    def obtener_todos_libros(self) -> List[Libro]:
        pass
    
    @abstractmethod
    def obtener_libros_disponibles(self) -> List[Libro]:
        pass
    
    @abstractmethod
    def actualizar_libro(self, libro: Libro) -> None:
        pass
    
    @abstractmethod
    def agregar_prestamo(self, prestamo: Prestamo) -> Prestamo:
        pass
    
    @abstractmethod
    def obtener_prestamo_por_id(self, prestamo_id: int) -> Optional[Prestamo]:
        pass
    
    @abstractmethod
    def obtener_prestamos_activos(self) -> List[Prestamo]:
        pass
    
    @abstractmethod
    def actualizar_prestamo(self, prestamo: Prestamo) -> None:
        pass


# 2. Implementación concreta: RepositorioArchivo
class RepositorioArchivo(IRepositorioBiblioteca):
    """Implementación que persiste datos en archivo"""
    
    def __init__(self, archivo: str = "biblioteca.txt"):
        self.archivo = archivo
        self.libros: List[Libro] = []
        self.prestamos: List[Prestamo] = []
        self.contador_libro = 1
        self.contador_prestamo = 1
        self._cargar_desde_archivo()
    
    def agregar_libro(self, libro: Libro) -> Libro:
        libro.id = self.contador_libro
        self.libros.append(libro)
        self.contador_libro += 1
        self._guardar_en_archivo()
        return libro
    
    def obtener_libro_por_id(self, libro_id: int) -> Optional[Libro]:
        for libro in self.libros:
            if libro.id == libro_id:
                return libro
        return None
    
    def obtener_todos_libros(self) -> List[Libro]:
        return self.libros.copy()
    
    def obtener_libros_disponibles(self) -> List[Libro]:
        return [libro for libro in self.libros if libro.disponible]
    
    def actualizar_libro(self, libro: Libro) -> None:
        for i, l in enumerate(self.libros):
            if l.id == libro.id:
                self.libros[i] = libro
                break
        self._guardar_en_archivo()
    
    def agregar_prestamo(self, prestamo: Prestamo) -> Prestamo:
        prestamo.id = self.contador_prestamo
        self.prestamos.append(prestamo)
        self.contador_prestamo += 1
        self._guardar_en_archivo()
        return prestamo
    
    def obtener_prestamo_por_id(self, prestamo_id: int) -> Optional[Prestamo]:
        for prestamo in self.prestamos:
            if prestamo.id == prestamo_id:
                return prestamo
        return None
    
    def obtener_prestamos_activos(self) -> List[Prestamo]:
        return [p for p in self.prestamos if not p.devuelto]
    
    def actualizar_prestamo(self, prestamo: Prestamo) -> None:
        for i, p in enumerate(self.prestamos):
            if p.id == prestamo.id:
                self.prestamos[i] = prestamo
                break
        self._guardar_en_archivo()
    
    def _guardar_en_archivo(self):
        """Guarda el estado actual en archivo"""
        with open(self.archivo, 'w') as f:
            f.write(f"Libros: {len(self.libros)}\n")
            f.write(f"Préstamos: {len(self.prestamos)}\n")
            # Guardar detalles de libros
            for libro in self.libros:
                f.write(f"LIBRO|{libro.id}|{libro.titulo}|{libro.autor}|{libro.isbn}|{libro.disponible}\n")
            # Guardar detalles de préstamos
            for prestamo in self.prestamos:
                f.write(f"PRESTAMO|{prestamo.id}|{prestamo.libro_id}|{prestamo.usuario}|{prestamo.fecha}|{prestamo.devuelto}\n")
    
    def _cargar_desde_archivo(self):
        """Carga datos desde archivo si existe"""
        try:
            with open(self.archivo, 'r') as f:
                lineas = f.readlines()
            
            # Reiniciar contadores
            max_libro_id = 0
            max_prestamo_id = 0
            
            for linea in lineas:
                partes = linea.strip().split('|')
                if partes[0] == "LIBRO" and len(partes) == 6:
                    libro_id = int(partes[1])
                    libro = Libro(
                        libro_id,
                        partes[2],
                        partes[3],
                        partes[4],
                        partes[5].lower() == "true"
                    )
                    self.libros.append(libro)
                    max_libro_id = max(max_libro_id, libro_id)
                
                elif partes[0] == "PRESTAMO" and len(partes) == 6:
                    prestamo_id = int(partes[1])
                    prestamo = Prestamo(
                        prestamo_id,
                        int(partes[2]),
                        partes[3],
                        partes[4]
                    )
                    prestamo.devuelto = partes[5].lower() == "true"
                    self.prestamos.append(prestamo)
                    max_prestamo_id = max(max_prestamo_id, prestamo_id)
            
            # Actualizar contadores
            self.contador_libro = max_libro_id + 1 if max_libro_id > 0 else 1
            self.contador_prestamo = max_prestamo_id + 1 if max_prestamo_id > 0 else 1
            
            return True
        except FileNotFoundError:
            # Archivo no existe, empezar con datos vacíos
            return False
        except Exception as e:
            print(f"Error cargando archivo: {e}")
            return False


class RepositorioMemoria(IRepositorioBiblioteca):
    """Implementación en memoria para testing o desarrollo rápido"""
    
    def __init__(self):
        self.libros: List[Libro] = []
        self.prestamos: List[Prestamo] = []
        self.contador_libro = 1
        self.contador_prestamo = 1
    
    def agregar_libro(self, libro: Libro) -> Libro:
        libro.id = self.contador_libro
        self.libros.append(libro)
        self.contador_libro += 1
        return libro
    
    def obtener_libro_por_id(self, libro_id: int) -> Optional[Libro]:
        for libro in self.libros:
            if libro.id == libro_id:
                return libro
        return None
    
    def obtener_todos_libros(self) -> List[Libro]:
        return self.libros.copy()
    
    def obtener_libros_disponibles(self) -> List[Libro]:
        return [libro for libro in self.libros if libro.disponible]
    
    def actualizar_libro(self, libro: Libro) -> None:
        for i, l in enumerate(self.libros):
            if l.id == libro.id:
                self.libros[i] = libro
                break
    
    def agregar_prestamo(self, prestamo: Prestamo) -> Prestamo:
        prestamo.id = self.contador_prestamo
        self.prestamos.append(prestamo)
        self.contador_prestamo += 1
        return prestamo
    
    def obtener_prestamo_por_id(self, prestamo_id: int) -> Optional[Prestamo]:
        for prestamo in self.prestamos:
            if prestamo.id == prestamo_id:
                return prestamo
        return None
    
    def obtener_prestamos_activos(self) -> List[Prestamo]:
        return [p for p in self.prestamos if not p.devuelto]
    
    def actualizar_prestamo(self, prestamo: Prestamo) -> None:
        for i, p in enumerate(self.prestamos):
            if p.id == prestamo.id:
                self.prestamos[i] = prestamo
                break


# 3. SistemaBiblioteca refactorizado con inyección de dependencias
class SistemaBibliotecaDIP:
    """
    Sistema refactorizado que depende de abstracciones (IRepositorioBiblioteca)
    en lugar de implementaciones concretas
    """
    
    def __init__(self, repositorio: IRepositorioBiblioteca):
        # Inyección de dependencia: recibimos el repositorio como parámetro
        self.repositorio = repositorio
    
    def agregar_libro(self, titulo: str, autor: str, isbn: str) -> str:
        """Agrega un libro usando el repositorio inyectado"""
        if not titulo or len(titulo) < 2:
            return "Error: Título inválido"
        if not autor or len(autor) < 3:
            return "Error: Autor inválido"
        if not isbn or len(isbn) < 10:
            return "Error: ISBN inválido"
        
        libro = Libro(None, titulo, autor, isbn, True)
        libro_guardado = self.repositorio.agregar_libro(libro)
        
        return f"Libro '{titulo}' agregado exitosamente (ID: {libro_guardado.id})"
    
    def buscar_libro(self, criterio: str, valor: str) -> List[Libro]:
        """Busca libros usando el repositorio inyectado"""
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
    
    def realizar_prestamo(self, libro_id: int, usuario: str) -> str:
        """Realiza un préstamo usando el repositorio inyectado"""
        if not usuario or len(usuario) < 3:
            return "Error: Nombre de usuario inválido"
        
        libro = self.repositorio.obtener_libro_por_id(libro_id)
        if not libro:
            return "Error: Libro no encontrado"
        
        if not libro.disponible:
            return "Error: Libro no disponible"
        
        prestamo = Prestamo(
            None,
            libro_id,
            usuario,
            datetime.now().strftime("%Y-%m-%d")
        )
        
        prestamo_guardado = self.repositorio.agregar_prestamo(prestamo)
        libro.disponible = False
        self.repositorio.actualizar_libro(libro)
        
        print(f"[NOTIFICACIÓN] {usuario}: Préstamo de '{libro.titulo}'")
        
        return f"Préstamo realizado a {usuario} (ID Préstamo: {prestamo_guardado.id})"
    
    def devolver_libro(self, prestamo_id: int) -> str:
        """Devuelve un libro usando el repositorio inyectado"""
        prestamo = self.repositorio.obtener_prestamo_por_id(prestamo_id)
        
        if not prestamo:
            return "Error: Préstamo no encontrado"
        
        if prestamo.devuelto:
            return "Error: Libro ya devuelto"
        
        libro = self.repositorio.obtener_libro_por_id(prestamo.libro_id)
        if libro:
            libro.disponible = True
            self.repositorio.actualizar_libro(libro)
        
        prestamo.devuelto = True
        self.repositorio.actualizar_prestamo(prestamo)
        
        if libro:
            print(f"[NOTIFICACIÓN] {prestamo.usuario}: Devolución de '{libro.titulo}'")
        
        return "Libro devuelto exitosamente"
    
    def obtener_todos_libros(self) -> List[Libro]:
        return self.repositorio.obtener_todos_libros()
    
    def obtener_libros_disponibles(self) -> List[Libro]:
        return self.repositorio.obtener_libros_disponibles()
    
    def obtener_prestamos_activos(self) -> List[Prestamo]:
        return self.repositorio.obtener_prestamos_activos()


# 4. main() refactorizado con configuración de dependencias
def main():
    """Función principal con configuración de dependencias"""
    
    print("=== EJERCICIO 3: DEPENDENCY INVERSION PRINCIPLE ===\n")
    
    # CONFIGURACIÓN DE DEPENDENCIAS
    # Podemos cambiar fácilmente entre RepositorioArchivo y RepositorioMemoria
    print("Configurando dependencias...")
    
    # Opción 1: Usar repositorio de archivo (persistente)
    repositorio = RepositorioArchivo("biblioteca_dip.txt")
    print("✓ Usando RepositorioArchivo con persistencia en archivo")
    
    # Opción 2: Usar repositorio en memoria (para testing)
    # repositorio = RepositorioMemoria()
    # print("✓ Usando RepositorioMemoria (sin persistencia)")
    
    # INYECCIÓN DE DEPENDENCIAS
    sistema = SistemaBibliotecaDIP(repositorio)
    
    print("\n=== AGREGANDO LIBROS ===")
    print(sistema.agregar_libro("Cien Años de Soledad", "Gabriel García Márquez", "9780060883287"))
    print(sistema.agregar_libro("El Principito", "Antoine de Saint-Exupéry", "9780156012195"))
    print(sistema.agregar_libro("1984", "George Orwell", "9780451524935"))
    
    print("\n=== BÚSQUEDA POR AUTOR ===")
    resultados = sistema.buscar_libro("autor", "Garcia")
    for libro in resultados:
        print(f"- {libro.titulo} por {libro.autor}")
    
    print("\n=== REALIZAR PRÉSTAMO ===")
    print(sistema.realizar_prestamo(1, "Juan Pérez"))
    
    print("\n=== LIBROS DISPONIBLES ===")
    disponibles = sistema.obtener_libros_disponibles()
    for libro in disponibles:
        print(f"- {libro.titulo}")
    
    print("\n=== DEVOLVER LIBRO ===")
    print(sistema.devolver_libro(1))
    
    print("\n=== PRÉSTAMOS ACTIVOS ===")
    activos = sistema.obtener_prestamos_activos()
    print(f"Total de préstamos activos: {len(activos)}")
    
    # Demostración de persistencia
    print("\n=== DEMOSTRACIÓN PERSISTENCIA ===")
    print("Creando nuevo sistema con mismo repositorio...")
    sistema2 = SistemaBibliotecaDIP(repositorio)
    libros = sistema2.obtener_todos_libros()
    print(f"Libros cargados desde persistencia: {len(libros)}")
    for libro in libros:
        print(f"- {libro.titulo} (ID: {libro.id})")


def demostrar_repositorios_intercambiables():
    """Demuestra que podemos cambiar fácilmente entre repositorios"""
    
    print("\n" + "="*60)
    print("DEMOSTRACIÓN: REPOSITORIOS INTERCAMBIABLES")
    print("="*60)
    
    # Probar con RepositorioMemoria
    print("\n--- Probando con RepositorioMemoria ---")
    repositorio_memoria = RepositorioMemoria()
    sistema_memoria = SistemaBibliotecaDIP(repositorio_memoria)
    
    sistema_memoria.agregar_libro("Libro en Memoria", "Autor Test", "1234567890")
    libros_memoria = sistema_memoria.obtener_todos_libros()
    print(f"Libros en memoria: {len(libros_memoria)}")
    
    # Probar con RepositorioArchivo
    print("\n--- Probando con RepositorioArchivo ---")
    repositorio_archivo = RepositorioArchivo("test_biblioteca.txt")
    sistema_archivo = SistemaBibliotecaDIP(repositorio_archivo)
    
    sistema_archivo.agregar_libro("Libro en Archivo", "Autor Test", "0987654321")
    libros_archivo = sistema_archivo.obtener_todos_libros()
    print(f"Libros en archivo: {len(libros_archivo)}")
    
    print("\n✅ Ambos repositorios funcionan con la misma interfaz!")


if __name__ == "__main__":
    main()
    demostrar_repositorios_intercambiables()

'''
Esto es lo que deberias ver:

Configurando dependencias...
✓ Usando RepositorioArchivo con persistencia en archivo

=== AGREGANDO LIBROS ===
Libro 'Cien Años de Soledad' agregado exitosamente (ID: 1)
Libro 'El Principito' agregado exitosamente (ID: 2)
Libro '1984' agregado exitosamente (ID: 3)

=== BÚSQUEDA POR AUTOR ===
- Cien Años de Soledad por Gabriel García Márquez

=== REALIZAR PRÉSTAMO ===
[NOTIFICACIÓN] Juan Pérez: Préstamo de 'Cien Años de Soledad'
Préstamo realizado a Juan Pérez (ID Préstamo: 1)

=== LIBROS DISPONIBLES ===
- El Principito
- 1984

=== DEVOLVER LIBRO ===
[NOTIFICACIÓN] Juan Pérez: Devolución de 'Cien Años de Soledad'
Libro devuelto exitosamente

=== PRÉSTAMOS ACTIVOS ===
Total de préstamos activos: 0

=== DEMOSTRACIÓN PERSISTENCIA ===
Creando nuevo sistema con mismo repositorio...
Libros cargados desde persistencia: 3
- Cien Años de Soledad (ID: 1)
- El Principito (ID: 2)
- 1984 (ID: 3)

============================================================
DEMOSTRACIÓN: REPOSITORIOS INTERCAMBIABLES
============================================================

--- Probando con RepositorioMemoria ---
Libro 'Libro en Memoria' agregado exitosamente (ID: 1)
Libros en memoria: 1

--- Probando con RepositorioArchivo ---
Libro 'Libro en Archivo' agregado exitosamente (ID: 1)
Libros en archivo: 1

Ambos repositorios funcionan con la misma interfaz!
'''
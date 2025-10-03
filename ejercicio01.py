from abc import ABC, abstractmethod
from typing import List
from libro import Libro


# 1. Clase abstracta para estrategias de búsqueda
class EstrategiaBusqueda(ABC):
    """Interfaz abstracta para definir estrategias de búsqueda de libros"""
    
    @abstractmethod
    def buscar(self, libros: List[Libro], valor: str) -> List[Libro]:
        """Método abstracto para implementar la lógica de búsqueda"""
        pass


# 2. Implementación de 3 estrategias de búsqueda existentes
class BusquedaPorTitulo(EstrategiaBusqueda):
    """Estrategia para buscar libros por título (búsqueda parcial case-insensitive)"""
    
    def buscar(self, libros: List[Libro], valor: str) -> List[Libro]:
        resultados = []
        for libro in libros:
            if valor.lower() in libro.titulo.lower():
                resultados.append(libro)
        return resultados


class BusquedaPorAutor(EstrategiaBusqueda):
    """Estrategia para buscar libros por autor (búsqueda parcial case-insensitive)"""
    
    def buscar(self, libros: List[Libro], valor: str) -> List[Libro]:
        resultados = []
        for libro in libros:
            if valor.lower() in libro.autor.lower():
                resultados.append(libro)
        return resultados


class BusquedaPorISBN(EstrategiaBusqueda):
    """Estrategia para buscar libros por ISBN exacto"""
    
    def buscar(self, libros: List[Libro], valor: str) -> List[Libro]:
        resultados = []
        for libro in libros:
            if libro.isbn == valor:
                resultados.append(libro)
        return resultados


# 3. Nueva estrategia agregada SIN modificar código existente
class BusquedaPorDisponibilidad(EstrategiaBusqueda):
    """Estrategia para buscar libros por disponibilidad"""
    
    def buscar(self, libros: List[Libro], valor: str) -> List[Libro]:
        resultados = []
        disponible = valor.lower() in ["true", "1", "si", "sí", "yes"]
        for libro in libros:
            if libro.disponible == disponible:
                resultados.append(libro)
        return resultados


# 4. Método refactorizado en SistemaBiblioteca (versión simplificada para demostración)
class SistemaBibliotecaRefactorizado:
    def __init__(self):
        self.libros = []
        self._estrategias_busqueda = {
            "titulo": BusquedaPorTitulo(),
            "autor": BusquedaPorAutor(),
            "isbn": BusquedaPorISBN(),
            "disponible": BusquedaPorDisponibilidad()
        }
    
    def agregar_libro(self, libro: Libro):
        """Método auxiliar para agregar libros de prueba"""
        self.libros.append(libro)
    
    def buscar_libro(self, criterio: str, valor: str) -> List[Libro]:
        """
        Método refactorizado que usa estrategias de búsqueda
        Ahora está abierto a extensión pero cerrado a modificación
        """
        if criterio not in self._estrategias_busqueda:
            raise ValueError(f"Criterio de búsqueda no válido: {criterio}")
        
        estrategia = self._estrategias_busqueda[criterio]
        return estrategia.buscar(self.libros, valor)
    
    def registrar_estrategia(self, criterio: str, estrategia: EstrategiaBusqueda):
        """
        Permite registrar nuevas estrategias de búsqueda sin modificar el código existente
        """
        self._estrategias_busqueda[criterio] = estrategia


# 5. Documentación y demostración de uso
def demostrar_funcionamiento():
    """Función para demostrar que el código refactorizado funciona correctamente"""
    
    print("=== DEMOSTRACIÓN EJERCICIO 1: OPEN/CLOSED PRINCIPLE ===\n")
    
    # Crear sistema y agregar libros de prueba
    sistema = SistemaBibliotecaRefactorizado()
    
    sistema.agregar_libro(Libro(1, "Cien Años de Soledad", "Gabriel García Márquez", "9780060883287", True))
    sistema.agregar_libro(Libro(2, "El Principito", "Antoine de Saint-Exupéry", "9780156012195", True))
    sistema.agregar_libro(Libro(3, "1984", "George Orwell", "9780451524935", False))
    sistema.agregar_libro(Libro(4, "Crónica de una Muerte Anunciada", "Gabriel García Márquez", "9781400034956", True))
    
    print("Libros en el sistema:")
    for libro in sistema.libros:
        estado = "Disponible" if libro.disponible else "Prestado"
        print(f"- {libro.titulo} por {libro.autor} [{estado}]")
    
    print("\n--- PRUEBA 1: Búsqueda por autor 'Garcia' ---")
    resultados = sistema.buscar_libro("autor", "Garcia")
    for libro in resultados:
        print(f"- {libro.titulo} por {libro.autor}")
    
    print("\n--- PRUEBA 2: Búsqueda por título 'Principito' ---")
    resultados = sistema.buscar_libro("titulo", "Principito")
    for libro in resultados:
        print(f"- {libro.titulo} por {libro.autor}")
    
    print("\n--- PRUEBA 3: Búsqueda por ISBN exacto ---")
    resultados = sistema.buscar_libro("isbn", "9780451524935")
    for libro in resultados:
        print(f"- {libro.titulo} por {libro.autor} (ISBN: {libro.isbn})")
    
    print("\n--- PRUEBA 4: Búsqueda por disponibilidad 'true' ---")
    resultados = sistema.buscar_libro("disponible", "true")
    print("Libros disponibles:")
    for libro in resultados:
        print(f"- {libro.titulo}")
    
    print("\n--- PRUEBA 5: Búsqueda por disponibilidad 'false' ---")
    resultados = sistema.buscar_libro("disponible", "false")
    print("Libros prestados:")
    for libro in resultados:
        print(f"- {libro.titulo}")
    
    print("\n--- PRUEBA 6: Extensión sin modificación - Nueva estrategia ---")
    
    # Ejemplo de cómo agregar una nueva estrategia sin modificar el código existente
    class BusquedaPorPalabraClave(EstrategiaBusqueda):
        """Nueva estrategia que busca en título Y autor"""
        
        def buscar(self, libros: List[Libro], valor: str) -> List[Libro]:
            resultados = []
            for libro in libros:
                if (valor.lower() in libro.titulo.lower() or 
                    valor.lower() in libro.autor.lower()):
                    resultados.append(libro)
            return resultados
    
    # Registrar nueva estrategia sin modificar buscar_libro
    sistema.registrar_estrategia("palabra_clave", BusquedaPorPalabraClave())
    
    print("Búsqueda por palabra clave 'Gabriel':")
    resultados = sistema.buscar_libro("palabra_clave", "Gabriel")
    for libro in resultados:
        print(f"- {libro.titulo} por {libro.autor}")
    
    print("\n✅ DEMOSTRACIÓN COMPLETADA: OCP CUMPLIDO")
    print("   - Se pueden agregar nuevas estrategias sin modificar código existente")
    print("   - El sistema está ABIERTO para extensión pero CERRADO para modificación")


if __name__ == "__main__":
    demostrar_funcionamiento()

'''
Esto es lo que tiene que dar : 

Libros en el sistema:
- Cien Años de Soledad por Gabriel García Márquez [Disponible]
- El Principito por Antoine de Saint-Exupéry [Disponible]
- 1984 por George Orwell [Prestado]
- Crónica de una Muerte Anunciada por Gabriel García Márquez [Disponible]

--- PRUEBA 1: Búsqueda por autor 'Garcia' ---
- Cien Años de Soledad por Gabriel García Márquez
- Crónica de una Muerte Anunciada por Gabriel García Márquez

--- PRUEBA 2: Búsqueda por título 'Principito' ---
- El Principito por Antoine de Saint-Exupéry

(resto de las pruebas)
'''
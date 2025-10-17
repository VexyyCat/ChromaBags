"""
Módulo de Gestión de Catálogos para ChromaBags
Maneja catálogos de colores, diseños y materiales
"""

import json
from datetime import datetime
from typing import List, Dict, Optional


class Color:
    """Clase para representar un color en el catálogo"""
    
    def __init__(self, id_color: int, nombre: str, codigo_hex: str, 
                 familia: str, stock: int = 0):
        self.id_color = id_color
        self.nombre = nombre
        self.codigo_hex = codigo_hex
        self.familia = familia  # Cálidos, fríos, neutros, etc.
        self.stock = stock
        self.fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict:
        """Convierte el color a diccionario"""
        return {
            'id_color': self.id_color,
            'nombre': self.nombre,
            'codigo_hex': self.codigo_hex,
            'familia': self.familia,
            'stock': self.stock,
            'fecha_registro': self.fecha_registro
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Color':
        """Crea un Color desde un diccionario"""
        color = Color(
            data['id_color'],
            data['nombre'],
            data['codigo_hex'],
            data['familia'],
            data.get('stock', 0)
        )
        color.fecha_registro = data.get('fecha_registro', color.fecha_registro)
        return color


class Diseno:
    """Clase para representar un diseño en el catálogo"""
    
    def __init__(self, id_diseno: int, nombre: str, tipo_modelo: str,
                 descripcion: str = "", colores_ids: List[int] = None):
        self.id_diseno = id_diseno
        self.nombre = nombre
        self.tipo_modelo = tipo_modelo  # Simple, Combinado, Especial
        self.descripcion = descripcion
        self.colores_ids = colores_ids if colores_ids else []
        self.fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.activo = True
    
    def to_dict(self) -> Dict:
        """Convierte el diseño a diccionario"""
        return {
            'id_diseno': self.id_diseno,
            'nombre': self.nombre,
            'tipo_modelo': self.tipo_modelo,
            'descripcion': self.descripcion,
            'colores_ids': self.colores_ids,
            'fecha_creacion': self.fecha_creacion,
            'activo': self.activo
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Diseno':
        """Crea un Diseño desde un diccionario"""
        diseno = Diseno(
            data['id_diseno'],
            data['nombre'],
            data['tipo_modelo'],
            data.get('descripcion', ''),
            data.get('colores_ids', [])
        )
        diseno.fecha_creacion = data.get('fecha_creacion', diseno.fecha_creacion)
        diseno.activo = data.get('activo', True)
        return diseno


class Material:
    """Clase para representar un material en el catálogo"""
    
    def __init__(self, id_material: int, nombre: str, tipo: str,
                 unidad_medida: str, precio_unitario: float, 
                 stock_actual: float = 0):
        self.id_material = id_material
        self.nombre = nombre
        self.tipo = tipo  # Tela, Hilo, Asa, Accesorio, etc.
        self.unidad_medida = unidad_medida  # metros, unidades, kg, etc.
        self.precio_unitario = precio_unitario
        self.stock_actual = stock_actual
        self.stock_minimo = 0
        self.fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict:
        """Convierte el material a diccionario"""
        return {
            'id_material': self.id_material,
            'nombre': self.nombre,
            'tipo': self.tipo,
            'unidad_medida': self.unidad_medida,
            'precio_unitario': self.precio_unitario,
            'stock_actual': self.stock_actual,
            'stock_minimo': self.stock_minimo,
            'fecha_registro': self.fecha_registro
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Material':
        """Crea un Material desde un diccionario"""
        material = Material(
            data['id_material'],
            data['nombre'],
            data['tipo'],
            data['unidad_medida'],
            data['precio_unitario'],
            data.get('stock_actual', 0)
        )
        material.stock_minimo = data.get('stock_minimo', 0)
        material.fecha_registro = data.get('fecha_registro', material.fecha_registro)
        return material


class CatalogosManager:
    """Gestor principal de todos los catálogos"""
    
    def __init__(self):
        self.colores: Dict[int, Color] = {}
        self.disenos: Dict[int, Diseno] = {}
        self.materiales: Dict[int, Material] = {}
        
        # Contadores para IDs autoincrementales
        self._next_color_id = 1
        self._next_diseno_id = 1
        self._next_material_id = 1
    
    # ============ GESTIÓN DE COLORES ============
    
    def agregar_color(self, nombre: str, codigo_hex: str, familia: str, 
                      stock: int = 0) -> Color:
        """Agrega un nuevo color al catálogo"""
        color = Color(self._next_color_id, nombre, codigo_hex, familia, stock)
        self.colores[self._next_color_id] = color
        self._next_color_id += 1
        return color
    
    def obtener_color(self, id_color: int) -> Optional[Color]:
        """Obtiene un color por su ID"""
        return self.colores.get(id_color)
    
    def listar_colores(self, familia: Optional[str] = None) -> List[Color]:
        """Lista todos los colores, opcionalmente filtrados por familia"""
        if familia:
            return [c for c in self.colores.values() if c.familia == familia]
        return list(self.colores.values())
    
    def actualizar_color(self, id_color: int, **kwargs) -> bool:
        """Actualiza los datos de un color existente"""
        color = self.colores.get(id_color)
        if not color:
            return False
        
        for key, value in kwargs.items():
            if hasattr(color, key):
                setattr(color, key, value)
        return True
    
    def eliminar_color(self, id_color: int) -> bool:
        """Elimina un color del catálogo"""
        if id_color in self.colores:
            del self.colores[id_color]
            return True
        return False
    
    # ============ GESTIÓN DE DISEÑOS ============
    
    def agregar_diseno(self, nombre: str, tipo_modelo: str, 
                       descripcion: str = "", colores_ids: List[int] = None) -> Diseno:
        """Agrega un nuevo diseño al catálogo"""
        diseno = Diseno(self._next_diseno_id, nombre, tipo_modelo, 
                        descripcion, colores_ids)
        self.disenos[self._next_diseno_id] = diseno
        self._next_diseno_id += 1
        return diseno
    
    def obtener_diseno(self, id_diseno: int) -> Optional[Diseno]:
        """Obtiene un diseño por su ID"""
        return self.disenos.get(id_diseno)
    
    def listar_disenos(self, tipo_modelo: Optional[str] = None, 
                       solo_activos: bool = True) -> List[Diseno]:
        """Lista todos los diseños, con filtros opcionales"""
        disenos = self.disenos.values()
        
        if solo_activos:
            disenos = [d for d in disenos if d.activo]
        
        if tipo_modelo:
            disenos = [d for d in disenos if d.tipo_modelo == tipo_modelo]
        
        return list(disenos)
    
    def actualizar_diseno(self, id_diseno: int, **kwargs) -> bool:
        """Actualiza los datos de un diseño existente"""
        diseno = self.disenos.get(id_diseno)
        if not diseno:
            return False
        
        for key, value in kwargs.items():
            if hasattr(diseno, key):
                setattr(diseno, key, value)
        return True
    
    def desactivar_diseno(self, id_diseno: int) -> bool:
        """Desactiva un diseño (no lo elimina)"""
        return self.actualizar_diseno(id_diseno, activo=False)
    
    # ============ GESTIÓN DE MATERIALES ============
    
    def agregar_material(self, nombre: str, tipo: str, unidad_medida: str,
                         precio_unitario: float, stock_actual: float = 0) -> Material:
        """Agrega un nuevo material al catálogo"""
        material = Material(self._next_material_id, nombre, tipo, 
                           unidad_medida, precio_unitario, stock_actual)
        self.materiales[self._next_material_id] = material
        self._next_material_id += 1
        return material
    
    def obtener_material(self, id_material: int) -> Optional[Material]:
        """Obtiene un material por su ID"""
        return self.materiales.get(id_material)
    
    def listar_materiales(self, tipo: Optional[str] = None) -> List[Material]:
        """Lista todos los materiales, opcionalmente filtrados por tipo"""
        if tipo:
            return [m for m in self.materiales.values() if m.tipo == tipo]
        return list(self.materiales.values())
    
    def actualizar_material(self, id_material: int, **kwargs) -> bool:
        """Actualiza los datos de un material existente"""
        material = self.materiales.get(id_material)
        if not material:
            return False
        
        for key, value in kwargs.items():
            if hasattr(material, key):
                setattr(material, key, value)
        return True
    
    def ajustar_stock_material(self, id_material: int, cantidad: float) -> bool:
        """Ajusta el stock de un material (positivo suma, negativo resta)"""
        material = self.materiales.get(id_material)
        if not material:
            return False
        
        material.stock_actual += cantidad
        return True
    
    def eliminar_material(self, id_material: int) -> bool:
        """Elimina un material del catálogo"""
        if id_material in self.materiales:
            del self.materiales[id_material]
            return True
        return False
    
    def materiales_bajo_stock(self) -> List[Material]:
        """Obtiene lista de materiales con stock por debajo del mínimo"""
        return [m for m in self.materiales.values() 
                if m.stock_actual <= m.stock_minimo]
    
    # ============ PERSISTENCIA ============
    
    def guardar_catalogos(self, archivo: str = "/data/catalogos.json") -> bool:
        """Guarda todos los catálogos en un archivo JSON"""
        try:
            datos = {
                'colores': [c.to_dict() for c in self.colores.values()],
                'disenos': [d.to_dict() for d in self.disenos.values()],
                'materiales': [m.to_dict() for m in self.materiales.values()],
                'contadores': {
                    'next_color_id': self._next_color_id,
                    'next_diseno_id': self._next_diseno_id,
                    'next_material_id': self._next_material_id
                }
            }
            
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Error al guardar catálogos: {e}")
            return False

    def cargar_catalogos(self, archivo: str = "/data/catalogos.json") -> bool:
        """Carga todos los catálogos desde un archivo JSON"""
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            # Cargar colores
            self.colores = {
                c['id_color']: Color.from_dict(c) 
                for c in datos.get('colores', [])
            }
            
            # Cargar diseños
            self.disenos = {
                d['id_diseno']: Diseno.from_dict(d) 
                for d in datos.get('disenos', [])
            }
            
            # Cargar materiales
            self.materiales = {
                m['id_material']: Material.from_dict(m) 
                for m in datos.get('materiales', [])
            }
            
            # Cargar contadores
            contadores = datos.get('contadores', {})
            self._next_color_id = contadores.get('next_color_id', 1)
            self._next_diseno_id = contadores.get('next_diseno_id', 1)
            self._next_material_id = contadores.get('next_material_id', 1)
            
            return True
        except FileNotFoundError:
            print(f"Archivo {archivo} no encontrado. Iniciando con catálogos vacíos.")
            return False
        except Exception as e:
            print(f"Error al cargar catálogos: {e}")
            return False


# ============ DEMOSTRACIÓN DE LOGICA INTEGRADA ============
if __name__ == "__main__":
    # Crear gestor de catálogos
    gestor = CatalogosManager()
    
    # Agregar algunos colores de ejemplo
    gestor.agregar_color("Rojo Carmesí", "#DC143C", "Cálidos", 100)
    gestor.agregar_color("Azul Marino", "#000080", "Fríos", 150)
    gestor.agregar_color("Verde Esmeralda", "#50C878", "Fríos", 80)
    gestor.agregar_color("Beige", "#F5F5DC", "Neutros", 200)
    
    # Agregar materiales
    gestor.agregar_material("Tela de Algodón", "Tela", "metros", 45.50, 50.0)
    gestor.agregar_material("Hilo Polyester", "Hilo", "carretes", 12.00, 30)
    gestor.agregar_material("Asa de Cuero", "Asa", "unidades", 25.00, 15)
    
    # Agregar diseños
    gestor.agregar_diseno("Bolsa Clásica Roja", "Simple", 
                         "Diseño simple con un solo color", [1])
    gestor.agregar_diseno("Bolsa Bicolor Marina", "Combinado",
                         "Combinación de dos colores complementarios", [2, 4])
    
    # Listar colores por familia
    print("=== COLORES FRÍOS ===")
    for color in gestor.listar_colores(familia="Fríos"):
        print(f"- {color.nombre} ({color.codigo_hex})")
    
    # Listar materiales
    print("\n=== MATERIALES ===")
    for material in gestor.listar_materiales():
        print(f"- {material.nombre}: ${material.precio_unitario} por {material.unidad_medida}")
        print(f"  Stock actual: {material.stock_actual}")
    
    # Guardar catálogos
    if gestor.guardar_catalogos():
        print("\n✓ Catálogos guardados exitosamente")
    
    # Simular carga de catálogos
    gestor_nuevo = CatalogosManager()
    if gestor_nuevo.cargar_catalogos():
        print("✓ Catálogos cargados exitosamente")
        print(f"Total de colores: {len(gestor_nuevo.colores)}")
        print(f"Total de materiales: {len(gestor_nuevo.materiales)}")
        print(f"Total de diseños: {len(gestor_nuevo.disenos)}")
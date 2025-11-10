"""
Módulo de Gestión de Catálogos para ChromaBags
Maneja catálogos de colores, diseños y materiales con SQLite
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple


class Color:
    """Clase para representar un color en el catálogo"""
    
    def __init__(self, id_color: int, nombre: str, codigo_hex: str, 
                 id_paleta: int = None):
        self.id_color = id_color
        self.nombre = nombre
        self.codigo_hex = codigo_hex
        self.id_paleta = id_paleta
    
    def to_dict(self) -> Dict:
        """Convierte el color a diccionario"""
        return {
            'id_color': self.id_color,
            'nombre': self.nombre,
            'codigo_hex': self.codigo_hex,
            'id_paleta': self.id_paleta
        }
    
    @staticmethod
    def from_row(row: Tuple) -> 'Color':
        """Crea un Color desde una fila de la BD"""
        return Color(row[0], row[1], row[2], row[3])


class Diseno:
    """Clase para representar un diseño/modelo en el catálogo"""
    
    def __init__(self, id_modelo: int, nombre: str, tipo: str,
                 descripcion: str = "", ancho: float = 30.0, alto: float = 40.0):
        self.id_modelo = id_modelo
        self.nombre = nombre
        self.tipo = tipo
        self.descripcion = descripcion
        self.ancho = ancho
        self.alto = alto
    
    def to_dict(self) -> Dict:
        """Convierte el diseño a diccionario"""
        return {
            'id_modelo': self.id_modelo,
            'nombre': self.nombre,
            'tipo': self.tipo,
            'descripcion': self.descripcion,
            'ancho': self.ancho,
            'alto': self.alto
        }
    
    @staticmethod
    def from_row(row: Tuple) -> 'Diseno':
        """Crea un Diseño desde una fila de la BD"""
        return Diseno(row[0], row[1], row[2], row[3] or "", row[4], row[5])


class Material:
    """Clase para representar un material en el catálogo"""
    
    def __init__(self, id_material: int, nombre: str, tipo: str,
                 unidad_medida: str, costo_unitario: float, 
                 descripcion: str = ""):
        self.id_material = id_material
        self.nombre = nombre
        self.tipo = tipo
        self.unidad_medida = unidad_medida
        self.costo_unitario = costo_unitario
        self.descripcion = descripcion
    
    def to_dict(self) -> Dict:
        """Convierte el material a diccionario"""
        return {
            'id_material': self.id_material,
            'nombre': self.nombre,
            'tipo': self.tipo,
            'unidad_medida': self.unidad_medida,
            'costo_unitario': self.costo_unitario,
            'descripcion': self.descripcion
        }
    
    @staticmethod
    def from_row(row: Tuple) -> 'Material':
        """Crea un Material desde una fila de la BD"""
        return Material(row[0], row[1], row[2], row[3], row[4], row[5] or "")


class ProductoTerminado:
    """Clase para representar un producto terminado"""
    
    def __init__(self, id_producto: int, nombre: str, modelo: str, 
                 tipo_modelo: str, color_principal: str, precio: float, 
                 stock: int, color_secundario: str = None, 
                 color_hilo: str = None, color_asa: str = None):
        self.id_producto = id_producto
        self.nombre = nombre
        self.modelo = modelo
        self.tipo_modelo = tipo_modelo
        self.color_principal = color_principal
        self.color_secundario = color_secundario
        self.color_hilo = color_hilo
        self.color_asa = color_asa
        self.precio = precio
        self.stock = stock
    
    def to_dict(self) -> Dict:
        """Convierte el producto a diccionario"""
        return {
            'id_producto': self.id_producto,
            'nombre': self.nombre,
            'modelo': self.modelo,
            'tipo_modelo': self.tipo_modelo,
            'color_principal': self.color_principal,
            'color_secundario': self.color_secundario,
            'color_hilo': self.color_hilo,
            'color_asa': self.color_asa,
            'precio': self.precio,
            'stock': self.stock
        }


class CatalogosManager:
    """Gestor principal de todos los catálogos con SQLite"""
    
    def __init__(self, db_path: str = "database/chromabags.db"):
        self.db_path = db_path
    
    def _get_connection(self):
        """Obtiene una conexión a la base de datos"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    # ============ GESTIÓN DE COLORES ============
    
    def agregar_color(self, nombre: str, codigo_hex: str, 
                      id_paleta: int = None) -> Optional[Color]:
        """Agrega un nuevo color al catálogo"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO colores (nombre_color, codigo_hex, id_paleta)
                VALUES (?, ?, ?)
            """, (nombre, codigo_hex, id_paleta))
            conn.commit()
            id_color = cursor.lastrowid
            conn.close()
            return Color(id_color, nombre, codigo_hex, id_paleta)
        except Exception as e:
            print(f"Error al agregar color: {e}")
            return None
    
    def obtener_color(self, id_color: int) -> Optional[Color]:
        """Obtiene un color por su ID"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_color, nombre_color, codigo_hex, id_paleta 
                FROM colores WHERE id_color = ?
            """, (id_color,))
            row = cursor.fetchone()
            conn.close()
            return Color.from_row(row) if row else None
        except Exception as e:
            print(f"Error al obtener color: {e}")
            return None
    
    def listar_colores(self, id_paleta: Optional[int] = None) -> List[Color]:
        """Lista todos los colores, opcionalmente filtrados por paleta"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            if id_paleta:
                cursor.execute("""
                    SELECT id_color, nombre_color, codigo_hex, id_paleta 
                    FROM colores WHERE id_paleta = ?
                    ORDER BY nombre_color
                """, (id_paleta,))
            else:
                cursor.execute("""
                    SELECT id_color, nombre_color, codigo_hex, id_paleta 
                    FROM colores ORDER BY nombre_color
                """)
            rows = cursor.fetchall()
            conn.close()
            return [Color.from_row(row) for row in rows]
        except Exception as e:
            print(f"Error al listar colores: {e}")
            return []
    
    def actualizar_color(self, id_color: int, nombre: str = None, 
                        codigo_hex: str = None, id_paleta: int = None) -> bool:
        """Actualiza los datos de un color existente"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            updates = []
            params = []
            
            if nombre:
                updates.append("nombre_color = ?")
                params.append(nombre)
            if codigo_hex:
                updates.append("codigo_hex = ?")
                params.append(codigo_hex)
            if id_paleta is not None:
                updates.append("id_paleta = ?")
                params.append(id_paleta)
            
            if not updates:
                return False
            
            params.append(id_color)
            query = f"UPDATE colores SET {', '.join(updates)} WHERE id_color = ?"
            cursor.execute(query, params)
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            print(f"Error al actualizar color: {e}")
            return False
    
    def eliminar_color(self, id_color: int) -> bool:
        """Elimina un color del catálogo"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM colores WHERE id_color = ?", (id_color,))
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            print(f"Error al eliminar color: {e}")
            return False
    
    # ============ GESTIÓN DE DISEÑOS/MODELOS ============
    
    def agregar_diseno(self, nombre: str, tipo: str, 
                       descripcion: str = "", ancho: float = 30.0, 
                       alto: float = 40.0) -> Optional[Diseno]:
        """Agrega un nuevo diseño/modelo al catálogo"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO modelos_bolsas 
                (nombre_modelo, tipo, descripcion, ancho, alto)
                VALUES (?, ?, ?, ?, ?)
            """, (nombre, tipo, descripcion, ancho, alto))
            conn.commit()
            id_modelo = cursor.lastrowid
            conn.close()
            return Diseno(id_modelo, nombre, tipo, descripcion, ancho, alto)
        except Exception as e:
            print(f"Error al agregar diseño: {e}")
            return None
    
    def obtener_diseno(self, id_modelo: int) -> Optional[Diseno]:
        """Obtiene un diseño por su ID"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_modelo, nombre_modelo, tipo, descripcion, ancho, alto 
                FROM modelos_bolsas WHERE id_modelo = ?
            """, (id_modelo,))
            row = cursor.fetchone()
            conn.close()
            return Diseno.from_row(row) if row else None
        except Exception as e:
            print(f"Error al obtener diseño: {e}")
            return None
    
    def listar_disenos(self, tipo: Optional[str] = None) -> List[Diseno]:
        """Lista todos los diseños, con filtros opcionales"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            if tipo:
                cursor.execute("""
                    SELECT id_modelo, nombre_modelo, tipo, descripcion, ancho, alto 
                    FROM modelos_bolsas WHERE tipo = ?
                    ORDER BY nombre_modelo
                """, (tipo,))
            else:
                cursor.execute("""
                    SELECT id_modelo, nombre_modelo, tipo, descripcion, ancho, alto 
                    FROM modelos_bolsas ORDER BY nombre_modelo
                """)
            rows = cursor.fetchall()
            conn.close()
            return [Diseno.from_row(row) for row in rows]
        except Exception as e:
            print(f"Error al listar diseños: {e}")
            return []
    
    def actualizar_diseno(self, id_modelo: int, **kwargs) -> bool:
        """Actualiza los datos de un diseño existente"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            updates = []
            params = []
            
            campo_map = {
                'nombre': 'nombre_modelo',
                'tipo': 'tipo',
                'descripcion': 'descripcion',
                'ancho': 'ancho',
                'alto': 'alto'
            }
            
            for key, value in kwargs.items():
                if key in campo_map:
                    updates.append(f"{campo_map[key]} = ?")
                    params.append(value)
            
            if not updates:
                return False
            
            params.append(id_modelo)
            query = f"UPDATE modelos_bolsas SET {', '.join(updates)} WHERE id_modelo = ?"
            cursor.execute(query, params)
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            print(f"Error al actualizar diseño: {e}")
            return False
    
    def eliminar_diseno(self, id_modelo: int) -> bool:
        """Elimina un diseño del catálogo"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM modelos_bolsas WHERE id_modelo = ?", (id_modelo,))
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            print(f"Error al eliminar diseño: {e}")
            return False
    
    # ============ GESTIÓN DE MATERIALES ============
    
    def agregar_material(self, nombre: str, tipo: str, unidad_medida: str,
                         costo_unitario: float, descripcion: str = "") -> Optional[Material]:
        """Agrega un nuevo material al catálogo"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO materiales 
                (nombre_material, tipo, unidad_medida, costo_unitario, descripcion)
                VALUES (?, ?, ?, ?, ?)
            """, (nombre, tipo, unidad_medida, costo_unitario, descripcion))
            conn.commit()
            id_material = cursor.lastrowid
            conn.close()
            return Material(id_material, nombre, tipo, unidad_medida, 
                          costo_unitario, descripcion)
        except Exception as e:
            print(f"Error al agregar material: {e}")
            return None
    
    def obtener_material(self, id_material: int) -> Optional[Material]:
        """Obtiene un material por su ID"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_material, nombre_material, tipo, unidad_medida, 
                       costo_unitario, descripcion 
                FROM materiales WHERE id_material = ?
            """, (id_material,))
            row = cursor.fetchone()
            conn.close()
            return Material.from_row(row) if row else None
        except Exception as e:
            print(f"Error al obtener material: {e}")
            return None
    
    def listar_materiales(self, tipo: Optional[str] = None) -> List[Material]:
        """Lista todos los materiales, opcionalmente filtrados por tipo"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            if tipo:
                cursor.execute("""
                    SELECT id_material, nombre_material, tipo, unidad_medida, 
                           costo_unitario, descripcion 
                    FROM materiales WHERE tipo = ?
                    ORDER BY nombre_material
                """, (tipo,))
            else:
                cursor.execute("""
                    SELECT id_material, nombre_material, tipo, unidad_medida, 
                           costo_unitario, descripcion 
                    FROM materiales ORDER BY nombre_material
                """)
            rows = cursor.fetchall()
            conn.close()
            return [Material.from_row(row) for row in rows]
        except Exception as e:
            print(f"Error al listar materiales: {e}")
            return []
    
    def actualizar_material(self, id_material: int, **kwargs) -> bool:
        """Actualiza los datos de un material existente"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            updates = []
            params = []
            
            campo_map = {
                'nombre': 'nombre_material',
                'tipo': 'tipo',
                'unidad_medida': 'unidad_medida',
                'costo_unitario': 'costo_unitario',
                'descripcion': 'descripcion'
            }
            
            for key, value in kwargs.items():
                if key in campo_map:
                    updates.append(f"{campo_map[key]} = ?")
                    params.append(value)
            
            if not updates:
                return False
            
            params.append(id_material)
            query = f"UPDATE materiales SET {', '.join(updates)} WHERE id_material = ?"
            cursor.execute(query, params)
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            print(f"Error al actualizar material: {e}")
            return False
    
    def eliminar_material(self, id_material: int) -> bool:
        """Elimina un material del catálogo"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM materiales WHERE id_material = ?", (id_material,))
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            print(f"Error al eliminar material: {e}")
            return False
    
    def obtener_stock_material(self, id_material: int) -> float:
        """Obtiene el stock actual de un material"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT SUM(cantidad) 
                FROM inventario_materiales 
                WHERE id_material = ?
            """, (id_material,))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result[0] else 0.0
        except Exception as e:
            print(f"Error al obtener stock: {e}")
            return 0.0
    
    def ajustar_stock_material(self, id_material: int, cantidad: float) -> bool:
        """Ajusta el stock de un material"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO inventario_materiales (id_material, cantidad)
                VALUES (?, ?)
            """, (id_material, cantidad))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al ajustar stock: {e}")
            return False
    
    # ============ GESTIÓN DE PRODUCTOS TERMINADOS ============
    
    def listar_productos_catalogo(self, filtro_tipo: Optional[str] = None,
                                  filtro_modelo: Optional[int] = None) -> List[ProductoTerminado]:
        """Lista todos los productos del catálogo con sus detalles completos"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT
                    pt.id_producto,
                    pt.nombre_producto,
                    mb.nombre_modelo,
                    mb.tipo AS tipo_modelo,
                    cp.nombre_color AS color_principal,
                    cs.nombre_color AS color_secundario,
                    ch.nombre_color AS color_hilo,
                    ca.nombre_color AS color_asa,
                    pt.precio_sugerido,
                    pt.stock
                FROM productos_terminados pt
                JOIN modelos_bolsas mb ON pt.id_modelo = mb.id_modelo
                LEFT JOIN combinaciones c ON pt.id_combinacion = c.id_combinacion
                LEFT JOIN colores cp ON c.id_color_principal = cp.id_color
                LEFT JOIN colores cs ON c.id_color_secundario = cs.id_color
                LEFT JOIN colores ch ON c.id_color_hilo = ch.id_color
                LEFT JOIN colores ca ON c.id_color_asa = ca.id_color
            """
            
            conditions = []
            params = []
            
            if filtro_tipo:
                conditions.append("mb.tipo = ?")
                params.append(filtro_tipo)
            
            if filtro_modelo:
                conditions.append("mb.id_modelo = ?")
                params.append(filtro_modelo)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY pt.nombre_producto"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()
            
            productos = []
            for row in rows:
                producto = ProductoTerminado(
                    id_producto=row[0],
                    nombre=row[1],
                    modelo=row[2],
                    tipo_modelo=row[3],
                    color_principal=row[4] or "Sin definir",
                    precio=row[8] or 0.0,
                    stock=row[9] or 0,
                    color_secundario=row[5],
                    color_hilo=row[6],
                    color_asa=row[7]
                )
                productos.append(producto)
            
            return productos
        except Exception as e:
            print(f"Error al listar productos del catálogo: {e}")
            return []
    
    def obtener_producto(self, id_producto: int) -> Optional[ProductoTerminado]:
        """Obtiene un producto terminado por su ID"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    pt.id_producto,
                    pt.nombre_producto,
                    mb.nombre_modelo,
                    mb.tipo AS tipo_modelo,
                    cp.nombre_color AS color_principal,
                    cs.nombre_color AS color_secundario,
                    ch.nombre_color AS color_hilo,
                    ca.nombre_color AS color_asa,
                    pt.precio_sugerido,
                    pt.stock
                FROM productos_terminados pt
                JOIN modelos_bolsas mb ON pt.id_modelo = mb.id_modelo
                LEFT JOIN combinaciones c ON pt.id_combinacion = c.id_combinacion
                LEFT JOIN colores cp ON c.id_color_principal = cp.id_color
                LEFT JOIN colores cs ON c.id_color_secundario = cs.id_color
                LEFT JOIN colores ch ON c.id_color_hilo = ch.id_color
                LEFT JOIN colores ca ON c.id_color_asa = ca.id_color
                WHERE pt.id_producto = ?
            """, (id_producto,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return ProductoTerminado(
                    id_producto=row[0],
                    nombre=row[1],
                    modelo=row[2],
                    tipo_modelo=row[3],
                    color_principal=row[4] or "Sin definir",
                    precio=row[8] or 0.0,
                    stock=row[9] or 0,
                    color_secundario=row[5],
                    color_hilo=row[6],
                    color_asa=row[7]
                )
            return None
        except Exception as e:
            print(f"Error al obtener producto: {e}")
            return None
"""
Módulo de Diseño y Modelos para ChromaBags
Maneja modelos de bolsas y aplicación de colores con SQLite
"""

import sqlite3
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from colorsys import rgb_to_hls


class ModeloBolsa:
    """Representa un modelo de bolsa con sus componentes"""
    
    # Tipos de modelos disponibles
    TIPOS = {
        'ESTANDAR': 'Estándar',
        'ESPECIAL': 'Especial',
        'PREMIUM': 'Premium'
    }
    
    def __init__(self, id_modelo: int, nombre: str, tipo: str, 
                 descripcion: str = "", ancho: float = 30.0, alto: float = 35.0):
        self.id_modelo = id_modelo
        self.nombre = nombre
        self.tipo = tipo.lower()
        self.descripcion = descripcion
        self.ancho = ancho
        self.alto = alto
    
    def obtener_area_superficie(self) -> float:
        """Calcula el área aproximada de superficie de la bolsa"""
        # Cálculo aproximado simple
        return self.ancho * self.alto * 2.5  # Factor para considerar laterales
    
    def to_dict(self) -> Dict:
        """Convierte el modelo a diccionario"""
        return {
            'id_modelo': self.id_modelo,
            'nombre': self.nombre,
            'tipo': self.tipo,
            'descripcion': self.descripcion,
            'ancho': self.ancho,
            'alto': self.alto
        }
    
    @staticmethod
    def from_row(row: Tuple) -> 'ModeloBolsa':
        """Crea un ModeloBolsa desde una fila de la BD"""
        return ModeloBolsa(
            row[0],  # id_modelo
            row[1],  # nombre_modelo
            row[2],  # tipo
            row[3] if row[3] else "",  # descripcion
            row[4],  # ancho
            row[5]   # alto
        )


class Combinacion:
    """Representa una combinación de colores aplicada a un modelo"""
    
    def __init__(self, id_combinacion: int, id_modelo: int, nombre: str,
                 esquema: str = "armonico"):
        self.id_combinacion = id_combinacion
        self.id_modelo = id_modelo
        self.nombre = nombre
        self.esquema = esquema
        
        # IDs de colores aplicados
        self.id_color_principal = None
        self.id_color_secundario = None
        self.id_color_hilo = None
        self.id_color_asa = None
        
        self.fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict:
        """Convierte la combinación a diccionario"""
        return {
            'id_combinacion': self.id_combinacion,
            'id_modelo': self.id_modelo,
            'nombre': self.nombre,
            'esquema': self.esquema,
            'id_color_principal': self.id_color_principal,
            'id_color_secundario': self.id_color_secundario,
            'id_color_hilo': self.id_color_hilo,
            'id_color_asa': self.id_color_asa,
            'fecha_creacion': self.fecha_creacion
        }
    
    @staticmethod
    def from_row(row: Tuple) -> 'Combinacion':
        """Crea una Combinación desde una fila de la BD"""
        comb = Combinacion(
            row[0],  # id_combinacion
            row[1],  # id_modelo
            row[7] if row[7] else f"Combinación {row[0]}",  # nombre_guardado
            row[2] if row[2] else "armonico"  # esquema
        )
        comb.id_color_principal = row[3]
        comb.id_color_secundario = row[4]
        comb.id_color_hilo = row[5]
        comb.id_color_asa = row[6]
        comb.fecha_creacion = row[8] if len(row) > 8 else comb.fecha_creacion
        return comb


class CombinacionDetallada:
    """Combinación con información completa de colores"""
    
    def __init__(self, combinacion: Combinacion, modelo: ModeloBolsa,
                 colores: Dict[str, Tuple[str, str]]):
        self.combinacion = combinacion
        self.modelo = modelo
        self.colores = colores  # {'principal': ('nombre', 'hex'), ...}
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario con toda la información"""
        return {
            'id_combinacion': self.combinacion.id_combinacion,
            'nombre': self.combinacion.nombre,
            'modelo': self.modelo.nombre,
            'tipo_modelo': self.modelo.tipo,
            'esquema': self.combinacion.esquema,
            'colores': self.colores,
            'fecha_creacion': self.combinacion.fecha_creacion
        }


class DisenoModelosManager:
    """Gestor de modelos de bolsas y diseños aplicados con SQLite"""
    
    def __init__(self, db_path: str = "database/chromabags.db"):
        self.db_path = db_path
    
    def _get_connection(self):
        """Obtiene una conexión a la base de datos"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    # ============ GESTIÓN DE MODELOS ============
    
    def agregar_modelo(self, nombre: str, tipo: str, descripcion: str = "",
                       ancho: float = 30.0, alto: float = 35.0) -> Optional[ModeloBolsa]:
        """Agrega un nuevo modelo de bolsa"""
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
            return ModeloBolsa(id_modelo, nombre, tipo, descripcion, ancho, alto)
        except Exception as e:
            print(f"Error al agregar modelo: {e}")
            return None
    
    def obtener_modelo(self, id_modelo: int) -> Optional[ModeloBolsa]:
        """Obtiene un modelo por su ID"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_modelo, nombre_modelo, tipo, descripcion, ancho, alto
                FROM modelos_bolsas WHERE id_modelo = ?
            """, (id_modelo,))
            row = cursor.fetchone()
            conn.close()
            return ModeloBolsa.from_row(row) if row else None
        except Exception as e:
            print(f"Error al obtener modelo: {e}")
            return None
    
    def listar_modelos(self, tipo: Optional[str] = None) -> List[ModeloBolsa]:
        """Lista todos los modelos con filtros opcionales"""
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
                    FROM modelos_bolsas
                    ORDER BY nombre_modelo
                """)
            
            rows = cursor.fetchall()
            conn.close()
            return [ModeloBolsa.from_row(row) for row in rows]
        except Exception as e:
            print(f"Error al listar modelos: {e}")
            return []
    
    def actualizar_modelo(self, id_modelo: int, **kwargs) -> bool:
        """Actualiza los datos de un modelo"""
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
            print(f"Error al actualizar modelo: {e}")
            return False
    
    def eliminar_modelo(self, id_modelo: int) -> bool:
        """Elimina un modelo"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM modelos_bolsas WHERE id_modelo = ?", (id_modelo,))
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            print(f"Error al eliminar modelo: {e}")
            return False
    
    # ============ GESTIÓN DE COMBINACIONES ============
    
    def crear_combinacion(self, id_modelo: int, nombre: str, esquema: str,
                         id_color_principal: int = None,
                         id_color_secundario: int = None,
                         id_color_hilo: int = None,
                         id_color_asa: int = None) -> Optional[Combinacion]:
        """Crea una nueva combinación de colores"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO combinaciones 
                (id_modelo, esquema, id_color_principal, id_color_secundario, 
                 id_color_hilo, id_color_asa, nombre_guardado)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (id_modelo, esquema, id_color_principal, id_color_secundario,
                  id_color_hilo, id_color_asa, nombre))
            conn.commit()
            id_combinacion = cursor.lastrowid
            conn.close()
            
            comb = Combinacion(id_combinacion, id_modelo, nombre, esquema)
            comb.id_color_principal = id_color_principal
            comb.id_color_secundario = id_color_secundario
            comb.id_color_hilo = id_color_hilo
            comb.id_color_asa = id_color_asa
            return comb
        except Exception as e:
            print(f"Error al crear combinación: {e}")
            return None
    
    def obtener_combinacion(self, id_combinacion: int) -> Optional[Combinacion]:
        """Obtiene una combinación por su ID"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_combinacion, id_modelo, esquema, 
                       id_color_principal, id_color_secundario,
                       id_color_hilo, id_color_asa, nombre_guardado, fecha_creacion
                FROM combinaciones WHERE id_combinacion = ?
            """, (id_combinacion,))
            row = cursor.fetchone()
            conn.close()
            return Combinacion.from_row(row) if row else None
        except Exception as e:
            print(f"Error al obtener combinación: {e}")
            return None
    
    def obtener_combinacion_detallada(self, id_combinacion: int) -> Optional[CombinacionDetallada]:
        """Obtiene una combinación con todos sus detalles"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Obtener combinación con información de colores
            cursor.execute("""
                SELECT 
                    c.id_combinacion, c.id_modelo, c.esquema,
                    c.id_color_principal, c.id_color_secundario,
                    c.id_color_hilo, c.id_color_asa, c.nombre_guardado,
                    c.fecha_creacion,
                    m.nombre_modelo, m.tipo, m.descripcion, m.ancho, m.alto,
                    cp.nombre_color AS nombre_principal, cp.codigo_hex AS hex_principal,
                    cs.nombre_color AS nombre_secundario, cs.codigo_hex AS hex_secundario,
                    ch.nombre_color AS nombre_hilo, ch.codigo_hex AS hex_hilo,
                    ca.nombre_color AS nombre_asa, ca.codigo_hex AS hex_asa
                FROM combinaciones c
                JOIN modelos_bolsas m ON c.id_modelo = m.id_modelo
                LEFT JOIN colores cp ON c.id_color_principal = cp.id_color
                LEFT JOIN colores cs ON c.id_color_secundario = cs.id_color
                LEFT JOIN colores ch ON c.id_color_hilo = ch.id_color
                LEFT JOIN colores ca ON c.id_color_asa = ca.id_color
                WHERE c.id_combinacion = ?
            """, (id_combinacion,))
            
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                return None
            
            # Crear objetos
            comb = Combinacion(row[0], row[1], row[7], row[2])
            comb.id_color_principal = row[3]
            comb.id_color_secundario = row[4]
            comb.id_color_hilo = row[5]
            comb.id_color_asa = row[6]
            comb.fecha_creacion = row[8]
            
            modelo = ModeloBolsa(row[1], row[9], row[10], row[11] or "", row[12], row[13])
            
            colores = {}
            if row[14]:  # nombre_principal
                colores['principal'] = (row[14], row[15])
            if row[16]:  # nombre_secundario
                colores['secundario'] = (row[16], row[17])
            if row[18]:  # nombre_hilo
                colores['hilo'] = (row[18], row[19])
            if row[20]:  # nombre_asa
                colores['asa'] = (row[20], row[21])
            
            return CombinacionDetallada(comb, modelo, colores)
            
        except Exception as e:
            print(f"Error al obtener combinación detallada: {e}")
            return None
    
    def listar_combinaciones(self, id_modelo: Optional[int] = None,
                            esquema: Optional[str] = None) -> List[CombinacionDetallada]:
        """Lista todas las combinaciones con sus detalles"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT 
                    c.id_combinacion, c.id_modelo, c.esquema,
                    c.id_color_principal, c.id_color_secundario,
                    c.id_color_hilo, c.id_color_asa, c.nombre_guardado,
                    c.fecha_creacion,
                    m.nombre_modelo, m.tipo, m.descripcion, m.ancho, m.alto,
                    cp.nombre_color AS nombre_principal, cp.codigo_hex AS hex_principal,
                    cs.nombre_color AS nombre_secundario, cs.codigo_hex AS hex_secundario,
                    ch.nombre_color AS nombre_hilo, ch.codigo_hex AS hex_hilo,
                    ca.nombre_color AS nombre_asa, ca.codigo_hex AS hex_asa
                FROM combinaciones c
                JOIN modelos_bolsas m ON c.id_modelo = m.id_modelo
                LEFT JOIN colores cp ON c.id_color_principal = cp.id_color
                LEFT JOIN colores cs ON c.id_color_secundario = cs.id_color
                LEFT JOIN colores ch ON c.id_color_hilo = ch.id_color
                LEFT JOIN colores ca ON c.id_color_asa = ca.id_color
            """
            
            conditions = []
            params = []
            
            if id_modelo:
                conditions.append("c.id_modelo = ?")
                params.append(id_modelo)
            
            if esquema:
                conditions.append("c.esquema = ?")
                params.append(esquema)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY c.fecha_creacion DESC"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()
            
            combinaciones = []
            for row in rows:
                comb = Combinacion(row[0], row[1], row[7], row[2])
                comb.id_color_principal = row[3]
                comb.id_color_secundario = row[4]
                comb.id_color_hilo = row[5]
                comb.id_color_asa = row[6]
                comb.fecha_creacion = row[8]
                
                modelo = ModeloBolsa(row[1], row[9], row[10], row[11] or "", row[12], row[13])
                
                colores = {}
                if row[14]:
                    colores['principal'] = (row[14], row[15])
                if row[16]:
                    colores['secundario'] = (row[16], row[17])
                if row[18]:
                    colores['hilo'] = (row[18], row[19])
                if row[20]:
                    colores['asa'] = (row[20], row[21])
                
                combinaciones.append(CombinacionDetallada(comb, modelo, colores))
            
            return combinaciones
            
        except Exception as e:
            print(f"Error al listar combinaciones: {e}")
            return []
    
    def actualizar_combinacion(self, id_combinacion: int, **kwargs) -> bool:
        """Actualiza una combinación existente"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            updates = []
            params = []
            
            campos_permitidos = {
                'nombre': 'nombre_guardado',
                'esquema': 'esquema',
                'id_color_principal': 'id_color_principal',
                'id_color_secundario': 'id_color_secundario',
                'id_color_hilo': 'id_color_hilo',
                'id_color_asa': 'id_color_asa'
            }
            
            for key, value in kwargs.items():
                if key in campos_permitidos:
                    updates.append(f"{campos_permitidos[key]} = ?")
                    params.append(value)
            
            if not updates:
                return False
            
            params.append(id_combinacion)
            query = f"UPDATE combinaciones SET {', '.join(updates)} WHERE id_combinacion = ?"
            cursor.execute(query, params)
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            print(f"Error al actualizar combinación: {e}")
            return False
    
    def eliminar_combinacion(self, id_combinacion: int) -> bool:
        """Elimina una combinación"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM combinaciones WHERE id_combinacion = ?", (id_combinacion,))
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            print(f"Error al eliminar combinación: {e}")
            return False
    
    # ============ ANÁLISIS Y REPORTES ============
    
    def obtener_estadisticas_modelo(self, id_modelo: int) -> Optional[Dict]:
        """Obtiene estadísticas de uso de un modelo"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Contar combinaciones del modelo
            cursor.execute("""
                SELECT COUNT(*) FROM combinaciones WHERE id_modelo = ?
            """, (id_modelo,))
            total_combinaciones = cursor.fetchone()[0]
            
            # Obtener info del modelo
            modelo = self.obtener_modelo(id_modelo)
            conn.close()
            
            if not modelo:
                return None
            
            return {
                'id_modelo': id_modelo,
                'nombre': modelo.nombre,
                'tipo': modelo.tipo,
                'total_combinaciones': total_combinaciones,
                'area_superficie': modelo.obtener_area_superficie()
            }
        except Exception as e:
            print(f"Error al obtener estadísticas: {e}")
            return None
    
    def obtener_colores_mas_usados(self, limite: int = 5) -> List[Tuple[str, str, int]]:
        """Obtiene los colores más utilizados en las combinaciones"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    c.nombre_color,
                    c.codigo_hex,
                    COUNT(*) as uso
                FROM (
                    SELECT id_color_principal as id_color FROM combinaciones WHERE id_color_principal IS NOT NULL
                    UNION ALL
                    SELECT id_color_secundario FROM combinaciones WHERE id_color_secundario IS NOT NULL
                    UNION ALL
                    SELECT id_color_hilo FROM combinaciones WHERE id_color_hilo IS NOT NULL
                    UNION ALL
                    SELECT id_color_asa FROM combinaciones WHERE id_color_asa IS NOT NULL
                ) as colores_usados
                JOIN colores c ON colores_usados.id_color = c.id_color
                GROUP BY c.id_color, c.nombre_color, c.codigo_hex
                ORDER BY uso DESC
                LIMIT ?
            """, (limite,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [(row[0], row[1], row[2]) for row in rows]
        except Exception as e:
            print(f"Error al obtener colores más usados: {e}")
            return []
    
    def obtener_paletas_disponibles(self) -> List[Dict]:
        """Obtiene todas las paletas de colores disponibles"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id_paleta, nombre, esquema, descripcion
                FROM paletas_colores
                ORDER BY nombre
            """)
            
            rows = cursor.fetchall()
            conn.close()
            
            return [{
                'id_paleta': row[0],
                'nombre': row[1],
                'esquema': row[2],
                'descripcion': row[3] or ''
            } for row in rows]
        except Exception as e:
            print(f"Error al obtener paletas: {e}")
            return []
    
    def obtener_colores_por_paleta(self, id_paleta: int) -> List[Dict]:
        """Obtiene todos los colores de una paleta específica"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id_color, nombre_color, codigo_hex
                FROM colores
                WHERE id_paleta = ?
                ORDER BY nombre_color
            """, (id_paleta,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [{
                'id_color': row[0],
                'nombre': row[1],
                'codigo_hex': row[2]
            } for row in rows]
        except Exception as e:
            print(f"Error al obtener colores de paleta: {e}")
            return []
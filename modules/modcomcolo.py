"""
Módulo de Combinación de Colores para ChromaBags
Genera combinaciones armónicas, complementarias y análogas
"""

import json
import colorsys
from typing import List, Dict, Optional, Tuple


class ColorRGB:
    """Clase auxiliar para trabajar con colores RGB"""
    
    def __init__(self, r: int, g: int, b: int):
        self.r = max(0, min(255, r))
        self.g = max(0, min(255, g))
        self.b = max(0, min(255, b))
    
    @staticmethod
    def from_hex(hex_color: str) -> 'ColorRGB':
        """Convierte un color hexadecimal a RGB"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) != 6:
            raise ValueError("Formato hexadecimal inválido")
        
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return ColorRGB(r, g, b)
    
    def to_hex(self) -> str:
        """Convierte RGB a hexadecimal"""
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}".upper()
    
    def to_hsv(self) -> Tuple[float, float, float]:
        """Convierte RGB a HSV"""
        r, g, b = self.r / 255.0, self.g / 255.0, self.b / 255.0
        return colorsys.rgb_to_hsv(r, g, b)
    
    @staticmethod
    def from_hsv(h: float, s: float, v: float) -> 'ColorRGB':
        """Convierte HSV a RGB"""
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return ColorRGB(int(r * 255), int(g * 255), int(b * 255))
    
    def to_hls(self) -> Tuple[float, float, float]:
        """Convierte RGB a HLS"""
        r, g, b = self.r / 255.0, self.g / 255.0, self.b / 255.0
        return colorsys.rgb_to_hls(r, g, b)
    
    @staticmethod
    def from_hls(h: float, l: float, s: float) -> 'ColorRGB':
        """Convierte HLS a RGB"""
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return ColorRGB(int(r * 255), int(g * 255), int(b * 255))


class Combinacion:
    """Representa una combinación de colores"""
    
    def __init__(self, id_combinacion: int, nombre: str, tipo_esquema: str,
                 colores_hex: List[str], descripcion: str = ""):
        self.id_combinacion = id_combinacion
        self.nombre = nombre
        self.tipo_esquema = tipo_esquema  # Armónico, Complementario, Análogo
        self.colores_hex = colores_hex
        self.descripcion = descripcion
        self.fecha_creacion = None
        self.favorito = False
    
    def to_dict(self) -> Dict:
        """Convierte la combinación a diccionario"""
        return {
            'id_combinacion': self.id_combinacion,
            'nombre': self.nombre,
            'tipo_esquema': self.tipo_esquema,
            'colores_hex': self.colores_hex,
            'descripcion': self.descripcion,
            'fecha_creacion': self.fecha_creacion,
            'favorito': self.favorito
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Combinacion':
        """Crea una Combinación desde un diccionario"""
        comb = Combinacion(
            data['id_combinacion'],
            data['nombre'],
            data['tipo_esquema'],
            data['colores_hex'],
            data.get('descripcion', '')
        )
        comb.fecha_creacion = data.get('fecha_creacion')
        comb.favorito = data.get('favorito', False)
        return comb


class CombinacionColoresManager:
    """Gestor de combinaciones de colores"""
    
    # Tipos de esquemas disponibles
    ESQUEMAS = {
        'ARMONICO': 'Armónico',
        'COMPLEMENTARIO': 'Complementario',
        'ANALOGO': 'Análogo',
        'TRIADICO': 'Triádico',
        'TETRADICO': 'Tetrádico',
        'MONOCROMATICO': 'Monocromático'
    }
    
    def __init__(self):
        self.combinaciones_guardadas: Dict[int, Combinacion] = {}
        self._next_combinacion_id = 1
    
    # ============ GENERACIÓN DE ESQUEMAS ============
    
    def generar_complementario(self, hex_base: str) -> List[str]:
        """
        Genera un esquema complementario (color base + su opuesto en el círculo cromático)
        """
        color_base = ColorRGB.from_hex(hex_base)
        h, s, v = color_base.to_hsv()
        
        # Color complementario está a 180° en el círculo cromático
        h_complementario = (h + 0.5) % 1.0
        color_complementario = ColorRGB.from_hsv(h_complementario, s, v)
        
        return [hex_base, color_complementario.to_hex()]
    
    def generar_analogo(self, hex_base: str, num_colores: int = 3) -> List[str]:
        """
        Genera un esquema análogo (colores adyacentes en el círculo cromático)
        """
        color_base = ColorRGB.from_hex(hex_base)
        h, s, v = color_base.to_hsv()
        
        colores = [hex_base]
        
        # Generar colores a ±30° del color base
        angulo = 30 / 360  # 30 grados en el círculo cromático
        
        for i in range(1, num_colores):
            if i % 2 == 1:  # Impar: color a la derecha
                h_nuevo = (h + angulo * ((i + 1) // 2)) % 1.0
            else:  # Par: color a la izquierda
                h_nuevo = (h - angulo * (i // 2)) % 1.0
            
            color_nuevo = ColorRGB.from_hsv(h_nuevo, s, v)
            colores.append(color_nuevo.to_hex())
        
        return colores
    
    def generar_triadico(self, hex_base: str) -> List[str]:
        """
        Genera un esquema triádico (3 colores equidistantes en el círculo cromático)
        """
        color_base = ColorRGB.from_hex(hex_base)
        h, s, v = color_base.to_hsv()
        
        colores = [hex_base]
        
        # Colores a 120° de distancia
        for i in [1, 2]:
            h_nuevo = (h + (i * 120 / 360)) % 1.0
            color_nuevo = ColorRGB.from_hsv(h_nuevo, s, v)
            colores.append(color_nuevo.to_hex())
        
        return colores
    
    def generar_tetradico(self, hex_base: str) -> List[str]:
        """
        Genera un esquema tetrádico (4 colores: 2 pares complementarios)
        """
        color_base = ColorRGB.from_hex(hex_base)
        h, s, v = color_base.to_hsv()
        
        colores = [hex_base]
        
        # Colores a 90° de distancia
        for i in [1, 2, 3]:
            h_nuevo = (h + (i * 90 / 360)) % 1.0
            color_nuevo = ColorRGB.from_hsv(h_nuevo, s, v)
            colores.append(color_nuevo.to_hex())
        
        return colores
    
    def generar_monocromatico(self, hex_base: str, num_colores: int = 4) -> List[str]:
        """
        Genera un esquema monocromático (variaciones de luminosidad del mismo color)
        """
        color_base = ColorRGB.from_hex(hex_base)
        h, l, s = color_base.to_hls()
        
        colores = []
        
        # Generar variaciones de luminosidad
        for i in range(num_colores):
            # Distribuir luminosidades entre 0.2 y 0.9
            l_nuevo = 0.2 + (0.7 * i / (num_colores - 1)) if num_colores > 1 else l
            color_nuevo = ColorRGB.from_hls(h, l_nuevo, s)
            colores.append(color_nuevo.to_hex())
        
        return colores
    
    def generar_armonico(self, hex_base: str, num_colores: int = 3) -> List[str]:
        """
        Genera un esquema armónico (colores que funcionan bien juntos)
        Combina análogos con variaciones de saturación
        """
        color_base = ColorRGB.from_hex(hex_base)
        h, s, v = color_base.to_hsv()
        
        colores = [hex_base]
        
        # Generar colores armónicos con variaciones sutiles
        for i in range(1, num_colores):
            # Pequeñas variaciones en matiz y saturación
            h_nuevo = (h + (i * 15 / 360)) % 1.0
            s_nuevo = max(0.3, min(1.0, s - (i * 0.1)))
            v_nuevo = max(0.4, min(1.0, v + (i * 0.05)))
            
            color_nuevo = ColorRGB.from_hsv(h_nuevo, s_nuevo, v_nuevo)
            colores.append(color_nuevo.to_hex())
        
        return colores
    
    # ============ GENERACIÓN AUTOMÁTICA POR TIPO ============
    
    def generar_esquema(self, tipo_esquema: str, hex_base: str, 
                        num_colores: int = 3) -> List[str]:
        """
        Genera un esquema de color según el tipo especificado
        """
        tipo_esquema = tipo_esquema.upper()
        
        if tipo_esquema == 'COMPLEMENTARIO':
            return self.generar_complementario(hex_base)
        elif tipo_esquema == 'ANALOGO':
            return self.generar_analogo(hex_base, num_colores)
        elif tipo_esquema == 'TRIADICO':
            return self.generar_triadico(hex_base)
        elif tipo_esquema == 'TETRADICO':
            return self.generar_tetradico(hex_base)
        elif tipo_esquema == 'MONOCROMATICO':
            return self.generar_monocromatico(hex_base, num_colores)
        elif tipo_esquema == 'ARMONICO':
            return self.generar_armonico(hex_base, num_colores)
        else:
            raise ValueError(f"Tipo de esquema no válido: {tipo_esquema}")
    
    # ============ GESTIÓN DE COMBINACIONES GUARDADAS ============
    
    def guardar_combinacion(self, nombre: str, tipo_esquema: str,
                           colores_hex: List[str], descripcion: str = "") -> Combinacion:
        """Guarda una combinación de colores"""
        from datetime import datetime
        
        combinacion = Combinacion(
            self._next_combinacion_id,
            nombre,
            tipo_esquema,
            colores_hex,
            descripcion
        )
        combinacion.fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.combinaciones_guardadas[self._next_combinacion_id] = combinacion
        self._next_combinacion_id += 1
        
        return combinacion
    
    def obtener_combinacion(self, id_combinacion: int) -> Optional[Combinacion]:
        """Obtiene una combinación guardada por su ID"""
        return self.combinaciones_guardadas.get(id_combinacion)
    
    def listar_combinaciones(self, tipo_esquema: Optional[str] = None,
                            solo_favoritos: bool = False) -> List[Combinacion]:
        """Lista todas las combinaciones guardadas con filtros opcionales"""
        combinaciones = list(self.combinaciones_guardadas.values())
        
        if solo_favoritos:
            combinaciones = [c for c in combinaciones if c.favorito]
        
        if tipo_esquema:
            combinaciones = [c for c in combinaciones 
                           if c.tipo_esquema.upper() == tipo_esquema.upper()]
        
        return combinaciones
    
    def actualizar_combinacion(self, id_combinacion: int, **kwargs) -> bool:
        """Actualiza los datos de una combinación"""
        combinacion = self.combinaciones_guardadas.get(id_combinacion)
        if not combinacion:
            return False
        
        campos_permitidos = ['nombre', 'descripcion', 'favorito']
        
        for key, value in kwargs.items():
            if key in campos_permitidos and hasattr(combinacion, key):
                setattr(combinacion, key, value)
        
        return True
    
    def marcar_favorito(self, id_combinacion: int, favorito: bool = True) -> bool:
        """Marca o desmarca una combinación como favorita"""
        return self.actualizar_combinacion(id_combinacion, favorito=favorito)
    
    def eliminar_combinacion(self, id_combinacion: int) -> bool:
        """Elimina una combinación guardada"""
        if id_combinacion in self.combinaciones_guardadas:
            del self.combinaciones_guardadas[id_combinacion]
            return True
        return False
    
    # ============ ANÁLISIS DE COLORES ============
    
    def calcular_contraste(self, hex_color1: str, hex_color2: str) -> float:
        """
        Calcula el contraste relativo entre dos colores (0-21)
        Basado en WCAG 2.0
        """
        def luminancia_relativa(color_rgb: ColorRGB) -> float:
            # Normalizar valores RGB
            r, g, b = color_rgb.r / 255.0, color_rgb.g / 255.0, color_rgb.b / 255.0
            
            # Aplicar corrección gamma
            r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
            g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
            b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
            
            return 0.2126 * r + 0.7152 * g + 0.0722 * b
        
        color1 = ColorRGB.from_hex(hex_color1)
        color2 = ColorRGB.from_hex(hex_color2)
        
        l1 = luminancia_relativa(color1)
        l2 = luminancia_relativa(color2)
        
        # Asegurar que l1 es el más brillante
        if l2 > l1:
            l1, l2 = l2, l1
        
        return (l1 + 0.05) / (l2 + 0.05)
    
    def es_color_claro(self, hex_color: str) -> bool:
        """Determina si un color es claro u oscuro"""
        color = ColorRGB.from_hex(hex_color)
        # Usar luminosidad percibida
        luminosidad = (0.299 * color.r + 0.587 * color.g + 0.114 * color.b)
        return luminosidad > 127.5
    
    def sugerir_color_texto(self, hex_fondo: str) -> str:
        """Sugiere color de texto (blanco o negro) según el fondo"""
        return "#000000" if self.es_color_claro(hex_fondo) else "#FFFFFF"
    
    # ============ PERSISTENCIA ============
    
    def guardar_datos(self, archivo: str = "combinaciones.json") -> bool:
        """Guarda las combinaciones en un archivo JSON"""
        try:
            datos = {
                'combinaciones': [c.to_dict() for c in self.combinaciones_guardadas.values()],
                'contadores': {
                    'next_combinacion_id': self._next_combinacion_id
                }
            }
            
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Error al guardar combinaciones: {e}")
            return False
    
    def cargar_datos(self, archivo: str = "combinaciones.json") -> bool:
        """Carga las combinaciones desde un archivo JSON"""
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            self.combinaciones_guardadas = {
                c['id_combinacion']: Combinacion.from_dict(c)
                for c in datos.get('combinaciones', [])
            }
            
            contadores = datos.get('contadores', {})
            self._next_combinacion_id = contadores.get('next_combinacion_id', 1)
            
            return True
        except FileNotFoundError:
            print(f"Archivo {archivo} no encontrado.")
            return False
        except Exception as e:
            print(f"Error al cargar combinaciones: {e}")
            return False
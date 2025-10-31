"""
Módulo de Diseño y Modelos para ChromaBags
Maneja modelos de bolsas y aplicación de colores
"""

import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime


class ModeloBolsa:
    """Representa un modelo de bolsa con sus componentes"""
    
    # Tipos de modelos disponibles
    TIPOS = {
        'SIMPLE': 'Simple',
        'COMBINADO': 'Combinado',
        'ESPECIAL': 'Especial'
    }
    
    def __init__(self, id_modelo: int, nombre: str, tipo: str, descripcion: str = ""):
        if tipo.upper() not in self.TIPOS:
            raise ValueError(f"Tipo de modelo no válido: {tipo}")
        
        self.id_modelo = id_modelo
        self.nombre = nombre
        self.tipo = tipo.upper()
        self.descripcion = descripcion
        
        # Componentes del modelo
        self.componentes = {
            'cuerpo_principal': None,      # Color principal del cuerpo
            'cuerpo_secundario': None,     # Color secundario (para combinados)
            'asa': None,                    # Color del asa
            'hilo': None,                   # Color del hilo de costura
            'forro': None,                  # Color del forro (opcional)
            'detalles': []                  # Lista de colores para detalles adicionales
        }
        
        # Dimensiones estándar (en cm)
        self.dimensiones = {
            'ancho': 30.0,
            'alto': 35.0,
            'fondo': 10.0
        }
        
        # Configuración del modelo
        self.requiere_forro = False
        self.numero_asas = 2
        self.tiene_bolsillos = False
        
        self.activo = True
        self.fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def establecer_dimensiones(self, ancho: float, alto: float, fondo: float):
        """Establece las dimensiones del modelo"""
        self.dimensiones['ancho'] = ancho
        self.dimensiones['alto'] = alto
        self.dimensiones['fondo'] = fondo
    
    def obtener_area_superficie(self) -> float:
        """Calcula el área aproximada de superficie de la bolsa"""
        ancho = self.dimensiones['ancho']
        alto = self.dimensiones['alto']
        fondo = self.dimensiones['fondo']
        
        # Cálculo aproximado: 2 caras principales + 2 laterales + base
        area_frontal = ancho * alto * 2
        area_lateral = fondo * alto * 2
        area_base = ancho * fondo
        
        return area_frontal + area_lateral + area_base
    
    def to_dict(self) -> Dict:
        """Convierte el modelo a diccionario"""
        return {
            'id_modelo': self.id_modelo,
            'nombre': self.nombre,
            'tipo': self.tipo,
            'descripcion': self.descripcion,
            'componentes': self.componentes,
            'dimensiones': self.dimensiones,
            'requiere_forro': self.requiere_forro,
            'numero_asas': self.numero_asas,
            'tiene_bolsillos': self.tiene_bolsillos,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'ModeloBolsa':
        """Crea un ModeloBolsa desde un diccionario"""
        modelo = ModeloBolsa(
            data['id_modelo'],
            data['nombre'],
            data['tipo'],
            data.get('descripcion', '')
        )
        modelo.componentes = data.get('componentes', modelo.componentes)
        modelo.dimensiones = data.get('dimensiones', modelo.dimensiones)
        modelo.requiere_forro = data.get('requiere_forro', False)
        modelo.numero_asas = data.get('numero_asas', 2)
        modelo.tiene_bolsillos = data.get('tiene_bolsillos', False)
        modelo.activo = data.get('activo', True)
        modelo.fecha_creacion = data.get('fecha_creacion', modelo.fecha_creacion)
        return modelo


class DisenoAplicado:
    """Representa un diseño con colores aplicados a un modelo"""
    
    def __init__(self, id_diseno: int, id_modelo: int, nombre: str = ""):
        self.id_diseno = id_diseno
        self.id_modelo = id_modelo
        self.nombre = nombre if nombre else f"Diseño {id_diseno}"
        
        # Colores aplicados (códigos hex)
        self.colores_aplicados = {
            'cuerpo_principal': None,
            'cuerpo_secundario': None,
            'asa': None,
            'hilo': None,
            'forro': None,
            'detalles': []
        }
        
        # Configuración de aplicación automática
        self.sincronizar_hilo = True  # El hilo toma el color del cuerpo principal
        self.ajustar_asa_automatico = True  # Asa blanca/negra según contraste
        
        self.fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.guardado = False
    
    def aplicar_color_cuerpo(self, hex_color: str):
        """Aplica color al cuerpo principal"""
        self.colores_aplicados['cuerpo_principal'] = hex_color
        
        # Sincronizar hilo si está activado
        if self.sincronizar_hilo:
            self.colores_aplicados['hilo'] = hex_color
    
    def aplicar_color_secundario(self, hex_color: str):
        """Aplica color al cuerpo secundario (para bolsas combinadas)"""
        self.colores_aplicados['cuerpo_secundario'] = hex_color
    
    def aplicar_color_asa(self, hex_color: str):
        """Aplica color al asa"""
        self.colores_aplicados['asa'] = hex_color
    
    def aplicar_color_forro(self, hex_color: str):
        """Aplica color al forro"""
        self.colores_aplicados['forro'] = hex_color
    
    def ajustar_color_asa_automatico(self, hex_fondo: str):
        """
        Ajusta el color del asa automáticamente (blanco/negro)
        según el contraste con el color de fondo
        """
        from colorsys import rgb_to_hls
        
        # Convertir hex a RGB
        hex_fondo = hex_fondo.lstrip('#')
        r = int(hex_fondo[0:2], 16) / 255.0
        g = int(hex_fondo[2:4], 16) / 255.0
        b = int(hex_fondo[4:6], 16) / 255.0
        
        # Calcular luminosidad
        h, l, s = rgb_to_hls(r, g, b)
        
        # Si el fondo es claro, usar asa negra; si es oscuro, usar asa blanca
        if l > 0.5:
            self.colores_aplicados['asa'] = "#000000"
        else:
            self.colores_aplicados['asa'] = "#FFFFFF"
    
    def agregar_detalle(self, hex_color: str):
        """Agrega un color de detalle"""
        if hex_color not in self.colores_aplicados['detalles']:
            self.colores_aplicados['detalles'].append(hex_color)
    
    def obtener_paleta_completa(self) -> List[str]:
        """Obtiene todos los colores únicos utilizados en el diseño"""
        colores = []
        
        for key, value in self.colores_aplicados.items():
            if key == 'detalles':
                colores.extend(value)
            elif value is not None:
                colores.append(value)
        
        # Retornar lista sin duplicados
        return list(set(colores))
    
    def validar_diseno(self) -> Tuple[bool, List[str]]:
        """
        Valida que el diseño tenga todos los componentes necesarios
        Retorna (es_valido, lista_errores)
        """
        errores = []
        
        if not self.colores_aplicados['cuerpo_principal']:
            errores.append("Falta color del cuerpo principal")
        
        if not self.colores_aplicados['asa']:
            errores.append("Falta color del asa")
        
        if not self.colores_aplicados['hilo']:
            errores.append("Falta color del hilo")
        
        return (len(errores) == 0, errores)
    
    def to_dict(self) -> Dict:
        """Convierte el diseño aplicado a diccionario"""
        return {
            'id_diseno': self.id_diseno,
            'id_modelo': self.id_modelo,
            'nombre': self.nombre,
            'colores_aplicados': self.colores_aplicados,
            'sincronizar_hilo': self.sincronizar_hilo,
            'ajustar_asa_automatico': self.ajustar_asa_automatico,
            'fecha_creacion': self.fecha_creacion,
            'guardado': self.guardado
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'DisenoAplicado':
        """Crea un DisenoAplicado desde un diccionario"""
        diseno = DisenoAplicado(
            data['id_diseno'],
            data['id_modelo'],
            data.get('nombre', '')
        )
        diseno.colores_aplicados = data.get('colores_aplicados', diseno.colores_aplicados)
        diseno.sincronizar_hilo = data.get('sincronizar_hilo', True)
        diseno.ajustar_asa_automatico = data.get('ajustar_asa_automatico', True)
        diseno.fecha_creacion = data.get('fecha_creacion', diseno.fecha_creacion)
        diseno.guardado = data.get('guardado', False)
        return diseno


class DisenoModelosManager:
    """Gestor de modelos de bolsas y diseños aplicados"""
    
    def __init__(self):
        self.modelos: Dict[int, ModeloBolsa] = {}
        self.disenos_aplicados: Dict[int, DisenoAplicado] = {}
        
        self._next_modelo_id = 1
        self._next_diseno_id = 1
        
        # Inicializar con modelos predeterminados
        self._crear_modelos_predeterminados()
    
    def _crear_modelos_predeterminados(self):
        """Crea los modelos de bolsa predeterminados"""
        
        # Modelo Simple
        modelo_simple = ModeloBolsa(
            self._next_modelo_id,
            "Bolsa Simple",
            "SIMPLE",
            "Bolsa de un solo color, diseño clásico y versátil"
        )
        modelo_simple.establecer_dimensiones(30.0, 35.0, 8.0)
        modelo_simple.numero_asas = 2
        self.modelos[self._next_modelo_id] = modelo_simple
        self._next_modelo_id += 1
        
        # Modelo Combinado
        modelo_combinado = ModeloBolsa(
            self._next_modelo_id,
            "Bolsa Combinada",
            "COMBINADO",
            "Bolsa con dos colores principales que se complementan"
        )
        modelo_combinado.establecer_dimensiones(32.0, 38.0, 10.0)
        modelo_combinado.numero_asas = 2
        modelo_combinado.tiene_bolsillos = True
        self.modelos[self._next_modelo_id] = modelo_combinado
        self._next_modelo_id += 1
        
        # Modelo Especial
        modelo_especial = ModeloBolsa(
            self._next_modelo_id,
            "Bolsa Especial",
            "ESPECIAL",
            "Bolsa con diseño elaborado, múltiples colores y detalles"
        )
        modelo_especial.establecer_dimensiones(35.0, 40.0, 12.0)
        modelo_especial.numero_asas = 2
        modelo_especial.requiere_forro = True
        modelo_especial.tiene_bolsillos = True
        self.modelos[self._next_modelo_id] = modelo_especial
        self._next_modelo_id += 1
    
    # ============ GESTIÓN DE MODELOS ============
    
    def agregar_modelo(self, nombre: str, tipo: str, descripcion: str = "") -> ModeloBolsa:
        """Agrega un nuevo modelo de bolsa"""
        modelo = ModeloBolsa(self._next_modelo_id, nombre, tipo, descripcion)
        self.modelos[self._next_modelo_id] = modelo
        self._next_modelo_id += 1
        return modelo
    
    def obtener_modelo(self, id_modelo: int) -> Optional[ModeloBolsa]:
        """Obtiene un modelo por su ID"""
        return self.modelos.get(id_modelo)
    
    def listar_modelos(self, tipo: Optional[str] = None, 
                       solo_activos: bool = True) -> List[ModeloBolsa]:
        """Lista todos los modelos con filtros opcionales"""
        modelos = list(self.modelos.values())
        
        if solo_activos:
            modelos = [m for m in modelos if m.activo]
        
        if tipo:
            modelos = [m for m in modelos if m.tipo == tipo.upper()]
        
        return modelos
    
    def actualizar_modelo(self, id_modelo: int, **kwargs) -> bool:
        """Actualiza los datos de un modelo"""
        modelo = self.modelos.get(id_modelo)
        if not modelo:
            return False
        
        campos_permitidos = ['nombre', 'descripcion', 'requiere_forro', 
                            'numero_asas', 'tiene_bolsillos', 'activo']
        
        for key, value in kwargs.items():
            if key in campos_permitidos and hasattr(modelo, key):
                setattr(modelo, key, value)
        
        return True
    
    def desactivar_modelo(self, id_modelo: int) -> bool:
        """Desactiva un modelo"""
        return self.actualizar_modelo(id_modelo, activo=False)
    
    # ============ GESTIÓN DE DISEÑOS APLICADOS ============
    
    def crear_diseno(self, id_modelo: int, nombre: str = "") -> Optional[DisenoAplicado]:
        """Crea un nuevo diseño basado en un modelo"""
        if id_modelo not in self.modelos:
            return None
        
        diseno = DisenoAplicado(self._next_diseno_id, id_modelo, nombre)
        self.disenos_aplicados[self._next_diseno_id] = diseno
        self._next_diseno_id += 1
        
        return diseno
    
    def obtener_diseno(self, id_diseno: int) -> Optional[DisenoAplicado]:
        """Obtiene un diseño aplicado por su ID"""
        return self.disenos_aplicados.get(id_diseno)
    
    def listar_disenos(self, id_modelo: Optional[int] = None,
                       solo_guardados: bool = False) -> List[DisenoAplicado]:
        """Lista todos los diseños aplicados con filtros opcionales"""
        disenos = list(self.disenos_aplicados.values())
        
        if id_modelo:
            disenos = [d for d in disenos if d.id_modelo == id_modelo]
        
        if solo_guardados:
            disenos = [d for d in disenos if d.guardado]
        
        return disenos
    
    def aplicar_colores_automaticos(self, id_diseno: int, 
                                    colores_hex: List[str]) -> bool:
        """
        Aplica colores automáticamente según el tipo de modelo
        """
        diseno = self.disenos_aplicados.get(id_diseno)
        if not diseno:
            return False
        
        modelo = self.modelos.get(diseno.id_modelo)
        if not modelo or not colores_hex:
            return False
        
        # Aplicar color principal
        diseno.aplicar_color_cuerpo(colores_hex[0])
        
        # Para modelos combinados, aplicar segundo color si existe
        if modelo.tipo == 'COMBINADO' and len(colores_hex) > 1:
            diseno.aplicar_color_secundario(colores_hex[1])
        
        # Para modelos especiales, agregar detalles
        if modelo.tipo == 'ESPECIAL' and len(colores_hex) > 2:
            for color in colores_hex[2:]:
                diseno.agregar_detalle(color)
        
        # Ajustar asa automáticamente
        if diseno.ajustar_asa_automatico:
            diseno.ajustar_color_asa_automatico(colores_hex[0])
        
        # Aplicar forro si el modelo lo requiere
        if modelo.requiere_forro and len(colores_hex) > 1:
            diseno.aplicar_color_forro(colores_hex[-1])
        
        return True
    
    def guardar_diseno(self, id_diseno: int) -> bool:
        """Marca un diseño como guardado"""
        diseno = self.disenos_aplicados.get(id_diseno)
        if not diseno:
            return False
        
        es_valido, errores = diseno.validar_diseno()
        if not es_valido:
            print(f"No se puede guardar el diseño. Errores: {', '.join(errores)}")
            return False
        
        diseno.guardado = True
        return True
    
    def eliminar_diseno(self, id_diseno: int) -> bool:
        """Elimina un diseño aplicado"""
        if id_diseno in self.disenos_aplicados:
            del self.disenos_aplicados[id_diseno]
            return True
        return False
    
    # ============ ANÁLISIS Y REPORTES ============
    
    def obtener_estadisticas_modelo(self, id_modelo: int) -> Optional[Dict]:
        """Obtiene estadísticas de uso de un modelo"""
        modelo = self.modelos.get(id_modelo)
        if not modelo:
            return None
        
        disenos_del_modelo = [d for d in self.disenos_aplicados.values() 
                             if d.id_modelo == id_modelo]
        
        return {
            'id_modelo': id_modelo,
            'nombre': modelo.nombre,
            'tipo': modelo.tipo,
            'total_disenos': len(disenos_del_modelo),
            'disenos_guardados': sum(1 for d in disenos_del_modelo if d.guardado),
            'area_superficie': modelo.obtener_area_superficie()
        }
    
    def obtener_colores_mas_usados(self, limite: int = 5) -> List[Tuple[str, int]]:
        """Obtiene los colores más utilizados en los diseños"""
        contador_colores = {}
        
        for diseno in self.disenos_aplicados.values():
            if diseno.guardado:
                paleta = diseno.obtener_paleta_completa()
                for color in paleta:
                    contador_colores[color] = contador_colores.get(color, 0) + 1
        
        # Ordenar por uso y retornar top
        colores_ordenados = sorted(contador_colores.items(), 
                                   key=lambda x: x[1], reverse=True)
        return colores_ordenados[:limite]
    
    # ============ PERSISTENCIA ============
    
    def guardar_datos(self, archivo_modelos: str = "modelos.json",
                     archivo_disenos: str = "disenos_aplicados.json") -> bool:
        """Guarda modelos y diseños en archivos JSON"""
        try:
            # Guardar modelos
            datos_modelos = {
                'modelos': [m.to_dict() for m in self.modelos.values()],
                'contadores': {
                    'next_modelo_id': self._next_modelo_id
                }
            }
            
            with open(archivo_modelos, 'w', encoding='utf-8') as f:
                json.dump(datos_modelos, f, ensure_ascii=False, indent=2)
            
            # Guardar diseños aplicados
            datos_disenos = {
                'disenos': [d.to_dict() for d in self.disenos_aplicados.values()],
                'contadores': {
                    'next_diseno_id': self._next_diseno_id
                }
            }
            
            with open(archivo_disenos, 'w', encoding='utf-8') as f:
                json.dump(datos_disenos, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Error al guardar datos: {e}")
            return False
    
    def cargar_datos(self, archivo_modelos: str = "modelos.json",
                    archivo_disenos: str = "disenos_aplicados.json") -> bool:
        """Carga modelos y diseños desde archivos JSON"""
        try:
            # Cargar modelos
            with open(archivo_modelos, 'r', encoding='utf-8') as f:
                datos_modelos = json.load(f)
            
            self.modelos = {
                m['id_modelo']: ModeloBolsa.from_dict(m)
                for m in datos_modelos.get('modelos', [])
            }
            
            contadores = datos_modelos.get('contadores', {})
            self._next_modelo_id = contadores.get('next_modelo_id', 1)
            
            # Cargar diseños
            with open(archivo_disenos, 'r', encoding='utf-8') as f:
                datos_disenos = json.load(f)
            
            self.disenos_aplicados = {
                d['id_diseno']: DisenoAplicado.from_dict(d)
                for d in datos_disenos.get('disenos', [])
            }
            
            contadores = datos_disenos.get('contadores', {})
            self._next_diseno_id = contadores.get('next_diseno_id', 1)
            
            return True
        except FileNotFoundError:
            print("Archivos no encontrados. Usando modelos predeterminados.")
            return False
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            return False
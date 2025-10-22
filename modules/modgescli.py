"""
Módulo de Gestión de Clientes para ChromaBags
Maneja información de clientes, historial y preferencias
"""

import json
from datetime import datetime
from typing import List, Dict, Optional


class Cliente:
    """Clase para representar un cliente"""
    
    def __init__(self, id_cliente: int, nombre: str, telefono: str = "",
                 email: str = "", direccion: str = ""):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.direccion = direccion
        self.fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.activo = True
        self.notas = ""
        
        # Preferencias del cliente
        self.preferencias = {
            'colores_favoritos': [],  # IDs de colores
            'disenos_favoritos': [],  # IDs de diseños
            'tipo_bolsa_preferido': ""  # Simple, Combinado, Especial
        }
        
        # Historial
        self.historial_compras = []  # Lista de IDs de pedidos
        self.total_compras = 0.0
        self.numero_pedidos = 0
    
    def agregar_preferencia_color(self, id_color: int):
        """Agrega un color a las preferencias del cliente"""
        if id_color not in self.preferencias['colores_favoritos']:
            self.preferencias['colores_favoritos'].append(id_color)
    
    def agregar_preferencia_diseno(self, id_diseno: int):
        """Agrega un diseño a las preferencias del cliente"""
        if id_diseno not in self.preferencias['disenos_favoritos']:
            self.preferencias['disenos_favoritos'].append(id_diseno)
    
    def establecer_tipo_bolsa_preferido(self, tipo: str):
        """Establece el tipo de bolsa preferido"""
        self.preferencias['tipo_bolsa_preferido'] = tipo
    
    def agregar_compra(self, id_pedido: int, monto: float):
        """Registra una nueva compra en el historial"""
        self.historial_compras.append({
            'id_pedido': id_pedido,
            'monto': monto,
            'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self.total_compras += monto
        self.numero_pedidos += 1
    
    def obtener_promedio_compra(self) -> float:
        """Calcula el promedio de compra del cliente"""
        if self.numero_pedidos == 0:
            return 0.0
        return self.total_compras / self.numero_pedidos
    
    def to_dict(self) -> Dict:
        """Convierte el cliente a diccionario"""
        return {
            'id_cliente': self.id_cliente,
            'nombre': self.nombre,
            'telefono': self.telefono,
            'email': self.email,
            'direccion': self.direccion,
            'fecha_registro': self.fecha_registro,
            'activo': self.activo,
            'notas': self.notas,
            'preferencias': self.preferencias,
            'historial_compras': self.historial_compras,
            'total_compras': self.total_compras,
            'numero_pedidos': self.numero_pedidos
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Cliente':
        """Crea un Cliente desde un diccionario"""
        cliente = Cliente(
            data['id_cliente'],
            data['nombre'],
            data.get('telefono', ''),
            data.get('email', ''),
            data.get('direccion', '')
        )
        cliente.fecha_registro = data.get('fecha_registro', cliente.fecha_registro)
        cliente.activo = data.get('activo', True)
        cliente.notas = data.get('notas', '')
        cliente.preferencias = data.get('preferencias', cliente.preferencias)
        cliente.historial_compras = data.get('historial_compras', [])
        cliente.total_compras = data.get('total_compras', 0.0)
        cliente.numero_pedidos = data.get('numero_pedidos', 0)
        return cliente


class ClientesManager:
    """Gestor principal de clientes"""
    
    def __init__(self):
        self.clientes: Dict[int, Cliente] = {}
        self._next_cliente_id = 1
    
    # ============ OPERACIONES BÁSICAS ============
    
    def agregar_cliente(self, nombre: str, telefono: str = "",
                       email: str = "", direccion: str = "") -> Cliente:
        """Agrega un nuevo cliente"""
        if not nombre or nombre.strip() == "":
            raise ValueError("El nombre del cliente no puede estar vacío")
        
        cliente = Cliente(self._next_cliente_id, nombre.strip(), 
                         telefono.strip(), email.strip(), direccion.strip())
        self.clientes[self._next_cliente_id] = cliente
        self._next_cliente_id += 1
        return cliente
    
    def obtener_cliente(self, id_cliente: int) -> Optional[Cliente]:
        """Obtiene un cliente por su ID"""
        return self.clientes.get(id_cliente)
    
    def listar_clientes(self, solo_activos: bool = True) -> List[Cliente]:
        """Lista todos los clientes"""
        if solo_activos:
            return [c for c in self.clientes.values() if c.activo]
        return list(self.clientes.values())
    
    def actualizar_cliente(self, id_cliente: int, **kwargs) -> bool:
        """Actualiza los datos de un cliente existente"""
        cliente = self.clientes.get(id_cliente)
        if not cliente:
            return False
        
        # Campos actualizables directamente
        campos_permitidos = ['nombre', 'telefono', 'email', 'direccion', 'notas']
        
        for key, value in kwargs.items():
            if key in campos_permitidos and hasattr(cliente, key):
                setattr(cliente, key, value)
        
        return True
    
    def desactivar_cliente(self, id_cliente: int) -> bool:
        """Desactiva un cliente (no lo elimina)"""
        cliente = self.clientes.get(id_cliente)
        if not cliente:
            return False
        cliente.activo = False
        return True
    
    def reactivar_cliente(self, id_cliente: int) -> bool:
        """Reactiva un cliente previamente desactivado"""
        cliente = self.clientes.get(id_cliente)
        if not cliente:
            return False
        cliente.activo = True
        return True
    
    def eliminar_cliente(self, id_cliente: int) -> bool:
        """Elimina permanentemente un cliente (usar con precaución)"""
        if id_cliente in self.clientes:
            del self.clientes[id_cliente]
            return True
        return False
    
    # ============ BÚSQUEDA Y FILTRADO ============
    
    def buscar_clientes(self, termino: str) -> List[Cliente]:
        """Busca clientes por nombre, teléfono o email"""
        termino = termino.lower().strip()
        if not termino:
            return []
        
        resultados = []
        for cliente in self.clientes.values():
            if (termino in cliente.nombre.lower() or
                termino in cliente.telefono.lower() or
                termino in cliente.email.lower()):
                resultados.append(cliente)
        
        return resultados
    
    def obtener_clientes_por_preferencia_color(self, id_color: int) -> List[Cliente]:
        """Obtiene clientes que prefieren un color específico"""
        return [c for c in self.clientes.values() 
                if id_color in c.preferencias['colores_favoritos'] and c.activo]
    
    def obtener_clientes_por_preferencia_diseno(self, id_diseno: int) -> List[Cliente]:
        """Obtiene clientes que prefieren un diseño específico"""
        return [c for c in self.clientes.values() 
                if id_diseno in c.preferencias['disenos_favoritos'] and c.activo]
    
    def obtener_clientes_por_tipo_bolsa(self, tipo_bolsa: str) -> List[Cliente]:
        """Obtiene clientes que prefieren un tipo de bolsa específico"""
        return [c for c in self.clientes.values() 
                if c.preferencias['tipo_bolsa_preferido'] == tipo_bolsa and c.activo]
    
    # ============ GESTIÓN DE PREFERENCIAS ============
    
    def agregar_preferencia_color(self, id_cliente: int, id_color: int) -> bool:
        """Agrega un color favorito a las preferencias del cliente"""
        cliente = self.clientes.get(id_cliente)
        if not cliente:
            return False
        cliente.agregar_preferencia_color(id_color)
        return True
    
    def agregar_preferencia_diseno(self, id_cliente: int, id_diseno: int) -> bool:
        """Agrega un diseño favorito a las preferencias del cliente"""
        cliente = self.clientes.get(id_cliente)
        if not cliente:
            return False
        cliente.agregar_preferencia_diseno(id_diseno)
        return True
    
    def establecer_tipo_bolsa_preferido(self, id_cliente: int, tipo: str) -> bool:
        """Establece el tipo de bolsa preferido del cliente"""
        cliente = self.clientes.get(id_cliente)
        if not cliente:
            return False
        cliente.establecer_tipo_bolsa_preferido(tipo)
        return True
    
    def eliminar_preferencia_color(self, id_cliente: int, id_color: int) -> bool:
        """Elimina un color de las preferencias del cliente"""
        cliente = self.clientes.get(id_cliente)
        if not cliente:
            return False
        
        if id_color in cliente.preferencias['colores_favoritos']:
            cliente.preferencias['colores_favoritos'].remove(id_color)
            return True
        return False
    
    # ============ GESTIÓN DE HISTORIAL ============
    
    def registrar_compra(self, id_cliente: int, id_pedido: int, monto: float) -> bool:
        """Registra una compra en el historial del cliente"""
        cliente = self.clientes.get(id_cliente)
        if not cliente:
            return False
        
        if monto < 0:
            raise ValueError("El monto no puede ser negativo")
        
        cliente.agregar_compra(id_pedido, monto)
        return True
    
    def obtener_historial_cliente(self, id_cliente: int) -> List[Dict]:
        """Obtiene el historial de compras de un cliente"""
        cliente = self.clientes.get(id_cliente)
        if not cliente:
            return []
        return cliente.historial_compras
    
    def obtener_estadisticas_cliente(self, id_cliente: int) -> Optional[Dict]:
        """Obtiene estadísticas de compra de un cliente"""
        cliente = self.clientes.get(id_cliente)
        if not cliente:
            return None
        
        return {
            'id_cliente': cliente.id_cliente,
            'nombre': cliente.nombre,
            'numero_pedidos': cliente.numero_pedidos,
            'total_compras': cliente.total_compras,
            'promedio_compra': cliente.obtener_promedio_compra(),
            'fecha_registro': cliente.fecha_registro,
            'ultima_compra': cliente.historial_compras[-1] if cliente.historial_compras else None
        }
    
    # ============ REPORTES Y ANÁLISIS ============
    
    def obtener_mejores_clientes(self, limite: int = 10) -> List[Cliente]:
        """Obtiene los clientes con mayor total de compras"""
        clientes_activos = [c for c in self.clientes.values() if c.activo]
        return sorted(clientes_activos, 
                     key=lambda c: c.total_compras, 
                     reverse=True)[:limite]
    
    def obtener_clientes_frecuentes(self, limite: int = 10) -> List[Cliente]:
        """Obtiene los clientes con mayor número de pedidos"""
        clientes_activos = [c for c in self.clientes.values() if c.activo]
        return sorted(clientes_activos, 
                     key=lambda c: c.numero_pedidos, 
                     reverse=True)[:limite]
    
    def obtener_clientes_inactivos(self, dias: int = 90) -> List[Cliente]:
        """Obtiene clientes que no han comprado en X días"""
        # Nota: Esta función requeriría comparar fechas de última compra
        # Por ahora retorna clientes sin compras
        return [c for c in self.clientes.values() 
                if c.activo and c.numero_pedidos == 0]
    
    def obtener_total_clientes(self) -> Dict[str, int]:
        """Obtiene conteo de clientes por estado"""
        activos = sum(1 for c in self.clientes.values() if c.activo)
        inactivos = sum(1 for c in self.clientes.values() if not c.activo)
        
        return {
            'total': len(self.clientes),
            'activos': activos,
            'inactivos': inactivos
        }
    
    # ============ PERSISTENCIA ============
    
    def guardar_clientes(self, archivo: str = "clientes.json") -> bool:
        """Guarda todos los clientes en un archivo JSON"""
        try:
            datos = {
                'clientes': [c.to_dict() for c in self.clientes.values()],
                'contadores': {
                    'next_cliente_id': self._next_cliente_id
                }
            }
            
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Error al guardar clientes: {e}")
            return False
    
    def cargar_clientes(self, archivo: str = "clientes.json") -> bool:
        """Carga todos los clientes desde un archivo JSON"""
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            # Cargar clientes
            self.clientes = {
                c['id_cliente']: Cliente.from_dict(c) 
                for c in datos.get('clientes', [])
            }
            
            # Cargar contador
            contadores = datos.get('contadores', {})
            self._next_cliente_id = contadores.get('next_cliente_id', 1)
            
            return True
        except FileNotFoundError:
            print(f"Archivo {archivo} no encontrado. Iniciando sin clientes.")
            return False
        except Exception as e:
            print(f"Error al cargar clientes: {e}")
            return False


# ============ EJEMPLO DE USO ============
if __name__ == "__main__":
    pass
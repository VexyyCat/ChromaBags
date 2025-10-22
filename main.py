from modules.modcatal import CatalogosManager
from modules.modgescli import ClientesManager

print("Módulo de catálogos cargado correctamente.")

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


print("\nMódulo de gestión de clientes cargado correctamente.")

gescli = ClientesManager()
    
    # Agregar clientes
cliente1 = gescli.agregar_cliente(
    "María González López",
    telefono="442-123-4567",
    email="maria.gonzalez@email.com",
    direccion="Av. Principal #123, Querétaro")
print(f"✓ Cliente agregado: {cliente1.nombre} (ID: {cliente1.id_cliente})")
    
cliente2 = gescli.agregar_cliente(
    "Juan Pérez Ramírez",
    telefono="442-987-6543",
    email="juan.perez@email.com",
    direccion="Calle Secundaria #456")
    
cliente3 = gescli.agregar_cliente(
    "Ana Martínez",
    telefono="442-555-1234",
    email="ana.martinez@email.com")
    
    # Agregar preferencias
gescli.agregar_preferencia_color(1, 1)  # María prefiere color ID 1
gescli.agregar_preferencia_color(1, 3)  # María prefiere color ID 3
gescli.establecer_tipo_bolsa_preferido(1, "Combinado")
    
gescli.agregar_preferencia_diseno(2, 1)  # Juan prefiere diseño ID 1
gescli.establecer_tipo_bolsa_preferido(2, "Simple")
    
    # Registrar compras
gescli.registrar_compra(1, 1001, 450.00)
gescli.registrar_compra(1, 1002, 320.00)
gescli.registrar_compra(2, 1003, 580.00)
    
# Listar clientes
print("\n=== LISTA DE CLIENTES ACTIVOS ===")
for cliente in gescli.listar_clientes():
    print(f"- {cliente.nombre}")
    print(f"  Teléfono: {cliente.telefono}")
    print(f"  Email: {cliente.email}")
    print(f"  Pedidos realizados: {cliente.numero_pedidos}")
    print(f"  Total de compras: ${cliente.total_compras:.2f}")
    print(f"  Promedio por compra: ${cliente.obtener_promedio_compra():.2f}")
    
# Buscar clientes
print("\n=== BÚSQUEDA: 'María' ===")
resultados = gescli.buscar_clientes("María")
for cliente in resultados:
    print(f"- {cliente.nombre} ({cliente.email})")
    
# Mejores clientes
print("\n=== TOP 3 MEJORES CLIENTES ===")
for i, cliente in enumerate(gescli.obtener_mejores_clientes(3), 1):
    print(f"{i}. {cliente.nombre} - ${cliente.total_compras:.2f}")
    
# Estadísticas de un cliente
print("\n=== ESTADÍSTICAS DE CLIENTE 1 ===")
stats = gescli.obtener_estadisticas_cliente(1)
if stats:
    print(f"Nombre: {stats['nombre']}")
    print(f"Total de pedidos: {stats['numero_pedidos']}")
    print(f"Total gastado: ${stats['total_compras']:.2f}")
    print(f"Promedio por pedido: ${stats['promedio_compra']:.2f}")
    
# Resumen general
print("\n=== RESUMEN GENERAL ===")
totales = gescli.obtener_total_clientes()
print(f"Total de clientes: {totales['total']}")
print(f"Clientes activos: {totales['activos']}")
print(f"Clientes inactivos: {totales['inactivos']}")
    
# Guardar clientes
if gescli.guardar_clientes():
    print("\n✓ Base de clientes guardada exitosamente")
    
# Simular carga
gescli_nuevo = ClientesManager()
if gescli_nuevo.cargar_clientes():
    print("✓ Base de clientes cargada exitosamente")
    print(f"Total de clientes cargados: {len(gescli_nuevo.clientes)}")
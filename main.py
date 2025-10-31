from modules.modcatal import CatalogosManager
from modules.modgescli import ClientesManager
from modules.modcomcolo import CombinacionColoresManager
from modules.modboldis import DisenoModelosManager

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


print("\nMódulo de combinaciones de colores cargado correctamente.")
gescomcolo = CombinacionColoresManager()
    
# Color base para ejemplos
color_base = "#3498DB"  # Azul
    
print("=== GENERACIÓN DE ESQUEMAS DE COLOR ===\n")
    
# Generar diferentes tipos de esquemas
print(f"Color base: {color_base}")
print()
    
print("1. Esquema Complementario:")
colores = gescomcolo.generar_complementario(color_base)
for i, color in enumerate(colores, 1):
    print(f"   Color {i}: {color}")
    
print("\n2. Esquema Análogo (3 colores):")
colores = gescomcolo.generar_analogo(color_base, 3)
for i, color in enumerate(colores, 1):
    print(f"   Color {i}: {color}")
    
print("\n3. Esquema Triádico:")
colores = gescomcolo.generar_triadico(color_base)
for i, color in enumerate(colores, 1):
    print(f"   Color {i}: {color}")
    
print("\n4. Esquema Tetrádico:")
colores = gescomcolo.generar_tetradico(color_base)
for i, color in enumerate(colores, 1):
    print(f"   Color {i}: {color}")
    
print("\n5. Esquema Monocromático:")
colores = gescomcolo.generar_monocromatico(color_base, 4)
for i, color in enumerate(colores, 1):
    print(f"   Color {i}: {color}")
    
print("\n6. Esquema Armónico:")
colores = gescomcolo.generar_armonico(color_base, 3)
for i, color in enumerate(colores, 1):
    print(f"   Color {i}: {color}")
    
# Guardar combinaciones
print("\n=== GUARDANDO COMBINACIONES ===\n")
    
comb1 = gescomcolo.guardar_combinacion(
    "Azul Océano",
    "Complementario",
    gescomcolo.generar_complementario(color_base),
    "Combinación complementaria basada en azul océano"
)
print(f"✓ Guardada: {comb1.nombre} (ID: {comb1.id_combinacion})")
    
comb2 = gescomcolo.guardar_combinacion(
    "Armonía Natural",
    "Análogo",
    gescomcolo.generar_analogo(color_base, 3),
    "Colores análogos para diseños naturales"
)
print(f"✓ Guardada: {comb2.nombre} (ID: {comb2.id_combinacion})")
    
gescomcolo.marcar_favorito(1, True)
    
# Análisis de colores
print("\n=== ANÁLISIS DE COLORES ===\n")
    
color1 = "#3498DB"
color2 = "#E74C3C"
    
contraste = gescomcolo.calcular_contraste(color1, color2)
print(f"Contraste entre {color1} y {color2}: {contraste:.2f}")
    
print(f"\n¿{color1} es claro? {gescomcolo.es_color_claro(color1)}")
print(f"Color de texto sugerido para fondo {color1}: {gescomcolo.sugerir_color_texto(color1)}")
    
# Listar combinaciones guardadas
print("\n=== COMBINACIONES GUARDADAS ===\n")
for comb in gescomcolo.listar_combinaciones():
    print(f"- {comb.nombre} ({comb.tipo_esquema})")
    print(f"  Colores: {', '.join(comb.colores_hex)}")
    print(f"  Favorito: {'Sí' if comb.favorito else 'No'}")
    
# Guardar en archivo
if gescomcolo.guardar_datos():
    print("\n✓ Combinaciones guardadas en archivo")

print("\nMódulo de diseños de modelos de bolsa cargado correctamente.")
gesboldis = DisenoModelosManager()
    
print("=== MODELOS DE BOLSA DISPONIBLES ===\n")
for modelo in gesboldis.listar_modelos():
    print(f"ID: {modelo.id_modelo} - {modelo.nombre} ({modelo.tipo})")
    print(f"  Descripción: {modelo.descripcion}")
    print(f"  Dimensiones: {modelo.dimensiones['ancho']}x{modelo.dimensiones['alto']}x{modelo.dimensiones['fondo']} cm")
    print(f"  Área superficie: {modelo.obtener_area_superficie():.2f} cm²")
    print(f"  Asas: {modelo.numero_asas}")
    print(f"  Requiere forro: {'Sí' if modelo.requiere_forro else 'No'}")
    print()
    
# Crear diseños
print("=== CREANDO DISEÑOS ===\n")
    
# Diseño simple
diseno1 = gesboldis.crear_diseno(1, "Bolsa Roja Clásica")
if diseno1:
    colores_simple = ["#E74C3C"]
    gesboldis.aplicar_colores_automaticos(diseno1.id_diseno, colores_simple)
    gesboldis.guardar_diseno(diseno1.id_diseno)
    print(f"✓ Diseño creado: {diseno1.nombre}")
    print(f"  Colores aplicados: {diseno1.obtener_paleta_completa()}")
    
# Diseño combinado
diseno2 = gesboldis.crear_diseno(2, "Bolsa Bicolor Azul-Amarillo")
if diseno2:
    colores_combinado = ["#3498DB", "#F1C40F"]
    gesboldis.aplicar_colores_automaticos(diseno2.id_diseno, colores_combinado)
    gesboldis.guardar_diseno(diseno2.id_diseno)
    print(f"✓ Diseño creado: {diseno2.nombre}")
    print(f"  Colores aplicados: {diseno2.obtener_paleta_completa()}")
    
# Diseño especial
diseno3 = gesboldis.crear_diseno(3, "Bolsa Premium Multicolor")
if diseno3:
    colores_especial = ["#9B59B6", "#E67E22", "#1ABC9C", "#ECF0F1"]
    gesboldis.aplicar_colores_automaticos(diseno3.id_diseno, colores_especial)
    gesboldis.guardar_diseno(diseno3.id_diseno)
    print(f"✓ Diseño creado: {diseno3.nombre}")
    print(f"  Colores aplicados: {diseno3.obtener_paleta_completa()}")
    
# Estadísticas
print("\n=== ESTADÍSTICAS ===\n")
for modelo in gesboldis.listar_modelos():
    stats = gesboldis.obtener_estadisticas_modelo(modelo.id_modelo)
    if stats:
        print(f"{stats['nombre']}:")
        print(f"  Total de diseños: {stats['total_disenos']}")
        print(f"  Diseños guardados: {stats['disenos_guardados']}")
    
# Colores más usados
print("\n=== COLORES MÁS UTILIZADOS ===\n")
colores_top = gesboldis.obtener_colores_mas_usados(5)
for i, (color, veces) in enumerate(colores_top, 1):
    print(f"{i}. {color} - usado {veces} veces")
    
# Guardar
if gesboldis.guardar_datos():
    print("\n✓ Datos guardados exitosamente")
from modules.modcatal import CatalogosManager

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
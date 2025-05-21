from pydantic import BaseModel

from ollama import chat


# Definir el esquema para los productos
class Producto(BaseModel):
    nombre: str
    precio: float
    categoria: str
    disponible: bool
    cantidad_inventario: int


class CatalogoProductos(BaseModel):
    productos: list[Producto]


# Realizar la consulta al modelo
response = chat(
    model='llama3.1:8b',
    messages=[{
        'role': 'user', 
        'content': '''Dame información sobre 3 productos de una tienda de electrónicos:
        1. Un iPhone 14 que cuesta 19999.99 pesos, de la categoría smartphones, está disponible y hay 5 unidades
        2. Una MacBook Pro que cuesta 34999.99 pesos, de la categoría laptops, está disponible y hay 3 unidades
        3. Unos AirPods que cuestan 4999.99 pesos, de la categoría audio, no están disponibles y hay 0 unidades.
        Devuelve la lista en formato JSON.'''
    }],
    format=CatalogoProductos.model_json_schema(),
    options={'temperature': 0},  # Hacer las respuestas más deterministas
)

# Usar Pydantic para validar la respuesta
catalogo = CatalogoProductos.model_validate_json(response.message.content)
print("\nCatálogo de Productos:")
for producto in catalogo.productos:
    print(f"\nProducto: {producto.nombre}")
    print(f"Precio: ${producto.precio:,.2f}")
    print(f"Categoría: {producto.categoria}")
    print(f"Disponible: {'Sí' if producto.disponible else 'No'}")
    print(f"Inventario: {producto.cantidad_inventario} unidades")

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def inicio():
    return {
        "success": True,
        "statusCode": 200,
        "message": "API de Taller Evaluado 1 funcionando correctamente",
        "data": None
    }

@app.get("/usuarios")
def obtener_usuarios():
    return {
        "success": True,
        "statusCode": 200,
        "message": "Lista de usuarios obtenida con éxito",
        "data": ["pedro", "maria", "fernanda"]
    }

@app.get("/productos")
def obtener_productos():
    return {
        "success": True,
        "statusCode": 200,
        "message": "Productos encontrados",
        "data": [{"id": 1, "nombre": "Notebook"}]
    }
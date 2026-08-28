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
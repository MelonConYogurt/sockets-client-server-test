from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from enum import Enum

app = FastAPI()

class RoleEnum(str, Enum):
    admin = "admin"
    jefe = "manager"
    empleado = "empleado"

class User(BaseModel):
    id: int
    nombre: str
    rol: RoleEnum
    estado: bool = True

class Message(BaseModel):
    id: int
    usuario_envia_id: int
    mensaje_id: int
    contenido: str
    priorida: int
    estado_lectura: bool = False

# guardamos los datos de forma local para hacer las pruebas
usuarios = []
mensajes = []

@app.post("/usuarios/")
def crear_usuario(user: User):
    usuarios.append(user)
    return user

@app.get("/usuarios/")
def obtener_usuarios():
    return usuarios

@app.post("/mensajes/", response_model=Message)
def enviar_mensaje(message: Message):
    mensajes.append(message)
    return message

@app.get("/mensajes/", response_model=List[Message])
def obtener_mensaje():
    return mensajes

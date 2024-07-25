import socket

informacion = {
    'Python': 'Un lenguaje de programación interpretado.',
    'JavaScript': 'Un lenguaje de programación que se usa principalmente en el navegador web.',
}

HOST = '127.0.0.1'  # Dirección IP del servidor
PORT = 65432        # Puerto de conexión

def manejar_cliente(conn, addr):
    print(f"Conectado a {addr}")
    try:
        while True:
            menu = "Menu\n1. Consultar temas.\n2. Listar todos los temas.\n3. Ingresar nuevo tema\n4. Salir\n"
            conn.send(menu.encode('utf-8'))

            respuesta_menu = conn.recv(1024).decode('utf-8').strip()
            if respuesta_menu == '1':
                consulta_tema_mensaje = "Ingrese el tema que desea buscar:\n"
                conn.send(consulta_tema_mensaje.encode('utf-8'))
                
                respuesta_consulta_tema = conn.recv(1024).decode('utf-8').strip()
                if respuesta_consulta_tema in informacion:
                    mensaje = f"Definición de {respuesta_consulta_tema}: {informacion[respuesta_consulta_tema]}\n"
                else:
                    mensaje = f"Tema {respuesta_consulta_tema} no encontrado.\n"
                conn.send(mensaje.encode('utf-8'))
            
            elif respuesta_menu == '2':
                lista_temas = "\n".join([f"{tema}: {definicion}" for tema, definicion in informacion.items()]) + "\n"
                conn.send(lista_temas.encode('utf-8'))
            
            elif respuesta_menu == '3':
                mensaje_nuevo_tema = "Ingrese el nuevo tema:\n"
                conn.send(mensaje_nuevo_tema.encode('utf-8'))
                
                nuevo_tema = conn.recv(1024).decode('utf-8').strip()
                
                mensaje_nueva_definicion = "Ingrese la definición del nuevo tema:\n"
                conn.send(mensaje_nueva_definicion.encode('utf-8'))
                
                nueva_definicion = conn.recv(1024).decode('utf-8').strip()
                
                informacion[nuevo_tema] = nueva_definicion
                confirmacion = f"Nuevo tema '{nuevo_tema}' agregado con éxito.\n"
                conn.send(confirmacion.encode('utf-8'))
            
            elif respuesta_menu == '4':
                print(f"Cliente {addr} desconectado.")
                break
            
            else:
                conn.send("Opción no válida. Intente de nuevo.\n".encode('utf-8'))
    except (ConnectionResetError, ConnectionAbortedError):
        print(f"Conexión con {addr} perdida.")
    finally:
        conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Servidor escuchando en {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        manejar_cliente(conn, addr)

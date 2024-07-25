import socket

HOST = '127.0.0.1'  # Dirección IP del servidor
PORT = 65432        # Puerto de conexión

def recibir_y_mostrar(s):
    """
    Recibe datos del servidor y los muestra en la consola.

    Parametros:
    s (socket): El socket de conexión con el servidor.

    Returns:
    bool: True si se recibieron y mostraron los datos correctamente, False en caso contrario.
    """
    try:
        data = s.recv(1024).decode('utf-8')
        if not data:
            raise ConnectionError("Conexión perdida.")
        print("-----------------------------------")
        print(f"Respuesta del servidor:\n\n{data}")
        print("-----------------------------------")
    except ConnectionError as e:
        print(e)
        return False
    return True

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    while True:
        menu = s.recv(1024).decode('utf-8')
        print(menu)
        
        command = input("Ingrese una opción: ").strip()
        s.sendall(command.encode('utf-8'))
        
        if command == '1':
            additional_info = s.recv(1024).decode('utf-8')
            print(additional_info)
            response = input().strip()
            s.sendall(response.encode('utf-8'))
        elif command == "3":
            additional_info = s.recv(1024).decode('utf-8')
            print(additional_info)
            response = input().strip()
            s.sendall(response.encode('utf-8'))
            
            additional_info_2 = s.recv(1024).decode('utf-8')
            print(additional_info_2)
            response_2 = input().strip()
            s.sendall(response_2.encode('utf-8'))
        
        if not recibir_y_mostrar(s):
            break
        if command == '4':
            print("Desconectando del servidor.")
            break

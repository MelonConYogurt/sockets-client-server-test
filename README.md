
## Descripción

Este proyecto consiste en una aplicación cliente-servidor simple escrita en Python. El servidor ofrece un menú a los clientes conectados para consultar, listar y añadir temas con sus respectivas definiciones. El cliente interactúa con el servidor a través de una conexión de red utilizando sockets.

## Requisitos

- Python 3.x
- Biblioteca estándar de Python

## Estructura del Proyecto

El proyecto consta de dos archivos principales:

1. **Servidor (`servidor.py`)**: Este archivo contiene el código del servidor que maneja las conexiones de los clientes y proporciona un menú interactivo.
2. **Cliente (`cliente.py`)**: Este archivo contiene el código del cliente que se conecta al servidor y permite interactuar con el menú proporcionado por el servidor.

## Ejecución del Proyecto

### Ejecutar el Servidor

1. Abre una terminal.
2. Navega hasta el directorio donde se encuentra el archivo `servidor.py`.
3. Ejecuta el siguiente comando:

    ```sh
    python servidor.py
    ```

   Esto iniciará el servidor y lo pondrá a escuchar conexiones en `127.0.0.1` en el puerto `65432`.

### Ejecutar el Cliente

1. Abre una nueva terminal.
2. Navega hasta el directorio donde se encuentra el archivo `cliente.py`.
3. Ejecuta el siguiente comando:

    ```sh
    python cliente.py
    ```

   Esto iniciará el cliente y lo conectará al servidor en `127.0.0.1` en el puerto `65432`.

## Funcionalidades

### Menú del Servidor

El servidor ofrece las siguientes opciones a través de un menú interactivo:

1. **Consultar temas**: Permite al cliente buscar la definición de un tema específico.
2. **Listar todos los temas**: Muestra una lista de todos los temas y sus definiciones.
3. **Ingresar nuevo tema**: Permite al cliente añadir un nuevo tema con su respectiva definición.
4. **Salir**: Desconecta al cliente del servidor.

### Comunicación entre Cliente y Servidor

- El cliente recibe el menú del servidor y envía su selección.
- Según la selección, el servidor solicita información adicional si es necesario (por ejemplo, el nombre y la definición de un nuevo tema).
- El servidor envía la respuesta correspondiente que se muestra en la consola del cliente.

## Código del Servidor (`servidor.py`)

```python
import socket

informacion = {
    'Python': 'Un lenguaje de programación interpretado.',
    'JavaScript': 'Un lenguaje de programación que se usa principalmente en el navegador web.',
}

HOST = '127.0.0.1'  # Dirección IP del servidor
PORT = 65432        # Puerto de conexión

def manejar_cliente(conn, addr):
    """
    Maneja la conexión con un cliente.

    Parametros
    - conn: objeto de conexión del cliente
    - addr: dirección del cliente

    Returns:
    None
    """
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
```

## Código del Cliente (`cliente.py`)

```python
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
```

## Notas

- El servidor debe estar en ejecución antes de iniciar el cliente.
- El cliente debe conectarse al mismo `HOST` y `PORT` que el servidor.
- Este proyecto es una demostración básica de una aplicación cliente-servidor y no está diseñado para uso en producción.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un "issue" para discutir cualquier cambio que te gustaría hacer.

## Licencia

Este proyecto está bajo la Licencia MIT.

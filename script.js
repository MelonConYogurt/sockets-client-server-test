document.addEventListener('DOMContentLoaded', function() {
    // Función para cargar usuarios
    function loadUsers() {
        fetch('http://localhost:8000/users/') // Reemplaza con tu URL de FastAPI
            .then(response => response.json())
            .then(users => {
                const userList = document.getElementById('user-list');
                userList.innerHTML = ''; // Limpiar la lista antes de agregar nuevos datos

                users.forEach(user => {
                    const userItem = document.createElement('li');
                    userItem.textContent = `${user.name} (${user.role}) - ${user.available ? 'Available' : 'Unavailable'}`;
                    userList.appendChild(userItem);
                });
            })
            .catch(error => console.error('Error fetching users:', error));
    }

    // Función para cargar mensajes
    function loadMessages() {
        fetch('http://localhost:8000/messages/') // Reemplaza con tu URL de FastAPI
            .then(response => response.json())
            .then(messages => {
                const messageList = document.getElementById('message-list');
                messageList.innerHTML = ''; // Limpiar la lista antes de agregar nuevos datos

                messages.forEach(message => {
                    const messageItem = document.createElement('li');
                    messageItem.textContent = `Message from ${message.sender_id} to ${message.recipient_id}: ${message.content} (Priority: ${message.priority}, Read: ${message.read})`;
                    messageList.appendChild(messageItem);
                });
            })
            .catch(error => console.error('Error fetching messages:', error));
    }

    // Cargar usuarios y mensajes al iniciar
    loadUsers();
    loadMessages();
});

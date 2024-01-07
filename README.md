# Real time Chat App
This project is a Flask-based web application with SocketIO integration for real-time chat functionality. It includes user authentication, signup, login, and chat room creation features. The application connects to a MySQL database to store user information, messages, and chat rooms. Users can join existing chat rooms, create new ones, and send/receive messages in real-time. The server-side application is structured with routes for handling user interactions and utilizes SocketIO for handling real-time communication between clients. The project also includes API endpoints for retrieving messages, searching users, and other related functionalities.

# API Endpoints

## 1. Get Messages by Room

### Endpoint: `GET /api/messages/room`

### Description:
Retrieves messages for a specific chat room.

### Parameters:
- `q` (Query parameter): Room name for which messages are to be retrieved.

### Example: `GET /api/messages/room?q=example_room`

## 2. Get All Messages

### Endpoint:
`GET /api/messages`

### Description:
Retrieves all messages from all chat rooms.

### Example:
```bash
GET /api/messages
```

## 3. Search Messages

### Endpoint: `GET /api/messages/search`

### Description:
Searches messages based on a provided search term.

### Parameters:
- `q` (Query parameter): Search term.

### Example:
```bash
GET /api/messages/search?q=search_term
```

## 4. Get Messages by Username

### Endpoint: `GET /api/messages/username`

### Description:
Retrieves messages for a specific user.

### Parameters:
- `q` (Query parameter): Username for which messages are to be retrieved.

### Example:
```bash
GET /api/messages/username?q=example_user
```

## 5. Search Users

### Endpoint: `GET /api/users`

### Description:
Searches users based on a provided search term.

### Parameters:
- `q` (Query parameter): Search term.

### Example:
```bash
GET /api/users?q=search_term
```
---

## Database Schema 📚
```mermaid
erDiagram
    CHAT_ROOMS {
       int room_id PK
       varchar(255) room_name
       int owner_id FK
    }
    CHAT_ROOM_ACCESS {
       int id PK
       int user_id FK
       int room_id FK
    }
    MESSAGES {
       int message_id PK
       int user_id FK
       int room_id FK
       varchar(255) content
       timestamp created_at
    }
    USERS {
       int user_id PK
       varchar(60) username
       varchar(255) email "Check for %_@__%.__%"
       varchar(255) profile_picture
       varchar(255) password_hash
       timestamp created_at
    }

    USERS ||--o{ MESSAGES : ""
    CHAT_ROOM_ACCESS }o--|| USERS : ""
    CHAT_ROOM_ACCESS }o--|| CHAT_ROOMS : ""
    CHAT_ROOMS }o--|| USERS : "owns"
    CHAT_ROOMS ||--o{ MESSAGES : ""
```

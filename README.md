# Real time Chat App

## Features 🚀

### Registration

- **Authentication:** Only authenticated users can access the application.
- **Username Collision Check:** Ensure unique usernames to prevent conflicts.
- **Password Security:** Hash passwords for enhanced security.

### Chat

- **Chat Room Creation:** Users can effortlessly create chat rooms.
- **Accessibility Control:** Choose whether the chat room is open to everyone or only selected users.
- **Real-time Chatting:** Enjoy seamless real-time conversations without refreshing the entire page.

### REST API

- **Authentication Guard:** API is restricted to authenticated users only.
- **GET Endpoints:**
  - Retrieve all messages from all chat rooms.
  - Retrieve all messages from a specific user.
  - Retrieve all messages from a particular chat room.
  - Retrieve all messages containing a specific word (case insensitive).

## Instructions 🛠️

Follow these steps to set up and run the project:

1. **Clone the Repository:**
   ```bash
   git clone [repository_url]
   ```

2. **Installation:**
   ```bash
   cd project_directory
   npm install
   ```

3. **Run the Application:**
   ```bash
   npm start
   ```
   

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

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
classDiagram
    direction BT
    class chat_rooms {
       varchar(255) room_name
       int owner_id
       int room_id
    }
    class chat_rooms_access {
       int user_id
       int room_id
       int id
    }
    class messages {
       int user_id
       int room_id
       varchar(255) content
       timestamp timestamp
       int message_id
    }
    class users {
       varchar(60) username
       varchar(255) email
       varchar(255) profile_picture
       varchar(255) password_hash
       timestamp created_at
       int user_id
    }
    
    chat_rooms  -->  users : owner_id:user_id
    chat_rooms_access  -->  chat_rooms : room_id
    chat_rooms_access  -->  users : user_id
    messages  -->  chat_rooms : room_id
    messages  -->  users : user_id

```
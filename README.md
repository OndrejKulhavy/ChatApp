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
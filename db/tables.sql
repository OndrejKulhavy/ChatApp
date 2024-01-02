create database chat_app;
use chat_app;

CREATE TABLE users
(
    user_id         INT AUTO_INCREMENT PRIMARY KEY,
    username        VARCHAR(60) UNIQUE NOT NULL,
    email           VARCHAR(255) UNIQUE NOT NULL CHECK ( email LIKE '%_@__%.__%'  ),
    profile_picture VARCHAR(255)        NOT NULL DEFAULT 'https://raw.githubusercontent.com/OndrejKulhavy/ChatApp/main/db/data/user_profile_picture.png',
    password_hash   VARCHAR(255)        NOT NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chat_rooms
(
    room_id   INT AUTO_INCREMENT PRIMARY KEY,
    room_name VARCHAR(255) NOT NULL,
    owner_id  INT          NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users (user_id)
);

CREATE TABLE chat_rooms_access
(
    id     INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    room_id INT,
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (room_id) REFERENCES chat_rooms (room_id)
);

CREATE TABLE messages
(
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id    INT,
    room_id    INT,
    content    varchar(255) NOT NULL,
    timestamp  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (room_id) REFERENCES chat_rooms (room_id)
);

CREATE PROCEDURE get_messages_by_room_id(IN room_id INT)
BEGIN
    SELECT messages.message_id, messages.user_id, messages.room_id, messages.content, messages.timestamp, users.username, users.profile_picture
    FROM messages
    INNER JOIN users ON messages.user_id = users.user_id
    WHERE messages.room_id = room_id
    ORDER BY messages.timestamp ASC;
END;



CREATE PROCEDURE get_rooms_by_user_id(IN user_id INT)
BEGIN
    SELECT chat_rooms.room_id, chat_rooms.room_name, chat_rooms.owner_id
    FROM chat_rooms
    INNER JOIN chat_rooms_access ON chat_rooms.room_id = chat_rooms_access.room_id
    WHERE chat_rooms_access.user_id = user_id;
END;

CREATE PROCEDURE GET_ROOMS_BY_USERNAME(IN username VARCHAR(60))
BEGIN
    SELECT chat_rooms.room_id, chat_rooms.room_name, chat_rooms.owner_id
    FROM chat_rooms
    INNER JOIN chat_rooms_access ON chat_rooms.room_id = chat_rooms_access.room_id
    INNER JOIN users ON chat_rooms_access.user_id = users.user_id
    WHERE users.username = username;
END;

CREATE PROCEDURE get_users_by_room_id(IN room_id INT)
BEGIN
    SELECT users.user_id, users.username, users.profile_picture
    FROM users
    INNER JOIN chat_rooms_access ON users.user_id = chat_rooms_access.user_id
    WHERE chat_rooms_access.room_id = room_id;
END;

CREATE PROCEDURE get_user_by_username(IN username VARCHAR(60))
BEGIN
    SELECT user_id, username, profile_picture
    FROM users
    WHERE users.username = username;
END;

CREATE PROCEDURE grant_access_to_room(IN username VARCHAR(60), IN room_name VARCHAR(255), IN owner_id INT)
BEGIN
    DECLARE user_id INT;
    DECLARE room_id INT;
    SELECT users.user_id INTO user_id
    FROM users
    WHERE users.username = username;
    SELECT chat_rooms.room_id INTO room_id
    FROM chat_rooms
    WHERE chat_rooms.room_name = room_name AND chat_rooms.owner_id = owner_id;
    INSERT INTO chat_rooms_access (user_id, room_id) VALUES (user_id, room_id);
END;

drop procedure if exists grant_access_to_room;

select * from users;
select * from chat_rooms;
select * from chat_rooms_access;
select * from messages;

drop table chat_rooms_access;


delete from chat_rooms;
delete from chat_rooms_access;

CREATE PROCEDURE GET_MESSAGES_BY_ROOM_NAME(IN room_name VARCHAR(255))
BEGIN
    SELECT messages.message_id, messages.user_id, messages.room_id, messages.content, messages.timestamp, users.username, users.profile_picture
    FROM messages
    INNER JOIN users ON messages.user_id = users.user_id
    INNER JOIN chat_rooms ON messages.room_id = chat_rooms.room_id
    WHERE chat_rooms.room_name = room_name
    ORDER BY messages.timestamp ASC;
END;


INSERT INTO messages (user_id, room_id, content) VALUES (1, 10, 'Hello world!');
INSERT INTO messages (user_id, room_id, content) VALUES (1, 10, 'How are you?');
INSERT INTO messages (user_id, room_id, content) VALUES (2, 10, 'I am fine, thanks!');

call GET_ROOMS_BY_USERNAME('pavlas');
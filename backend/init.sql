DROP TABLE IF EXISTS auth_users;
DROP TABLE IF EXISTS message_list;
DROP TABLE IF EXISTS messages;


CREATE TABLE auth_users (
    userID   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL UNIQUE,
	password TEXT NOT NULL
);

CREATE TABLE message_list(
    messageID INTEGER PRIMARY KEY AUTOINCREMENT,
    convoPreview TEXT NOT NULL,
    userSender TEXT NOT NULL,
    userRecieve TEXT NOT NULL
);

CREATE TABLE messages(
    msg TEXT NOT NULL,
    msgID INTEGER NOT NULL,
    sender TEXT NOT NULL,
    reciever TEXT NOT NULL
);

--Generating test cases--
INSERT INTO auth_users VALUES(1,"alice","1234");
INSERT INTO auth_users VALUES(2,"bob", "5678");
INSERT INTO auth_users VALUES(3,"charlie","123");
INSERT INTO message_list VALUES(1,"Did you see that movie last week?","alice","charlie");
INSERT INTO messages VALUES("Hey how are you?", 1, "charlie", "alice");
INSERT INTO messages VALUES("I am good!", 1, "alice", "charlie");
INSERT INTO messages VALUES("Did you see that movie last week?", 1, "charlie", "alice");


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
    convoTitle TEXT NOT NULL,
    convoPreview TEXT NOT NULL,
    timeUpdate date,
    userSender TEXT NOT NULL,
    userRecieve TEXT NOT NULL
);

CREATE TABLE messages(
    msg TEXT NOT NULL,
    msgID INTEGER NOT NULL,
    timeUpdate date,
    FOREIGN KEY(msgID) REFERENCES message_list(messageID)
);

--Generating test cases--
INSERT INTO auth_users VALUES(1,"alice","Gr3atPA$$W0Rd");
INSERT INTO auth_users VALUES(2,"bob", "Gr3attPA$$W0Rd");
INSERT INTO auth_users VALUES(3,"charlie","Gr3attPA$$W0Rd");
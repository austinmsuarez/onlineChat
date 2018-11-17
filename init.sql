DROP TABLE IF EXISTS auth_users;
CREATE TABLE auth_users (
	username TEXT NOT NULL UNIQUE,
    userID   INT NOT NULL UNIQUE,
	password TEXT NOT NULL
);

CREATE TABLE message_list(
    messageID INT NOT NULL UNIQUE,
    convoTitle TEXT NOT NULL,
    createdFor TEXT NOT NULL,
    timeUpdate date,
    ownedBy    BLOB
)

CREATE TABLE messages(
    msg TEXT NOT NULL,
    msgeID INT NOT NULL,
    FOREIGN KEY(msgeID) REFERENCES message_list(messageID)
)

--Generating test cases--
INSERT INTO auth_users VALUES("alice", 1,"Gr3atPA$$W0Rd");
INSERT INTO auth_users VALUES("bob", 2,"Gr3attPA$$W0Rd");
INSERT INTO auth_users VALUES("charlie", 3,"Gr3attPA$$W0Rd");
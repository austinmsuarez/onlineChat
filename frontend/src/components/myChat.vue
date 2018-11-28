<template>
  <div>
    <div class="messageList">
      <div class="messageListHeader">
        <p>{{username}}'s message list</p>
      </div>
      <div class="messageListBody">
        <li
          v-on:click="openMessage(value.title, value.id)"
          class="messageListItem"
          :key="value.id"
          v-for="value in messageListItems"
        >
          <p id="messageTitle">{{ value.title }}</p>
          <p id="messagePreview">{{value.preview}}</p>
        </li>
      </div>
      <input class="newMessageButton" type="button" v-on:click="newMessage" value="New Message">
    </div>

    <div class="messageLog">
      <div class="messageHeader">
        <p>To:</p>
        <input v-model="recepient" type="text" name="text" placeholder="No recepients...">
      </div>
      <div class="messageHistory">
        <li
          v-bind:class="[{ sentMessage: value.sent }, recievedMessage]"
          :key="value.id"
          v-for="value in convoHistory"
        >
          <p id="message">{{ value.message }}</p>
        </li>
      </div>
      <div class="messageEntry">
        <input
          class="messageText"
          type="text"
          name="text"
          v-model="message"
          placeholder="New Message..."
        >
        <input
          class="sendMessageButton"
          type="button"
          v-on:click="sendMessage(message)"
          value="Send"
        >
      </div>
    </div>
  </div>
</template> 

<script>
import axios from "axios";

export default {
  data: () => {
    return {
      username: localStorage.username,
      password: localStorage.psw,
      messageListItems: [],
      newMessageCreated: true,
      convoHistory: [],
      recepient: "",
      message: "",
      msgID: "",
      messageTitle: "",
      timerConvoList: '',
      sentMessage: "sentMessage",
      recievedMessage: "recievedMessage",
      sent: ""
    };
  },
  methods: {
    getMessageList() {
      var verified = "";
      const path = "http://127.0.0.1:5000/messageList";

      axios
        .get(path, {
          auth: {
            username: this.username,
            password: this.password
          }
        })
        .then(response => {
          this.messageListItems = []
          for (var message in response.data) {
              
            if (this.username == response.data[message].userSender) {
              this.messageTitle = response.data[message].userRecieve;
            } else {
              this.messageTitle = response.data[message].userSender;
            }
            this.messageListItems.push({
              title: this.messageTitle,
              preview: response.data[message].convoPreview,
              id: response.data[message].messageID
            });
          }
        });
    },
    newMessage() {
      this.messageListItems.push({
        title: "newMessage",
        preview: "",
        id: "",
        newmessageList: true
      });
    },
    
    openMessage(title, id) {
      this.recepient = title;
      console.log(id);
      const path = "http://127.0.0.1:5000/messageList/" + id;
      this.msgID = id;
      axios
        .get(path, {
          auth: {
            username: this.username,
            password: this.password
          }
        })
        .then(response => {
          this.convoHistory = [];
          for (var message in response.data) {
            if (response.data[message].sender == this.username) {
              this.sent = true;
            } else {
              this.sent = false;
            }
            this.convoHistory.push({
              message: response.data[message].msg,
              sent: this.sent
            });
          }
        });
    },
    
    sendMessage(message) {
      this.message = message;
      console.log(this.message);
      const path = "http://127.0.0.1:5000/messageList/" + this.msgID;

      if (this.newMessageCreated){
          
      }
      axios
        .post(
          path,
          {
            msg: this.message,
            msgID: this.msgID,
            sender: this.username,
            reciever: this.recepient
          },
          {
            auth: {
              username: this.username,
              password: this.password
            }
          }
        )
        .then(response => {
          this.message = "";
          this.openMessage(this.recepient, this.msgID);
          this.getMessageList();
        });
    }
  },
  
  created: function() {
    this.getMessageList();
    this.timerConvoList = setInterval(this.getMessageList(), 300)
  }
};
</script>

<style>
.messageList {
  height: 100%;
  position: fixed;
  width: 200px;
  z-index: 1;
  top: 0px;
  left: 0px;
  background-color: #1111;
}
.messageListHeader {
  top: 0px;
  height: 10%;
  width: 200px;
  left: 0px;
  position: fixed;
  background-color: #5555;
}
.messageListBody {
  margin-bottom: 10%;
  height: 100%;
  width: 200px;
  position: fixed;
  top: 10%;
  left: 0px;
  overflow: scroll;
}
.messageListItem {
  list-style-type: none;
  border-bottom: 1px solid white;
}
#messageTitle {
  font-weight: bold;
  text-align: left;
}
.messageLog {
  height: 100%;
  margin-left: 160px;
  background-color: rgb(33, 150, 243);
  left: 0px;
  top: 0px;
}
.messageHeader {
  text-align: left;
  background-color: #1111;
  top: 0px;
  left: 0px;
  position: fixed;
  width: 100%;
  height: 10%;
  margin-left: 200px;
}
.messageHeader p {
  left: 0px;
  text-align: left;
  display: inline-block;
}
.messageHeader input {
  border: none;
  width: 50%;
}
.messageHistory {
  margin-left: 200px;
  margin-bottom: 60px;
  top: 10%;
  width: 80%;
  left: 0px;
  height: 80%;
  position: fixed;
  overflow: scroll;
}
.recievedMessage {
  text-align: left;
  background-color: #1111;
  list-style-type: none;
}
.sentMessage {
  text-align: right;
  background-color: #4caf50;
  color: white;
  list-style-type: none;
}
#messagePreview {
  text-align: left;
}

.messageEntry {
  text-align: left;
  background-color: #1111;
  bottom: 0px;
  left: 0px;
  position: fixed;
  width: 100%;
  height: 10%;
  margin-left: 200px;
}

.messageText {
  margin: 20px;
  display: inline;
  width: 70%;
  padding: 5px;
  border-radius: 25px;
}
.sendMessageButton {
  border: none;
  bottom: 0px;
  padding: 5px;
  width: 10%;
  color: white;
  background-color: #4caf50;
  border-radius: 25px;
}
.newMessageButton {
  border: none;
  bottom: 0px;
  left: 0px;
  position: fixed;
  height: 10%;
  width: 200px;
  color: white;
  font-size: 12pt;
  background-color: #4caf50;
}
</style>
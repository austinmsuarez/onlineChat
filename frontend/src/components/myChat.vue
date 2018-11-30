<template>
  <div>
    <div class="messageList">
      <div class="messageListHeader">
        <p>{{username}}'s message list</p>
      </div>
      <div class="messageListBody">
        <li v-on:click="openMessage(value.title, value.id)" class="messageListItem" :key="value.id" v-for="value in messageListItems">
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
        <li v-bind:class="[{ sentMessage: value.sent }, recievedMessage]" :key="value.id" v-for="value in convoHistory">
          <p id="message">{{ value.message }}</p>
        </li>
      </div>
      <div class="messageEntry">
        <input class="messageText" type="text" name="text" v-model="message" placeholder="New Message...">
        <input class="sendMessageButton" type="button" v-on:click="sendMessage(message)" value="Send">
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
      convoHistory: [],
      recepient: '',
      message: '',
      msgID: '',
      messageTitle: '',
      timerConvoList: '',
      sentMessage: 'sentMessage',
      recievedMessage: 'recievedMessage',
      sent: ''
    };
  },
  methods: {

    // Gets all conversation lists
    getMessageList() {
      // sets the path to the messageList
      const path = 'http://127.0.0.1:5000/messageList'
      //  performs a GET request on the backend API
      axios.get(path, {
          //  passes in the authorization paramenters
          auth: {
            username: this.username,
            password: this.password
          }
        })
        .then(response => {
          //  clears the list to the so that it doesnt readd messagesList
          this.messageListItems = []
          //  for every message in the payload add it to the message list
          for (var message in response.data) {
            //  assigns the messageTitle correctly so that it displays the other name instead
            //  the current user's name
            if (this.username = response.data[message].userSender) {
              this.messageTitle = response.data[message].userRecieve
            } else {
              this.messageTitle = response.data[message].userSender
            }
            //  pushes it ontothe array
            this.messageListItems.push({
              title: this.messageTitle,
              preview: response.data[message].convoPreview,
              id: response.data[message].messageID
            });
          }
        });
    },
    // TODO: make this
    newMessage() {
      this.messageListItems.push({
        title: "newMessage",
        preview: '',
      })
    },
    // TODO: fix this
    newMessagePost() {
      const path = 'http://127.0.0.1:5000/messageList'
        axios
          .post(
            path, {
              convoPreview: this.message,
              sender: this.username,
              recepient: this.recepient
            }, {
              auth: {
                username: this.username,
                password: this.password
              }
            }
          )
          .then(response => {
            this.getMessageList()
            console.log(this.messageListItems.length)
            this.msgID = this.messageListItems[this.messageListItems.length].messageID
          })
    },
    // Gets all messages from the conversation
    openMessage(title, id) {
      // assigns values
      this.recepient = title
      console.log(this.recepient)
      const path = 'http://127.0.0.1:5000/messageList/' + this.msgID
      this.msgID = id
      console.log(this.msgID)
      //  clears the message list so there is no duplicates 
      this.convoHistory = []
      //  checks to make sure that the messageID is defined and it is not trying
      //  to pull messages from a newly created list
      if (this.msgID != undefined) {
        axios.get(path,{
                auth: {
                username: this.username,
                password: this.password
                }
            })
          .then(response => {
            //  goes through data and adds the information to the array 
            for (var message in response.data) {
              // used for styling based on sender
              if (response.data[message].sender === this.username) {
                this.sent = true
              } else {
                this.sent = false
              }
              this.convoHistory.push({
                message: response.data[message].msg,
                sent: this.sent
              })
            }
          })
      }
    },
    //  sends the message
    sendMessage(message) {
      // assign variables
      this.message = message
      console.log(this.msgID)
      const path = 'http://127.0.0.1:5000/messageList/' + this.msgID

      // checks if there is any messages in the convo history 
      // if not then send a post request to add the message convo to the table
      if (this.convoHistory.length === 0) {
        this.newMessagePost()
      }
    console.log("hello")

    axios.post(
        path, {
            msg: this.message,
            msgID: this.msgID,
            sender: this.username,
            reciever: this.recepient
        }, {
            auth: {
            username: this.username,
            password: this.password
            }
        }
        )
        .then(response => {
        console.log("hello")
        this.message = ''
        this.openMessage(this.recepient, this.msgID)
        this.getMessageList()
    })        
    }
  },

  created: function () {
    this.getMessageList()
    this.timerConvoList = setInterval(this.getMessageList(), 300)
  }
}
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
  height: 50px;
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
  top: 50px;
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
  height: 50px;
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
  top: 50px;
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
  height: 50px;
  margin-left: 200px;
}

.messageText {
  margin: 20px;
  display: inline;
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

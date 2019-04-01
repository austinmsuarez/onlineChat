<template>
  <div>
    <!--This section is to list out conversation threads --> 
    <div class="messageList">
      <!-- Adds a personal touch to show username above convo list --> 
      <div class="messageListHeader">
        <p>{{username}}'s message list</p>
      </div>
      <!-- convo list assigning keys to elements --> 
      <div class="messageListBody">
        <li v-on:click="openMessage(value.title, value.id)" class="messageListItem" :key="value.id" v-for="value in messageListItems">
          <p id="messageTitle">{{ value.title }}</p>
          <p id="messagePreview">{{value.preview}}</p>
        </li>
      </div>
      <!-- button used to create a new message Convo-->
      <input class="newMessageButton" type="button" v-on:click="newMessage" value="New Message">
    </div>
    <!-- Div that is used to view the messages in a convo -->
    <div class="messageLog">
      <!-- Includes the to addressing for your convo--> 
      <div class="messageHeader">
        <p>To:</p>
        <input v-model="recepient" type="text" name="text" placeholder="No recepients...">
      </div>
      <!-- Used to view the actual messages of the conversation --> 
      <div class="messageHistory">
        <li v-bind:class="[{ sentMessage: value.sent }, recievedMessage]" :key="value.id" v-for="value in convoHistory">
          <p id="message">{{ value.message }}</p>
        </li>
      </div>
      <!-- View to enter new message --> 
      <div class="messageEntry">
        <input class="messageText" type="text" name="text" v-model="message" placeholder="New Message...">
        <input class="sendMessageButton" type="button" v-on:click="sendMessage(message)" value="Send">
      </div>
    </div>
  </div>
</template>

<script>
    // used to make http requests
    import axios from "axios";

export default {
  // all variable data 
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
      sent: '',
      posted: ''
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
            username: localStorage.username,
            password: localStorage.psw
          }
        })
        .then(response => {
          //  clears the list to the so that it doesnt readd messagesList
          this.messageListItems = []
          //  for every message in the payload add it to the message list
          for (var message in response.data) {
            //  assigns the messageTitle correctly so that it displays the other name instead
            //  the current user's name
            if (localStorage.username == response.data[message].userSender) {
              this.messageTitle = response.data[message].userRecieve
            } else {
              this.messageTitle = response.data[message].userSender
            }
            //  pushes it onto the array
            this.messageListItems.push({
              title: this.messageTitle,
              preview: response.data[message].convoPreview,
              id: response.data[message].messageID
            });
          }
        });
    },

    //used when the user press the new message button 
    //clears the view
    newMessage() {
      this.recepient = ''
      this.message = ''
      this.convoHistory = []
    },

    // posts a new message convo to the backend 
    newMessagePost() {
      // path of the backend server 
      const path = 'http://127.0.0.1:5000/messageList'
        // http request posts through the path the data convoPreview,sender,recepient
        // sends out your username and password to make sure that you are authenticated
        // TODO: find a way to encrypt all data being sent out
        axios
          .post(
            path, {
              convoPreview: this.message,
              sender: localStorage.username,
              recepient: this.recepient
            }, {
              auth: {
                username: localStorage.username,
                password: localStorage.psw
              }
            }
          )
          .then(response => {
            // If this is successful it gets the assigned message convo id from the server 
            this.getMessageID(this.recepient)
          })
    },

    // Gets all messages from the conversation
    openMessage(title, id) {
      // assigns values
      this.recepient = title
      this.msgID = id
      const path = 'http://127.0.0.1:5000/messageList/' + this.msgID
      
      //  clears the message list so there is no duplicates 
      this.convoHistory = []
      //  checks to make sure that the messageID is defined and it is not trying
      //  to pull messages from a newly created list
      if (this.msgID != undefined) {
        axios.get(path,{
                auth: {
                username: localStorage.username,
                password: localStorage.psw
                }
            })
          .then(response => {
            //  goes through data and adds the information to the array 
            for (var message in response.data) {
              // used for styling based on sender
              if (response.data[message].sender === localStorage.username) {
                this.sent = true
              } else {
                this.sent = false
              }
              this.convoHistory.push({
                // loads messages 
                message: response.data[message].msg,
                sent: this.sent
              })
            }
            this.getMessageList()
          })
      }
    },
    // gets the message Id to index the convo list and retrieve messages in message history requests
    getMessageID(recepient){
        const path = 'http://127.0.0.1:5000/'+recepient
        axios.get(path, {
                auth: {
                username: localStorage.username,
                password: localStorage.psw
                }
            })
            .then(response => {
               this.msgID = response.data[0].messageID
               axios.post(
                'http://127.0.0.1:5000/messageList/' + this.msgID, {
                    msg: this.message,
                    msgID: this.msgID,
                    sender: localStorage.username,
                    reciever: this.recepient
                }, {
                    auth: {
                    username: localStorage.username,
                    password: localStorage.psw
                    }
                }
                )
                .then(response => {
                    this.message = ''    
                    this.openMessage(this.recepient, this.msgID)
                })       
                
        })   
        
    },
    //  sends the message
    sendMessage(message) {
        // assign variables
        this.message = message
     
        // checks if there is any messages in the convo history 
        // if not then send a post request to add the message convo to the table
        if (this.convoHistory.length === 0) {
            this.newMessagePost()
        }
        else{
                axios.post(
                'http://127.0.0.1:5000/messageList/' + this.msgID, {
                    msg: this.message,
                    msgID: this.msgID,
                    sender: localStorage.username,
                    reciever: this.recepient
                }, {
                    auth: {
                    username: localStorage.username,
                    password: localStorage.psw
                    }
                }
                )
                .then(response => {
                    this.message = ''
                    this.openMessage(this.recepient, this.msgID)
                    
                })       
        }
        
    }
  },

  created: function () {
    this.getMessageList()
    this.timerConvoList = setInterval(this.getMessageList(), 300)
  }
}
</script>

<style>
 .scrollable-content::-webkit-scrollbar * {
      background:transparent;
    }
    .scrollable-content::-webkit-scrollbar-thumb {
      background:#999 !important;
    }
::-webkit-scrollbar{
  width:5px;
}

 
/* Handle */
::-webkit-scrollbar-thumb {
  background: #888; 
  border-radius: 10px;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #555; 
}

.messageList {
  height: 100%;
  position: fixed;
  width: 200px;
  top: 0px;
  left: 0px;
  background-color: lightgrey;
}

.messageListHeader {
  top: 0px;
  height: 50px;
  width: 200px;
  left: 0px;
  position: fixed;
  background-color:#4caf50;
}
.messageListHeader p {
  color:white;
}
.messageListBody {
  height:   100%;
  width:    200px;
  position: fixed;
  top:      50px;
  bottom:   50px;
  left:     0px;
  overflow: scroll;
}

.messageListItem {
  list-style-type:  none;
  margin-left:      10px;
  border-bottom:    1px solid white;
}
.messageListItem:hover{
  background-color: #4caf50;
  color:            white;
}
#messageTitle {
  font-weight: bold;
  text-align: left;
}

.messageLog {
  height:  100%;
  left:    200px;
  top:     0px;
}

.messageHeader {
  text-align:       left;
  background-color: white;
  top:              0px;
  left:             0px;
  width:            100%;
  height:           50px;
  margin-left:      200px;
  position:         fixed;
}

.messageHeader p {
  left:             0px;
  text-align:       left;
  display:          inline-block;
}

.messageHeader input{
  border:           none;
  display:          inline-block;
  border-radius:    10px;
  width:            80%;
  min-width:        100px;
}
.messageHeader input:focus{
     border: 3px solid #4caf50;
}
.messageHistory{
  top:              50px;
  left:             200px;
  right:            0px;
  bottom:           50px;
  position:         fixed;
  overflow:         scroll;
  background: whitesmoke;
}

.recievedMessage{
  text-align:       left;
  background-color: #1111;
  list-style-type:  none;
}

.sentMessage{
  text-align:       right;
  background-color: #4caf50;
  color:            white;
  list-style-type:  none;
}

#messagePreview{
  text-align: left;
}

.messageEntry {
  text-align:       left;
  background-color: #1111;
  bottom:           0px;
  left:             200px;
  position:         fixed;
  width:            100%;
  height:           50px;
}

.messageText {
  margin-top:    15px;
  margin-left:   5px;
  width:         50%;
  display:       inline;
  padding:       5px;
  border-radius: 25px;
  border:       none;
}
.messageText:focus{
     border: 3px solid #4caf50;
}
.sendMessageButton {
  margin-left: 10px;
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
  height: 50px;
  width: 200px;
  color: white;
  font-size: 12pt;
  background-color: #4caf50;
}
</style>

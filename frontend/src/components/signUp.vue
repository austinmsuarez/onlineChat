
<template>
    <div>
        <img src="../assets/logo.png" alt="onlineChat logo">
        <h1>OnlineChat</h1> 
        <form id = "loginForm">
            <br>
            <input id="inputText" placeholder="Username" type="text" v-model="username">
            <br>
            <input id="inputText" placeholder="Password" type="password" v-model="psw">
            <br>
            <input id="inputText" placeholder="Confirm Password" type="password" v-model="pswConfirm">
            <br>
            <input id="buttons" v-on:click="signUp" type="submit" value="Sign Up">
            <p class="errorMessage">{{errorMessage}}</p>
        </form>
    </div>
</template> 

<script>
    import axios from 'axios'
    import Vue from 'vue'

    import Router from 'vue-router'
    Vue.use(Router)

    export default{
        data: () => {
            return {
                username: '',
                psw: '',
                pswConfirm: '',
                errorMessage: ''
            };
        },
        methods: { 
            // used to insert new user into database 
            getSignUpResponseAPI(){
                var verified = ""
                const path = 'http://127.0.0.1:5000/signup';
                
                axios.post(path,
                    {
                        username: this.username,
                        password: this.psw
                    },
                    {headers: {
                        'Content-Type': 'application/json;charset=UTF-8',
                        "Access-Control-Allow-Origin": "*",
                    }}
                 ).then(response => { 
                        // if the account was created 
                        if(response.status == 201){
                            localStorage.username = this.username;
                            localStorage.password = this.psw;
                            console.log("saved and transitioning");
                            this.$router.push({name:'myChat'});
                        }
                       
                    })
                    .catch(error=> {
                        // if the username isnt available
                        console.log(error.response)
                        if(error.response.status == 409){
                            this.errorMessage = "USERNAME UNAVAILABLE"
                        }
                    });
             },
            // method used for sign up checks for matching passwords 
            signUp(){
                if(this.psw == this.pswConfirm){
                    this.getSignUpResponseAPI();
                }
                else{
                    this.errorMessage = "PASSWORDS DO NOT MATCH";
                }
            }
        
        },
        // watches password and username changes
        watch: {
            username(name){
                localStorage.username = name
            },
            psw(password){
                localStorage.psw = password
            }
        }
    };
   
</script>

<style>
#buttons{
  margin-top: 10px;
  border-radius: 10px;
  padding-left: 10%;
  padding-right: 10%;
  border: none;
  color: white;
  font-size: 12pt;
  background-color: #4caf50;
}


.errorMessage{
    margin-top: 10px;
    color: darkred;
}
#inputText{
    border: 2px solid lightgrey;
    width: 20%;
    border-radius: 4px;
}
#inputText:focus{
     border: 3px solid #4caf50;
}
</style>


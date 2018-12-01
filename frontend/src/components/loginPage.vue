
<template>
    <div>
        <img src="../assets/logo.png" alt="onlineChat logo">
        <h1>OnlineChat</h1> 
        <form id = "loginForm">
            <input class="inputText" placeholder="Username" type="text" v-model="username">
            <br>
            <input class="inputText" placeholder="Password" type="password" v-model="psw">
            <br>
            <input class="buttons" v-on:click="login" type="submit" value="Login">
        </form>
        <input class="buttons" v-on:click="signUp" type="submit" value="Sign Up">
        <br>
        <p class="errorMessage">{{errorMessage}}</p>
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
                errorMessage: ''
            };
        },
        methods: { 
            login(){
                if(this.username != null && this.psw != null){
                    this.getLoginResponseAPI()
                }
                else{
                    console.log("input both parameters")
                }
            },

            getLoginResponseAPI(){
                 var verified = ""
                 const path = 'http://127.0.0.1:5000/login';
                 if(this.username == '' || this.psw == ''){
                    this.errorMessage = "ENTER USERNAME OR PASSWORD"
                 }
                 else{
                    localStorage.username = this.username;
                    localStorage.password = this.psw;
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
                            if(response.status == 202){
                                localStorage.username = this.username;
                                localStorage.password = this.psw;
                                console.log("saved and transitioning");
                                this.$router.push({name:'myChat'});
                            } 
                        }).catch(error=>{
                            if(error.response.status == 409){
                                this.errorMessage = "INVALID USERNAME OR PASSWORD"
                            }
                        });
                }
             },
        
            signUp(){
                localStorage.username = name
                localStorage.psw = password
                this.$router.push({name:'signUp'});
            }
        
        },

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
.buttons{
 margin-top: 10px;
  border-radius: 10px;
  padding-left: 10%;
  padding-right: 10%;
  border: none;
  color: white;
  font-size: 12pt;
  background-color: #4caf50;
}
.inputText{
    border: 2px solid lightgrey;
    width: 20%;
    border-radius: 4px;
}
.inputText:focus{
     border: 3px solid #4caf50;
}
.errorMessage{
    color: darkred;
}
</style>


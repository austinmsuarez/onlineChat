
<template>
    <div>
        <h1>Login</h1> 
        <form id = "loginForm">
            Username:
            <br>
            <input type="text" v-model="username">
            <br> 
            Password:
            <br>
            <input type="password" v-model="psw">
            <br>
            <input v-on:click="login" type="submit" value="Login">
        </form>
    </div>
</template> 

<script>
    import axios from 'axios'

    export default{
        data: () => {
            return {
                username: '',
                psw: ''
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
                 const path = 'http://127.0.0.1:5000/login';
                 console.log("bye")

                 axios.post(path,
                    {Authorization: {
                        username: this.username,
                        password: this.password
                    }}
                 )
                 console.log("hello")
            }
        }
    };
   
</script>


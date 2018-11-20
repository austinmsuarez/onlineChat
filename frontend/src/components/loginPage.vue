
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
                var verified = ""
                 const path = 'http://127.0.0.1:5000/login';
                 console.log("bye")

                 console.log(axios.post(path,
                     {
                        username: this.username,
                        password: this.psw
                    }
                 ).then(response => {response.status}))
             }
        }
    };
   
</script>


<template>
    <div class="login">
        <div class="login__banner">
            Admin
        </div>
        <form class="login-form" @submit.prevent="loginUser">
            <span class="login__error" v-if="serverErrors !== null">
                {{ serverErrors }}
            </span>
            <span class="login__error" v-if="errors.any()">
                {{ errors.all()[0] }}
            </span>
            <input 
                type="email" 
                class="login-form__input" 
                name="email" 
                placeholder="Email" 
                v-model="email" 
                @keyup.13="loginUser" 
                v-validate="'required|email'" 
                data-vv-value-path="email" 
            />
            <input 
                type="password" 
                class="login-form__input" 
                name="password" 
                placeholder="Password" 
                v-model="password" 
                @keyup.13="loginUser" 
                v-validate="'required'" 
                data-vv-value-path="password" 
            />
            <button 
                type="button" 
                class="login-form__button" 
                @click="loginUser"
            >Login</button>
        </form>
    </div>
</template>

<script>
import axios from "../../node_modules/axios"
import router from "../router"

export default {
    name: "Login",
    data() {
        return {
            email: "",
            password: "",
            serverErrors: null
        }
    },
    methods: {
        loginUser: function(event) {
            this.$validator.validateAll().then(result => {
                if (this.errors.any()) {
                    return;
                }

                axios.post("/login/", {
                    email: this.email,
                    password: this.password
                }).then((response) => {
                    router.replace("/");
                }).catch((error) => {
                    this.serverErrors = error.response.data;
                });
            });
        }
    }
}

</script>

<style lang="scss">

.login {
    font-family: 'Martel Sans', sans-serif;
    width: 300px;
    margin-left: auto;
    margin-right: auto;
    margin-top: 300px;
    border: none;
    padding: 20px;
    text-align: center;
    background-color: #B1EFC6;
}

.login__banner {
    font-weight: 400;
    display: inline-block;
    padding: 4px 10px;
    font-size: 20px;
    cursor: pointer;
    margin-bottom: 20px;
    color: #00B545;
}

.login__error {
    color: red;
}

.login-form__input {
    padding: 4px;
    border: 1px solid #F6F6F6;
    background-color: #FAFAFA;
    height: 32px;
    display: block;
    margin-bottom: 10px;
    margin-left: auto;
    margin-right: auto;
}

.login-form__button {
    font-size: 20px;
    height: 32px;
    border: 1px solid #CCCCCC;
    color: #333333;
    padding: 4px 10px;
    border-radius: 3px;
    background-color: #CCCCCC;
    vertical-align: top;
    cursor: pointer;
    display: block;
    margin-left: auto;
    margin-right: auto;

    &:hover {
        background-color: #F3F3F3;
    }
}

</style>
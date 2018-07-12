<template>
    <div class="account-popup">
        <h3 class="account-popup__banner">Account</h3>
        <span @click="hideAccount" class="account-popup__close">
            X
        </span>
        <form @submit.prevent="onSubmit" class="account-popup__form">
            <span class="account-popup__error" v-if="errors.any()">
                {{ errors.all()[0] }}
            </span>
            <div class="account-popup__form-group">
                <img :src="userImage" class="account-popup__image" alt="account image" />
            </div>
            <div class="account-popup__form-group">
                <input 
                    type="file" 
                    @change="onFileChanged" 
                    name="crudImage" 
                    id="crudImage" 
                    class="account-popup__image-input" 
                    v-validate="'size:1000'" 
                />
                <label for="crudImage" class="account-popup__image-label">
                    Add/Edit Image
                </label>
            </div>
            <div class="account-popup__form-group">
                <label for="userEmail">
                    Email
                </label>
                <input 
                    type="email" 
                    name="userEmail" 
                    :value="userEmail" 
                    class="account-popup__form-group-input" 
                    v-validate.disable="'required|email'" 
                    data-vv-value-path="emailBind" 
                />
            </div>
            <div class="account-popup__form-group">
                <label for="rememberMe">
                    Remember Me
                </label>
                <input 
                    type="checkbox" 
                    name="rememberMe" 
                    v-model="rememberMe" 
                />
            </div>
            <div class="account-popup__form-group">
                <button 
                    type="button" 
                    @click="saveAccount" 
                    class="account-popup__button"
                >Save</button>
            </div>
        </form>
    </div>
</template>

<script>
import { bus } from "../main"
import axios from "../../node_modules/axios"

export default {
    data() {
        return {
            fileString: null,
            emailBind: "",
            rememberMe: document.cookie.split(";").filter((item) => item.includes("remember_token=")).length == "true"
        }
    },
    methods: {
        hideAccount: function() {
            this.fileString = null;
            bus.$emit("hideAccount");
        },
        onFileChanged: function(event) {
            let reader = new FileReader();
            let self = this;

            reader.addEventListener("load", function() {
                let fileData = reader.result;
                self.fileString = fileData;

                bus.$emit("hideLoading");
            }, false);

            if (event.target.files[0]) {
                bus.$emit("showLoading", "Uploading File");

                reader.readAsDataURL(event.target.files[0]);
            }
        },
        saveAccount: function(event) {
            this.$validator.validateAll().then(result => {
                if (this.errors.any()) {
                    return;
                }

                let updatedInfo = {};

                if (this.fileString !== null) {
                    updatedInfo["account_image"] = this.fileString;
                }
                if (this.emailBind !== this.$store.state.global.accountObj.email) {
                    updatedInfo["email"] = this.emailBind;
                }

                updatedInfo["remember_me"] = this.rememberMe;

                bus.$emit("showLoading", "Contacting Server");
                axios.post("/update_employee_info/", updatedInfo).then((response) => {
                    this.$store.commit("setAccountObj", response.data.result);
                    bus.$emit("hideAccount");
                }).catch((error) => {
                    bus.$emit("showWarning", error.response.data);
                }).finally(() => {
                    bus.$emit("hideLoading");
                });
            });
        }
    },
    computed: {
        userImage: function() {
            if (this.fileString !== null)  {
                return this.fileString;
            } else if (!this.$store.state.global.accountObj.hasOwnProperty("accountImage") || this.$store.state.global.accountObj.accountImage === null) {
                return "/static/img/user_default_image.png";
            } else {
                return this.$store.state.global.accountObj.accountImage;
            }
        },
        userEmail: function() {
            return this.$store.state.global.accountObj.email;
        }
    }
}
</script>

<style lang="scss">

.account-popup {
    border: 2px solid #555555;
    width: 600px;
    height: 800px;
    position: fixed;
    top: 50px;
    background-color: white;
    left: calc(50vw - 300px);
    padding: 20px;
    overflow-y: scroll;

    @media screen and (max-height: 880px) {
        height: 600px;
    }
}

.account-popup__banner {
    text-align: center;
    color: #00B545;
    font-size: 30px;
}

.account-popup__close {
    position: absolute;
    cursor: pointer;
    right: 20px;
    top: 20px;
    padding: 5px;

    &:hover {
        color: #AAAAAA;
    }
}

.account-popup__form {
    padding-top: 20px;
}

.account-popup__form-group {
    width: 400px;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 30px;
    position: relative;
    min-height: 40px;

    &.center_text {
        text-align: center;
    }
}

.account-popup__form-group-input {
    padding: 4px;
    border: 1px solid #F6F6F6;
    background-color: #FAFAFA;
    position: absolute;
    right: 0;
}

.account-popup__image {
    width: 200px;
    height: auto;
    display: block;
    margin-left: 100px;
}

.account-popup__image-input {
    display: none;
}

.account-popup__image-label {
    cursor: pointer;
    padding: 8px 8px;
    border: 1px solid #CCCCCC;
    background-color: #F3F3F3;
    color: #333333;
    margin-left: auto;
    margin-right: auto;
    display: block;
    width: 129px;

    &:hover {
        background-color: #CCCCCC;
    }
}

.account-popup__button {
    font-size: 20px;
    height: 32px;
    border: 1px solid #CCCCCC;
    padding: 4px 10px;
    background-color: #CCCCCC;
    color: #333333;
    vertical-align: top;
    cursor: pointer;
    float: right;
    margin-bottom: 10px;

    &:hover {
        background-color: #F3F3F3;
    }
}

.account-popup__error {
    color: red;
    text-align: center;
    display: block;
    margin-bottom: 12px;
}

</style>
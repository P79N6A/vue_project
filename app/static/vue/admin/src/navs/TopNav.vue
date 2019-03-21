<template>
    <div class="top-nav">
        <div class="top-nav__banner">Admin</div>
        <div class="nav-dropdown">
            <button @click="showMenu = !showMenu" class="nav-dropdown__button">
                Account <span>&#X25BC</span>
            </button>
            <div v-show="showMenu" class="nav-dropdown__dropdown">
                <a class="nav-dropdown__dropdown-item" @click="logout">
                    Logout
                </a>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "../../node_modules/axios"
import { bus } from "../main"

export default {
    data() {
        return {
            showMenu: false
        }
    },
    methods: {
        logout: function(event) {
            /*
            bus.$emit("showLoading", "Contacting Server");
            axios.post("/logout/").then((response) => {
                location.assign("/");
            }).catch((error) => {
                bus.$emit("showWarning", error.response.data);
            }).finally(() => {
                bus.$emit("hideLoading");
            });
            */
        }
    }
}
</script>

<style lang="scss">

.top-nav {
    background-color: #555555;
    height: 36px;
    position: relative;
    color: #FBFBFB;
}

.top-nav__banner {
    font-family: 'Martel Sans', sans-serif;
    font-weight: 400;
    display: inline-block;
    padding: 8px 10px 6px;
    font-size: 20px;
    cursor: pointer;
}

.nav-dropdown {
    display: inline-block;
    position: absolute;
    right: 0px;
    top: 0;    
    bottom: 0;
    font-family: 'Martel Sans', sans-serif;
    font-weight: 200;
} 

.nav-dropdown__button {
    background-color: #00B545;
    border: none;
    padding-right: 20px;
    padding-left: 20px;
    cursor: pointer;
    height: 100%;
    color: #EEEEEE;

    &:hover {
        background-color: #1DBA59;
    }
}

.nav-dropdown__dropdown {
    position: absolute;
    background-color: #FDFDFD;
    width: 123px;
    z-index: 1;
}

.nav-dropdown__dropdown-item {
    color: black;
    padding: 12px 16px;
    text-decoration: none;
    display: block;
    cursor: pointer;
    border: 1px solid #DDDDDD;

    a:hover {
        background-color: #F3F3F3;
    }
}

</style>

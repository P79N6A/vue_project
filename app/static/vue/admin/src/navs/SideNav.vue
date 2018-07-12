<template>
    <div class="sidenav__holder">
        <div v-show="showSidebar" class="sidenav__bar">
            <div @click="showSidebar = !showSidebar" class="sidenav__toggle"></div>
            <div class="sidenav__image-wrapper">
                <h3 @click="toggleAccount" class="sidenav__image-header">
                    {{ this.$store.state.global.accountObj.email }}
                </h3>
                <img 
                    @click="toggleAccount" 
                    :src="userImage" 
                    class="sidenav__image"
                    alt="account image" 
                />
            </div>
            <div 
                v-for="menuItem in sidebarMenuItems" 
                @click="changeMainView(menuItem)" 
                class="sidenav__item" 
                :class="{ 'active': menuItem === currentItem }"
            >{{ menuItem }}</div>
            <div @click="toggleSettings" class="sidenav__item">
                Settings
            </div>
        </div>
        <div 
            v-show="!showSidebar" 
            v-on:click="showSidebar = !showSidebar" 
            class="sidenav__toggle sidenav__toggle--hidden-bar"
        ></div>
    </div>
</template>

<script>
import { bus } from "../main"

export default {
    data() {
        return {
            showSidebar: true,
            sidebarMenuItems: ["Home", "Part", "Supplier", "Transactions", "Sales", "Customers", "Categories"],
            currentItem: this.$store.state.global.shownView
        }
    },
    methods: {
        toggleSettings: function(event) {
            bus.$emit("showSettings");
        },
        toggleAccount: function(event) {
            bus.$emit("showAccount");
        },
        changeMainView: function(menuItem) {
            bus.$emit("mainViewChange", menuItem);
            this.currentItem = menuItem;
        }
    },
    computed: {
        userImage: function() {
            if (!this.$store.state.global.accountObj.hasOwnProperty("accountImage") || this.$store.state.global.accountObj.accountImage === null) {
                return "/static/img/user_default_image.png";
            } else {
                return this.$store.state.global.accountObj.accountImage;
            }
        }
    },
    created() {
        bus.$on("changeSidebarView", (data) => {
            this.changeMainView(data);
        });
    }
}
</script>

<style lang="scss">

.sidenav__bar {
    width: 250px;
    height: calc(100vh - 36px);
    background-color: #FAFAFA;
    min-height: 600px;
}

.sidenav__toggle {
    width: 11px;
    height: 100%;
    float: right;
    background-color: #DDDDDD;
    cursor: pointer;
    font-size: 14px;
    padding-top: calc(50vh - 15px);

    &:hover {
        background-color: #EEEEEE;
    }

    @at-root #{&}--hiddenBar {
        float: none;
        height: 100%;
    }
}

.sidenav__image-wrapper {
    width: 200px;
    margin-left: auto;
    margin-right: auto;
    padding-top: 30px;
    padding-bottom: 50px;
    position: relative;
}

.sidenav__image-header {
    position: absolute;
    bottom: 50px;
    background-color: rgba(255, 255, 255, 0.9);
    left: 0;
    right: 0;
    text-align: center;
    margin-bottom: 0;
    padding-top: 10px;
    padding-bottom: 10px;
    cursor: pointer;
}

.sidenav__image {
    display: block;
    width: 200px;
    height: auto;
    border: 1px solid #FCFCFC;
    cursor: pointer;
}

.sidenav__item {
    padding: 10px;
    text-align: center;
    cursor: pointer;
    background-color: #00B545;

    &:hover {
        background-color: #B1EFC6;
    }

    &:last-of-type {
        margin-top: 60px;
        display: none;
    }

    &.active {
        background-color: #2DEF77;
    }
}

</style>

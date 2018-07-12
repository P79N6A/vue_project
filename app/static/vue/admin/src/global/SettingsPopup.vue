<template>
    <div class="settings-popup">
        <h3 class="settings-popup__banner">
            Settings
        </h3>
        <span @click="hideSettings" class="settings-popup__close">
            X
        </span>
        <form @submit.prevent="onSubmit" class="settings-popup__form">
            <div class="settings-popup__form-group">
                <label for="colorScheme">
                    Color Scheme
                </label>
                <select 
                    name="colorScheme" 
                    id="colorScheme" 
                    class="settings-popup__form-group-select"
                >
                    <option value="light">
                        Light
                    </option>
                    <option value="dark">
                        Dark
                    </option>
                </select>
            </div>
        </form>
    </div>
</template>

<script>
import { bus } from "../main"

export default {
    data() {
        return {}
    },
    methods: {
        hideSettings: function() {
            bus.$emit("hideSettings");
        }
    }
}
</script>

<style lang="scss">

.settings-popup {
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

.settings-popup__banner {
    text-align: center;
    color: #00B545;
    font-size: 30px;
}

.settings-popup__close {
    position: absolute;
    cursor: pointer;
    right: 20px;
    top: 20px;
    padding: 5px;

    &:hover {
        color: #AAAAAA;
    }
}

.settings-popup__form {
    padding-top: 20px;
}

.settings-popup__form-group {
    width: 400px;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 30px;
    position: relative;
}

.settings-popup__form-group-select {
    position: absolute;
    right: 0;
    border: 1px solid #F6F6F6;
    background-color: #FAFAFA;
}

</style>
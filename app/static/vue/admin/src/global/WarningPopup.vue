<template>
    <div>
        <div class="warning-popup">
            <h3 class="warning-popup__banner">Error</h3>
            <span @click="hideWarning" class="warning-popup__close">X</span>
            {{ this.$store.state.global.warningText }}
        </div>
        <div class="warning-overlay"></div>
    </div>
</template>

<script>
import { bus } from "../main"

export default {
    data() {
        return {}
    },
    methods: {
        hideWarning: function() {
            bus.$emit("hideWarning");
        }
    }
}
</script>

<style lang="scss">

.warning-popup {
    border: 2px solid #555555;
    width: 400px;
    height: 150px;
    position: fixed;
    top: 250px;
    background-color: white;
    left: calc(50vw - 200px);
    text-align: center;
    z-index: 100;  
}

.warning-popup__banner {
    text-align: center;
    color: red;
}

.warning-popup__close {
    position: absolute;
    cursor: pointer;
    right: 0;
    top: 0;
    padding: 5px;
}

.warning-overlay {
    z-index: 99;
    position: fixed;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    background-color: rgba(100, 100, 100, 0.4);
}

</style>
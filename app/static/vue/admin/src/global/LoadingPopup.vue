<template>
    <div class="loading-popup">
        {{ this.$store.state.global.loadingMessage }}
    </div>
</template>

<script>
export default {
    data() { return {} }
}
</script>

<style lang="scss">

.loading-popup {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    min-height: 20px;
    text-align: center;
    background-color: #CCCCCC;
    border-top: 1px solid #AAAAAA;
    padding: 6px;
}

</style>
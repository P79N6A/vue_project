<template>
	<div id="app" class="app">
        <router-view></router-view>
    </div>
</template>

<script>

export default {
    name: "app"
}

</script>

<style lang="scss">

* {
    box-sizing: border-box;
}

*:focus {
    outline: 0;
}

.app {
    min-width: 1200px;
}

</style>

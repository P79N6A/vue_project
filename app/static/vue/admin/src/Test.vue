<template>
    <ul>
        <li v-for="test in tests">{{ test }}</li>
    </ul>
</template>

<script>
export default {
    data () {
        return {
            tests: ["Python", "PHP", "JS"]
        }
    }
}
</script>

<style lang="scss">

</style>

<script>
export default {
  name: 'Home',
  data() {
    return {
    }
  },
  methods: {
    getLinkFromRouter(name) {
      return this.$router.resolve({ name }).href
    }
  }
}
</script>

<template>
  <v-container justify="center" align="center">
    <v-row>
      <v-col>
        <h1 class="text-center">{{program_name}}</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <div style="text-align: center"></div>
      </v-col>
    </v-row>
  </v-container>
</template>
<style lang="scss" scoped>
</style>

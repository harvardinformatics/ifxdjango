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
    <v-row align="center" justify="center" class="mt-3">
        <v-btn v-for="(button, index) in buttons"
          :key="index"
          elevation="1"
          tile
          color="primary"
          :disabled="!button.enabled"
          class="mr-3 mb-3 large-button"
          :href="getLinkFromRouter(button.link)"
        ><span class="d-flex flex-column"><v-icon x-large>{{button.icon}}</v-icon><p></p>{{ button.text}}</span></v-btn>
    </v-row>
  </v-container>
</template>
<style lang="scss" scoped>
  a.large-button.v-size--default,
  button.large-button.v-size--default  {
    height: 6rem;
  }
</style>

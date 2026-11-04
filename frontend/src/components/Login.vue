<script>

export default {
  name: 'Login',
  data: function () {
    return {
      success: false,
      failure: false,
      message: '',
      routeInfo: { name: 'Home' },
    }
  },
  methods: {
    sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms))
    },
    async execute() {
      await this.sleep(1000)
      await this.$api.auth.login()
      await this.sleep(100)
      this.$eventBus.emit('isLoggedIn', this.success)
      await this.sleep(1000)
      if (this.$route.query.next) {
        this.routeInfo = { path: this.$route.query.next }
      }
      this.rtr.push(this.routeInfo)
    },
  },
  computed: {
    rtr: function () {
      return this.$router
    },
    rt: function () {
      return this.$route
    },
  },
  mounted() {
    this.execute()
  },
}
</script>

<template>
  <v-container fluid>
    <v-row align="center" justify="center">
      <v-col v-if="success">
        <h1>Login Successful</h1>
        <p>You are being routed...</p>
      </v-col>
      <v-col v-else-if="failure">
        <h1>Login Unsucessful</h1>
        <p>An error occurred while attempting to log you in. Here is the error message:</p>
        <p>{{ message }}</p>
        <p>
          For more information, please contact
          <a href="mailto:informatics@rc.fas.harvard.edu">.</a>
        </p>
        <p>You are being routed...</p>
      </v-col>
      <v-col v-else>
        <h1>Logging you in...</h1>
      </v-col>
    </v-row>
  </v-container>
</template>

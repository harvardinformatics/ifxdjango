<script>
import axios from 'axios'
import { LOGIN_URL } from '@/urls'
import { mapActions } from 'vuex'
import auth from '@/auth'

export default {
  name: 'Logout',
  data: function() {
    return {
      success: false,
      failure: false,
      message: "",
      routeInfo: {name: "Home"}
    }
  },
  methods: {
    ...mapActions([
      'showMessage'
    ]),
    async execute() {
      await this.sleep(1000)
      this.logout()
      await this.sleep(100)
      this.eventHub.$emit('isLoggedIn', false);
      await this.sleep(1000)
      this.rtr.push(this.routeInfo)
    },
    logout() {
      auth.logout()
      this.success = true
    },
    sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms))
    }
  },
  computed: {
    rtr: function() {
      return this.$router
    },
    rt: function() {
      return this.$route
    }
  },
  mounted () {
    this.execute()
  },
}
</script>

<template>
  <v-container fluid>
    <v-row align="center" justify="center">
        <v-col v-if="success">
          <h1>Logout Successful</h1>
          <p>You are being routed...</p>
        </v-col>
        <v-col v-else-if="failure">
          <h1>Logout Unsucessful</h1>
          <p>An error occurred while attempting to log you out. Here is the error message:</p>
          <p>{% verbatim %}{{message}}{% endverbatim %}</p>
          <p>For more information, please contact <a href="mailto:informatics@rc.fas.harvard.edu">.</a></p>
          <p>You are being routed...</p>
        </v-col>
        <v-col v-else>
          <h1>Logging you out...</h1>
        </v-col>
    </v-row>
  </v-container>
</template>

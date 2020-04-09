<script>
import axios from "axios"
import { LOGIN_URL } from "@/urls"
import { mapActions } from "vuex"
import auth from "@/auth"

export default {
  name: "Login",
  data: function() {
    return {
      success: false,
      failure: false,
      message: "",
      routeInfo: { name: "Home" }
    }
  },
  methods: {
    ...mapActions(["showMessage"]),
    async execute() {
      await this.sleep(1000)
      this.login()
      await this.sleep(100)
      this.eventHub.$emit("isLoggedIn", this.success)
      await this.sleep(1000)
      this.rtr.push(this.routeInfo)
    },
    login() {
      // Get the token, set the value and redirect
      var me = this
      axios
        .get(LOGIN_URL)
        .then(res => {
          if (!res.data || !res.data.token) {
            me.failure = true
            me.message = "You are a known user of {{project_name}}, but your user data is malformed."
          } else {
            // If response has data and token, then it is successful
            me.success = true
            // Initialize user
            auth.initUser(res.data)
            // Check if route query has 'to' query
            if (me.rt.query.hasOwnProperty("to")) {
              const path = me.rt.query.to.path
              me.routeInfo = { path: path }
            }
          }
        })
        .catch(function(error) {
          me.failure = true
          me.message = error
        })
    },
    sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms))
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
  mounted() {
    this.execute()
  }
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
        <p>{% verbatim %}{{message}}{% endverbatim %}</p>
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

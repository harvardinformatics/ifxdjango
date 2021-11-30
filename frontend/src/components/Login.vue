<script>
/* eslint-disable vue/custom-event-name-casing */
import { mapActions } from 'vuex'

export default {
  name: 'Login',
  data: function () {
    return {
      success: false,
      failure: false,
      message: '',
      routeInfo: { name: 'Home' }
    }
  },
  methods: {
    ...mapActions([
      'showMessage'
    ]),
    sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms))
    },
    async execute() {
      await this.login()
      if (this.success) {
        this.rtr.push(this.routeInfo)
      }
    },
    async login() {
      // Get the token, set the value and redirect
      const me = this
      const result = await this.$api.auth.login()
        .catch((error) => {
          me.success = false
          me.failure = true
          if (error.hasOwnProperty('response') && error.response.hasOwnProperty('status') && error.response.status === 401) {
            me.message = 'You are not authorized to login to this application.'
          } else {
            me.showMessage({ error })
          }
        })
      if (result === 'Login successful.') {
        me.$emit('loginSuccessful', {})
        me.success = true
        const routerBase = this.$router.options.base
        if (me.rt.query.from && me.rt.query.from !== routerBase && me.rt.query.from !== routerBase.slice(0, -1)) {
          let path = me.rt.query.from
          if (path.startsWith(routerBase)) {
            // Have to strip the router base from the path; otherwise it gets added
            path = path.substring(3)
          }
          me.routeInfo = { path: path }
        }
      }
    }
  },
  computed: {
    rtr: function () {
      return this.$router
    },
    rt: function () {
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
    <v-layout align-center justify-center>
      <v-flex v-if="success">
        <h1>Login Successful</h1>
      </v-flex>
      <v-flex v-else-if="failure">
        <h1>Login Unsucessful</h1>
        <p>An error occurred while attempting to log you in.</p>
        <p>{% verbatim %}{{message}}{% endverbatim %}</p>
        <p>
          For more information, please contact
          <a href="mailto:informatics@rc.fas.harvard.edu">Informatics help</a>
        </p>
      </v-flex>
      <v-flex v-else>
        <h1>Logging you in...</h1>
      </v-flex>
    </v-layout>
  </v-container>
</template>
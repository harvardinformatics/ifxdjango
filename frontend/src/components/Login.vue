<script>
import axios from 'axios'
import { LOGIN_URL } from '@/urls'
import { mapActions } from 'vuex'
import auth from '@/auth'

export default {
  name: 'Login',
  methods: {
    ...mapActions([
      'showMessage'
    ])
  },
  mounted () {
    // Get the token, set the value and redirect
    var rtr = this.$router
    var rt = this.$route
    var me = this
    axios.get(LOGIN_URL, {
    })
      .then(function (response) {
        let message;
        if (!response.data || !response.data.token){
          message = 'You are a known user of {{project_name}}, but your user data is malformed.  Please send a note to ???.'
          me.showMessage({response, message})
        } else {
          auth.initUser(response.data)
          if (rt.query.from && rt.query.from != '/{{project_name}}/' && rt.query.from != '/{{project_name}}'){
            let path = rt.query.from
            let prefix = '/{{project_name}}/'
            if (path.startsWith(prefix)) {
              // Have to strip the router base from the path; otherwise it gets added
              path = path.substring(prefix.length)
            }
            rtr.replace({path: path})
          } else {
            rtr.replace({name: 'Home'})
          }
        }
      })
      .catch(function (error) {
        me.showMessage({error})
      })
  },
}
</script>

<template>
  <v-container grid-list-sm>
    <v-layout column justify-center>
      <v-flex xs12>
      </v-flex>
    </v-layout>
  </v-container>
</template>

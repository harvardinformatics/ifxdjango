<script>
import auth from '@/auth'

export default {
  name: 'home',
  data: function () {
    return {
      csrfToken: this.$cookie.get('csrftoken'),
    }
  }
}
</script>

<template>
    <v-container grid-list-sm>
      <v-layout column justify-center xs12>
        <v-flex>
          <v-layout row>
            <v-flex>
              Home
            </v-flex>
          </v-layout>
          <v-divider class="my-3"></v-divider>
        </v-flex>
      </v-layout>
    </v-container>
 </template>

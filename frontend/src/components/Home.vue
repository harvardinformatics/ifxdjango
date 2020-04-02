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
    <v-container fluid>
      <v-row>
        <v-col>
          <h1>Home</h1>
          <p>This is the home page.</p>
        </v-col>
      </v-row>
    </v-container>
 </template>

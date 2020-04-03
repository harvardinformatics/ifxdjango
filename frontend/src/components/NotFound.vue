<script>
export default {
  name: 'NotFound',
}
</script>

<template>
  <v-container fluid>
    <v-row align="center" justify="center">
      <v-card class="mx-auto">
        <v-card-title style="border-bottom: 1px solid #aaa">
          <span class="display-1" style="color: #db564c">Not Found!</span>
        </v-card-title>
        <v-card-text>
          The item you're looking for does not exist.
        </v-card-text>
      </v-card>
    </v-row>
  </v-container>
</template>

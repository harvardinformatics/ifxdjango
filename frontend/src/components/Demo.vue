<script>
export default {
  name: "Demo",
  data: function() {
    return {
      message: "And this is a message from the data."
    }
  }
}
</script>

<template>
  <v-container fluid>
    <v-row align='center' justify='center'>
      <v-col>
        <h1>Demo Page</h1>
        <p>This is a description of the demo page.</p>
        <p>
          {% verbatim %}
            {{message}}
          {% endverbatim %}</p>
      </v-col>
    </v-row>
  </v-container>
</template>
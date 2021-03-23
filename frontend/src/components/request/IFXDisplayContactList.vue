<script>
export default {
  name: 'IFXDisplayContactList',
  props: [
    'data'
  ]
}
</script>
<template>
  <v-layout column>
    <v-flex>
      <v-layout row v-for="contact in data" :key="contact.contact.detail">
        <v-flex xs4>
          {% verbatim %}{{contact.role}}{% endverbatim %}
        </v-flex>
        <v-flex>
          {% verbatim %}{{contact.contact.detail}}{% endverbatim %}
        </v-flex>
      </v-layout>
    </v-flex>
  </v-layout>
</template>
<style scoped>

</style>

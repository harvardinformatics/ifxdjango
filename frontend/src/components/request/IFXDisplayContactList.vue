<script>
export default {
  name: 'IFXDisplayContactList',
  props: [
    'data'
  ]
}
</script>
<template>
  <v-row>
    <v-col>
      <v-row v-for="contact in data" :key="contact.contact.detail">
        <v-col cols="4">
          {% verbatim %}{{contact.role}}{% endverbatim %}
        </v-col>
        <v-col>
          {% verbatim %}{{contact.contact.detail}}{% endverbatim %}
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>
<style scoped>

</style>

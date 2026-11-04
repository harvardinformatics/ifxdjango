<script>
export default {
  name: 'IFXDisplayAddressList',
  props: [
    'data'
  ]
}
</script>
<template>
  <v-row>
    <v-col>
      <v-row v-for="address in data" :key="address.type">
        <v-col>
          <v-row>
            <v-col cols="4">
              Street address
            </v-col>
            <v-col>
              {% verbatim %}{{address.street1}}{% endverbatim %}
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="4">
              City
            </v-col>
            <v-col>
              {% verbatim %}{{address.city}}{% endverbatim %}
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="4">
              State
            </v-col>
            <v-col>
              {% verbatim %}{{address.state}}{% endverbatim %}
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="4">
              Country
            </v-col>
            <v-col>
              {% verbatim %}{{address.country}}{% endverbatim %}
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="4">
              Postal code
            </v-col>
            <v-col>
              {% verbatim %}{{address.postal_code}}{% endverbatim %}
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>
<style scoped>

</style>

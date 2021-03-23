<script>
export default {
  name: 'IFXDisplayAddressList',
  props: [
    'data'
  ]
}
</script>
<template>
  <v-layout column>
    <v-flex>
      <v-layout row v-for="address in data" :key="address.type">
        <v-flex>
          <v-layout column>
            <v-flex>
              <v-layout row>
                <v-flex xs4>
                  Street address
                </v-flex>
                <v-flex>
                  {% verbatim %}{{address.street1}}{% endverbatim %}
                </v-flex>
              </v-layout>
            </v-flex>
            <v-flex>
              <v-layout row>
                <v-flex xs4>
                  City
                </v-flex>
                <v-flex>
                  {% verbatim %}{{address.city}}{% endverbatim %}
                </v-flex>
              </v-layout>
            </v-flex>
            <v-flex>
              <v-layout row>
                <v-flex xs4>
                  State
                </v-flex>
                <v-flex>
                  {% verbatim %}{{address.state}}{% endverbatim %}
                </v-flex>
              </v-layout>
            </v-flex>
            <v-flex>
              <v-layout row>
                <v-flex xs4>
                  Country
                </v-flex>
                <v-flex>
                  {% verbatim %}{{address.country}}{% endverbatim %}
                </v-flex>
              </v-layout>
            </v-flex>
            <v-flex>
              <v-layout row>
                <v-flex xs4>
                  Postal code
                </v-flex>
                <v-flex>
                  {% verbatim %}{{address.postal_code}}{% endverbatim %}
                </v-flex>
              </v-layout>
            </v-flex>
          </v-layout>
        </v-flex>
      </v-layout>
    </v-flex>
  </v-layout>
</template>
<style scoped>

</style>

<script>
// Display data common to all account requests
import DisplayAddressList from './IFXDisplayAddressList'
import DisplayContactList from './IFXDisplayContactList'
import DisplayHarvardKey from './IFXDisplayHarvardKey'

export default {
  name: 'IFXAccountRequestTrackDetail',
  props: {
    accountRequestData: Object,
    track: String,
    trackTitle: String
  },
  components: {
    DisplayAddressList,
    DisplayContactList,
    DisplayHarvardKey
  },
  data() {
    return {}
  }
}
</script>
<template>
  <v-container  v-if="accountRequestData" >
    <v-layout column>
      <v-flex>
        <span class="title">{% verbatim %}{{trackTitle}}{% endverbatim %}</span>
      </v-flex>
      <v-flex v-for="field in accountRequestData.tracks[track].fields.order" :key="field">
        <v-layout row wrap v-if="accountRequestData.tracks[track].fields[field]" justify-start>
          <v-flex class="field-label" xs12 md3 v-if="accountRequestData.tracks[track].fields[field].display_name">
            {% verbatim %}{{accountRequestData.tracks[track].fields[field].display_name}}{% endverbatim %}
          </v-flex>
          <v-flex class="field-label" xs12 md3 v-else>
            {% verbatim %}{{field}}{% endverbatim %}
          </v-flex>
          <v-flex xs12 md9 v-if="accountRequestData.tracks[track].fields[field].display_component">
            <component v-if="field == 'harvard_key'"
              :is="accountRequestData.tracks[track].fields[field].display_component"
              :data="accountRequestData[field]">
            </component>
            <component v-else
              :is="accountRequestData.tracks[track].fields[field].display_component"
              :data="accountRequestData.person[field]">
            </component>
          </v-flex>
          <v-flex xs12 md9 v-else>
            <span v-if="accountRequestData.person[field]">{% verbatim %}{{accountRequestData.person[field]}}{% endverbatim %}</span>
            <span v-else>{% verbatim %}{{accountRequestData[field]}}{% endverbatim %}</span>
          </v-flex>
          <v-flex>
          </v-flex>
        </v-layout>
      </v-flex>
    </v-layout>
  </v-container>
</template>
<style scoped>
  .field-label {
    font-weight: bold;
  }
</style>

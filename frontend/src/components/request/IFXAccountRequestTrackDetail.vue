<script>
import DisplayAddressList from './IFXDisplayAddressList.vue'
import DisplayContactList from './IFXDisplayContactList.vue'
import DisplayHarvardKey from './IFXDisplayHarvardKey.vue'

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
  <v-container v-if="accountRequestData">
    <v-row>
      <v-col>
        <span class="text-h6">{% verbatim %}{{trackTitle}}{% endverbatim %}</span>
      </v-col>
    </v-row>
    <v-row v-for="field in accountRequestData.tracks[track].fields.order" :key="field">
      <template v-if="accountRequestData.tracks[track].fields[field]">
        <v-col class="field-label" cols="12" md="3" v-if="accountRequestData.tracks[track].fields[field].display_name">
          {% verbatim %}{{accountRequestData.tracks[track].fields[field].display_name}}{% endverbatim %}
        </v-col>
        <v-col class="field-label" cols="12" md="3" v-else>
          {% verbatim %}{{field}}{% endverbatim %}
        </v-col>
        <v-col cols="12" md="9" v-if="accountRequestData.tracks[track].fields[field].display_component">
          <component v-if="field == 'harvard_key'"
            :is="accountRequestData.tracks[track].fields[field].display_component"
            :data="accountRequestData[field]">
          </component>
          <component v-else
            :is="accountRequestData.tracks[track].fields[field].display_component"
            :data="accountRequestData.person[field]">
          </component>
        </v-col>
        <v-col cols="12" md="9" v-else>
          <span v-if="accountRequestData.person[field]">{% verbatim %}{{accountRequestData.person[field]}}{% endverbatim %}</span>
          <span v-else>{% verbatim %}{{accountRequestData[field]}}{% endverbatim %}</span>
        </v-col>
      </template>
    </v-row>
  </v-container>
</template>
<style scoped>
  .field-label {
    font-weight: bold;
  }
</style>

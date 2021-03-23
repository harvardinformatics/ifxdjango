<script>

// const STEP_DISPLAY_NAMES = {
//   'welcome': 'Welcome',
//   'existing_email_checked': 'Existing email checked',
//   'existing_full_name_checked': 'Existing full name checked'
// }
export default {
  name: 'IFXDisplayOnboardStep',
  props: {
    step: Object,
    stepName: String,
    trackName: String
  },
  methods: {
    getStepDisplayName() {
      return this.stepName.charAt(0).toUpperCase() + this.stepName.slice(1).replace(/_/g, ' ')
    },
    emitUpdate() {
      this.$emit('update', {
        step: this.stepName,
        value: this.step.value,
        track: this.trackName
      })
    }
  }
}
</script>
<template>
  <v-layout row justify-space-between align-start>
    <v-flex>
      {% verbatim %}{{getStepDisplayName()}}{% endverbatim %}
    </v-flex>
    <v-flex grow>
      &nbsp;
    </v-flex>
    <v-flex shrink>
      <v-checkbox
        indeterminate-icon="cached"
        on-icon="done"
        off-icon="close"
        v-model="step.value"
        true-value="complete"
        false-value="incomplete"
        @click.native="emitUpdate()"
      >
      </v-checkbox>
    </v-flex>
  </v-layout>
</template>
<style scoped>
  .v-input--selection-controls {
    margin: 0;
    padding: 0;
  }
  .v-input--selection-controls {
    margin: 0;
  }
  .v-input--checkbox {
    height: 5px;
  }
  .v-input__control {
    height: 5px;
  }
  .v-messages {
    display: none;
  }
  .application {
    line-height: 1;
  }
</style>

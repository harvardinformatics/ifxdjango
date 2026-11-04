<script>
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
  <v-row justify="space-between" align="start">
    <v-col>
      {% verbatim %}{{getStepDisplayName()}}{% endverbatim %}
    </v-col>
    <v-col>
      &nbsp;
    </v-col>
    <v-col cols="auto">
      <v-checkbox
        :indeterminate-icon="'mdi-cached'"
        :true-icon="'mdi-check'"
        :false-icon="'mdi-close'"
        v-model="step.value"
        true-value="complete"
        false-value="incomplete"
        @click="emitUpdate()"
        hide-details
        density="compact"
      >
      </v-checkbox>
    </v-col>
  </v-row>
</template>
<style scoped>
</style>

<script>
export default {
  name: 'IFXDisplayHarvardKey',
  props: [
    'data'
  ]
}
</script>
<template>
  <v-row>
    <v-col v-if="data">
      Got it
    </v-col>
    <v-col v-else>
      Don't got it
    </v-col>
  </v-row>
</template>
<style scoped>

</style>

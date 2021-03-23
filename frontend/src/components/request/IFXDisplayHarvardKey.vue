<script>
export default {
  name: 'IFXDisplayHarvardKey',
  props: [
    'data'
  ]
}
</script>
<template>
  <v-layout column>
    <v-flex v-if="data">
      Got it
    </v-flex>
    <v-flex v-else>
      Don't got it
    </v-flex>
  </v-layout>
</template>
<style scoped>

</style>

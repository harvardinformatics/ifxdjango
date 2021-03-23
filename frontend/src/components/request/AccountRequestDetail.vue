<script>
import IFXAccountRequestDetail from './IFXAccountRequestDetail'

export default {
  components: {
    IFXAccountRequestDetail
  },
  data() {
    return {
      tracks: {
        general: 'General Information',
        {{project_name}}_user: '{{project_name}} User'
      }
    }
  }
}
</script>
<template>
  <IFXAccountRequestDetail :tracks="tracks">
  </IFXAccountRequestDetail>
</template>
<style scoped>

</style>

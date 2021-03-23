<script>
import IFXRequestList from './IFXRequestList'

export default {
  name: 'AccountRequestList',
  components: {
    IFXRequestList
  },
  data() {
    return {
      dataFields: [], // Fields in the request.data blob that should be surfaced.
      headers: [
        {
          text: 'ID',
          value: 'id'
        },
        {
          text: 'Status',
          align: 'left',
          value: 'currentState'
        },
        {
          text: 'Result',
          align: 'left',
          value: 'result'
        },
        {
          text: 'Requestor',
          value: 'requestor'
        },
        {
          text: 'Created',
          value: 'created'
        },
        {
          text: 'Updated',
          value: 'updated'
        }
      ]
    }
  }
}
</script>

<template>
  <v-container>
    <IFXRequestList :headers="headers" :dataFields="dataFields" requestType="account_request" title="Account Requests">
    </IFXRequestList>
  </v-container>

</template>

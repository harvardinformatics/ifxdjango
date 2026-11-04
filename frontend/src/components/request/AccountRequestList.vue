<script>
import { IFXRequestList }  from 'ifxvue'

export default {
  name: 'AccountRequestList',
  components: {
    IFXRequestList
  },
  data() {
    return {
      dataFields: [],
      headers: [
        {
          title: 'ID',
          key: 'id'
        },
        {
          title: 'Status',
          align: 'start',
          key: 'currentState'
        },
        {
          title: 'Result',
          align: 'start',
          key: 'result'
        },
        {
          title: 'Requestor',
          key: 'requestor'
        },
        {
          title: 'Created',
          key: 'created'
        },
        {
          title: 'Updated',
          key: 'updated'
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

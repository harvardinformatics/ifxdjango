<script>

export default {
  name: 'IFXAccountRequestStateList',
  props: {
    request: Object,
    validStates: Array
  },
  data() {
    return {
      default_approver: this.$requestApi.getDefaultApprover(),
      dialog: false,
      request_state: null,
      headers: [
        { text: 'Status', align: 'left', sortable: false, value: 'name' },
        { text: 'Updated', sortable: false, value: 'created' },
        { text: 'User', align: 'left', sortable: false, value: 'user' },
        { text: 'Comments', sortable: false, value: 'comment' }
      ]
    }
  },
  methods: {
    isUserApprover(request) {
      return this.$requestApi.isUserApprover(request)
    },
    updateRequest() {
      const me = this
      if (this.request_state) {
        this.$requestApi.setState(this.request.id, this.request_state)
          .then(() => {
            me.$router.go()
          })
          .catch((error) => {
            console.log(error)
          })
      }
    }
  }
}
</script>

<template>
  <v-card flat>
    <v-card-title>
      <v-layout row wrap justify-end align-center>
        <v-flex xs8>
          <div class="title">Request Status</div>
        </v-flex>
        <v-flex xs4>
          <v-layout row wrap justify-end align-center>
            <v-flex>
              <v-select
                label="Set state"
                v-model="request_state"
                :items="validStates"
                item-text="display"
                item-value="value"
                @change="updateRequest()"
              >
              </v-select>
            </v-flex>
          </v-layout>
        </v-flex>
      </v-layout>
    </v-card-title>
    <v-layout column>
      <v-flex>
        <v-data-table
          v-if="request.requestStates && request.requestStates.length"
          :headers="this.headers"
          :items="request.requestStates"
          class="elevation-1 mb-3"
          hide-default-footer
        >
            <v-progress-linear slot="progress" color="blue" indeterminate></v-progress-linear>
            <template slot="no-data">
              <span class="no-data">No users returned</span>
            </template>
            <template v-slot:[`item.name`]="{ item }">
                {% verbatim %}{{ item.name | stateDisplay }}{% endverbatim %}
            </template>
            <template v-slot:[`item.created`]="{ item }">
                {% verbatim %}{{ item.created | humanDatetime }}{% endverbatim %}
            </template>
            <template v-slot:[`item.user`]="{ item }">
                {% verbatim %}{{ item.user.full_name == default_approver ? '' : item.user.full_name }}{% endverbatim %}
            </template>
           <template v-slot:[`item.comment`]="{ item }">
                {% verbatim %}{{ item.comment ?  item.comment : "&nbsp;" }}{% endverbatim %}
            </template>
        </v-data-table>
      </v-flex>
    </v-layout>
  </v-card>
</template>
<style>

  table.v-table tbody td, table.v-table tbody th {
    padding: 8px;
    height: 20px;
  }

</style>

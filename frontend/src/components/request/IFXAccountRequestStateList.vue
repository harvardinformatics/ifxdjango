<script>
import { useFilters } from '@/composables/useFilters'

export default {
  name: 'IFXAccountRequestStateList',
  props: {
    request: Object,
    validStates: Array
  },
  setup() {
    const filters = useFilters()
    return { filters }
  },
  data() {
    return {
      default_approver: this.$requestApi.getDefaultApprover(),
      dialog: false,
      request_state: null,
      headers: [
        { title: 'Status', align: 'start', sortable: false, key: 'name' },
        { title: 'Updated', sortable: false, key: 'created' },
        { title: 'User', align: 'start', sortable: false, key: 'user' },
        { title: 'Comments', sortable: false, key: 'comment' }
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
      <v-row justify="end" align="center">
        <v-col cols="8">
          <div class="text-h6">Request Status</div>
        </v-col>
        <v-col cols="4">
          <v-row justify="end" align="center">
            <v-col>
              <v-select
                label="Set state"
                v-model="request_state"
                :items="validStates"
                item-title="display"
                item-value="value"
                @update:model-value="updateRequest()"
                density="compact"
              >
              </v-select>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-card-title>
    <v-row>
      <v-col>
        <v-data-table
          v-if="request.requestStates && request.requestStates.length"
          :headers="headers"
          :items="request.requestStates"
          class="elevation-1 mb-3"
          hide-default-footer
        >
            <template v-slot:loading>
              <v-progress-linear color="blue" indeterminate></v-progress-linear>
            </template>
            <template v-slot:no-data>
              <span class="no-data">No users returned</span>
            </template>
            <template v-slot:[`item.name`]="{ item }">
                {% verbatim %}{{ filters.stateDisplay(item.name) }}{% endverbatim %}
            </template>
            <template v-slot:[`item.created`]="{ item }">
                {% verbatim %}{{ filters.humanDatetime(item.created) }}{% endverbatim %}
            </template>
            <template v-slot:[`item.user`]="{ item }">
                {% verbatim %}{{ item.user.full_name == default_approver ? '' : item.user.full_name }}{% endverbatim %}
            </template>
           <template v-slot:[`item.comment`]="{ item }">
                {% verbatim %}{{ item.comment ?  item.comment : "&nbsp;" }}{% endverbatim %}
            </template>
        </v-data-table>
      </v-col>
    </v-row>
  </v-card>
</template>
<style>

  table.v-table tbody td, table.v-table tbody th {
    padding: 8px;
    height: 20px;
  }

</style>

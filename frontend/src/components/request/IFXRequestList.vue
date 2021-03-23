<script>
import { debounce } from 'lodash'
import { mapActions } from 'vuex'

export default {
  name: 'IFXRequestList',
  props: {
    headers: Array,
    dataFields: Array,
    requestType: String,
    title: String
  },
  data() {
    return {
      lockedFieldTemplates: ['id', 'requestType', 'currentState', 'created', 'updated'], // table fields whose templates cannot be customized
      requests: [],
      includeCompleted: true,
      search: localStorage.getItem(`${this.$api.vars.appName}_RequestListSearch`) || '',
      loading: null,
      selected: [],
      rowsPerPage: parseInt(localStorage.getItem(`${this.$api.vars.appName}_RequestListRowsPerPage`)) || 10,
      rowsPerPageItems: [10, 20, { text: 'All', value: -1 }],
    }
  },
  computed: {
    computedHeaders() {
      return this.headers.filter(h => !h.hide || !this.$vuetify.breakpoint[h.hide])
    }
  },
  methods: {
    display(header, item) {
      let result = item[header.value]
      if (header.display) {
        result = header.display(item[header.value])
      }
      return result
    },
    getDetailComponent(requestType) {
      return this.$requestApi.getRequestTypeDetailComponent(requestType)
    },
    getRequests: debounce(async function () {
      this.loading = true
      const me = this
      this.requests = await this.$requestApi.getRequestList(this.dataFields, this.search, this.includeCompleted, this.requestType)
        // .then(
        //   response => {
        //     me.requests = response.data.requests
        //     console.log('requests')
        //     console.log(me.requests)
        //     me.loading = false
        //   }
        // )
        .catch(error => {
          me.errored = true
          me.showMessage(error)
        })
      this.loading = false
    }, 1000),
    ...mapActions([
      'showMessage'
    ])
  },
  mounted() {
    this.getRequests()
  },
  watch: {
    rowsPerPage: function () {
      localStorage.setItem(`${this.$api.vars.appName}_RequestListRowsPerPage`, this.rowsPerPage.toString())
    },
    search: function () {
      localStorage.setItem(`${this.$api.vars.appName}_RequestListSearch`, this.search)
      this.getRequests()
    },
    includeCompleted: function () {
      this.getRequests()
    }
  }
}
</script>
<template>
  <v-container fill-height>
    <v-layout column>
      <v-flex xs12>
        <v-card>
          <v-card-title>
            <v-layout row align-center justify-space-between style="padding: 10px">
              <v-flex xs4>
                <span class="subheading">{{ title }}</span>
              </v-flex>
              <v-flex grow>
                <v-layout row>
                  <v-flex>
                    <v-text-field
                        v-model="search"
                        label="Search"
                        single-line
                        hide-details
                    ></v-text-field>
                  </v-flex>
                  <v-flex xs2>
                    <v-tooltip top>
                      <template v-slot:activator="{ on }">
                        <v-btn v-on="on" :disabled="!search" fab small color="white" @click="search = ''">
                          <v-icon>clear</v-icon>
                        </v-btn>
                      </template>
                      <span>Clear search</span>
                    </v-tooltip>
                  </v-flex>
                </v-layout>
              </v-flex>
              <v-flex xs3>
                <v-checkbox label="Include completed" v-model="includeCompleted"></v-checkbox>
              </v-flex>
            </v-layout>
          </v-card-title>
          <v-data-table
            v-model="selected"
            :search="search"
            :headers="computedHeaders"
            :items-per-page.sync="rowsPerPage"
            :items="requests"
            :loading="loading"
            item-key="id"
            class="elevation-1"
            :footer-props="{
              itemsPerPageOptions: rowsPerPageItems
            }"
          >
            <v-progress-linear slot="progress" color="blue" indeterminate></v-progress-linear>
            <template slot="no-data">
              <span class="no-data">No users returned</span>
            </template>
            <template v-slot:[`item.id`]="{ item }">
                <router-link class="no_decoration" :to="{name: getDetailComponent(item.requestType), params: {id:item.id}}" exact>
                  <span>{% verbatim %}{{item.id}}{% endverbatim %}</span>
                </router-link>
            </template>
            <template v-slot:[`item.requestType`]="{ item }">
                {% verbatim %}{{ item.requestType | stateDisplay }}{% endverbatim %}
            </template>
            <template v-slot:[`item.currentState`]="{ item }">
                {% verbatim %}{{ item.currentState | stateDisplay }}{% endverbatim %}
            </template>
           <template v-slot:[`item.created`]="{ item }">
                {% verbatim %}{{ item.created | humanDatetime }}{% endverbatim %}
            </template>
            <template v-slot:[`item.updated`]="{ item }">
                {% verbatim %}{{ item.updated | humanDatetime }}{% endverbatim %}
            </template>
            <template v-for="header in headers.filter(n => !lockedFieldTemplates.includes(n.value))" v-slot:[`item.${header.value}`]="{ item }">
              <span v-if="header.custom" v-bind:key="header.value">
                <slot :name="header.value" :item="item"></slot>
              </span>
              <span v-else v-bind:key="header.value">
                {% verbatim %}{{ display(header, item) }}{% endverbatim %}
              </span>
            </template>
            <v-alert id="no-results"
              slot="no-results"
              :value="true"
              color="error"
              icon="warning"
            >Your search found no results.</v-alert>
          </v-data-table>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<style lang="scss" scoped>
  .v-input--radio-group__input {
    margin-top: 1em;
  }
  table.compact tbody tr td {
    padding: 0 5px;
  }
  table.v-table thead th {
    text-align: left;
  }
  .v-card__title {
    border: none;
  }
</style>

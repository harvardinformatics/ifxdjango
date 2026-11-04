<script>
import moment from 'moment'
import forEach from 'lodash/forEach'
import { useFilters } from '@/composables/useFilters'
import IFXAccountRequestTrackDetail from './IFXAccountRequestTrackDetail.vue'
import IFXAccountRequestStateList from './IFXAccountRequestStateList.vue'
import IFXDisplayOnboardStep from './IFXDisplayOnboardStep.vue'
import IFXRequestCommentList from './IFXRequestCommentList.vue'

export default {
  name: 'IFXAccountRequestDetail',
  components: {
    IFXAccountRequestTrackDetail,
    IFXAccountRequestStateList,
    IFXRequestCommentList,
    IFXDisplayOnboardStep
  },
  props: {
    tracks: Object
  },
  setup() {
    const filters = useFilters()
    return { filters }
  },
  data() {
    return {
      request: null,
      approval: null,
      valid_states: [],
      refresh_timer: null,
      updating_expiration_date: false,
      expiration_date_menu: false
    }
  },
  methods: {
    addEmptyComment() {
      if (this.refresh_timer) {
        clearInterval(this.refresh_timer)
      }
      this.request.requestComments.unshift(this.$requestApi.newRequestComment())
    },
    handleStepChange(step) {
      if (this.refresh_timer) {
        clearInterval(this.refresh_timer)
      }
      if (step && step.value === 'incomplete') {
        if (step.track !== 'general' && this.tracks.hasOwnProperty(step.track)) {
          this.request.setTrackStepIncomplete(step.track, 'final_approval')
        }
      }
    },
    isAppTrack(track) {
      return this.tracks.hasOwnProperty(track)
    },
    getTrackDisplayName(track) {
      return this.tracks[track]
    },
    isDjangoStaff() {
      return this.$api.isDjangoStaff
    },
    canBeApproved() {
      return this.$requestApi.canBeApproved(this.request)
    },
    requestExpired() {
      return moment(this.request.continuationKeyExpiration).isBefore(moment())
    },
    updatingExpirationDate() {
      this.updating_expiration_date = true
      clearInterval(this.refresh_timer)
    },
    async updateRequestComment(commentData) {
      if (commentData.text) {
        this.request.requestComments[commentData.index] = {
          text: commentData.text,
          request: this.request.id
        }
      }
      this.updateRequest(false)
        .then(() => {
          this.getRequest(this.$route.params.id)
        })
    },
    async updateRequest(notify) {
      this.updating_expiration_date = false
      if (notify) {
        this.request.onBoardRequest.notifyRequestorOfUpdates = true
      }
      const me = this
      console.log('going to update request')
      console.log(this.request)
      await this.$requestApi.updateAccountRequest(this.request)
        .then(() => {
          const message = 'Account request updated'
          me.showMessage({ message })
        })
        .catch((error) => {
          me.showMessage(error)
        })
    },
    updateRequestState() {
      if (this.approval) {
        if (this.refresh_timer) {
          clearInterval(this.refresh_timer)
        }
        const me = this
        let newState = this.request.currentState
        if (this.approval === 'approve' && this.request.currentState.includes('APPROVAL_PENDING')) {
          newState = this.request.currentState.replace('APPROVAL_PENDING', 'APPROVED')
        } else if (this.approval === 'reject') {
          newState = 'REJECTED'
        } else {
          console.log('this is weird')
        }
        this.$requestApi.setState(this.request.id, newState)
          .then(() => {
            me.$router.go()
          })
          .catch((error) => {
            me.showMessage(error)
          })
      }
    },
    getRequest(id) {
      const me = this
      this.$requestApi.getRequest(id)
        .then((response) => {
          me.request = response
          console.log('request is ')
          console.log(me.request)
          if (me.request.result) {
            clearInterval(me.refresh_timer)
          }
          this.$requestApi.getValidProcessorStates(me.request.processor)
            .then((res) => {
              forEach(res.data, (state) => {
                const display = me.filters.stateDisplay(state)
                me.valid_states.push({ display: display, value: state })
              })
            })
            .catch((error) => {
              this.showMessage(error)
            })
        })
        .catch((error) => {
          console.log(error)
          this.showMessage(error)
        })
    }
  },
  computed: {
    django_admin_url: function () {
      return [this.$api.urls.DJANGO_ADMIN_ROOT, 'ifxrequest', 'request', this.request.id, 'change/'].join('/')
    }
  },
  beforeRouteLeave(to, from, next) {
    clearInterval(this.timer)
    next()
  },
  mounted() {
    const me = this
    this.getRequest(me.$route.params.id)
    this.refresh_timer = null
    this.refresh_timer = setInterval(() => {
      if (me.$route.params.id) {
        me.getRequest(me.$route.params.id)
      }
    }, 4000)
  }
}
</script>
<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card v-if="request">
          <v-card-title>
            <v-row justify="start" align="center">
              <v-col>
                <span class="text-h6">Account request from {% verbatim %}{{request.fullName}}{% endverbatim %}</span>
              </v-col>
              <v-col>
                <span v-if="request.result == 'SUCCESS'"><v-icon color="success">mdi-thumb-up</v-icon>&nbsp;Success</span>
                <span v-else-if="request.result == 'FAILED'"><v-icon color="error">mdi-alert-circle-outline</v-icon>&nbsp;Failed</span>
                <span v-else-if="request.result == 'REJECTED'"><v-icon color="error">mdi-thumb-down</v-icon>&nbsp;Rejected</span>
                <span v-else><v-icon color="grey">mdi-cached</v-icon>&nbsp;{% verbatim %}{{filters.stateDisplay(request.currentState)}}{% endverbatim %}</span>
              </v-col>
              <v-col cols="auto">
                <v-tooltip location="top">
                  <template v-slot:activator="{ props }">
                    <v-btn v-bind="props" icon size="small"
                      class="item-add"
                      color="green"
                      @click="addEmptyComment()"
                    >
                      <v-icon>mdi-playlist-plus</v-icon>
                    </v-btn>
                  </template>
                  <span>Add comment to request</span>
                </v-tooltip>
              </v-col>
              <v-col cols="auto">
                <v-tooltip location="top">
                  <template v-slot:activator="{ props }">
                    <v-btn v-bind="props" icon size="small" color="info" v-show="isDjangoStaff()" :href="django_admin_url">
                      <v-icon color="yellow">mdi-key</v-icon>
                    </v-btn>
                  </template>
                  <span>View request Django admin form</span>
                </v-tooltip>
              </v-col>
            </v-row>
          </v-card-title>
          <v-container>
            <v-row>
              <v-col cols="12" v-if="request.requestComments.length > 0">
                <IFXRequestCommentList :request="request" @update="updateRequestComment"/>
              </v-col>
              <v-col cols="6">
                <v-row justify="start" align="center">
                  <v-col cols="auto" class="expiration-date-label">
                    Onboard request
                    <span v-if="requestExpired()">expired</span>
                    <span v-else>expires</span>
                  </v-col>
                  <v-col v-if="updating_expiration_date" cols="auto">
                    <v-menu
                      v-model="expiration_date_menu"
                      :close-on-content-click="false"
                    >
                      <template v-slot:activator="{ props }">
                        <v-text-field
                          :model-value="request.continuationKeyExpiration"
                          v-bind="props"
                          readonly
                          density="compact"
                        >
                        </v-text-field>
                      </template>
                      <v-date-picker
                        v-model="request.continuationKeyExpiration"
                        @update:model-value="updateRequest()"
                      >
                     </v-date-picker>
                    </v-menu>
                  </v-col>
                  <v-col v-else cols="auto">
                    {% verbatim %}{{request.continuationKeyExpiration}}{% endverbatim %}
                  </v-col>
                  <v-col>
                    <v-btn :disabled="updating_expiration_date" icon size="small" color="info" @click="updatingExpirationDate()">
                      <v-icon>mdi-calendar-today</v-icon>
                    </v-btn>
                  </v-col>
                </v-row>
              </v-col>
              <v-col cols="6" v-if="canBeApproved()">
                <v-row justify="end">
                  <v-col>
                    &nbsp;
                  </v-col>
                  <v-col cols="auto">
                    <v-radio-group inline v-model="approval" @update:model-value="updateRequestState()">
                      <v-radio label="Approve" value="approve"></v-radio>
                      <v-radio label="Reject" value="reject"></v-radio>
                    </v-radio-group>
                  </v-col>
                </v-row>
              </v-col>
              <v-col cols="7">
                <v-row>
                  <v-col v-for="track in request.tracks.order" :key="track">
                    <IFXAccountRequestTrackDetail v-if="request && isAppTrack(track)" :track="track" :trackTitle="getTrackDisplayName(track)" :accountRequestData="request.onBoardRequest.data"/>
                  </v-col>
                </v-row>
              </v-col>
              <v-col>
                <v-container>
                  <v-row>
                    <v-col>
                      <span class="text-h6">Onboarding Steps</span>
                    </v-col>
                  </v-row>
                  <v-row v-for="track in request.tracks.order" :key="track">
                    <v-col v-if="isAppTrack(track)">
                      <div v-for="step in request.tracks[track].order" :key="step">
                        <IFXDisplayOnboardStep v-if="step !== 'completed_request'" @update="handleStepChange" :step="request.tracks[track][step]" :stepName="step" :trackName="track"/>
                      </div>
                    </v-col>
                  </v-row>
                  <v-row justify="center">
                    <v-col class="text-center">
                      <v-btn
                        color="primary"
                        @click="updateRequest('notify')"
                      >Update Steps
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-container>
              </v-col>
            </v-row>
            <v-row>
              <v-col v-if="request">
                <IFXAccountRequestStateList :request="request" :validStates="valid_states"/>
              </v-col>
            </v-row>
          </v-container>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
<style scoped>
  .expiration-date-label {
    font-size: 18px;
    color: rgba(0,0,0,0.87);
  }
</style>

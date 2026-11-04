<script>
import { useFilters } from '@/composables/useFilters'

export default {
  name: 'IFXRequestCommentList',
  props: {
    request: Object
  },
  setup() {
    const filters = useFilters()
    return { filters }
  },
  data() {
    return {}
  },
  methods: {
    updateRequestComment(index, text) {
      const data = { index: index }
      if (text) {
        data.text = text
      }
      this.$emit('update', data)
    }
  }
}
</script>
<template>
  <v-container>
    <v-row align="center">
      <v-col>
        <v-row>
          <v-col cols="12" v-for="(requestComment, index) in request.requestComments" :key="requestComment.id">
            <v-row justify="start" align="center">
              <v-col v-if="requestComment.id" cols="12" md="8" class="request-comment">
                <span v-html="requestComment.text"></span>
              </v-col>
              <v-col v-else cols="12" md="7" class="request-comment">
                <v-textarea
                  v-model="request.requestComments[index].text"
                  auto-grow
                  clearable
                  rows="3"
                  variant="solo"
                >
                </v-textarea>
              </v-col>
              <v-col v-if="requestComment.id" cols="10" md="3" class="request-author" align-self="end">
                <span>{{requestComment.author}}</span>&nbsp;
                <span style="white-space: nowrap;">{% verbatim %}{{filters.humanDatetime(requestComment.created)}}{% endverbatim %}</span>
              </v-col>
              <v-col v-if="requestComment.id" cols="auto">
                <v-tooltip location="top">
                  <template v-slot:activator="{ props }">
                    <v-btn v-bind="props" icon size="small" variant="text"
                      class="item-delete"
                      color="error"
                      @click="request.requestComments.splice(index, 1) && updateRequestComment(index)"
                    >
                      <v-icon>mdi-close</v-icon>
                    </v-btn>
                  </template>
                  <span>Remove comment</span>
                </v-tooltip>
              </v-col>
              <v-col v-else cols="auto">
                <v-tooltip location="top">
                  <template v-slot:activator="{ props }">
                    <v-btn v-bind="props" icon size="small" variant="text"
                      class="item-save"
                      color="green"
                      @click="updateRequestComment(index, request.requestComments[index].text)"
                    >
                      <v-icon>mdi-check</v-icon>
                    </v-btn>
                  </template>
                  <span>Save comment</span>
                </v-tooltip>
                <v-tooltip location="top">
                  <template v-slot:activator="{ props }">
                    <v-btn v-bind="props" icon size="small" variant="text"
                      class="item-delete"
                      color="error"
                      @click="request.requestComments.splice(index, 1)"
                    >
                      <v-icon>mdi-close</v-icon>
                    </v-btn>
                  </template>
                  <span>Remove comment</span>
                </v-tooltip>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>
<style>
  .request-comment {
    color: #00796B;
    font-size: larger;
    margin: 0em;
  }
  .request-author {
    font-style: italic;
  }
</style>

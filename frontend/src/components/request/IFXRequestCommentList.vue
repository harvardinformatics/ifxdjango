<script>
// TODO prevent mutating props
/* eslint-disable */
export default {
  name: 'IFXRequestCommentList',
  props: {
    request: Object
  },
  data() {
    return {}
  },
  methods: {
    updateRequestComment(index, text) {
      // when passed null in text, it means to remove
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
    <v-layout row align-center>
      <v-flex grow>
        <v-layout row wrap>
          <v-flex xs12 v-for="(requestComment, index) in request.requestComments" :key="requestComment.id">
            <v-layout row wrap justify-start align-center>
              <v-flex v-if="requestComment.id" xs12 md8 class="request-comment">
                <span v-html="requestComment.text"></span>
              </v-flex>
              <v-flex v-else xs12 md7 class="request-comment">
                <v-textarea
                  v-model="request.requestComments[index].text"
                  auto-grow
                  clearable
                  rows="3"
                  solo
                >
                </v-textarea>
              </v-flex>
              <v-flex v-if="requestComment.id" xs10 shrink md3 class="request-author" align-content-end>
                <span>{{requestComment.author}}</span>&nbsp;
                <span style="white-space: nowrap;">{% verbatim %}{{requestComment.created | humanDatetime}}{% endverbatim %}</span>
              </v-flex>
              <v-flex v-if="requestComment.id">
                <v-tooltip top>
                  <template v-slot:activator="{ on }">
                    <v-btn v-on="on" fab small text
                      class="item-delete"
                      color="error"
                      @click="request.requestComments.splice(index, 1) && updateRequestComment(index)"
                    >
                      <v-icon dark >clear</v-icon>
                    </v-btn>
                  </template>
                  <span>Remove comment</span>
                </v-tooltip>
              </v-flex>
              <v-flex v-else>
                <v-tooltip top>
                  <template v-slot:activator="{ on }">
                    <v-btn v-on="on" fab small text
                      class="item-save"
                      color="green"
                      @click="updateRequestComment(index, request.requestComments[index].text)"
                    >
                      <v-icon dark>done</v-icon>
                    </v-btn>
                  </template>
                  <span>Save comment</span>
                </v-tooltip>
                <v-tooltip top>
                  <template v-slot:activator="{ on }">
                    <v-btn v-on="on" fab small text
                      class="item-delete"
                      color="error"
                      @click="request.requestComments.splice(index, 1)"
                    >
                      <v-icon dark >clear</v-icon>
                    </v-btn>
                  </template>
                  <span>Remove comment</span>
                </v-tooltip>
              </v-flex>
            </v-layout>
          </v-flex>
        </v-layout>
      </v-flex>
    </v-layout>
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

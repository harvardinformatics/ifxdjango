<script>
export default {
  name: 'NotFound',
}
</script>

<template>
  <v-container grid-list-md fill-height >
    <v-layout row>
      <v-flex>
        <v-card style="padding: 10px">
          <v-card-title style="border-bottom: 1px solid #aaa">
            <span class="display-1" style="color: #db564c">Not Found!</span>
          </v-card-title>
          <v-container>
            <v-layout row align-center justify-space-around>
              <v-flex xs6 class="title">
                <p>
                  The item you're looking for does not exist
                </p>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<style scoped lang="css">
  .compact-container {
    padding: 5px;
  }
</style>

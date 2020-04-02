<script>
import auth from "@/auth"
import { DJANGO_ADMIN_ROOT } from "@/urls"
import { mapActions, mapGetters } from "vuex"
import { APIService } from "./api"

const api = new APIService()

export default {
  name: "App",
  data: function() {
    return {
      drawer: true,
      bigMiniToggle: false,
      smallMiniToggle: true,
      authenticated: false,
      name: null
    }
  },
  methods: {
    ...mapActions(["showMessage", "toggleDialog"]),
    async init() {
      await this.sleep(100)
      if (auth.isAuthenticated()) {
        this.authenticated = true
        this.name = auth.getFirstName()
          ? auth.getFirstName()
          : auth.getUsername()
      }
    },
    sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms))
    }
  },
  mounted: function() {
    this.init()
  },
  computed: {
    mini: {
      get: function() {
        return this.$vuetify.breakpoint.lgAndUp
          ? this.bigMiniToggle
          : this.smallMiniToggle
      },
      // By default the sidebar is full size for big screens
      // and mini for smaller ones.  The two values are separately managed.
      // If you toggle big on a small screen, the assumption is that you'll
      // want it big on a big screen.  If you toggle it small on a big
      // screen, you probably want it small on a small screen as well.
      set: function() {
        if (this.$vuetify.breakpoint.lgAndUp) {
          if (this.bigMiniToggle) {
            // eslint-disable-next-line
            this.smallMiniToggle = true
          }
          return this.bigMiniToggle
        } else {
          if (!this.smallMiniToggle) {
            // eslint-disable-next-line
            this.bigMiniToggle = false
          }
          return this.smallMiniToggle
        }
      }
    },
    auth: function() {
      // Make auth available to the template
      return auth
    }
  }
}
</script>

<template>
  <v-app id="inspire">
    <Message></Message>
    <v-navigation-drawer
      v-model="drawer"
      :mini-variant.sync="mini"
      clipped
      :mobile-break-point="400"
      app
    >
      <v-list>
        <v-list-item :to="{path: '/'}">
          <v-list-item-action>
            <v-icon>home</v-icon>
          </v-list-item-action>
          <v-list-item-title>Home</v-list-item-title>
        </v-list-item>
        <v-list-item :to="{path: '/demo'}">
          <v-list-item-action>
            <v-icon>assignment</v-icon>
          </v-list-item-action>
          <v-list-item-title>Demo</v-list-item-title>
        </v-list-item>
      </v-list>
      <template v-slot:append>
        <v-list>
          <v-list-item v-if="authenticated" :to="{path: '/logout'}">
            <v-list-item-action>
              <v-icon>person</v-icon>
            </v-list-item-action>
            <v-list-item-title>Login</v-list-item-title>
          </v-list-item>
          <v-list-item v-else :to="{path: '/login'}">
            <v-list-item-action>
              <v-icon>person</v-icon>
            </v-list-item-action>
            <v-list-item-title>Login</v-list-item-title>
          </v-list-item>
        </v-list>
      </template>
    </v-navigation-drawer>

    <v-app-bar
      app
      clipped-left
      id="app-bar"
      color="primary"
    >
      <v-app-bar-nav-icon
        v-if="$vuetify.breakpoint.mdAndUp"
        @click.native="bigMiniToggle = !bigMiniToggle"
      >
        <v-icon>menu</v-icon>
      </v-app-bar-nav-icon>
      <v-app-bar-nav-icon
        v-if="$vuetify.breakpoint.smAndDown"
        @click.native="smallMiniToggle = !smallMiniToggle"
      >
        <v-icon>menu</v-icon>
      </v-app-bar-nav-icon>
      <v-toolbar-title>
        <span class="app-title">IFXTEST</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-chip v-if="name" color="white">
        Welcome,
        <span class="username">{{name}}</span>
      </v-chip>
    </v-app-bar>

    <v-content>
      <router-view :key="$route.fullPath"></router-view>
    </v-content>

    <v-footer color="secondary" id="footer" app>
      <span class="white--text">2020 The Presidents and Fellows of Harvard College.</span>
    </v-footer>
  </v-app>
</template>
<style lang="css">
html {
  overflow-y: auto !important;
}

.username {
  font-weight: 700;
  margin-left: 0.3rem;
}

.v-list {
  padding: 0 !important;
}

.login-btn-wrapper {
  /* margin: 1rem; */
}

.login-btn-text {
  margin-left: .5rem;
}

.admin-group {
  background-color: rgb(250, 238, 238);
}

#app-bar {
  max-height: 64px;
}

.app-title {
  color: white;
  margin: 0 5rem 0 3rem;
}

#footer {
  padding: 12px;
}
.required label::after {
  content: " *";
}
</style>

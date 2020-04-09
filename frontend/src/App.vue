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
      isDrawerOpenMobile: false,
      drawerMiniPref: null,
      bigMiniToggle: false,
      smallMiniToggle: true,
      isLoggedIn: false
    }
  },
  methods: {
    ...mapActions(["showMessage", "toggleDialog"]),
    sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms))
    },
    isAuthenticated() {
      return auth.isAuthenticated() || this.isLoggedIn
    },
    getLoginLogoutString(lower) {
      const string = this.isAuthenticated() ? "Logout" : "Login"
      return lower ? string.toLowerCase() : string
    },
    toggleDrawerOpenMobile() {
      this.isDrawerOpenMobile = !this.isDrawerOpenMobile
    },
    toggleDrawerPref() {
      if (this.drawerMiniPref === null) {
        this.drawerMiniPref = !this.mini
      } else if (this.drawerMiniPref === false) {
        this.drawerMiniPref = true
      } else {
        this.drawerMiniPref = false
      }
    }
  },
  computed: {
    mobile: function() {
      return this.$vuetify.breakpoint.xs
    },
    mini: function() {
      // If user sets a drawerMini preference, this takes priority
      if (this.drawerMiniPref !== null) {
        return this.drawerMiniPref
      }
      // Otherwise, navigation drawer is minified on smaller screens only
      if (this.$vuetify.breakpoint.lgAndUp) {
        return false
      } else {
        return true
      }
    },
    name: function() {
      const firstName = auth.getFirstName()
      return firstName ? firstName : auth.getUsername()
    }
  },
  created: function() {
    let me = this
    this.eventHub.$on("isLoggedIn", bool => {
      me.isLoggedIn = bool
    })
  }
}
</script>

<template>
  <v-app>
    <Message></Message>
    <v-navigation-drawer
      :value="mobile ? isDrawerOpenMobile : true"
      :mini-variant="mini"
      clipped
      :mobile-break-point="200"
      app
    >
      <v-list class="pt-0">
        <v-tooltip right>
          <template v-slot:activator="{ on }">
            <v-list-item v-on="mini ? on : false" :to="{path: '/'}">
              <v-list-item-action>
                <v-icon>home</v-icon>
              </v-list-item-action>
              <v-list-item-title>Home</v-list-item-title>
            </v-list-item>
          </template>
          <span>Home</span>
        </v-tooltip>
        <v-tooltip right>
          <template v-slot:activator="{ on }">
            <v-list-item v-on="mini ? on : false" :to="{path: '/demo'}">
              <v-list-item-action>
                <v-icon>assignment</v-icon>
              </v-list-item-action>
              <v-list-item-title>Demo</v-list-item-title>
            </v-list-item>
          </template>
          <span>Demo</span>
        </v-tooltip>
      </v-list>
      <template v-slot:append>
        <v-tooltip right>
          <template v-slot:activator="{ on }">
            <v-list-item v-on="mini ? on : false" :to="{path: `/${getLoginLogoutString('lower')}`}">
              <v-list-item-action>
                <v-icon>person</v-icon>
              </v-list-item-action>
              <v-list-item-title>{% verbatim %}{{getLoginLogoutString()}}{% endverbatim %}
              </v-list-item-title>
            </v-list-item>
          </template>
          <span>{% verbatim %}{{getLoginLogoutString()}}{% endverbatim %}
          </span>
        </v-tooltip>
      </template>
    </v-navigation-drawer>

    <v-app-bar app clipped-left id="app-bar" color="primary">
      <v-app-bar-nav-icon v-if="mobile" @click.native="() => toggleDrawerOpenMobile()">
        <v-icon>menu</v-icon>
      </v-app-bar-nav-icon>
      <v-app-bar-nav-icon v-else @click.native="() => toggleDrawerPref()">
        <v-icon>menu</v-icon>
      </v-app-bar-nav-icon>
      <v-toolbar-title class="app-title">
        <span class="app-title-text">Project Name</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-chip v-if="isAuthenticated()" color="white">
        Welcome,
        <span class="username">{% verbatim %}{{name}}{% endverbatim %}</span>
      </v-chip>
    </v-app-bar>

    <v-content>
      <router-view :key="$route.fullPath"></router-view>
    </v-content>

    <v-footer color="secondary" id="footer" app>
      <span class="white--text">2020 The Presidents and Fellows of Harvard College</span>
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

  .login-btn-text {
    margin-left: 0.5rem;
  }

  .admin-group {
    background-color: rgb(250, 238, 238);
  }

  .app-title-text {
    color: white;
    padding-left: 0;
  }

  #footer {
    padding: 12px;
  }
  .required label::after {
    content: " *";
  }
</style>

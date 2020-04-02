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
    ...mapActions([
      "showMessage",
      "toggleDialog"
    ]),
    sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms))
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
    loginLogout: function() {
      return this.isAuthenticated ? 'Logout' : 'Login'
    },
    mobile: function() {
      return this.$vuetify.breakpoint.xs
    },
    mini: function() {
      if (this.drawerMiniPref !== null) {
        return this.drawerMiniPref
      }

      if (this.$vuetify.breakpoint.lgAndUp) {
        return false
      } else {
        return true
      }
    },
    isAuthenticated: function() {
      if (!this.isLoggedIn) {
        return false
      }
      return auth.isAuthenticated()
    },
    name: function() {
      if (!this.isLoggedIn) {
        return ""
      }
      const firstName = auth.getFirstName()
      return firstName ? firstName : auth.getUsername()
    }
  },
  mounted: function() {
    let me = this
    this.eventHub.$on('isLoggedIn', bool => {
      console.log(`isLoggedIn: ${bool}`)
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
      <v-list>
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
        <v-list>
          <v-tooltip right>
            <template v-slot:activator="{ on }">
            <v-list-item v-on="mini ? on : false" :to="{path: `/${loginLogout.toLowerCase()}`}">
              <v-list-item-action>
                <v-icon>person</v-icon>
              </v-list-item-action>
              <v-list-item-title>{{loginLogout}}</v-list-item-title>
            </v-list-item>
            </template>
            <span>{{loginLogout}}</span>
          </v-tooltip>
        </v-list>
      </template>
    </v-navigation-drawer>

    <v-app-bar
      app
      clipped-left
      id="app-bar"
      color="primary"
    >
      <v-app-bar-nav-icon v-if="mobile" @click.native="() => toggleDrawerOpenMobile()">
        <v-icon>menu</v-icon>
      </v-app-bar-nav-icon>
      <v-app-bar-nav-icon v-else @click.native="() => toggleDrawerPref()">
        <v-icon>menu</v-icon>
      </v-app-bar-nav-icon>
      <v-toolbar-title>
        <span class="app-title">IFXTEST</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-chip v-if="isAuthenticated" color="white">
        Welcome,
        <span class="username">{{name}}</span>
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

.v-list {
  padding: 0 !important;
}

.login-btn-text {
  margin-left: .5rem;
}

.admin-group {
  background-color: rgb(250, 238, 238);
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

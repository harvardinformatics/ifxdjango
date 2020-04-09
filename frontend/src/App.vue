<script>
import { mapActions } from 'vuex'
import { pick } from 'lodash'
import { IFXMessageDisplay } from 'ifxvue'
import navData from './navData'

export default {
  name: 'App',
  components: {
    IFXMessageDisplay
  },
  data() {
    return {
      isDrawerOpenMobile: false,
      drawerMiniPref: null,
      loading: false,
    }
  },
  methods: {
    ...mapActions(['showMessage', 'toggleDialog']),
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
    },
    getLoginLogoutString(lower) {
      const string = this.$api.authUser.isAuthenticated ? 'Logout' : 'Login'
      return lower ? string.toLowerCase() : string
    },
    loginLogout() {
      if (this.$api.authUser.isAuthenticated) {
        return this.$api.auth.logout()
          .then((res) => this.showMessage(res))
          .then(() => {
            if (this.rt.name !== 'Home') {
              this.rtr.push({ name: 'Home' })
            }
          })
          .catch(error => this.showMessage(error))
      }
      return this.$api.auth.login()
        .then(res => this.showMessage(res))
        .catch(error => this.showMessage(error))
    }
  },
  computed: {
    mobile() {
      return this.$vuetify.breakpoint.xs
    },
    mini() {
      // If user sets a drawerMini preference, this takes priority
      if (this.drawerMiniPref !== null) {
        return this.drawerMiniPref
      }
      // Otherwise, navigation drawer is minified on smaller screens only
      if (this.$vuetify.breakpoint.lgAndUp) {
        return false
      }
      return true
    },
    displayName() {
      // return this.firstName ? this.firstName : this.username
      const firstName = this.$api.authUser.firstName
      const username = this.$api.authUser.username
      let displayName = firstName || username
      if (!displayName) {
        console.error('No name to display')
        displayName = 'User'
      }
      return displayName
    },
    computedNav() {
      // By default, these keys are omitted from the nav data
      const addedKeys = ['actions']
      if (this.$api.authUser.isAuthenticated && this.$api.authUser.isAdmin) {
        const adminKeys = ['admin', 'staff', 'mailing']
        addedKeys.push(...adminKeys)
      }
      return pick(navData, addedKeys)
    },
    fullPageComponents() {
      return ['Home', 'Login', 'Logout']
    }
  },
  created() {
    this.loading = true
  },
  mounted() {
    // Is the test failing because it's loading too fast before the data can return?
    this.$nextTick(() => this.loading = false)
  }
}
</script>

<template>
  <v-app v-if="!loading">
    <IFXMessageDisplay/>
    <v-navigation-drawer
      :value="mobile ? isDrawerOpenMobile : true"
      :mini-variant="mini"
      clipped
      :mobile-breakpoint="200"
      app
    >
      <v-list nav dense expand>
        <v-tooltip>
          <template v-slot:activator="{ on }">
            <v-list-item
              link
              v-on="mini ? on : false"
              :to="{name: 'Home'}"
              class="nav-link"
            >
              <v-list-item-icon>
                <v-icon>home</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>Home</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </template>
          <span>Home</span>
        </v-tooltip>
        <v-list-group
          v-for="(group, name) in computedNav"
          :key="name"
          :prepend-icon="group.icon"
          :value="true"
        >
          <template v-slot:activator>
            <v-list-item-title>{% verbatim %}{{group.title}}{% endverbatim %}</v-list-item-title>
          </template>
          <v-tooltip right v-for="item in group.items" :key="item.link">
            <template v-slot:activator="{ on }">
              <v-list-item
                link
                v-on="mini ? on : false"
                :to="{name: item.link}"
                :class="mini ? 'nav-link nav-link-mini' : 'nav-link nav-link-expanded'"
                :disabled="item.hasOwnProperty('disabled') && item.disabled"
                >
                <v-list-item-icon>
                  <v-icon>{% verbatim %}{{item.icon}}{% endverbatim %}</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>{% verbatim %}{{item.title}}{% endverbatim %}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </template>
            <span>{% verbatim %}{{item.title}}{% endverbatim %}</span>
          </v-tooltip>
        </v-list-group>
      </v-list>
      <template v-slot:append>
        <v-tooltip right>
          <template v-slot:activator="{ on }">
            <v-list-item
              v-on="mini ? on : false"
              data-test='loginLogoutBtn'
              @click.prevent="loginLogout"
            >
              <v-list-item-action>
                <v-icon>person</v-icon>
              </v-list-item-action>
              <v-list-item-title>{% verbatim %}{{getLoginLogoutString()}}{% endverbatim %}</v-list-item-title>
            </v-list-item>
          </template>
          <span>{% verbatim %}{{getLoginLogoutString()}}{% endverbatim %}</span>
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
      <router-link to="/">
        <v-toolbar-title class="app-title">
          <span class="app-title-text">{{project_name}}</span>
        </v-toolbar-title>
      </router-link>
      <v-spacer></v-spacer>
      <v-chip v-if="$api.auth.isAuthenticated" color="white">
        Welcome,
        <span data-test='username' class="username">{% verbatim %}{{displayName}}{% endverbatim %}</span>
      </v-chip>
    </v-app-bar>

    <v-main class="app-content" v-if="fullPageComponents.includes($route.name)">
      <router-view :key="$route.fullPath"></router-view>
    </v-main>
    <v-main v-else class="app-content app-background">
      <v-container>
        <v-col>
          <v-card class="component-card">
            <router-view :key="$route.fullPath"></router-view>
          </v-card>
        </v-col>
      </v-container>
    </v-main>

    <v-footer color="secondary" id="footer" app>
      <span class="white--text">2021 The Presidents and Fellows of Harvard College</span>
    </v-footer>
  </v-app>
</template>
<style lang="css">
  html {
    overflow-y: auto !important;
    font-size: 14px;
  }

  a {
    text-decoration: none;
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
    margin-left: 1rem;
  }

  .nav-link {
    transition: margin .1s ease-in;
  }

  .nav-link-expanded {
    margin-left: 1rem;
  }

  .nav-link-mini {
    margin-left: 0;
  }

  #footer {
    padding: 12px;
  }
  .required label::after {
    content: " *";
  }

  .app-content {
    min-width: 400px;
  }

  .app-background {
    background-color: #f9f9f9;
  }
  .contact-address {
    white-space: pre-line;
  }

  .no-select {
    -webkit-touch-callout: none;
    -webkit-user-select: none;
    -khtml-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
  }

</style>

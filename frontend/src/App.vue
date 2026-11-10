<script>
import auth from '@/auth'
import { DJANGO_ADMIN_ROOT } from '@/urls'
import { mapActions } from 'vuex'
import { IFXMessageDisplay } from 'ifxvue'
import navData from './navData'
import eventHub from '@/eventHub'
import { pick } from 'lodash'

export default {
  name: 'App',
  components: {
    IFXMessageDisplay,
  },
  data() {
    return {
      drawer: true,
      isLoggedIn: false,
      msgText: '',
      name: null,
      toolbarKey: false,
      headerTimer: null,
      isDrawerOpenMobile: false,
      drawerMiniPref: null,
      loading: true,
      openedGroups: (() => {
        const storedOpenedGroups = localStorage.getItem('navOpenedGroups')
        if (storedOpenedGroups) {
          try {
            return JSON.parse(storedOpenedGroups)
          } catch (error) {
            // Fall through to default
          }
        }
        return null // Will be initialized in mounted
      })(),
    }
  },
  watch: {
    openedGroups: {
      deep: true,
      handler(groups) {
        if (groups !== null) {
          localStorage.setItem('navOpenedGroups', JSON.stringify(groups))
        }
      },
    },
  },
  methods: {
    ...mapActions(['showMessage', 'toggleDialog']),
    getDjangoUrl(django) {
      return `${this.$api.urls.DJANGO_ADMIN_ROOT}${django}`
    },
    goToUserDetailPage() {
      this.$router.push({ name: 'UserDetail', params: { id: this.$api.authUser.id } })
    },
    setAuthData() {
      this.name = this.$api.auth ? this.$api.auth.getFirstName() : this.$api.auth.getUsername()
    },
    getLoginLogoutString(lower) {
      const string = this.$api.authUser.isAuthenticated ? 'Logout' : 'Login'
      return lower ? string.toLowerCase() : string
    },
    // eslint-disable-next-line consistent-return
    loginLogout() {
      if (this.$api.authUser.isAuthenticated) {
        return this.$api.auth
          .logout()
          .then((res) => this.showMessage(res))
          .then(() => {
            if (this.headerTimer) {
              clearTimeout(this.headerTimer)
            }
            if (this.$cookie) {
              this.$cookie.delete('MOD_AUTH_CAS_S')
            }
            this.$router.push({
              name: 'Home',
            })
          })
          .catch((error) => this.showMessage(error))
      }
      const url = this.$router.resolve({ name: 'Login', query: { from: this.$route.fullPath } }).href
      window.location.replace(url)
    },
    isAuthenticated() {
      return this.$api.auth.isAuthenticated || this.isLoggedIn
    },
    getAdminUrl() {
      return this.$api.urls.DJANGO_ADMIN_ROOT
    },
    isDjangoStaff() {
      return this.$api.auth.can('access-django-admin', this.$api.authUser)
    },
    propsToPass(item) {
      const params = {}
      params['v-slot'] = 'activator'
      params['class'] = this.mini ? 'nav-link nav-link-mini' : 'nav-link nav-link-expanded'
      params['disabled'] = item.hasOwnProperty('disabled') && item.disabled
      params['key'] = item.link
      if (item.link) {
        params['to'] = { name: item.link, params: item.params }
      }
      if (item.django) {
        params['href'] = this.getDjangoUrl(item.django)
      }
      return params
    },
    checkPriv(item) {
      if (item.priv) {
        return this.$api.auth.can(item.priv, this.$api.authUser)
      }
      return true
    },
    pluralize(count, string) {
      return `${string}${count === 1 ? '' : 's'}`
    },
    initializeOpenedGroups() {
      // Initialize with all group names expanded by default
      // Groups with collapsed: true in navData will be collapsed
      if (this.openedGroups === null) {
        this.openedGroups = Object.entries(this.computedNav)
          .filter(([name, group]) => !group.collapsed)
          .map(([name]) => name)
      }
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
    },
    onDrawerClick() {
      // If in rail mode, expand the drawer instead of navigating
      if (this.mini && !this.niceMobile) {
        this.drawerMiniPref = false
      }
    },
  },
  created() {
    const me = this
    eventHub.on('isLoggedIn', (bool) => {
      me.isLoggedIn = bool
      me.setAuthData()
    })
  },
  unmounted() {
    if (this.headerTimer) {
      clearTimeout(this.headerTimer)
    }
  },
  async mounted() {
    const me = this
    // Is the test failing because it's loading too fast before the data can return?
    this.$nextTick(() => (this.loading = false))
    this.initializeOpenedGroups()
    if (me.isAuthenticated()) {
      me.setAuthData()
      this.toolbarKey = true
    }
  },
  computed: {
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
    niceMobile() {
      return this.$vuetify.display.xs
    },
    mini() {
      // If user sets a drawerMini preference, this takes priority
      if (this.drawerMiniPref !== null) {
        return this.drawerMiniPref
      }
      // Otherwise, navigation drawer is minified on smaller screens only
      if (this.$vuetify.display.xlAndUp) {
        return false
      }
      return true
    },
    auth: function () {
      // Make auth available to the template
      return this.$api.auth
    },
    computedNav() {
      const addedKeys = []
      if (this.$api.authUser.isAuthenticated && this.$api.authUser.isAdmin) {
        const adminKeys = ['admin', 'mailing']
        addedKeys.push(...adminKeys)
      }
      return pick(navData, addedKeys)
    },
    fullPageComponents() {
      return ['Home', 'Login', 'Logout']
    },
  },
}
</script>

<template>
  <v-app id="inspire">
    <IFXMessageDisplay />

    <v-app-bar app clipped-left color="primary" ref="toolbar">
      <v-app-bar-nav-icon
        v-if="!niceMobile"
        @click="toggleDrawerPref"
      ></v-app-bar-nav-icon>
      <v-app-bar-nav-icon
        v-if="niceMobile"
        @click="toggleDrawerOpenMobile"
      ></v-app-bar-nav-icon>
      <router-link to="/">
        <v-toolbar-title class="app-title-text">
          <span class="ml-3 mr-5"></span>
        </v-toolbar-title>
      </router-link>
      <v-tooltip location="bottom">
        <template v-slot:activator="{ props }">
          <v-btn v-bind="props" variant="text" href="mailto:fads@rc.fas.harvard.edu">Report an issue</v-btn>
        </template>
        <span>Submit a ticket</span>
      </v-tooltip>
      <v-spacer></v-spacer>

      <v-menu v-if="isAuthenticated()" location="bottom">
        <template #activator="{ props }">
          <v-chip v-bind="props" color="primary" variant="flat">
            <span class="username">Welcome, </span>
            <span data-test="username" class="username">{{ displayName }}</span>
          </v-chip>
        </template>

        <v-list density="compact" nav>
          <v-list-item @click="goToUserDetailPage()" prepend-icon="mdi-account" title="User Profile" />
          <v-list-item @click="loginLogout()" prepend-icon="mdi-exit-to-app" title="Logout" />
        </v-list>
      </v-menu>

      <span v-else>
        <v-btn @click="loginLogout()" variant="text">Login</v-btn>
      </span>

      <v-tooltip v-if="isDjangoStaff()" location="bottom">
        <template #activator="{ props }">
          <v-btn icon :href="getAdminUrl()" v-bind="props" variant="text">
            <v-icon color="yellow">mdi-key-variant</v-icon>
          </v-btn>
        </template>
        <span>Django admin panel</span>
      </v-tooltip>
    </v-app-bar>

    <v-navigation-drawer
      v-if="!loading"
      :model-value="niceMobile ? isDrawerOpenMobile : true"
      :rail="!niceMobile && mini"
      :mobile-breakpoint="200"
      :rail-width="80"
      :width="340"
      @click="onDrawerClick"
    >
      <v-list
        nav
        density="compact"
        v-model:opened="openedGroups"
        class="nav-list"
        open-strategy="multiple"
      >
        <v-tooltip location="right" :disabled="!mini">
          <template #activator="{ props }">
            <v-list-item
              link
              v-bind="props"
              :to="{ name: 'Home' }"
              prepend-icon="mdi-home"
              title="Home"
              :exact="true"
            />
          </template>
          <span>Home</span>
        </v-tooltip>

        <v-list-group
          v-for="(group, name) in computedNav"
          :key="name"
          :value="name"
          :prepend-icon="group.icon"
        >
          <template #activator="{ props }">
            <v-list-item v-bind="props" :title="group.title" />
          </template>

          <v-list-item
            v-for="item in group.items"
            :key="item.link || item.django || item.title"
            link
            :to="item.link ? { name: item.link, params: item.params } : undefined"
            :href="item.django ? getDjangoUrl(item.django) : undefined"
            :disabled="item.hasOwnProperty('disabled') && item.disabled"
            :prepend-icon="item.icon"
            :title="item.title"
          />
        </v-list-group>
      </v-list>
    </v-navigation-drawer>

    <v-main class="app-content" v-if="fullPageComponents.includes($route.name)">
      <router-view :key="$route.fullPath"></router-view>
    </v-main>
    <v-main v-else class="app-content app-background">
      <v-container>
        <v-row justify="center">
          <v-col>
            <v-card class="">
              <router-view :key="$route.fullPath"></router-view>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>

    <v-footer color="secondary" app>
      <span class="text-white text-caption">2026 The President and Fellows of Harvard College.</span>
    </v-footer>
  </v-app>
</template>
<style lang="scss">
// Re-import Vuetify utilities last to fix ordering issues
@use 'vuetify/lib/styles/utilities' as *;
</style>

<style lang="css">
html {
  overflow-y: auto !important;
  font-size: 16px;
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
  font-weight: 600;
}

#footer {
  padding: 12px;
}

.required label::after {
  content: ' *';
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

.mdi-menu-right::before {
  font-size: 1.5em !important;
}

/* Navigation list styling */
.nav-list {
  font-size: 13px;
}

.nav-list .v-list-item {
  min-height: 36px !important;
  padding-top: 4px !important;
  padding-bottom: 4px !important;
}

.nav-list .v-list-item-title {
  font-size: 13px !important;
}

.nav-list .v-icon {
  font-size: 24px !important;
}

.nav-list .v-list-item__prepend {
  width: 30px;
}

.nav-list .v-list-group__header .v-list-item__prepend > .v-icon {
  margin-inline-end: 6px;
}

.v-navigation-drawer:not(.v-navigation-drawer--rail) .nav-list .v-list-item {
  white-space: nowrap;
}

.v-navigation-drawer:not(.v-navigation-drawer--rail) .nav-list > .v-tooltip .v-list-item,
.v-navigation-drawer:not(.v-navigation-drawer--rail) .nav-list > .v-list-item {
  padding-inline-start: 4px !important;
}

.v-navigation-drawer:not(.v-navigation-drawer--rail) .nav-list .v-list-group > .v-list-group__header {
  padding-inline-start: 4px !important;
}

.v-navigation-drawer:not(.v-navigation-drawer--rail) .nav-list .v-list-group__items {
  --indent-padding: 3px !important;
}

.v-navigation-drawer:not(.v-navigation-drawer--rail) .nav-list .v-list-group__items .v-list-item {
  padding-inline-start: 22px !important;
}

.v-navigation-drawer:not(.v-navigation-drawer--rail) .nav-list .v-list-group__items .v-list-item .v-list-item__prepend {
  margin-inline-end: 4px;
}

.v-navigation-drawer--rail .nav-list {
  padding: 0 !important;
  overflow: visible !important;
}

.v-navigation-drawer--rail .nav-list .v-list-item {
  padding-left: 8px !important;
  padding-right: 8px !important;
  min-height: 40px !important;
}

.v-navigation-drawer--rail .nav-list .v-list-item__prepend {
  margin: 0 !important;
  width: auto;
  display: flex !important;
}

.v-navigation-drawer--rail .nav-list .v-list-item__prepend .v-icon {
  opacity: 1 !important;
  margin: 0 !important;
}

.v-navigation-drawer--rail .nav-list .v-list-item__content {
  display: none;
}

.v-navigation-drawer--rail .nav-list .v-list-item__append {
  display: none;
}

.v-navigation-drawer--rail .nav-list .v-list-group__items {
  display: none;
}

.v-navigation-drawer--rail .nav-list .v-list-group > .v-list-group__header {
  padding-left: 8px !important;
  padding-right: 8px !important;
}

.v-navigation-drawer--rail .nav-list .v-list-group > .v-list-group__header .v-list-item__prepend {
  margin: 0 !important;
}
/* Only apply black text when you add this class */
.v-chip.black-text,
.v-chip.black-text .v-chip__content {
  color: black !important;
}

.v-chip.white-text,
.v-chip.white-text .v-chip__content {
  color: white !important;
}

h3 {
  font-size: 1.2rem;
  margin-top: 0;
  margin-bottom: 0;
}
.v-btn--icon .v-icon {
    --v-icon-size-multiplier: 1.2 !important;
}
.roomy {
  margin-top: 2rem;
}
.theme--light.v-data-table .v-row-group__header:nth-child(odd) {
  background-color: #fff;
}
.theme--light.v-data-table .v-row-group__header:nth-child(even) {
  background-color: #e8f5e9;
}
</style>

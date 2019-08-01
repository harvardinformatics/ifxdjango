<script>
import auth from '@/auth'
import { DJANGO_ADMIN_ROOT } from '@/urls'
import { mapActions, mapGetters } from 'vuex'
import {APIService} from './api'

const api = new APIService()

export default {
  name: 'App',
  data: function () {
    return {
      drawer: true,
      bigMiniToggle: false,
      smallMiniToggle: true,
      msgText: '',
      authenticated: false,
      name: null,
      toolbarStyle: {
        'margin-top': '50px'
      }
    }
  },
  methods: {
    setNavbarMargin() {
      this.$set(this.toolbarStyle, 'margin-top', this.$refs.toolbar.computedHeight + 'px');
    },
    updateNavbarMargin(offset) {
      this.$set(this.toolbarStyle, 'margin-top', offset + 'px');
    },
    handleScroll() {
      let offset = window.scrollY - this.$refs.toolbar.computedHeight;
      if (offset < 0) {
        this.updateNavbarMargin(Math.abs(offset));
      }
    },
    ...mapActions([
      'showMessage',
      'toggleDialog'
    ]),
  },
  created () {
    window.addEventListener('scroll', this.handleScroll);
  },
  destroyed () {
    window.removeEventListener('scroll', this.handleScroll);
  },
  mounted: function () {
    setTimeout(()=> {
      if (auth.isAuthenticated) {
        this.authenticated = true
        this.authenticated = auth.isAuthenticated()
        this.name = auth.getFirstName() ? auth.getFirstName() : auth.getUsername()
      }
    }, 1000)
    this.setNavbarMargin();
  },
  computed: {
    mini: {
      get: function() {
        return this.$vuetify.breakpoint.lgAndUp ? this.bigMiniToggle : this.smallMiniToggle
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
    auth: function () {
      // Make auth available to the template
      return auth
    }
  },
}
</script>

<template>
  <v-app id="inspire">
    <Message></Message>
    <v-navigation-drawer
      v-model="drawer"
      :mini-variant.sync="mini"
      :clipped="false"
      :mobile-break-point="400"
      app
    >
      <v-list :style="this.toolbarStyle">
        <v-list-tile :to="{name: 'Home'}">
          <v-list-tile-action>
            <v-icon>home</v-icon>
          </v-list-tile-action>
          <v-list-tile-title>
            Home
          </v-list-tile-title>
        </v-list-tile>
    </v-navigation-drawer>

    <v-toolbar app absolute clipped-left color="primary" ref="toolbar">
      <v-toolbar-side-icon v-if="$vuetify.breakpoint.mdAndUp" @click.native="bigMiniToggle = !bigMiniToggle"></v-toolbar-side-icon>
      <v-toolbar-side-icon v-if="$vuetify.breakpoint.smAndDown" @click.native="smallMiniToggle = !smallMiniToggle"></v-toolbar-side-icon>
      <v-toolbar-title>
        <span class="title ml-3 mr-5">{{project_name}}</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn v-if="name" flat color="white">
        Welcome, {{name}}
      </v-btn>
    </v-toolbar>

    <v-content>
      <router-view :key="$route.fullPath"></router-view>
    </v-content>

    <v-footer color="secondary" app>
        <span class="white--text"> 2019 The Presidents and Fellows of Harvard College.</span>
    </v-footer>
  </v-app>
</template>
<style lang="scss">

  .admin-group {
    background-color: rgb(250, 238, 238);
  }
  .v-toolbar .title {
    color: white;
  }
  .v-footer {
    padding: 20px;
  }
  .v-navigation-drawer--open {
    width: 200px;
  }
  .required label::after {
      content: " *";
  }
  .no_decoration {
    text-decoration: none;
  }
  .v-input {
    font-size: 16px;
  }
  .v-label {
    font-size: 18px;
  }
  .v-expansion-panel__header {
    padding: 12px;
    font-weight: bold;
    font-size: 16px;
  }
  .v-list__tile__title {
    font-size: 12px;
  }
  .v-list__tile__content {
    font-size: 12px;
  }
  table.v-table tbody td, table.v-table tbody th {
    padding: 4px;
    height: 20px;
  }
  .v-btn--floating.v-btn--small {
      height: 30px;
      width: 30px;
  }
  .input-group--selection-controls__ripple {
    border-radius: 0 !important;
  }
  .v-card__title {
    border-bottom: 1px solid #ccc;
  }
  .v-card {
    padding: 20px;
  }
</style>

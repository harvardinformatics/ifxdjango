import Vue from 'vue'
import Vuetify, { VTextField } from 'vuetify/lib'
import '@mdi/font/css/materialdesignicons.css'
import { Ripple as VuetifyRipple } from 'vuetify/lib/directives/ripple';

Vue.use(Vuetify, {
  directives: {
    Ripple: VuetifyRipple,
  },
});

// [Does this still apply?]
// With tree-shaking enabled, webpack won't recognize v-text-field within the currency field
// Register explicitly
Vue.component('v-text-field', VTextField)

export default new Vuetify({
  dark: false,
  icons: {
    iconfont: 'mdi',
  },
  theme: {
    themes: {
      light: {
        primary: '#C62828',
        secondary: '#90A4AE',
        accent: '#5C6BC0',
        error: '#db564c',
        warning: '#fcf3a1',
        info: '#2196f3',
        success: '#4caf50',
      },
      dark: {
        primary: '#C62828',
        secondary: '#90A4AE',
        accent: '#5C6BC0',
        error: '#db564c',
        warning: '#fcf3a1',
        info: '#2196f3',
        success: '#4caf50',
      },
    },
  },
})

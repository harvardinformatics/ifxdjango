import Vue from 'vue'
import Vuetify from 'vuetify/lib'

Vue.use(Vuetify)

export default new Vuetify({
  dark: false,
  icons: {
    iconfont: 'mdi'
  },
  themes: {
    light: {
      primary: '#C62828',
      secondary: '#90A4AE',
      accent: '#5C6BC0',
      error: '#db564c',
      warning: '#fcf3a1',
      info: '#2196f3',
      success: '#4caf50'
    },
    dark: {
      primary: '#C62828',
      secondary: '#90A4AE',
      accent: '#5C6BC0',
      error: '#db564c',
      warning: '#fcf3a1',
      info: '#2196f3',
      success: '#4caf50'
    }
  }
})
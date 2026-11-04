import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

export default createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
  },
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        dark: false,
        colors: {
          primary: '#C62828',
          secondary: '#90A4AE',
          accent: '#5C6BC0',
          error: '#db564c',
          warning: '#fcf3a1',
          info: '#2196f3',
          success: '#4caf50',
        },
      },
      dark: {
        dark: true,
        colors: {
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
  },
})

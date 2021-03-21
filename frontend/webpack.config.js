const { VuetifyLoaderPlugin } = require('vuetify-loader')

module.exports = {
  module: {
    loaders: [
      { test: /\.css$/, loader: 'css-loader' }
    ]
  },
  plugins: [
    new VuetifyLoaderPlugin()
  ]
}

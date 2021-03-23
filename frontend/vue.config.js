module.exports = {
  configureWebpack: {
    resolve: {
      extensions: ['*', '.js', '.vue', '.json'],
    }
  },
  devServer: {
    host: '0.0.0.0',
    watchOptions: {
      poll: 1000,
      ignored: [
        /node_modules([\\]+|\/)+(?!ifxvue)/,
        /ifxvue([\\]+|\/)node_modules/
      ]
    },
    progress: false
  }
}

// if (process.env.NODE_ENV === 'development') {
//   // To allow cypress server to access {{project_name}} through docker-compose network
//   // TODO: can this be added to production?
//   // module.exports.devServer.public = '{{project_name}}-ui'
// }

if (process.env.NODE_ENV !== 'development') {
  module.exports.publicPath = '/{{project_name}}/static/'
}

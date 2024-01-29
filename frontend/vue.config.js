module.exports = {
  configureWebpack: {
    resolve: {
      extensions: ['*', '.js', '.vue', '.json'],
    },
  },
  devServer: {
    host: '0.0.0.0',
    public: 'localhost',
    watchOptions: {
      poll: 1000,
      ignored: [/node_modules([\\]+|\/)+(?!ifxvue)/, /ifxvue([\\]+|\/)node_modules/],
    },
    progress: false,
  },
}

if (process.env.NODE_ENV !== 'development') {
  module.exports.publicPath = '/{{project_name}}/static/'
}

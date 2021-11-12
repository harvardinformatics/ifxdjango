const path = require('path')

module.exports = {
  root: true,

  env: {
    node: true
  },

  extends: [
    'plugin:vue/essential',
    'eslint:recommended',
    '@vue/airbnb',
  ],

  parserOptions: {
    sourceType: 'module'
    ecmaVersion: 2020,
  },

  settings: {
    'import/resolver': {
      node: {
        extensions: ['.js', '.jsx', '.mjs', '.vue'],
        paths: [path.resolve(__dirname, 'src')],
      },
    },
  },

  rules: {
    'no-plusplus': 0,
    'no-continue': 0,
    'max-classes-per-file': 0,
    'semi': 0,
    'import/prefer-default-export': 0,
    'comma-dangle': 0,
    'prefer-template': 1,
    'object-curly-newline': 0,
    'no-else-return': 1,
    'object-shorthand': 0,
    'prefer-const': 1,
    'radix': 0,
    'no-param-reassign': 1,
    'no-extra-semi': 0,
    'max-len': 0,
    'no-underscore-dangle': 0,
    'no-prototype-builtins': 0,
    'no-return-assign': 0,
    'arrow-parens': 0,
    'prefer-destructuring': 0,
    'func-names': 0,
    'vue/no-mutating-props': 1,
    'no-param-reassign': 1,
    'import/extensions': [2, 'always', {
      js: 'never',
      mjs: 'never',
      jsx: 'never',
      ts: 'never',
      tsx: 'never',
      vue: 'never'
    }],
    'camelcase': 0,
    'class-methods-use-this': 0,
    'arrow-body-style': 0,
    'import/no-unresolved': [2, { caseSensitive: false }],
    'no-console': process.env.NODE_ENV === 'production' ? 1 : 0,
    'no-debugger': process.env.NODE_ENV === 'production' ? 1 : 0,
    'no-shadow': [2, { allow: ['state'] }]
  },

  // overrides: [
  //   {
  //     files: [
  //       '**/__tests__/*.{j,t}s?(x)',
  //       '**/tests/unit/**/*.spec.{j,t}s?(x)'
  //     ],
  //     env: {
  //       jest: true
  //     }
  //   }
  // ]
}

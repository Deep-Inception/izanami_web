'use strict'
const merge = require('webpack-merge')
const commonEnv = require('./common.env')

module.exports = merge(commonEnv, {
  NODE_ENV: '"development"',
  BACKEND_URL: '"http://127.0.0.1:5000/"',

})

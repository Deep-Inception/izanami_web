'use strict'
const merge = require('webpack-merge')
const commonEnv = require('./common.env')

module.exports = merge(commonEnv, {
  NODE_ENV: '"testing"'
})

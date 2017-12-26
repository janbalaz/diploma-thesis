import Vue from 'vue'

Vue.filter('toLowercase', value => {
  return value.toLowerCase()
})

Vue.filter('toTitlecase', value => {
  return value.charAt(0).toUpperCase() + value.slice(1)
})

Vue.filter('toPrecision', (value, precision = 2) => {
  try {
    return parseFloat(value).toPrecision(precision)
  } catch (e) {
    return ''
  }
})

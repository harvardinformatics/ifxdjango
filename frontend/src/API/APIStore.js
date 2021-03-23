// This file contains all application-specific to be used in ifxvue
import * as urls from '@/API/urls'

const appName = '{{project_name}}'
const appNameFormatted = '{{project_name}}'

const vars = {
  appName,
  appNameFormatted,
  appKey: `ifx_${appName}`
}

// Initialize with empty user template before authentication occurs
const APIStore = {
  urls,
  vars,
  ui: {}
}

export default APIStore

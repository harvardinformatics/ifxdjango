/*
    URLs for the REST API
*/
/* eslint-disable no-multi-spaces */

export const ROOT_URL = import.meta.env.VITE_VUE_APP_DJANGO
export const API_ROOT             = [ROOT_URL, 'api'].join('')
export const LOGIN_URL            = [API_ROOT, 'obtain-auth-token/'].join('/')
export const STATICS_ROOT         = [ROOT_URL, 'static'].join('')
export const DJANGO_ADMIN_ROOT    = [ROOT_URL, 'djadmin'].join('')
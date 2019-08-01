/*
    URLs for the REST API
*/
/* eslint-disable no-multi-spaces */

export const ROOT_URL             = process.env.VUE_APP_DJANGO
export const API_ROOT             = [ROOT_URL, 'api'].join('')
export const LOGIN_URL            = [API_ROOT, 'obtain-auth-token/'].join('/')
export const DJANGO_ADMIN_ROOT    = [ROOT_URL, 'djadmin'].join('')
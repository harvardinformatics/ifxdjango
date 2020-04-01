import axios from 'axios'
import { LOGIN_URL } from '@/urls'

/*
auth.js
An auth class with convenience methods for getting and setting auth tokens
*/

import { API_ROOT } from '@/urls'

class TokenAuth {
  constructor () {
    this.authTokenKey = 'auth-token'
    this.isAdminKey = 'is-admin'
    this.usernameKey = 'username'
    this.groupsKey = 'groups'
    this.firstNameKey = 'first-name'
    this.lastNameKey = 'last-name'
  }
  initUser (userinfo) {
    sessionStorage.setItem(this.isAdminKey, userinfo.is_staff)
    sessionStorage.setItem(this.usernameKey, userinfo.username)
    sessionStorage.setItem(this.groupsKey, userinfo.groups)
    sessionStorage.setItem(this.firstNameKey, userinfo.first_name)
    sessionStorage.setItem(this.lastNameKey, userinfo.last_name)
    this.setAuthToken(userinfo.token)
  }
  destroyUser () {
    sessionStorage.removeItem(this.isAdminKey)
    sessionStorage.removeItem(this.usernameKey)
    sessionStorage.removeItem(this.groupsKey)
    sessionStorage.removeItem(this.firstNameKey)
    sessionStorage.removeItem(this.lastNameKey)
    this.setAuthToken()
  }
  setAuthToken (token) {
    /*
      Sets the authentication token in sessionStorage.  If token is null
      the storage item is cleared
    */
    if (token) {
      sessionStorage.setItem(this.authTokenKey, token)
    } else {
      sessionStorage.removeItem(this.authTokenKey)
    }
    this.setAuthHeaderValue()
  }
  fetchToken () {
    return axios.get(LOGIN_URL).then((response) => {
      var token = response.data.token
      if (token) {
        this.setAuthToken(token)
        return token
      }
      return ''
    })
  }
  getAuthToken () {
    var token = sessionStorage.getItem(this.authTokenKey)
    if (token) {
      return token
    } else {
      return null
    }
  }
  setAuthHeaderValue () {
    axios.defaults.headers.common['Authorization'] = this.getAuthHeaderValue()
  }
  getAuthHeaderValue () {
    let token = this.getAuthToken() || ''
    return 'Token ' + token
  }
  checkAuthentication () {
    if (this.isAuthenticated()) {
      this.setAuthHeaderValue()
    }
  }
  isAuthenticated () {
    return (this.getUsername() !== null && this.getAuthToken() !== null)
  }
  isDjangoStaff () {
    return sessionStorage.getItem(this.isAdminKey)
  }
  getFirstName () {
    return sessionStorage.getItem(this.firstNameKey)
  }
  getFullName () {
    return `${sessionStorage.getItem(this.firstNameKey)} ${sessionStorage.getItem(this.lastNameKey)}`
  }
  logout () {
    this.destroyUser()
  }
  getUsername () {
    return sessionStorage.getItem(this.usernameKey)
  }
  hasGroup (group) {
    let groupstr = sessionStorage.getItem(this.groupsKey)
    if (!groupstr) {
      return false
    }
    let groups = groupstr.split(',')
    return groups.includes(group)
  }
}

let auth = new TokenAuth()
export default auth

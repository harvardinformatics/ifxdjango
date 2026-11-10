/* eslint-disable no-param-reassign */
/* eslint-disable class-methods-use-this */
/* eslint-disable no-useless-constructor */

import { IFXAPIService, IFXAuthUser } from 'ifxvue'

class APIService extends IFXAPIService {
  constructor(store) {
    super(store, store.urls)
  }

  get auth() {
    const auth = super.auth
    const authUser = this.authUser // Save for can function default
    // Logs user into the system. Retrieves token and sets user information if successful.
    auth.login = async () => {
      try {
        const response = await this.axios.get(this.urls.LOGIN_URL)
        if (!response.data || !response.data.token) {
          // failure
          const message = 'You are a known user, but your data is malformed.'
          throw new Error(message)
        } else {
          // If response has data and token, then it is successful
          const userData = response.data
          this.authUser = new IFXAuthUser(userData)
          return 'Login successful.'
        }
      } catch (error) {
        let message = 'Login failure.'
        if (error?.response?.status === 401) {
          let info = ''
          if (
            error.response.hasOwnProperty('data') &&
            error.response.data &&
            error.response.data.hasOwnProperty('error')
          ) {
            info = error.response.data.error
          }
          message = `${info}`
        } else {
          message = `Login failed: ${error}`
        }
        throw Error(message)
      }
    }
    auth.can = function (ability, user = authUser) {
      if (ability && user.isStaff) {
        return true
      }
      if (ability === 'access-django-admin') {
        return user.isStaff
      }
      return false
    }
    // Django staff uses the "isStaff" bit from authUser
    auth.isDjangoStaff = this.authUser?.isStaff

    auth.getFirstName = () => {
      return this.authUser.firstName
    }
    auth.getLastName = () => {
      return this.authUser.lastName
    }
    auth.getFullName = () => {
      return `${auth.getFirstName()} ${auth.getLastName()}`
    }
    auth.getUsername = () => {
      return this.authUser.username
    }
    return auth
  }
}

export default APIService

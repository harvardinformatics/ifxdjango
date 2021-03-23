/* eslint-disable no-param-reassign */
/* eslint-disable class-methods-use-this */
/* eslint-disable no-useless-constructor */

import { IFXAPIService } from 'ifxvue'

class APIService extends IFXAPIService {
  constructor(store) {
    super(store)
  }

  get auth() {
    const auth = super.auth
    auth.can = function (ability, user) {
      if (!user) {
        user = this.authUser
      }
      if (ability && this.isAdmin) {
        return true
      }
      return false
    }
    return auth
  }
}

export default APIService

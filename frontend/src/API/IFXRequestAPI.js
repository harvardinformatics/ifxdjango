import { forEach } from 'lodash'

class Request {
  constructor(requestData) {
    if (requestData) {
      this.requestData = requestData
    } else {
      this.requestData = {}
    }
    if (!this.requestData.data) {
      this.requestData.data = {}
    }
  }

  get id() {
    return this.requestData.id
  }

  get processor() {
    return this.requestData.processor
  }

  get currentState() {
    return this.requestData.current_state
  }

  get created() {
    return this.requestData.created
  }

  get updated() {
    return this.requestData.updated
  }

  get requestType() {
    return this.requestData.request_type
  }

  set requestType(requestType) {
    this.requestData.request_type = requestType
  }

  set currentState(state) {
    this.requestData.current_state = state
  }

  get result() {
    return this.requestData.result
  }

  set result(result) {
    this.requestData.result = result
  }

  get requestStates() {
    return this.requestData.request_states
  }

  set requestStates(requestStates) {
    this.requestData.request_states = requestStates
  }

  get requestComments() {
    return this.requestData.request_comments
  }

  set requestComments(requestComments) {
    this.requestData.request_comments = requestComments
  }

  get requestor() {
    return this.requestData.requestor
  }
}

class AccountRequest extends Request {
  constructor(requestData) {
    super(requestData)
    if (!this.requestData.data.data) {
      this.requestData.data.data = {}
    }
    if (!this.requestData.data.data.person) {
      this.requestData.data.data.person = {}
    }
    if (!this.requestData.data.data.tracks) {
      this.requestData.data.data.tracks = {}
    }
  }

  get onBoardRequest() {
    return this.requestData.data
  }

  set onBoardRequest(onBoardRequest) {
    this.requestData.data = onBoardRequest
  }

  get continuationKey() {
    return this.onBoardRequest.continuation_key
  }

  get continuationKeyExpiration() {
    return this.onBoardRequest.continuation_key_expiration
  }

  set continuationKeyExpiration(continuationKeyExpiration) {
    this.onBoardRequest.continuation_key_expiration = continuationKeyExpiration
  }

  get onBoardRequestData() {
    return this.onBoardRequest.data
  }

  set onBoardRequestData(onBoardRequestData) {
    this.onBoardRequest.data = onBoardRequestData
  }

  get tracks() {
    return this.onBoardRequestData.tracks
  }

  set tracks(tracks) {
    this.onBoardRequestData.tracks = tracks
  }

  setTrackStepStatus(trackName, stepName, status) {
    if (this.tracks && this.tracks[trackName]) {
      this.tracks[trackName][stepName].value = status
    } else {
      throw new Error(`Track ${trackName} is not valid on this request.`)
    }
  }

  getTrackStepStatus(trackName, stepName) {
    let result = null
    if (this.tracks && this.tracks[trackName] && this.tracks[trackName][stepName]) {
      result = this.tracks[trackName][stepName].value
    }
    return result
  }

  setTrackStepComplete(trackName, stepName) {
    this.setTrackStepStatus(trackName, stepName, 'complete')
  }

  setTrackStepPending(trackName, stepName) {
    this.setTrackStepStatus(trackName, stepName, 'pending')
  }

  setTrackStepIncomplete(trackName, stepName) {
    this.setTrackStepStatus(trackName, stepName, 'incomplete')
  }

  isTrackStepComplete(trackName, stepName) {
    return this.getTrackStepStatus(trackName, stepName) === 'complete'
  }

  get person() {
    return this.onBoardRequestData.person
  }

  set person(person) {
    this.onBoardRequestData.person = person
  }

  get primaryEmail() {
    return this.person.primary_email
  }

  set primaryEmail(primaryEmail) {
    this.person.primary_email = primaryEmail
  }

  get contacts() {
    return this.person.contacts
  }

  set contacts(contacts) {
    this.person.contacts = contacts
  }

  get fullName() {
    return this.person.full_name
  }

  set fullName(fullName) {
    this.person.full_name = fullName
  }
}

class IFXRequestAPI {
  constructor(applicationApi, defaultApprover) {
    this.applicationApi = applicationApi
    this.defaultApprover = defaultApprover
  }

  newRequest(requestData) {
    if (requestData) {
      if (requestData.request_type === 'account_request') {
        return new AccountRequest(requestData)
      }
    }
    return new Request(requestData)
  }

  setState(id, nextState, comment) {
    const url = this.applicationApi.urls.SET_REQUEST_STATE
    const data = { request_id: id, state: nextState, comment: comment }
    return this.applicationApi.axios.post(url, data, { headers: { 'Content-Type': 'application/json' } })
  }

  getRequestTypeDetailComponent(requestType) {
    console.log(`request type ${requestType}`)
    if (requestType === 'account_request') {
      return 'AccountRequestDetail'
    }
    return 'RequestDetail'
  }

  newRequestComment() {
    return {
      id: null,
      text: '',
      author: null
    }
  }

  async getRequest(id) {
    const url = `${this.applicationApi.urls.UPDATE_REQUESTS}${id}/`
    let result = null
    const data = await this.applicationApi.axios.get(url).then((res) => res.data).catch((err) => { throw new Error(err) })
    if (data) {
      result = this.newRequest(data)
    }
    return result
  }

  getDefaultApprover() {
    return this.defaultApprover
  }

  async getRequestList(dataFields, search, includeCompleted, requestType, currentState) {
    const params = {}
    if (dataFields) {
      params.data_fields = dataFields
    }
    if (search) {
      params.search = search
    }
    if (currentState) {
      params.current_state = currentState
    }
    if (includeCompleted) {
      params.include_completed = 'true'
    }
    if (requestType) {
      params.request_type = requestType
    }
    const requests = []
    const url = this.applicationApi.urls.GET_REQUEST_LIST
    const result = await this.applicationApi.axios.get(url, {
      params: params
    })
      .then((res) => res.data)
      .catch((err) => { throw new Error(err) })
    forEach(result.requests, (requestData) => {
      requests.push(this.newRequest(requestData))
    })
    return requests
  }

  updateAccountRequest(accountRequest) {
    // Update both the account request and the onboard request data
    const headers = {
      'Content-Type': 'application/json'
    }
    const id = accountRequest.id
    const url = `${this.applicationApi.urls.UPDATE_REQUESTS}${id}/`
    const onboardRequest = accountRequest.onBoardRequest
    const onboardRequestId = onboardRequest.id
    const onboardRequestUrl = `${this.applicationApi.urls.UPDATE_ONBOARD_REQUESTS}${onboardRequestId}/`
    return this.applicationApi.axios.put(
      url,
      accountRequest.requestData,
      { headers: headers }
    )
      .then(() => {
        this.applicationApi.axios.put(
          onboardRequestUrl,
          onboardRequest,
          { headers: headers }
        )
          .catch((err) => {
            console.log(err)
          })
      })
  }

  isUserApprover(request) {
    if (!request.requestStates || !request.requestStates[0] || !request.requestStates[0].approvers) return false
    return request.requestStates[0].approvers.includes(this.applicationApi.authUser.username) || this.applicationApi.auth.can('approve-account-requests')
  }

  isAwaitingApproval(request) {
    if (!request.currentState) return false
    return request.currentState.includes('APPROVAL_PENDING')
  }

  canBeApproved(request) {
    return this.isUserApprover(request) && this.isAwaitingApproval(request)
  }

  getValidProcessorStates(processor) {
    // For the processor class name, get the valid states
    const url = this.applicationApi.urls.GET_VALID_PROCESSOR_STATES
    const params = {
      processor: processor
    }
    return this.applicationApi.axios.get(url, {
      params: params,
    })
  }
}

export { IFXRequestAPI, Request, AccountRequest }

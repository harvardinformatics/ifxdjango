// URL roots
export const ROOT_URL = process.env.VUE_APP_DJANGO
export const API_ROOT = `${ROOT_URL}api/`
export const LOGIN_URL = 'obtain-auth-token/'
export const DJANGO_ADMIN_ROOT = `${ROOT_URL}djadmin/`

// URLs
export const MESSAGES = 'messages/'
export const MAILINGS = 'mailings/'
export const SEND_MAILING = 'send-mailing/'
export const MOCK_ERRORS = 'mock-errors/'
export const USERS = 'users/'
export const GROUPS = 'groups/'
export const GET_USERS = 'users/'
export const UPDATE_USER = 'users/'
export const UPDATE_PERSON = 'users/update-person/'
export const GET_LOCATION_INFO = 'get-location-info/'
export const GET_NANITE_LOGIN = 'users/get-nanite-login/'
export const SET_REQUEST_STATE = 'requests/set-request-state/'
export const UPDATE_REQUESTS = 'requests/'
export const GET_REQUEST_LIST = 'requests/get-request-list/'
export const UPDATE_ONBOARD_REQUESTS = 'onboard-requests/'
export const GET_VALID_PROCESSOR_STATES = 'requests/get-valid-processor-states/'
export const GET_CONTACT_LIST = 'contacts/get-contact-list/'
export const CONTACTS = 'contacts/'
export const ORGANIZATIONS = 'organizations/'
export const ORGANIZATION_NAMES = 'get-org-names/'

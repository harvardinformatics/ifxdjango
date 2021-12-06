import { cloneDeep } from 'lodash'
import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Login from '@/components/Login'
import UserList from '@/components/user/UserList'
import UserEdit from '@/components/user/UserEdit'
import UserDetail from '@/components/user/UserDetail'
import AccountRequestList from '@/components/request/AccountRequestList'
import AccountRequestDetail from '@/components/request/AccountRequestDetail'
import {
  IFXMailingList,
  IFXMailingDetail,
  IFXMailingCompose,
  ifxcomponents,
  IFXMessageCreateEdit,
  IFXMessageList,
  IFXMessageDetail,
  IFXContactList,
  IFXContactDetail,
  IFXContactCreateEdit,
  IFXOrganizationList,
  IFXOrganizationDetail,
  IFXOrganizationCreateEdit,
  IFXAccountList
} from 'ifxvue'

const { IFXNotFound, IFXForbidden } = ifxcomponents

Vue.use(Router)

const routes = [
  {
    path: '/',
    name: 'Home',
    pathToRegexpOptions: { strict: true },
    component: Home
  },
  {
    path: '/login/',
    name: 'Login',
    pathToRegexpOptions: { strict: true },
    component: Login
  },
  {
    path: '/users/list/',
    name: 'UserList',
    pathToRegexpOptions: { strict: true },
    component: UserList,
    isAdminRoute: true
  },
  {
    path: '/users/:id/edit/',
    name: 'UserEdit',
    pathToRegexpOptions: { strict: true },
    component: UserEdit,
    props: route => ({
      id: String(route.params.id),
      isEditing: true
    }),
    isAdminRoute: true
  },
  {
    path: '/users/:id/',
    name: 'UserDetail',
    pathToRegexpOptions: { strict: true },
    component: UserDetail,
    props: route => ({
      id: String(route.params.id)
    }),
    isAdminRoute: true
  },
  {
    path: '/requests/account_request/list/',
    name: 'AccountRequestList',
    pathToRegexpOptions: { strict: true },
    component: AccountRequestList,
    isAdminRoute: true
  },
  {
    path: '/requests/account_request/:id/',
    name: 'AccountRequestDetail',
    pathToRegexpOptions: { strict: true },
    component: AccountRequestDetail,
    isAdminRoute: true,
    props: true
  },
  {
    path: '/contacts/list/',
    name: 'ContactList',
    pathToRegexpOptions: { strict: true },
    component: IFXContactList,
    isAdminRoute: true
  },
  {
    path: '/contacts/create/',
    name: 'ContactCreate',
    pathToRegexpOptions: { strict: true },
    component: IFXContactCreateEdit,
    isAdminRoute: true
  },
  {
    path: '/contacts/:id/edit/',
    name: 'ContactEdit',
    pathToRegexpOptions: { strict: true },
    component: IFXContactCreateEdit,
    props: route => ({
      id: String(route.params.id),
      isEditing: true
    }),
    isAdminRoute: true
  },
  {
    path: '/contacts/:id/',
    name: 'ContactDetail',
    pathToRegexpOptions: { strict: true },
    component: IFXContactDetail,
    props: route => ({
      id: String(route.params.id)
    }),
    isAdminRoute: true
  },
  {
    path: '/organizations/list/',
    name: 'OrganizationList',
    pathToRegexpOptions: { strict: true },
    component: IFXOrganizationList,
    isAdminRoute: true
  },
  {
    path: '/organizations/create/',
    name: 'OrganizationCreate',
    pathToRegexpOptions: { strict: true },
    component: IFXOrganizationCreateEdit,
    props: () => ({
      isEditing: false
    }),
    isAdminRoute: true
  },
  {
    path: '/organizations/:id/edit/',
    name: 'OrganizationEdit',
    pathToRegexpOptions: { strict: true },
    component: IFXOrganizationCreateEdit,
    props: route => ({
      id: String(route.params.id),
      isEditing: true
    }),
    isAdminRoute: true
  },
  {
    path: '/organizations/:id/',
    name: 'OrganizationDetail',
    pathToRegexpOptions: { strict: true },
    component: IFXOrganizationDetail,
    props: route => ({
      id: String(route.params.id),
    }),
    isAdminRoute: true
  },
  {
    path: '/mailings/compose/',
    name: 'MailingCompose',
    component: IFXMailingCompose
  },
  {
    path: '/mailings/list/',
    name: 'MailingList',
    pathToRegexpOptions: { strict: true },
    component: IFXMailingList
  },
  {
    path: '/mailings/:id/',
    name: 'MailingDetail',
    component: IFXMailingDetail,
    props: route => ({
      id: String(route.params.id),
      selectedMailing: cloneDeep(route.params.selectedMailing)
    })
  },
  {
    path: '/messages/create/',
    name: 'MessageCreate',
    component: IFXMessageCreateEdit,
  },
  {
    path: '/messages/list/',
    name: 'MessageList',
    component: IFXMessageList
  },
  {
    path: '/messages/:id/',
    name: 'MessageDetail',
    component: IFXMessageDetail,
    props: route => ({
      id: String(route.params.id),
      selectedMessage: cloneDeep(route.params.selectedMessage)
    })
  },
  {
    path: '/messages/:id/edit/',
    name: 'MessageEdit',
    component: IFXMessageCreateEdit,
    props: route => ({
      id: String(route.params.id),
      isEditing: true,
      selectedMessage: cloneDeep(route.params.selectedMessage)
    })
  },
  {
    path: '/accounts/list/',
    name: 'IFXAccountList',
    component: IFXAccountList
  },
  {
    path: '/forbidden/',
    name: 'Forbidden',
    pathToRegexpOptions: { strict: true },
    component: IFXForbidden
  },
  {
    path: '/404/',
    name: 'NotFound',
    pathToRegexpOptions: { strict: true },
    component: IFXNotFound
  },
  {
    path: '*',
    redirect: '/404/'
  }
]

routes.forEach(r => {
  const route = r
  route.pathToRegexpOptions = { strict: true }
})

const router = new Router({
  base: '/{{project_name}}/',
  mode: 'history',
  routes
})

export default router

import { cloneDeep } from 'lodash'
import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/components/Home.vue'
import Login from '@/components/Login.vue'
import UserList from '@/components/user/UserList.vue'
import UserEdit from '@/components/user/UserEdit.vue'
import UserDetail from '@/components/user/UserDetail.vue'
import AccountRequestList from '@/components/request/AccountRequestList.vue'
import AccountRequestDetail from '@/components/request/AccountRequestDetail.vue'
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
  IFXOrganizationCreateEdit,
  IFXOrganizationDetail,
  IFXAccountList,
  IFXAccountDetail,
  IFXBillingRecordDetail,
  IFXCalculateBillingMonth,
  IFXBillingRecords,
  IFXReportRunList,
} from 'ifxvue'

const { IFXNotFound, IFXForbidden } = ifxcomponents

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login/',
    name: 'Login',
    component: Login
  },
  {
    path: '/users/list/',
    name: 'UserList',
    component: UserList,
    meta: { AdminRoute: true }
  },
  {
    path: '/users/:id/edit/',
    name: 'UserEdit',
    component: UserEdit,
    props: route => ({
      id: String(route.params.id),
      isEditing: true
    }),
    meta: { AdminRoute: true }
  },
  {
    path: '/users/:id/',
    name: 'UserDetail',
    component: UserDetail,
    props: route => ({
      id: String(route.params.id)
    }),
    meta: { AdminRoute: true }
  },
  {
    path: '/requests/account_request/list/',
    name: 'AccountRequestList',
    component: AccountRequestList,
    meta: { AdminRoute: true }
  },
  {
    path: '/requests/account_request/:id/',
    name: 'AccountRequestDetail',
    component: AccountRequestDetail,
    meta: { AdminRoute: true },
    props: true
  },
  {
    path: '/contacts/list/',
    name: 'ContactList',
    component: IFXContactList,
    meta: { AdminRoute: true }
  },
  {
    path: '/contacts/create/',
    name: 'ContactCreate',
    component: IFXContactCreateEdit,
    meta: { AdminRoute: true }
  },
  {
    path: '/contacts/:id/edit/',
    name: 'ContactEdit',
    component: IFXContactCreateEdit,
    props: route => ({
      id: String(route.params.id),
      isEditing: true
    }),
    meta: { AdminRoute: true }
  },
  {
    path: '/contacts/:id/',
    name: 'ContactDetail',
    component: IFXContactDetail,
    props: route => ({
      id: String(route.params.id)
    }),
    meta: { AdminRoute: true }
  },
  {
    path: '/organizations/list/',
    name: 'OrganizationList',
    component: IFXOrganizationList,
    meta: { AdminRoute: true }
  },
  {
    path: '/organizations/create/',
    name: 'OrganizationCreate',
    component: IFXOrganizationCreateEdit,
    props: () => ({
      isEditing: false
    }),
    meta: { AdminRoute: true }
  },
  {
    path: '/organizations/:id/edit/',
    name: 'OrganizationEdit',
    component: IFXOrganizationCreateEdit,
    props: route => ({
      id: String(route.params.id),
      isEditing: true
    }),
    meta: { AdminRoute: true }
  },
  {
    path: '/organizations/:id/',
    name: 'OrganizationDetail',
    component: IFXOrganizationDetail,
    props: route => ({
      id: String(route.params.id),
    }),
    meta: { AdminRoute: true }
  },
  {
    path: '/mailings/compose/',
    name: 'MailingCompose',
    component: IFXMailingCompose,
    meta: { AdminRoute: true },
    props: (route) => ({
      from: route.params.from,
      to: cloneDeep(route.params.to),
      cc: cloneDeep(route.params.cc),
      bcc: cloneDeep(route.params.bcc),
      message: route.params.message,
      messageName: route.params.messageName,
      subject: route.params.subject,
      recipients: route.params.recipients,
      recipientField: route.params.recipientField,
      labManagerOrgSlugs: cloneDeep(route.params.labManagerOrgSlugs),
    }),
  },
  {
    path: '/mailings/list/',
    name: 'MailingList',
    component: IFXMailingList,
    meta: { AdminRoute: true },
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
    name: 'AccountList',
    component: IFXAccountList
  },
  {
    path: '/accounts/:id/',
    name: 'AccountDetail',
    component: IFXAccountDetail,
    props: (route) => ({
      id: String(route.params.id),
    }),
  },
  {
    path: '/billing/billing-records/list/',
    name: 'BillingRecordList',
    component: IFXBillingRecords,
    props: () => ({
      useDefaultMailButton: false,
      allowChangeExpenseCode: true,
      allowDownloads: true,
      showDates: true,
      showTotals: true,
      totalUnits: 'hours'
    }),
    meta: { AdminRoute: true },
  },
  {
    path: '/billing/calculate-billing-month/:facility_id/',
    name: 'CalculateBillingMonthFacility',
    component: IFXCalculateBillingMonth,
    meta: { AdminRoute: true },
    props: (route) => ({
      facilityId: String(route.params.facility_id),
    }),
  },
  {
    path: '/billing/calculate-billing-month/:facility_id/:year/:month/',
    name: 'CalculateBillingMonthAll',
    component: IFXCalculateBillingMonth,
    meta: { AdminRoute: true },
    props: (route) => ({
      facilityId: String(route.params.facility_id),
      year: String(route.params.year),
      month: String(route.params.month),
    }),
  },
  {
    path: '/billing/calculate-billing-month/',
    name: 'CalculateBillingMonth',
    component: IFXCalculateBillingMonth,
    meta: { AdminRoute: true },
  },
  {
    path: '/billing/billing-records/:facility_id/:id/',
    name: 'BillingRecordDetail',
    component: IFXBillingRecordDetail,
    meta: { AdminRoute: true },
    props: (route) => ({
      id: String(route.params.id),
      facilityId: String(route.params.facility_id),
      showEditButtons: true,
    }),
  },
  {
    path: '/report-runs/list/',
    name: 'ReportRunList',
    component: IFXReportRunList,
    meta: { AdminRoute: true },
  },
  {
    path: '/forbidden/',
    name: 'Forbidden',
    component: IFXForbidden
  },
  {
    path: '/404/',
    name: 'NotFound',
    component: IFXNotFound
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/404/'
  }
]

const router = createRouter({
  history: createWebHistory('/{{project_name}}/'),
  routes,
  strict: true
})

export { router, routes }

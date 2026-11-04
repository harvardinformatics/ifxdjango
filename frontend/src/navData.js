export default {
  actions: {
    icon: 'mdi-check-circle',
    title: 'Actions',
    items: [
    ]
  },
  admin: {
    icon: 'mdi-bank',
    title: 'Admin',
    items: [
      {
        icon: 'mdi-wallet',
        title: 'Expense Codes / POs',
        link: 'AccountList',
      },
      {
        icon: 'mdi-currency-usd',
        title: 'Billing Records',
        link: 'BillingRecordList',
      },
      {
        icon: 'mdi-finance',
        title: 'Reports',
        link: 'ReportRunList',
      },
      {
        icon: 'mdi-account-group',
        title: 'Users',
        link: 'UserList'
      },
      {
        icon: 'mdi-card-account-mail',
        title: 'Contacts',
        link: 'ContactList'
      },
      {
        icon: 'mdi-account',
        title: 'Account Requests',
        link: 'AccountRequestList'
      },
      {
        icon: 'mdi-domain',
        title: 'Organizations',
        link: 'OrganizationList'
      }
    ]
  },
  mailing: {
    icon: 'mdi-inbox',
    title: 'Mailing',
    items: [
      {
        icon: 'mdi-email',
        title: 'Compose New Mailing',
        link: 'MailingCompose'
      },
      {
        icon: 'mdi-email-multiple',
        title: 'Mailings',
        link: 'MailingList'
      },
      {
        icon: 'mdi-message',
        title: 'Messages',
        link: 'MessageList'
      },
    ]
  }
}

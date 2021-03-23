export default {
  actions: {
    icon: 'check_circle',
    title: 'Actions',
    items: [
    ]
  },
  admin: {
    icon: 'account_balance',
    title: 'Admin',
    items: [
      {
        icon: 'group',
        title: 'Users',
        link: 'UserList'
      },
      {
        icon: 'contact_mail',
        title: 'Contacts',
        link: 'ContactList'
      },
      {
        icon: 'person',
        title: 'Account Requests',
        link: 'AccountRequestList'
      },
      {
        icon: 'mdi-account-group',
        title: 'Organizations',
        link: 'OrganizationList'
      }
    ]
  },
  mailing: {
    icon: 'inbox',
    title: 'Mailing',
    items: [
      {
        icon: 'email',
        title: 'Compose New Mailing',
        link: 'MailingCompose'
      },
      {
        icon: 'mdi-email-multiple',
        title: 'Mailings',
        link: 'MailingList'
      },
      {
        icon: 'message',
        title: 'Messages',
        link: 'MessageList'
      },
    ]
  }
}

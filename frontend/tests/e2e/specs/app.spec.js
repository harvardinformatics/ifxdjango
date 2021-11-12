// https://docs.cypress.io/api/introduction/api.html
/* eslint-disable brace-style, no-else-return, import/no-unresolved */

describe('App Home', () => {
  beforeEach(() => {
    cy.login()
    cy.visit('/')
  })
  /**it('App title appears at app root', () => {
    const appTitle = '@@App Title@@'
    cy.contains('h1', appTitle)
  }) **/
  it('Login icon appears in header', () => {
    const name = 'Vera'
    cy.contains('span', name)
  })
  it('Has all nav items', () => {
    const navItems = [
      'Home',
      'Actions',
      'Users',
      'Contacts',
      'Organizations',
      'Compose New Mailing',
      'Mailings',
      'Messages',
      'Logout',
    ]
    cy.wrap(navItems).each((ni) => cy.contains('.v-list-item__title', ni))
  })
  it('Has proper footer text', () => {
    const footerText = '2021 The Presidents and Fellows of Harvard College'
    cy.contains('span', footerText)
  })
})

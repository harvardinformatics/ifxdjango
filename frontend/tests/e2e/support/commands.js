import FT from '../fixtures/fieldTypes'

Cypress.Commands.add('login', () => {
  cy.request({
    method: 'GET',
    url: `http://${Cypress.env('{{project_name|upper}}_DRF')}/{{project_name}}/api/obtain-auth-token/`,
  }).then((res) => window.localStorage.setItem('ifx_{{project_name}}_user', JSON.stringify(res.body)))
})

Cypress.Commands.add('checkPathContains', (str) => {
  cy.location().should((loc) => expect(loc.pathname.toString()).to.contain(str))
})

Cypress.Commands.add('checkIs404', () => {
  cy.checkPathContains('404')
})

Cypress.Commands.add('checkIsForbidden', () => {
  cy.checkPathContains('forbidden')
})

Cypress.Commands.add('inputValuesAndSubmit', (values) => {
  cy.wrap(values).each((val) => {
    cy.get(`[data-cy=${val.key}]`).as('input')
    if (val.type === FT.TEXT) {
      cy.get('@input')
        .first()
        .type(val.value)
    } else if (val.type === FT.CHECK) {
      if (val.value === true) {
        cy.get('@input').check({ force: true })
      } else {
        cy.get('@input').uncheck({ force: true })
      }
    } else if (val.type === FT.SELECT) {
      cy.get('@input')
        .parent()
        .click()
      cy.get('.v-menu__content')
        .contains(val.value)
        .click()
    }
  })
  // Click submit
  cy.get('[data-cy=submit-btn]').click()
})

Cypress.Commands.add('checkValues', (values) => {
  cy.wrap(values).each((val) => {
    return val.ignore ? true : cy.contains(val.value.toString())
  })
})

Cypress.Commands.add('visitHomePage', () => {
  cy.visit('/')
})

Cypress.Commands.add('visitCreatePage', (url) => {
  cy.visit(`/${url}/create/`)
})

Cypress.Commands.add('visitDetailPage', (url, id) => {
  cy.visit(`/${url}/${id}/`)
})

Cypress.Commands.add('visitEditPage', (url, id) => {
  cy.visit(`/${url}/${id}/edit/`)
})

Cypress.Commands.add('visitListPage', (url) => {
  cy.visit(`${url}/list/`)
})

import allItemData from '../fixtures/itemData'

// Filter item types to focus on one or more in the list
const itemData = allItemData.filter((i) => ['user', 'organization'].includes(i.type))

// const itemData = allItemData
describe('Item List', () => {
  itemData.forEach((i) => {
    const checkListLength = (listLength = 5, comparison = 'be.gte') => cy
      .get('tr')
      .its('length')
      .should(comparison, listLength)
    // const getNthRow = (n = 0) => cy.get('tr').its('length').should(comparison, listLength)
    context(`Tests for ${i.type}`, () => {
      beforeEach(() => {
        cy.login()
      })
      it(`Loads list page for ${i.type}`, () => {
        cy.visit(`/${i.url}/list/`)
        cy.contains('h1', i.title)
      })
      it(`${i.type} data table has at least ${i.listLength} rows`, () => {
        checkListLength(i.listLength)
      })
      it('Enters text in search field and updates results', () => {
        cy.get('[data-cy=ifx-search-field]').type(i.searchText)
        checkListLength(i.listLength, 'be.lte')
      })
      it('Clears search field and updates results', () => {
        cy.get('[data-cy=ifx-search-field]').as('searchField')
        cy.get('.v-input__icon--clear')
          .first()
          .click()
        cy.get('@searchField').should('have.value', '')
        checkListLength(i.listLength)
      })
      it('Navigates to item edit', () => {
        cy.visit(`/${i.url}/list/`)
        cy.get('[data-cy=navigate-to-edit]')
          .first()
          .then(($el) => {
            $el.click()
            // TODO: add check for specific id
            cy.url().then(($url) => expect($url).to.contain('edit'))
          })
      })
      it('Navigates to item create', () => {
        cy.visit(`/${i.url}/list/`)
        cy.get('[data-cy=add-btn]')
          .first()
          .then(($el) => {
            $el.click()
            cy.checkPathContains(`${i.url}/create/`)
          })
      })
      it('Has footer selection', () => {
        cy.visit(`/${i.url}/list/`)
        cy.contains('Rows per page')
      })
      it('Footer selection is sticky', () => {
        cy.visit(`/${i.url}/list/`)
        cy.contains('Rows per page')
      })
    })
  })
})

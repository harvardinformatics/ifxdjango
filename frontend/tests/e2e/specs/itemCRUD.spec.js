import allItemData from '../fixtures/itemData'

const itemData = allItemData.filter((i) => ['user', 'organization', 'message'].includes(i.type))
let createID
let deleteID
itemData.forEach((item) => {
  describe(`CRUD operations for ${item.type}`, () => {
    beforeEach(() => {
      cy.login()
    })
    // Use the above data to create
    it('Creates a record, navigates to details page, checks values', () => {
      cy.visitCreatePage(item.url)
      cy.inputValuesAndSubmit(item.inputs.create)
      // Should navigate to details page with inputs
      cy.checkValues(item.inputs.create)
      // Save itemID for later
      cy.get('[data-cy=header-id]')
        .invoke('text')
        .then((text) => (createID = text))
    })
    it('visits detail page', () => {
      cy.visitDetailPage(item.url, createID)
    })
    it('visits detail page with bad id', () => {
      const id = 'probablynotarealid'
      cy.visitDetailPage(item.url, id)
      cy.visit(`/${item.url}/${id}/`, { failOnStatusCode: false })
    })
    it('updates a record with valid data', () => {
      cy.visitEditPage(item.url, createID)
      cy.inputValuesAndSubmit(item.inputs.update)
      cy.checkValues(item.inputs.update)
      cy.visitHomePage()
    })
    it('Deletes the record we just created or the first record from the list page', () => {
      cy.visitListPage(item.url)
      // Select row in data table with our search item in body and get checkbox
      if (item.searchItem) {
        cy.get('[data-cy=ifx-search-field]').type(item.searchItem)
      }
      cy.get('tbody > tr')
        .eq(0)
        .find('.v-simple-checkbox')
        .click()
      cy.get('[data-cy=action-select]').click({ force: true })
      cy.get('.v-list-item__title')
        .contains('Delete')
        .click({ force: true })
      cy.get('[data-cy=complete-action]').click({ force: true })
    })
    if (item.canDeleteFromDetail !== false) {
      it('Creates record, deletes it from details page, and confirms not in list', () => {
        cy.visitCreatePage(item.url)
        cy.inputValuesAndSubmit(item.inputs.create)
        cy.checkValues(item.inputs.create)
        // Get created record ID and store it for use in update and delete
        cy.get('[data-cy=header-id]')
          .invoke('text')
          .then((text) => (deleteID = text))
        cy.get('[data-cy=item-delete]').click({ force: true })
        cy.get('[data-cy=complete-action]').click({ force: true })
        cy.visitListPage(item.url)
        cy.get(deleteID).should('not.exist')
      })
    }
  })
})

Feature: Invoice search

    @selenium
    @bdd
    Scenario: Search an invoice by customer
        Given the billing dashboard is open
        When I search for customer "CUST-001"
        Then invoice "INV-1001" should be visible
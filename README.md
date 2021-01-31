# SimpleLoanSystemLenmeAssignment

# Notes
First:
  I created a borrower module that handle all borrower operation such that :-
  
    add new borrower.         `     [url]("borrower-create/")
    update an existing borrower.    [url]("borrower-detail/pk/")
    read borrower informations.     [url]("borrower-update/pk/")
    delete an existing borrower.    [url]("borrower-delete/pk/")
  
 The same operations above is created for investors.
    
    add new investor.         `     [url]("investor-create/")
    update an existing investor.    [url]("investor-detail/pk/")
    read investor informations.     [url]("investor-update/pk/")
    delete an existing investor.    [url]("investor-delete/pk/")

Second:
  I created my main api which is (loan operations whether are beloning to borrower or investor).
  The loan system is applying to all these features:-
      
      1 - A borrower request a loan (5000$)          
          [url]("borrower/pk/loan_request")
          [I made the borrower request as general his can request any loan]
          
      2 - An investor can see all the borrower's loan requests before offer to pay for them.  
          [url]("investor/pk/list_loan")
          
      3 - An investor can make an offer to any borrower's loan request and will be wait until borrower accpet offer.  
          [url]("investor/pk_investor/offer/pk_loan")
          
      4 - A borrower can see all investor's offer to his particular loan request and can be choose one of them.   
          [url]("borrower/pk_borrower/request_offers/pk_loan")
          
      5 - A borrower can accept any offer from investor.
          [url]("borrower/pk_borrower/list_request/pk_loan/accept_offer/pk_investor")
          
      6 - A borrower can access all his loan  requests. 
          [url]("borrower/pk/list_request")
          
      7- A borrower can access all his submitted requests.
          [url]("borrower/pk_borrower/loan_submit")
          
      6 - The system api submitted the request after borrower accepted it, And creates scheduled to borrower for payement.
          
      7 - The system api update each payment date for borrower until completed all payment.
          [url]("admin/pay_update/pk_borrower/pk_loan/pk_investor/month")
          
      8 - The system api completed the loan request until borrower complete all the payment, And return the money for investor.
          [url]("admin/submitted/pk_borrower/pk_loan/pk_investor/completed")]
      
  

  
    

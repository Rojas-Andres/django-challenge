MESSAGE_LOAN_CREATE = """ \
The customer's score is not enough to request the loan. \
customer_score = {custom_score} and total_debt = {debt}, you can request a maximum of {max_debt} \
"""
MESSAGE_AMOUNT_NOT_NEGATIVE = "El monto no puede ser negativo"
MESSAGE_STATUS_PERMISSION_LOAN = "El estatus para actualizar no permitido, status permitidos: {status}"
MESSAGE_LOAD_EXTERNAL_ID_NOT_FOUND = "El load_external_id {value} no existe."
MESSAGE_PAYMENT_EXTERNAL_ID_EXISTS = "El external_id {external_id} ya existe con el pago."
MESSAGE_EXTERNAL_ID_DUPLICATE = "Duplicate load_external_id found: {load_external_id}"
MESSAGE_AMOUNT_GREATHER = """ The amount of the payment cannot be greater than the outstanding balance of the loan.\
loan_outstanding = {outstanding} and payment_amount = {amount} """
MESSAGE_CUSTOMER_EXTERNAL_ID_NOT_FOUND = "El customer_external_id {value} no existe."
MESSAGE_NOT_PERMISSION_PAYMENT = "El estado del prestamo no esta activo por lo tanto no se puede realizar el pago."

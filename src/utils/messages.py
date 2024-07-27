MESSAGE_LOAN_CREATE = """ \
The customer's score is not enough to request the loan. \
customer_score = {custom_score} and total_debt = {debt}, you can request a maximum of {max_debt} \
"""
MESSAGE_AMOUNT_NOT_NEGATIVE = "El monto no puede ser negativo"
MESSAGE_STATUS_PERMISSION = "El estatus para actualizar no permitido, status permitidos: {status}"
MESSAGE_LOAD_EXTERNAL_ID_NOT_FOUND = "El load_external_id {value} no existe."
MESSAGE_PAYMENT_EXTERNAL_ID_EXISTS = "El external_id {external_id} ya existe con el pago."
MESSAGE_EXTERNAL_ID_DUPLICATE = "Duplicate load_external_id found: {loan_external_id}"
MESSAGE_AMOUNT_GREATHER = """El monto del pago no puede ser mayor que el saldo pendiente del préstamo.\
saldo_pendiente = {outstanding} y monto_del_pago = {amount}"""
MESSAGE_CUSTOMER_EXTERNAL_ID_NOT_FOUND = "El customer_external_id {value} no existe."
MESSAGE_NOT_PERMISSION_PAYMENT = "El estado del prestamo no esta activo por lo tanto no se puede realizar el pago."
MESSAGE_PAYMENT_NOT_FOUND = "Pago no encontrado"
MESSAGE_PAYMENT_STATUS = "El pago ya esta en ese estado"
MESSAGE_PAYMENT_UPDATE_ACTIVE_REJECTED = "El pago no se puede actualizar a active porque esta en active"

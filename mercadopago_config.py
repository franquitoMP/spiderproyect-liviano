import os
import mercadopago

sdk = mercadopago.SDK(os.getenv("MP_ACCESS_TOKEN"))

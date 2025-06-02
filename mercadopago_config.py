from dotenv import load_dotenv
import os
import mercadopago

load_dotenv()
sdk = mercadopago.SDK(os.getenv("MP_ACCESS_TOKEN"))

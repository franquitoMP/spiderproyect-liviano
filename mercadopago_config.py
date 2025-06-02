from dotenv import load_dotenv
import os
import mercadopago

load_dotenv()
print("TOKEN:", os.getenv("MP_ACCESS_TOKEN"))

sdk = mercadopago.SDK(os.getenv("MP_ACCESS_TOKEN"))

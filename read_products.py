
import google.auth
from google.auth.transport.requests import AuthorizedSession

SPREADSHEET_ID = "1I5AygTu_f3l6M_IUkwjwp4xlCKI5KA-GEp1u_SNh06E"

credentials, _ = google.auth.default(
    scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
)

session = AuthorizedSession(credentials)

url = (
    f"https://sheets.googleapis.com/v4/spreadsheets/"
    f"{SPREADSHEET_ID}/values/Products!A1:Z1000"
)

response = session.get(url, timeout=30)
response.raise_for_status()

values = response.json().get("values", [])

if not values:
    print("Sheet Products chưa có dữ liệu.")
    raise SystemExit(0)

headers = values[0]

products = []

for row in values[1:]:
    product = dict(zip(headers, row))

    if (
        product.get("status", "").strip() == "READY"
        and product.get("approved", "").strip() == "YES"
    ):
        products.append(product)

print(f"Tim thay {len(products)} san pham hop le.")

for product in products:
    print(
        "San pham:",
        product.get("product_id"),
        "-",
        product.get("product_name")
    )

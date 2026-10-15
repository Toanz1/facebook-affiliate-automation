
import os
from datetime import datetime, timezone, timedelta

import google.auth
from googleapiclient.discovery import build

SHEET_ID = os.environ["GOOGLE_SHEET_ID"]
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

HEADERS = [
    "product_id", "product_name", "affiliate_url",
    "group_url", "post_text", "status", "created_at"
]

def create_post(product):
    name = product["product_name"].strip()
    description = product.get("description", "").strip()
    link = product["affiliate_url"].strip()

    try:
        price = float(
            str(product.get("price", "0"))
            .replace(",", "").replace("₫", "").strip()
        )
        price_text = f"{price:,.0f}".replace(",", ".") + "đ"
    except ValueError:
        price_text = ""

    lines = [
        f"🛍️ {name.upper()}",
        "",
        "Bạn đang tìm một sản phẩm phù hợp với nhu cầu?",
        "",
        f"✨ {name}",
    ]

    if description:
        lines.append(f"✅ {description}")

    if price_text and price > 0:
        lines.append(f"💰 Giá tham khảo: {price_text}")

    lines.extend([
        "",
        "🔎 Xem thông tin và giá mới nhất tại:",
        link,
        "",
        "📌 Bài viết có chứa liên kết tiếp thị liên kết.",
        "#SanPhamHay #MuaSam #Affiliate"
    ])

    return "\n".join(lines)


def get_records(service, sheet_name):
    result = service.spreadsheets().values().get(
        spreadsheetId=SHEET_ID,
        range=f"'{sheet_name}'!A1:ZZ"
    ).execute()

    values = result.get("values", [])
    if not values:
        return [], []

    headers = [str(h).strip() for h in values[0]]
    records = []

    for row_index, row in enumerate(values[1:], start=2):
        item = {
            header: row[i] if i < len(row) else ""
            for i, header in enumerate(headers)
            if header
        }
        item["_row"] = row_index
        records.append(item)

    return headers, records


def main():
    credentials, _ = google.auth.default(scopes=SCOPES)
    service = build(
        "sheets", "v4", credentials=credentials,
        cache_discovery=False
    )

    product_headers, products = get_records(
        service, "Products"
    )
    post_headers, posts = get_records(service, "Posts")

    if post_headers != HEADERS:
        raise ValueError(
            "Sheet Posts phải có đúng 7 cột theo hướng dẫn."
        )

    if "status" not in product_headers:
        raise ValueError("Products thiếu cột status.")

    existing = {
        p.get("product_id", "").strip()
        for p in posts
        if p.get("product_id", "").strip()
    }

    eligible = [
        p for p in products
        if p.get("status", "").strip().upper() == "READY"
        and p.get("approved", "").strip().upper() == "YES"
        and p.get("product_id", "").strip()
        and p.get("product_name", "").strip()
        and p.get("affiliate_url", "").strip().startswith(
            ("https://", "http://")
        )
        and p["product_id"].strip() not in existing
    ]

    print(f"Tìm thấy {len(eligible)} sản phẩm cần tạo bài.")

    status_column = (
        product_headers.index("status") + 1
    )

    def column_letter(number):
        result = ""
        while number:
            number, remainder = divmod(number - 1, 26)
            result = chr(65 + remainder) + result
        return result

    status_letter = column_letter(status_column)

    for product in eligible:
        product_id = product["product_id"].strip()
        post_text = create_post(product)

        created_at = datetime.now(
            timezone(timedelta(hours=7))
        ).isoformat()

        new_row = [
            product_id,
            product["product_name"],
            product["affiliate_url"],
            product.get("group_url", ""),
            post_text,
            "DRAFT",
            created_at
        ]

        # Lưu bài trước, sau đó mới cập nhật trạng thái.
        service.spreadsheets().values().append(
            spreadsheetId=SHEET_ID,
            range="'Posts'!A:G",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": [new_row]}
        ).execute()

        print(f"Đã lưu DRAFT: {product_id}")

        service.spreadsheets().values().update(
            spreadsheetId=SHEET_ID,
            range=(
                f"'Products'!{status_letter}"
                f"{product['_row']}"
            ),
            valueInputOption="RAW",
            body={"values": [["DRAFTED"]]}
        ).execute()

        print(f"Đã cập nhật DRAFTED: {product_id}")

    print("Hoàn thành xử lý.")


if __name__ == "__main__":
    main()

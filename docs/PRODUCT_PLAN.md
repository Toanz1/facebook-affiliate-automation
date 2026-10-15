# Định hướng sản phẩm: Affiliate Niche Studio

## Mục tiêu

Làm công cụ local-first trên Windows giúp một creator đi trọn quy trình affiliate:

1. Tìm và so sánh các ngách bằng dữ liệu có nguồn gốc rõ ràng.
2. Chọn sản phẩm đã được người dùng kiểm tra và có link affiliate hợp lệ.
3. Soạn kịch bản, caption và checklist quay phù hợp từng nền tảng.
4. Tạo video dọc 9:16 từ tư liệu người dùng có quyền sử dụng.
5. Xuất nội dung để đăng, rồi ghi nhận click, đơn và hoa hồng đã được nền tảng xác nhận.

Công cụ hỗ trợ quy trình kiếm tiền; không cam kết doanh thu. Điểm số ngách chỉ là gợi ý từ dữ liệu đầu vào, không được trình bày như số liệu thị trường nếu chưa có nguồn.

## Người dùng mục tiêu và phạm vi V1

Một người làm affiliate tại Việt Nam, làm nội dung sản phẩm bằng Windows, muốn bắt đầu với TikTok, Shopee Video và Facebook Reels. Ưu tiên chạy local, miễn phí/open-source khi có thể; dịch vụ cloud hoặc API là tùy chọn.

V1 giữ phạm vi nhỏ: một creator, một ngách thử nghiệm tại một thời điểm, dữ liệu sản phẩm nhập từ CSV/Google Sheets hoặc điền tay. Không tự thu thập dữ liệu bằng cookie, không giả API, không tự đăng hàng loạt vào Facebook Groups.

## Ngách thử nghiệm (giả thuyết cần kiểm chứng)

| Ngách nhỏ | Vì sao đáng thử | Rủi ro cần đo |
| --- | --- | --- |
| Đồ sắp xếp nhà trọ/căn hộ nhỏ | Dễ quay trước–sau; có thể chứng minh cách dùng trong vài giây; nhiều tình huống nội dung lặp lại | Dễ thành nội dung chung chung; hoa hồng và nhu cầu thực tế phải lấy từ tài khoản affiliate |
| Dụng cụ bếp giải quyết việc cụ thể | Video demo trực quan; có thể làm hướng dẫn, so sánh và thử nghiệm | Chất lượng hàng không đồng đều; cần kiểm tra đánh giá, đổi trả và độ bền |
| Đồ chăm sóc thú cưng tại nhà | Có nhiều tình huống sử dụng và khả năng mua lại | Cần tự trải nghiệm; tránh lời khuyên y tế hoặc tuyên bố hiệu quả không có chứng cứ |
| Chăm sóc da/làm đẹp giá phổ thông | Nhiều chủ đề và sản phẩm để thử | Cạnh tranh cao; rủi ro lớn nếu video đưa tuyên bố y tế, trị bệnh hoặc kết quả thiếu căn cứ |

**Giả thuyết ưu tiên đầu tiên:** giải pháp sắp xếp và tiện ích cho phòng trọ/căn hộ nhỏ. Chưa coi đây là ngách thắng. Chỉ chuyển thành quyết định sau khi kiểm tra sản phẩm, hoa hồng, tín hiệu tìm kiếm, độ cạnh tranh và kết quả đăng thử.

## Cách công cụ chấm ngách và sản phẩm

Mỗi bản ghi cần lưu nguồn và ngày lấy dữ liệu. Có thể nhập thủ công hoặc CSV từ nguồn mà người dùng được phép sử dụng.

Điểm thử nghiệm 0–100, hiển thị từng thành phần thay vì chỉ đưa một con số:

- Nhu cầu/tín hiệu tìm kiếm: 25%.
- Tín hiệu sản phẩm (lượt bán/đánh giá/độ mới nếu nguồn có cung cấp): 20%.
- Hoa hồng dự kiến, đúng theo dashboard của tài khoản: 20%.
- Khả năng quay demo thật và tạo nhiều góc nội dung: 20%.
- Mức cạnh tranh trong kết quả tìm kiếm/video quan sát được: 10%.
- Độ an toàn nội dung và tuân thủ nền tảng: 5%.

Thiếu dữ liệu thì hiển thị “chưa biết”, không tự điền 0 hoặc bịa hoa hồng. Điểm cạnh tranh và chính sách phải có ghi chú/phương pháp quan sát để người dùng kiểm tra lại.



### Bộ chấm điểm thử nghiệm đã có trong nhánh này

File `niche_scorer.py` là bộ CLI đầu tiên. Nhập điểm thủ công theo thang 0–5 cho sáu yếu tố trên; ở yếu tố cạnh tranh, điểm cao nghĩa là ít cạnh tranh hơn, còn ở an toàn chính sách, điểm cao nghĩa là rủi ro thấp hơn. Không có điểm nào được tự suy ra từ lượt bán/hoa hồng.

CLI chỉ xuất tổng điểm khi đủ cả sáu điểm, có ít nhất một URL bằng chứng và có ngày kiểm tra. Thiếu bất kỳ dữ liệu nào thì kết quả là `NEED_DATA`, không bị quy thành điểm 0.

CSV đầu vào cần cột: `niche,demand,product_signal,commission,demo,competition,policy_safety,evidence_urls,checked_at`. Điểm điền từ dữ liệu quan sát được và đánh giá thủ công; giữ ghi chú/nguồn ngoài CSV nếu cần giải thích cách chấm.

Chạy bằng Python 3:

```bash
python niche_scorer.py niche-candidates.csv --output niche-rankings.csv
python -m unittest discover -s tests -v
```

## Luồng MVP

1. **Nhập ứng viên:** tên, URL sản phẩm, nền tảng affiliate, hoa hồng nếu có nguồn, giá quan sát, đánh giá/lượt bán nếu có, ngày kiểm tra, ghi chú và quyền sử dụng tư liệu.
2. **So sánh ngách:** lọc theo nền tảng và tình trạng dữ liệu; sửa trọng số; xem vì sao từng ngách được xếp hạng.
3. **Tạo brief nội dung:** nêu vấn đề, người xem, cách demo, ưu điểm/nhược điểm đã xác minh, CTA và disclosure affiliate.
4. **Tạo tài sản:** kịch bản 15/30/60 giây, caption/hashtag theo nền tảng, giọng đọc/phụ đề, video MP4 9:16. Nội dung được duyệt trước khi xuất.
5. **Đăng thủ công trước:** xuất file và checklist từng nền tảng; ghi URL bài đăng sau khi đăng.
6. **Theo dõi:** nhập lượt xem, click, đơn và hoa hồng từ báo cáo chính thức; so sánh theo ngách, sản phẩm, format và kênh.

V1 hoàn tất khi có thể nhập dữ liệu → chọn ngách → tạo brief/script → xuất video 9:16 → ghi kết quả đăng/bán, và người dùng có thể truy ngược nguồn của mọi số liệu.

## Thử nghiệm ngách trong 4 tuần

- Chọn 3 ngách nhỏ; lấy 3 sản phẩm phù hợp mỗi ngách từ dashboard affiliate và nguồn tìm kiếm được phép.
- Đăng một nội dung gốc cho mỗi sản phẩm; biến thể caption/hook riêng cho từng kênh, dùng video sạch không watermark.
- Ghi lại view, thời gian xem nếu có, click, đơn được xác nhận, hoa hồng và thời gian sản xuất.
- Đánh giá theo dữ liệu đủ thời gian đối soát; chọn ngách tiếp tục dựa trên click/đơn/hoa hồng và công sức làm video. Không kết luận thắng chỉ từ lượt xem.

## Ranh giới tích hợp nền tảng

- **Shopee Video:** V1 xuất video và hướng dẫn đăng/gắn sản phẩm thủ công. Tài liệu Shopee mô tả tạo video, chọn ảnh bìa, mô tả/hashtag và thêm sản phẩm. Tài liệu cũng yêu cầu nội dung tập trung vào sản phẩm được gắn, không có watermark/logo nền tảng video khác, và khuyến nghị sản phẩm xuất hiện/được sử dụng trong video.
- **TikTok:** bắt đầu bằng xuất video hoặc upload bản nháp. Direct Post chỉ là giai đoạn sau khi có app, scope được duyệt, người dùng ủy quyền và hoàn tất audit; client chưa audit bị giới hạn hiển thị riêng tư theo tài liệu TikTok.
- **Facebook Page/Reels:** V1 xuất nội dung để người dùng đăng; chỉ thêm API sau khi xác minh quyền Page và yêu cầu quyền/app review hiện hành.
- **Facebook Groups:** không hứa tự động đăng. Meta đã thông báo Groups API bị deprecated và bị gỡ khỏi các phiên bản; V1 chỉ tạo bản nháp/copy nội dung để người dùng tự đăng theo quy định của nhóm.

## Các bước phát triển

### Giai đoạn 1 — Chốt nền

- Làm rõ repo này là pipeline Google Sheets/GitHub Actions hiện có; không tuyên bố rằng nó đã là app Windows.
- Thêm schema dữ liệu chuẩn cho ngách, sản phẩm, nguồn dữ liệu, nội dung và kết quả.
- Viết bộ nhập CSV/Google Sheets có kiểm tra dữ liệu và chống tạo bài trùng.
- Giữ thông tin xác thực trong GitHub Secrets hoặc máy người dùng; không đưa token/khóa vào repo.

### Giai đoạn 2 — Niche Finder và Content Factory local

- Xây màn hình so sánh ngách/sản phẩm và hiển thị nguồn, ngày cập nhật, dữ liệu thiếu.
- Tích hợp tạo kịch bản/caption và xuất MP4 9:16 dựa trên công nghệ local có sẵn trong MoneyAI Studio.
- Giữ bước duyệt nội dung và đăng thủ công.

### Giai đoạn 3 — Đo lường

- Nhập báo cáo nền tảng/affiliate bằng CSV.
- Tính click-through, đơn/click và hoa hồng theo nguồn, ngách, sản phẩm và format.
- Chỉ triển khai API đăng sau khi hồ sơ nhà phát triển được duyệt và có use case thực tế.

## Ngoài phạm vi V1

- Tự đăng bài hàng loạt vào nhóm Facebook.
- Đăng nhập bằng cookie, né hạn chế API, cào dữ liệu sau đăng nhập hoặc vượt CAPTCHA.
- Tự tạo số liệu lượt bán/commission khi API hoặc dashboard không cung cấp.
- Cam kết video AI tự tạo sẽ kiếm tiền hoặc được nền tảng phân phối.
- Tự động gắn sản phẩm Shopee Video nếu không có API công khai/được cấp quyền cho tài khoản.

## Nguồn nền tảng đã kiểm tra ngày 15/10/2026

- Shopee Help — [Tham gia Affiliate cùng Shopee Video](https://help.shopee.vn/portal/10/article/141537).
- Shopee Help — [Điều khoản Chương trình Tiếp thị liên kết (cập nhật 08/07/2026)](https://help.shopee.vn/portal/10/article/122944).
- TikTok for Developers — [Get Started: Direct Post](https://developers.tiktok.com/docs/en/content-posting-api-get-started).
- TikTok for Developers — [Content Sharing Guidelines](https://developers.tiktok.com/docs/en/content-sharing-guidelines).
- Meta for Developers — [Graph API v19.0 announcement](https://developers.facebook.com/blog/post/2024/01/23/introducing-facebook-graph-and-marketing-api-v19/).
- Meta for Developers — [Pages API: Posts](https://developers.facebook.com/documentation/pages-api/posts).

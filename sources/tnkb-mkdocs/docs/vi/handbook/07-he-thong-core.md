# Hệ Thống CORE

Cách Sân và Bóng Dẫn Đến Cầm Vợt, Điểm Tiếp Xúc, Vung Nạp, và Độ Căng Cơ

Mỗi pha bóng là một vòng lặp: sân cho bạn biết mặt vợt nào bạn cần. Bóng cho bạn biết vung nạp nào bạn có. Bạn thực hiện cả hai bằng cầm vợt, điểm tiếp xúc, và độ căng cơ.

*Sân cộng bóng đưa ra bài toán. Cầm vợt cộng điểm tiếp xúc cộng vung nạp cộng độ căng cơ là lời giải của bạn. Vòng lặp khép lại tại thời điểm tiếp xúc.*

— Henry Phạm

## Phương Trình CORE

Vòng lặp CORE chạy trong thời gian thực, trên từng pha bóng một:

Vòng lặp CORE: sân cộng bóng → góc mặt vợt bắt buộc → cầm vợt cộng điểm tiếp xúc → vung nạp cộng độ căng cơ → truyền tải góc mặt vợt tại tiếp xúc → kết quả nuôi lại vòng lặp tiếp theo.

| Biến Số | Đầu Vào                            | Chức Năng                                    | Quy Tắc Chính                                            |
| ------- | ---------------------------------- | -------------------------------------------- | -------------------------------------------------------- |
| C       | Vị trí sân + độ cao bóng           | Quyết định góc mặt vợt bắt buộc tại tác động | Sâu = mở, trong sân = khép, thấp = mở, cao = khép        |
| O       | Tốc độ bóng đến                    | Quyết định kích cỡ vung nạp                  | Nhanh = ngắn, chậm = đầy đủ, trung bình = trung bình     |
| R       | Hệ thống vợt — cầm vợt             | Đặt góc mặt vợt cơ bản                       | Chọn sao cho tiếp xúc lý tưởng = góc mặt vợt bắt buộc    |
| E       | Năng lượng — vung nạp + độ căng cơ | Nạp và truyền năng lượng đến mặt vợt         | Khớp hình lồng với thời gian, khớp gradient với tiếp xúc |

## Thứ Bậc Quyết Định (0.8 Giây)

Bộ não của bạn xử lý theo một trình tự cố định. Bạn không thể bỏ qua bước nào.

| Thời Điểm   | Pha                     | Quyết Định                                       | Kết Quả                                               | Nếu Sai                                                                 |
| ----------- | ----------------------- | ------------------------------------------------ | ----------------------------------------------------- | ----------------------------------------------------------------------- |
| -0.8 giây  | Đối thủ tiếp xúc bóng   | Đọc quỹ đạo, tốc độ, độ xoáy                     | Vị trí sân + độ cao bóng + tốc độ                     | Sai vị trí = sai cửa sổ góc mặt vợt                                     |
| -0.6 giây  | Bóng qua lưới           | Xác nhận độ cao, chốt yêu cầu góc mặt vợt        | Góc mặt vợt bắt buộc tại tác động                     | Sai góc mặt vợt = không thể sửa về sau                                  |
| -0.5 giây  | Xoay người + split step | Chọn cầm vợt, bắt đầu vung nạp                   | Cầm vợt đã chọn, kích cỡ vung nạp đã khởi động        | Xoay muộn = vung nạp bị vội                                             |
| -0.3 giây  | Bóng nảy (bên bạn)      | Vung nạp hoàn tất, vung tiến bắt đầu             | Kích cỡ vung nạp đã chốt, gradient độ căng cơ bắt đầu | Vẫn đang vung nạp = muộn                                                |
| -0.1 giây  | Vung tiến               | Gradient độ căng cơ tăng dần                     | Đỉnh độ căng cơ tại tiếp xúc                          | Chắc quá sớm = không có công suất; lỏng quá muộn = không kiểm soát được |
| 0 mili-giây | Tiếp xúc                | Góc mặt vợt được truyền tải, độ căng cơ đạt đỉnh | Bóng được phóng đi với góc mặt vợt bắt buộc           | Sai góc mặt vợt = bóng đi sai                                           |
| +0.1 giây  | Giữ                     | Quiet Eye giữ nguyên, độ căng cơ giảm xuống      | Góc mặt vợt ổn định suốt pha thoát vợt                | Liếc nhìn sớm = mặt vợt mở ra                                           |
| +0.3 giây  | Thả và hồi phục         | Đầu thả lỏng, chân trở lại vị trí                | Sẵn sàng cho vòng lặp tiếp theo                       | Bị kẹt lại = hồi phục chậm                                              |

**Quy Tắc.** Vòng lặp mang tính tuần tự: sân, rồi đến bóng, rồi mặt vợt, rồi cầm vợt, rồi điểm tiếp xúc, rồi vung nạp, rồi độ căng cơ. Bỏ qua một mắt xích, cả chuỗi sẽ đứt.

## Ví Dụ Tích Hợp: Cùng Một Trái Bóng, Khác Vị Trí Sân

Hãy lấy một trái bóng ngang hông đến với tốc độ 80 km/h. Góc mặt vợt bắt buộc giống nhau ở mọi nơi: hơi khép, khoảng 3 độ. Nhưng vị trí của bạn làm thay đổi mọi thứ khác về cách bạn truyền tải góc mặt vợt đó.

| Vị Trí Sân                         | Góc Mặt Vợt Bắt Buộc              | Chọn Cầm Vợt                          | Điểm Tiếp Xúc                 | Vung Nạp                    | Chìa Khóa Độ Căng Cơ             |
| ---------------------------------- | --------------------------------- | ------------------------------------- | ----------------------------- | --------------------------- | -------------------------------- |
| Sâu (4m sau vạch cuối sân)         | Hơi khép (3°)                     | Semi-Western (tự nhiên 3° ngang hông) | Chân trước, ngang hông        | Lồng đầy đủ, khuỷu tay cao  | Rơi lỏng, chắc tại tiếp xúc      |
| Vạch cuối sân (trên vạch)          | Hơi khép (3°)                     | Semi-Western                          | Chân trước, ngang hông        | Lồng trung bình             | Rơi lỏng, chắc tại tiếp xúc      |
| Trong sân (1m trong vạch cuối sân) | Hơi khép (3°)                     | Semi-Western hoặc Eastern             | Xa hơn phía trước, ngang hông | Lồng ngắn gọn               | Chắc sớm hơn, cảm giác đấm xuyên |
| Ở lưới (vị trí vô-lê)              | Không áp dụng — vô-lê thay vào đó | Continental                           | Phía trước, ngang ngực        | Không vung nạp, chỉ đặt vợt | Chắc ngay từ đầu, block/đẩy      |

**Mẹo Huấn Luyện.** Cùng một trái bóng, bốn vị trí, bốn lời giải khác nhau. Trái bóng không hề thay đổi. Chính vị trí của bạn đã thay đổi bối cảnh của góc mặt vợt bắt buộc, và điều đó làm thay đổi lời giải về cầm vợt, điểm tiếp xúc, vung nạp, và độ căng cơ. Đó chính là CORE trong thực tế.

## Ví Dụ Tích Hợp: Cùng Một Vị Trí, Khác Trái Bóng

Giờ hãy đảo ngược lại. Bạn đang đứng ở vạch cuối sân, và ba trái bóng khác nhau lần lượt đến.

| Bóng Đến                       | Góc Mặt Vợt Bắt Buộc | Cầm Vợt              | Tiếp Xúc               | Vung Nạp              | Độ Căng Cơ                  |
| ------------------------------ | -------------------- | -------------------- | ---------------------- | --------------------- | --------------------------- |
| Thấp, chậm (ngang gối)         | Hơi mở (mở 2°)       | Eastern/Semi-Western | Chân trước, thấp       | Lồng đầy đủ, rơi thấp | Rơi lỏng, đẩy lên           |
| Ngang hông, trung bình (rally) | Khép 3°              | Semi-Western         | Chân trước, ngang hông | Lồng trung bình       | Rơi lỏng, chắc tại tiếp xúc |
| Cao, nhanh (ngang vai trở lên) | Khép 6°              | Semi-Western         | Xa hơn phía trước, cao | Lồng ngắn, cao        | Chắc sớm hơn, đấm xuống     |

**Nguyên Lý Cốt Lõi.** Cùng một vị trí, khác trái bóng, nghĩa là khác yêu cầu về góc mặt vợt, nghĩa là khác lời giải về cầm vợt, điểm tiếp xúc, vung nạp, và độ căng cơ. Trái bóng là thứ quyết định.

## Vòng Lặp CORE Trong Thực Hành: Nghi Thức Ba Giây

Giữa các điểm, hãy chạy vòng lặp CORE một cách có ý thức:

1. Mình đang ở đâu? (Sâu / Vạch cuối sân / Trong sân / Lưới) — đặt xu hướng góc mặt vợt.

2. Bóng gì đang đến? (Nhanh/Trung bình/Chậm, Cao/Trung bình/Thấp) — đặt vung nạp và góc mặt vợt.

3. Mình cần góc mặt vợt nào? (Mở/Trung lập/Khép) — xác nhận cầm vợt và vùng tiếp xúc.

4. Điểm tiếp xúc của mình ở đâu? (Chân trước, độ cao, bên nào) — di chuyển chân ngay.

5. Vung nạp nào? (Không/Ngắn/Trung bình/Đầy đủ) — đặt kích cỡ hình lồng.

6. Kế hoạch độ căng cơ: "rơi lỏng, chắc tại tiếp xúc, kết thúc lỏng."

SÂN → BÓNG → MẶT VỢT → CẦM VỢT → TIẾP XÚC → VUNG NẠP → ĐỘ CĂNG CƠ → THỰC HIỆN.

## Các Điểm Gãy Vỡ Thường Gặp Của CORE

Khi một mắt xích nào đó trong chuỗi bị gãy, nó sẽ hiện ra thành một triệu chứng cụ thể, dễ nhận biết.

| Điểm Gãy Vỡ                | Triệu Chứng                                   | Mắt Xích Bị Đứt                                                 | Cách Sửa                                                        |
| -------------------------- | --------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------- |
| Sai góc mặt vợt cho vị trí | Lỗi dài/lưới ở những vùng cụ thể              | Ánh xạ Sân → Góc mặt vợt bị sai                                 | Drill: cửa sổ góc mặt vợt riêng theo từng vị trí                |
| Vung nạp muộn              | Vội vã, bị kẹp, vung bằng cơ bắp              | Chuỗi Tốc độ bóng → Vung nạp bị đứt                             | Split step sớm hơn, xoay người ngay khi đối thủ tiếp xúc bóng   |
| Cầm vợt không khớp         | Lỗi dài hoặc lưới lặp lại cùng một bên        | Chuỗi Cầm vợt → Góc mặt vợt cơ bản bị sai                       | Kiểm tra: đóng băng tại tiếp xúc lý tưởng, kiểm tra góc mặt vợt |
| Điểm tiếp xúc trôi dạt     | Chiều sâu hoặc độ xoáy không ổn định          | Chuỗi Tiếp xúc → Tinh chỉnh góc mặt vợt bị đứt                  | Drill: gọi to điểm tiếp xúc trước mỗi bóng, liên tục 20 quả     |
| Độ căng cơ sai             | Không có công suất, hoặc không kiểm soát được | Gradient độ căng cơ bị đứt                                      | Shadow: 3/10 → 6/10 tại tiếp xúc → 3/10                         |
| Ngẩng đầu quá sớm          | Mặt vợt mở ra tại tiếp xúc                    | Chuỗi Quiet Eye / năng lượng bị đứt → mất kiểm soát góc mặt vợt | Drill Quiet Eye: "đỗ, giữ, thả"                                 |

## Bài Tập CORE: Vị Trí Cộng Trái Bóng Bằng Lời Giải

Đối tác nạp bóng từ giỏ. Trước mỗi lần nạp, bạn gọi to:

"Vị trí: [Sâu/Vạch cuối sân/Trong sân/Lưới]. Bóng: [Nhanh/Trung bình/Chậm, Cao/Trung bình/Thấp]. Mặt vợt: [Mở/Trung lập/Khép]. Cầm vợt: [Continental/Eastern/Semi-Western/Western]. Tiếp xúc: [ở đâu]. Vung nạp: [Không/Ngắn/Trung bình/Đầy đủ]. Độ căng cơ: [lỏng/chắc/lỏng]."

- Đối tác nạp bóng. Bạn thực hiện. Đối tác xác nhận: "đúng rồi," hoặc sửa lại một biến số.

- 20 quả bóng. Mục tiêu: 18 trên 20 lần gọi tên hoàn hảo cộng với thực hiện đúng.

- Nâng cao hơn: đối tác thay đổi ngẫu nhiên cách nạp, buộc bạn phải thích ứng vòng lặp CORE theo thời gian thực.

**Quy Tắc.** Vòng lặp CORE không phải lý thuyết suông. Đó là động cơ ra quyết định theo thời gian thực. Nói to nó lên giúp bạn ý thức được nó. Tự động hóa nó giúp nó trở nên nhanh.

SÂN → BÓNG → MẶT VỢT → CẦM VỢT → TIẾP XÚC → VUNG NẠP → ĐỘ CĂNG CƠ → THỰC HIỆN.

## Những Điều Cần Nhớ

- Trước mỗi điểm, tự hỏi: mình đang ở đâu, bóng gì, mặt vợt nào, cầm vợt nào, tiếp xúc ở đâu, vung nạp nào, độ căng cơ nào?

- Vị trí sân quyết định xu hướng góc mặt vợt: đứng sâu nghĩa là mở, đứng trong sân nghĩa là khép.

- Tốc độ bóng quyết định kích cỡ vung nạp: bóng nhanh nghĩa là ngắn, bóng chậm nghĩa là đầy đủ.

- Chọn cầm vợt sao cho điểm tiếp xúc lý tưởng của bạn khớp với góc mặt vợt bắt buộc.

- Di chuyển chân để đưa bóng vào đúng vùng tiếp xúc lý tưởng đó.

- Hoàn tất vung nạp trước khi bóng nảy.

- Độ căng cơ: 3/10, lên 6/10 tại tiếp xúc, rồi trở lại 3/10.

- Cho Quiet Eye "đỗ" tại vùng tiếp xúc, từ lúc bóng nảy cho đến khi tiếp xúc.

**Chương Này Dẫn Đến Đâu.** Chương này tích hợp Chương 1 đến Chương 6 vào vòng lặp CORE. Chương 8 đến 18 xây dựng nền tảng điều khiển — Quiet Eye, ổn định tiền đình, fascia và cảm nhận bản thể, tensegrity, chu kỳ căng-rút, hình số 8, mặt phẳng 45 độ, xung phanh, rooting, và Jin — giúp việc thực thi CORE trở nên đáng tin cậy dưới áp lực. Chương 19 đến 25 áp dụng CORE cho từng loại pha bóng. Chương 26 đến 30 bao quát chiến thuật, tâm lý, thể lực, và thẻ tham chiếu thống nhất.

# Bin Packing Problem

## 1. Mô tả bài toán

*Bài toán Xếp thùng* (Bin Packing Problem - BPP) thuộc vấn đề tối ưu hóa tổ hợp và lớp NP khó. Bài toán này được mô tả như sau:

1. **Đầu vào:**
    - Một tập hợp các vật phẩm (item) $I = \{1, 2, ..., n\}$, mỗi vật phẩm $i$ có dạng hình hợp chữ nhật với kích thước $w_i \times l_i \times h_i$ (chiều rộng, chiều dài, chiều cao).
    - Một tập hợp các thùng chứa (bin/box) $B = \{1, 2, ..., m\}$, tất cả các thùng đều có cùng kích thước $W \times L \times H$.
2. **Yêu cầu:**
    - Xếp tất cả các vật phẩm vào các thùng sao cho:
        - Mỗi vật phẩm chỉ thuộc vào một thùng.
        - Các vật phẩm không được chồng lấn lên nhau.
        - Có thể xoay các vật phẩm theo 6 hướng (3 chiều) để xếp vào thùng.
        - Tổng kích thước của các vật phẩm trong mỗi thùng không vượt quá kích thước của thùng.
    - Mục tiêu: Tối thiểu hóa số lượng thùng sử dụng.
3. Ngoài ra, cấu hình của các vật phẩm trong thùng cũng có thể được yêu cầu theo một số hàm mục tiêu khác nhau, ví dụ:
    - **Tính ổn định vật lý** (stablity) của các vật phẩm: các vật phẩm được nâng đỡ bởi các vật phẩm khác hoặc đáy thùng để tránh bị rơi khi vận chuyển.
    - **Tính tiện dụng** (accessibility) khi sử dụng: các vật phẩm cần được xếp sao cho dễ dàng lấy ra theo yêu cầu sử dụng, hoặc thứ tự về độ ưu tiên.
    - **Tính linh hoạt** (flexibility) trong việc thêm/xóa vật phẩm: cấu hình xếp thùng cần dễ dàng thay đổi khi có thêm/xóa vật phẩm.
    - **Tính an toàn** (safety) khi vận chuyển: trong trường hợp các vật phẩm có khối lượng thì cần xếp sao cho trọng lượng của các vật phẩm không tập trung ở một phía thùng, hoặc vật phẩm quá nặng không được xếp ở trên vật phẩm nhẹ.
    - **Tính đồng đều** (uniformity) trong việc xếp thùng: các thùng cần chứa số lượng vật phẩm gần bằng nhau hoặc có tỷ lệ nhất định.
    - **Tính tổng quát** (generality) của cấu hình xếp thùng: cấu hình xếp thùng cần phù hợp với nhiều loại vật phẩm có hình dạng và kích thước khác nhau.
    - ...

## 2. Các phiên bản khác nhau của bài toán

- Theo số chiều của vật phẩm:
  - *1D BPP*: các vật phẩm và thùng là các đoạn thẳng.
  - *2D BPP*: các vật phẩm và thùng là các hình chữ nhật.
  - *3D BPP*: các vật phẩm và thùng là các hình hộp chữ nhật.
- Theo thông tin về các vật phẩm:
  - *Offline BPP*: tất cả thông tin về các vật phẩm đã biết trước khi xếp.
  - *Online BPP*: các vật phẩm được đưa vào xếp một cách tuần tự, thông tin về vật phẩm tiếp theo chỉ được biết sau khi vật phẩm ngay trước đó đã được xếp. Phù hợp với các bài toán thực tế khi các vật phẩm đến theo băng chuyền.
  - *Semionline BPP*: một số thông tin về các vật phẩm được biết trước, một số thông tin khác chỉ được biết khi vật phẩm đến.
- Theo trạng thái của vật phẩm:
  - *Static BPP*: các vật phẩm không thay đổi vị trí sau khi xếp.
  - *Dynamic BPP*: các vật phẩm có thể đến và rời đi theo thời gian.

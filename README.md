<p align="center">
  <img src="https://www.uit.edu.vn/sites/vi/files/banner_uit_0.png" title="avatar_UIT">
</p>


<h1 align="center">
  CS112 - PHÂN TÍCH VÀ THIẾT KẾ THUẬT TOÁN 
</h1>


<h1 align="center">
  TRAVELLING SALESMAN PROBLEM 
</h1>


# Member
| STT | Họ tên | MSSV | Vai trò | E-mail | Github |
| :---: | --- | --- | --- | --- | --- |
# Tóm tắt các giải thuật
## Bruteforce (Thuật toán tối ưu)
### Mã giả:
Với mảng chứa các tọa độ thành phố ban đầu, tạo ra tập hợp **S** chứa **n** hoán vị của mảng trên.

Với mối **S_i** (**i** thuộc 1,2,3,...n) ta tính khoảng cách Euclid của tất cả các điểm trong mảng và chọn ra **S_min** có khoảng cách ngắn nhất.

In ra kết quả ngắn nhất và trả về **S_min**
### Độ phức tạp:
Giả sử có **n** thành phố, ta cần tạo thành **n!** hoán vị -> độ phức tạp hàm permutation là **n!**

Một vòng lăp để duyệt tất cả các hoán vị trên **n!** -> độ phức tạp vòng lặp **n!**

=> **F(n) = n! + n!**

=> **O(n) = n!** hay độ phức tạp của thuật toán bruteforce cho bài toán là **n!**

## Christophides (Thuật toán xấp xỉ)
### Mã giả:
Tìm một cây bao trùm **T** nhỏ nhất của **G** (minimum spanning tree)

Tìm tập hợp **O** chứa các đỉnh có bậc lẻ trong cây **T**

Tìm một cặp ghép đầy đủ ([perfect matching](https://en.wikipedia.org/wiki/Perfect_matching)) **M** với các đỉnh trong **O** có trọng số nhỏ nhất

Hợp **M** và **T** tạo thành một đa đồ thị **H** mà mỗi đỉnh trong đó đều có bậc chẵn

Tìm một chu trình Euler trong **H** (**H** có chu trình Euler do tất cả các đỉnh đều liên thông và có bậc chẵn)

Biến đổi thành chu trình Hamilton bằng các bỏ qua các đỉnh lặp lại trên đường đi.

### Độ phức tạp
Giả sử có **n** thành phố:

Hàm xây dựng đồ thị: dùng 2 vòng lặp duyệt qua tất cả **n** thành phố -> độ phức tạp **n^2** -> **O(n) = n^2**

Hàm tìm cây bao trùm sử dụng thuật toán Kruskal có độ phức tạp **E*Log(V)**. Trong đó **E** là số cạnh và **V** là số đỉnh. Vì đồ thị của bài toán đang xét là một đồ thị đầy đủ vô hướng nên dễ dàng tính được **E = (V-1)/2 = (n-1)/2** -> độ phức tạp **((n-1)/2)Log(n)** -> **O(n) = nlog(n)**

Hàm tìm đỉnh bậc lẻ của cây bao trùm **T** dùng 2 vòng lặp: 1 vòng dùng đếm tần suất đỉnh xuất hiện trên cây bao trùm, 1 vòng duyệt tất cả đỉnh để chọn ra các đỉnh có tần suất xuất hiện là số lẻ -> Độ phức tạp **O(n) = n^2**

Hàm tìm minimum_perfect_matching có độ phức tạp 2m*m*log(m)*m*(m-1)*2m với m là số đỉnh bậc lẻ đã trong cây **T** -> **O(m) = (m^5)log(m)** < **(n^5)log(n)**

Hàm tìm chu trình Euler có độ phức tạp **O(E_H) = E_H^2 (E_H là số cạnh của đa đồ thị H)** < **n^2**

Nhìn chung độ phức tạp của thuật toán nhỏ hơn **(n^5)log(n)**

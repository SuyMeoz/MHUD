# LAB - 1 [ mã hóa caesar ]

### Một số hàm dùng và công dụng 

| Hàm | Công dụng |
| ----------- | ----------- |
| ord() | chuyển một ký tự đơn thành mã số nguyên Unicode tương ứng|
| chr() | ngược lại với hàm ord() chuyển mã số nguyên thành ký tự đơn tương ứng|

vd :
```
print(ord('A'))   # Kết quả: 65
print(ord('a'))   # Kết quả: 97
```

```
print(chr(65))    # Kết quả: 'A'
print(chr(ord('A')))  # Kết quả: 'A'
```

| Hàm | Công dụng |
| ----------- | ----------- |
| enumerate() | duyệt qua một đối tượng có thể lặp, đồng thời lấy cả chỉ số (index) và giá trị của từng phần tử trong vòng lặp|

vd:
```
names = ['Alice', 'Bob', 'Charlie']

for index, name in enumerate(names, start=0):
    print(index, name)
```
```
Ket qua
0 Alice
1 Bob
2 Charlie
```


### Một số modul dùng và công dụng 
import time
import threading
from tinydb import TinyDB, Query

# Khởi tạo TinyDB
db = TinyDB('todo.json')
todo_table = db.table('todos')
Task = Query()

def thong_ke_cong_viec_hoan_thanh():
    """Thực hiện tính toán thống kê công việc hoàn thành."""
    print("\n--- Bắt đầu tính toán thống kê (trong thread riêng)... ---") # Thông báo bắt đầu tính toán
    time.sleep(2) # Mô phỏng thời gian tính toán (có thể bỏ trong thực tế)

    tong_cong_viec = len(todo_table.all())
    cong_viec_da_hoan_thanh = len(todo_table.search(Task.hoan_thanh == True))
    cong_viec_chua_hoan_thanh = tong_cong_viec - cong_viec_da_hoan_thanh
    ty_le_hoan_thanh = (cong_viec_da_hoan_thanh / tong_cong_viec) * 100 if tong_cong_viec > 0 else 0

    thong_ke = {
        "tong_cong_viec": tong_cong_viec,
        "cong_viec_da_hoan_thanh": cong_viec_da_hoan_thanh,
        "cong_viec_chua_hoan_thanh": cong_viec_chua_hoan_thanh,
        "ty_le_hoan_thanh": ty_le_hoan_thanh
    }
    print("\n--- Hoàn thành tính toán thống kê. ---") # Thông báo hoàn thành
    return thong_ke

def hien_thi_thong_ke():
    """Hiển thị thống kê công việc hoàn thành (gọi hàm thống kê trong thread)."""
    def hien_thi_ket_qua_thong_ke(thong_ke_ket_qua):
        """Hàm con để hiển thị kết quả thống kê sau khi thread hoàn thành."""
        if thong_ke_ket_qua:
            print("\n--- Thống kê Công việc Hoàn thành ---")
            print(f"  Tổng số công việc: {thong_ke_ket_qua['tong_cong_viec']}")
            print(f"  Công việc đã hoàn thành: {thong_ke_ket_qua['cong_viec_da_hoan_thanh']}")
            print(f"  Công việc chưa hoàn thành: {thong_ke_ket_qua['cong_viec_chua_hoan_thanh']}")
            print(f"  Tỷ lệ hoàn thành: {thong_ke_ket_qua['ty_le_hoan_thanh']:.2f}%") # Định dạng phần trăm
        else:
            print("Không thể lấy được thống kê.")

    def worker_thong_ke():
        """Worker function chạy trong thread để thực hiện thống kê."""
        ket_qua = thong_ke_cong_viec_hoan_thanh() # Gọi hàm tính toán thống kê
        hien_thi_ket_qua_thong_ke(ket_qua) # Hiển thị kết quả sau khi tính toán xong

    thong_ke_thread = threading.Thread(target=worker_thong_ke) # Tạo thread cho việc thống kê
    thong_ke_thread.start() # Bắt đầu thread thống kê chạy song song
    print("\nĐang tính toán thống kê công việc... Vui lòng chờ trong giây lát.") # Thông báo cho người dùng biết đang xử lý


def them_cong_viec():
    """Thêm một công việc mới vào danh sách."""
    noi_dung = input("Nhập nội dung công việc: ")
    if noi_dung:
        todo_table.insert({'noi_dung': noi_dung, 'hoan_thanh': False})
        print("Công việc đã được thêm!")
    else:
        print("Nội dung công việc không được để trống.")

def danh_sach_cong_viec():
    """Liệt kê tất cả công việc trong danh sách."""
    tat_ca_cong_viec = todo_table.all()
    if tat_ca_cong_viec:
        print("\n--- Danh sách công việc ---")
        for cong_viec in tat_ca_cong_viec:
            trang_thai = "[x]" if cong_viec['hoan_thanh'] else "[ ]"
            print(f"{cong_viec.doc_id}. {trang_thai} {cong_viec['noi_dung']}")
    else:
        print("Danh sách công việc trống.")

def danh_sach_cong_viec_chua_hoan_thanh():
    """Liệt kê các công việc chưa hoàn thành."""
    cong_viec_chua_hoan_thanh = todo_table.search(Task.hoan_thanh == False)
    if cong_viec_chua_hoan_thanh:
        print("\n--- Công việc chưa hoàn thành ---")
        for cong_viec in cong_viec_chua_hoan_thanh:
            print(f"{cong_viec.doc_id}. [ ] {cong_viec['noi_dung']}")
    else:
        print("Không có công việc nào chưa hoàn thành.")

def danh_sach_cong_viec_da_hoan_thanh():
    """Liệt kê các công việc đã hoàn thành."""
    cong_viec_da_hoan_thanh = todo_table.search(Task.hoan_thanh == True)
    if cong_viec_da_hoan_thanh:
        print("\n--- Công việc đã hoàn thành ---")
        for cong_viec in cong_viec_da_hoan_thanh:
            print(f"{cong_viec.doc_id}. [x] {cong_viec['noi_dung']}")
    else:
        print("Không có công việc nào đã hoàn thành.")

def danh_dau_hoan_thanh():
    """Đánh dấu một công việc là đã hoàn thành."""
    try:
        cong_viec_id = int(input("Nhập ID công việc muốn đánh dấu hoàn thành: "))
        cong_viec = todo_table.get(doc_id=cong_viec_id)
        if cong_viec:
            todo_table.update({'hoan_thanh': True}, doc_ids=[cong_viec_id])
            print(f"Công việc ID {cong_viec_id} đã được đánh dấu là hoàn thành!")
        else:
            print(f"Không tìm thấy công việc với ID {cong_viec_id}.")
    except ValueError:
        print("ID công việc phải là một số nguyên.")

def xoa_cong_viec():
    """Xóa một công việc khỏi danh sách."""
    try:
        cong_viec_id = int(input("Nhập ID công việc muốn xóa: "))
        cong_viec = todo_table.get(doc_id=cong_viec_id)
        if cong_viec:
            todo_table.remove(doc_ids=[cong_viec_id])
            print(f"Công việc ID {cong_viec_id} đã được xóa!")
        else:
            print(f"Không tìm thấy công việc với ID {cong_viec_id}.")
    except ValueError:
        print("ID công việc phải là một số nguyên.")


def hien_thi_menu():
    """Hiển thị menu chức năng cho người dùng."""
    print("\n--- Menu ---")
    print("1. Thêm công việc")
    print("2. Xem danh sách công việc")
    print("3. Xem công việc chưa hoàn thành")
    print("4. Xem công việc đã hoàn thành")
    print("5. Đánh dấu công việc hoàn thành")
    print("6. Xóa công việc")
    print("7. Xem thống kê công việc") # Lựa chọn Xem thống kê
    print("8. Thoát")


def main():
    """Hàm chính điều khiển ứng dụng."""
    while True:
        hien_thi_menu()
        lua_chon = input("Chọn chức năng (1-8): ") # Menu chính chỉ còn 8 lựa chọn

        if lua_chon == '7':
            hien_thi_thong_ke() # Gọi hàm hiển thị thống kê (chạy trong thread)
        elif lua_chon == '8':
            print("Thoát ứng dụng. Hẹn gặp lại!")
            break
        elif lua_chon == '1':
            them_cong_viec()
        elif lua_chon == '2':
            danh_sach_cong_viec()
        elif lua_chon == '3':
            danh_sach_cong_viec_chua_hoan_thanh()
        elif lua_chon == '4':
            danh_sach_cong_viec_da_hoan_thanh()
        elif lua_chon == '5':
            danh_dau_hoan_thanh()
        elif lua_chon == '6':
            xoa_cong_viec()
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")


if __name__ == "__main__":
    main()
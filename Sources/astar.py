import time
from queue import PriorityQueue

import support_function as spf


def AStart_Search(board, list_check_point):
    start_time = time.time()
    if spf.check_win(board, list_check_point):
        print("Found win")
        return [board]
        #Kiểm tra xem trạng thái hiện tại của bảng đã là trạng thái thắng chưa.
        # Nếu đúng, in thông báo "Found win" và trả về bảng hiện tại.
    start_state = spf.state(board, None, list_check_point) #Tạo trạng thái bắt đầu từ bảng hiện tại.
    list_state = set()  # Dùng set để kiểm tra tồn tại nhanh hơn
    #Khởi tạo hàng đợi ưu tiên heuristic_queue để lưu trữ các trạng thái cần duyệt,
    # dựa trên giá trị heuristic (ước lượng chi phí tới đích).
    heuristic_queue = PriorityQueue()
    heuristic_queue.put(start_state)
    while not heuristic_queue.empty():
        #Vòng lặp tiếp tục duyệt các trạng thái trong hàng đợi ưu tiên
        # heuristic_queue cho đến khi hàng đợi rỗng.
        now_state = heuristic_queue.get()
        #Lấy trạng thái hiện tại now_state từ hàng đợi ưu tiên.
        cur_pos = spf.find_position_player(now_state.board)
        #Tìm vị trí hiện tại của người chơi trong bảng now_state.
        list_can_move = spf.get_next_pos(now_state.board, cur_pos)
        #Tìm các vị trí có thể đi đến từ vị trí hiện tại của người chơi.

        for next_pos in list_can_move:
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)
            # Tạo bảng mới new_board bằng cách di chuyển từ vị trí hiện tại cur_pos tới vị trí kế tiếp next_pos.
            # Kết hợp kiểm tra tồn tại và không thể thắng vào một điều kiện
            if (tuple(map(tuple, new_board)) in list_state or
                    spf.is_board_can_not_win(new_board, list_check_point) or
                    spf.is_all_boxes_stuck(new_board, list_check_point)):
                continue
            #Kiểm tra nếu bảng mới đã tồn tại trong list_state, hoặc bảng mới không thể thắng,
            # hoặc tất cả các hộp đều bị kẹt.
            # Nếu đúng, bỏ qua bảng này và chuyển sang vị trí kế tiếp trong vòng lặp.
            new_state = spf.state(new_board, now_state, list_check_point)
            #Tạo trạng thái mới new_state từ bảng mới new_board.
            if spf.check_win(new_board, list_check_point):
                print("Found win")
                print(f"số trạng thái đã duyệt {len(list_state)}")
                return (new_state.get_line(), len(list_state))
                #Kiểm tra nếu trạng thái mới new_state là trạng thái thắng.
                # Nếu đúng, in thông báo "Found win" và trả về đường đi tới đích cùng với số lượng trạng thái đã duyệt.
            list_state.add(tuple(map(tuple, new_board)))
            # Lưu trữ trạng thái bảng dưới dạng tuple bất biến
            heuristic_queue.put(new_state)
            #Thêm trạng thái mới new_state vào hàng đợi ưu tiên heuristic_queue.

        if time.time() - start_time > spf.TIME_OUT:
            print("Timeout")
            return []
        #Kiểm tra nếu thời gian thực hiện thuật toán đã vượt quá giới hạn spf.TIME_OUT.
        # Nếu đúng, in thông báo "Timeout" và trả về danh sách rỗng.
    print("Not Found")
    return []

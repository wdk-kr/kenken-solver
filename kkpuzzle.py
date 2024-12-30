def kenken_solver(given_grid, cages):
    N = len(given_grid) 

    def row_valid(grid, row, num):
        return num not in grid[row]

    def col_valid(grid, col, num):
        for r in range(N):
            if grid[r][col] == num:
                return False
        return True

    def cage_valid(grid, cages, row, col, num):
        # (row, col)
        cage_info = None
        for c in cages:
            if (row, col) in c[0]:
                cage_info = c
                break
        if cage_info is None:
            return False  # 케이지에 속하지 않으면 에러
        
        cells, operation, target = cage_info

        values = []
        for (r, c) in cells:
            if r == row and c == col:
                values.append(num)
            else:
                values.append(grid[r][c])

        # 아직 비어있는 칸(0)이 있으면, 일단 제약만 통과하면 OK
        if any(v == 0 for v in values):
            return True

        # 다 채워졌으면 연산 검사
        if operation == '+':
            return sum(values) == target
        elif operation == '-':
            # 2칸 전제
            return abs(values[0] - values[1]) == target
        elif operation == '*':
            prod = 1
            for v in values:
                prod *= v
            return prod == target
        elif operation == '/':
            # 2칸 전제
            bigger = max(values)
            smaller = min(values)
            return (smaller != 0) and (bigger / smaller == target)
        elif operation is None:
            # 1칸짜리 케이지
            return values[0] == target
        else:
            return False

    def backtrack(grid, row=0, col=0):
        if row == N:
            return True

        next_col = (col + 1) % N
        next_row = row + 1 if col == N-1 else row

        if grid[row][col] != 0:
            return backtrack(grid, next_row, next_col)

        for num in range(1, N+1):
            if row_valid(grid, row, num) and col_valid(grid, col, num) and cage_valid(grid, cages, row, col, num):
                grid[row][col] = num
                if backtrack(grid, next_row, next_col):
                    return True
                grid[row][col] = 0
        return False

    if backtrack(given_grid):
        print("KenKen 퍼즐 풀이 성공! 결과:")
        for row_data in given_grid:
            print(row_data)
    else:
        print("KenKen 퍼즐을 풀 수 없습니다.")


if __name__ == "__main__":
    # 격자 정의, 사전 정의된 수가 있으면 그 수를 채워넣기
    test_grid = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]

    # 모든 칸을 전부 채워야 함!!
    test_cages = [
    ([(0, 0), (1, 0), (0, 1), (1, 1), (2, 1)], "+", 12),   
    ([(0, 2), (0, 3), (0, 4)], "+", 12),
    ([(2, 0), (3, 0)], "-", 1),
    ([(3, 1), (3, 2), (4, 2)], "*", 60),
    ([(1, 2), (2, 2)], "/", 2),
    ([(1, 3), (2, 3), (3, 3)], "*", 15),
    ([(1, 4), (2, 4), (3, 4)], "+", 8),
    ([(4, 3), (4, 4)], "-", 2),
    ([(4, 0), (4, 1)], "*", 5),
    ]

    kenken_solver(test_grid, test_cages)
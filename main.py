# import tkinter as tk
# from tkinter import messagebox
# from collections import deque
# import copy

# class Item:
#     def __init__(self, hue):
#         self.hue = hue  # "red", "blue", "gray"
#         self.position = None

#     def __str__(self):
#         return self.hue[0].upper()

# class Cell:
#     def __init__(self, item, target):
#         self.item = item  # عنصر المغناطيس أو None
#         self.target = target  # هدف إذا كانت الخلية هدفا
#         self.position = None

#     def __str__(self):
#         return "G" if self.target == "goal" else ""

# # تعريف الرقع المتاحة
# grids = {
#     (5, 5): [
#         [
#             [Cell(None, None), Cell(None, None), Cell(None, 'goal'), Cell(None, None), Cell(None, None)],
#             [Cell(None, None), Cell(None, None), Cell(Item('gray'), None), Cell(None, None), Cell(None, None)],
#             [Cell(None, 'goal'), Cell(Item('gray'), None), Cell(None, 'goal'), Cell(Item('gray'), None), Cell(None, 'goal')],
#             [Cell(None, None), Cell(None, None), Cell(Item('gray'), None), Cell(None, None), Cell(None, None)],
#             [Cell(Item('red'), None), Cell(None, None), Cell(None, 'goal'), Cell(None, None), Cell(Item('blue'), None)]
#         ]
#     ]
# }

# class GameBoard:
#     def __init__(self, grid_layout):
#         self.grid = grid_layout
#         self.size = len(grid_layout)
#         self.num_cols = len(grid_layout[0]) if self.size > 0 else 0

#     def swap_item(self, x1, y1, item, new_x, new_y):
#         self.grid[x1][y1].item = None
#         self.grid[new_x][new_y].item = item
#         if item:
#             item.position = (new_x, new_y)

#     def swap_auto_item(self, x1, y1, item, new_x, new_y):
#         self.grid[x1][y1].item = None
#         self.grid[new_x][new_y].item = item
#         if item:
#             item.position = (new_x, new_y)

#     def is_completed(self):
#         for i in range(self.size):
#             for j in range(self.num_cols):
#                 cell = self.grid[i][j]
#                 if cell.target == "goal":
#                     if not cell.item or cell.item.hue not in ['gray', 'red', 'blue']:
#                         return False
#         return True

#     def get_magnetic_positions(self):
#         positions = []
#         for i in range(self.size):
#             for j in range(self.num_cols):
#                 cell = self.grid[i][j]
#                 if cell.item and cell.item.hue in ['red', 'blue']:
#                     positions.append((i, j, cell.item.hue))
#         return positions

# class MagneticGameGUI:
#     def __init__(self, root, grid_layout):
#         self.root = root
#         self.root.title("Magnetic Item Game")
#         self.board = GameBoard(grid_layout)
#         self.steps_remaining = 3
#         self.selected_item = None
#         self.selected_item_x = None
#         self.selected_item_y = None
#         self.create_board_ui()
        
#     def create_board_ui(self):
#         self.canvas = tk.Canvas(self.root, width=500, height=500, bg="white")
#         self.canvas.grid(row=0, column=0)
        
#         # عرض عدد الخطوات المتبقية
#         self.steps_label = tk.Label(self.root, text=f"Remaining steps: {self.steps_remaining}", font=("Arial", 14))
#         self.steps_label.grid(row=1, column=0)
        
#         self.update_board_ui()
#         self.canvas.bind("<Button-1>", self.select_item)
        
#         # زر لحل اللعبة تلقائيًا
#         solve_button = tk.Button(self.root, text="حل تلقائي", command=self.solve_game)
#         solve_button.grid(row=2, column=0)

#     def update_board_ui(self):
#         self.canvas.delete("all")
#         for i in range(self.board.size):
#             for j in range(self.board.num_cols):
#                 cell = self.board.grid[i][j]
#                 x1, y1, x2, y2 = j * 100, i * 100, (j + 1) * 100, (i + 1) * 100
#                 color = "yellow" if cell.target == "goal" else "white"
#                 self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                
#                 if cell.item:
#                     item_color = {
#                         "red": "red",
#                         "blue": "blue",
#                         "gray": "gray"
#                     }[cell.item.hue]
#                     self.canvas.create_oval(x1 + 15, y1 + 15, x2 - 15, y2 - 15, fill=item_color)

#     def select_item(self, event):
#         x, y = event.x // 100, event.y // 100
#         cell = self.board.grid[y][x]
#         if isinstance(cell.item, Item):
#             if cell.item.hue == "gray":
#                 messagebox.showwarning("تحذير", "يرجى اختيار عنصر مغناطيسي للتحريك.")
#             else:
#                 self.selected_item = cell.item
#                 self.selected_item_x = y
#                 self.selected_item_y = x
#         elif self.selected_item:
#             self.move_selected_item(self.selected_item_x, self.selected_item_y, y, x)

#     def move_selected_item(self, x1, y1, x2, y2):
#         if self.selected_item:
#             self.board.swap_item(x1, y1, self.selected_item, x2, y2)
#             self.steps_remaining -= 1  # تقليل عدد الخطوات
#             self.steps_label.config(text=f"Remaining steps: {self.steps_remaining}")
#             self.update_board_ui()
            
#             if self.board.is_completed():
#                 messagebox.showinfo("تهانينا!", "Conguration")
#                 self.root.quit()
#             elif self.steps_remaining == 0:
#                 messagebox.showinfo("you lose, game is finished")
#                 self.root.quit()
                
#             self.selected_item = None

#     def bfs_solve(self):
#         initial_positions = self.board.get_magnetic_positions()
#         queue = deque([(copy.deepcopy(self.board), 0)])  # كل حالة تحتوي على نسخة من اللوحة وعدد الخطوات
#         visited = set()

#         while queue:
#             current_board, steps = queue.popleft()
#             board_state = str([[str(cell.item) for cell in row] for row in current_board.grid])
            
#             if board_state in visited:
#                 continue
#             visited.add(board_state)

#             if current_board.is_completed():
#                 print(f"تم العثور على الحل! عدد الخطوات: {steps}")
#                 return steps

#             for x, y, hue in initial_positions:
#                 for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # الحركات الممكنة
#                     new_x, new_y = x + dx, y + dy
#                     if 0 <= new_x < current_board.size and 0 <= new_y < current_board.num_cols:
#                         if not current_board.grid[new_x][new_y].item:
#                             new_board = copy.deepcopy(current_board)
#                             item = new_board.grid[x][y].item
#                             if item:  # التأكد من أن العنصر ليس None
#                                 new_board.swap_item(x, y, item, new_x, new_y)
#                                 queue.append((new_board, steps + 1))

#         print("لم يتم العثور على حل.")
#         return -1  # إذا لم يتم العثور على الحل

#     def solve_game(self):
#         steps = self.bfs_solve()
#         if steps != -1:
#             messagebox.showinfo("نجاح", f"تم حل اللعبة تلقائيًا في {steps} خطوة!")
#         else:
#             messagebox.showwarning("فشل", "لم يتم العثور على حل.")

# # إدخال عدد الصفوف والأعمدة من المستخدم
# try:
#     num_rows = int(input("enter your rows: "))
#     num_cols = int(input("enter your columns: "))
# except ValueError:
#     print("please enter an integer number.")
#     exit()

# # التحقق من وجود رقع متوافقة
# available_grids = grids.get((num_rows, num_cols), [])
# if not available_grids:
#     print("لا توجد رقعة متوافقة مع الأبعاد المدخلة.")
#     exit()

# # اختيار الرقعة إذا كان هناك أكثر من واحدة
# if len(available_grids) > 1:
#     print("please enter number of grid:")
#     for i, grid in enumerate(available_grids, start=1):
#         print(f"grid {i}")
#     grid_index = int(input("enter number of your grid: ")) - 1
# else:
#     grid_index = 0

# selected_grid = available_grids[grid_index]

# # تشغيل اللعبة
# root = tk.Tk()
# game = MagneticGameGUI(root, selected_grid)
# root.mainloop()


















































# import tkinter as tk
# from tkinter import messagebox
# from queue import Queue

# class Item:
#     def __init__(self, hue):
#         self.hue = hue  # "red", "blue", "gray"
#         self.position = None

#     def __str__(self):
#         return self.hue[0].upper()

# class Cell:
#     def __init__(self, item, target):
#         self.item = item  # عنصر المغناطيس أو None
#         self.target = target  # هدف إذا كانت الخلية هدفا
#         self.position = None

#     def __str__(self):
#         return "G" if self.target == "goal" else ""

# # تعريف الرقع المتاحة
# grids = {
#     (5, 5): [
#         [
#             [Cell(None, None), Cell(None, None), Cell(None, 'goal'), Cell(None, None), Cell(None, None)],
#             [Cell(None, None), Cell(None, None), Cell(Item('gray'), None), Cell(None, None), Cell(None, None)],
#             [Cell(None, 'goal'), Cell(Item('gray'), None), Cell(None, 'goal'), Cell(Item('gray'), None), Cell(None, 'goal')],
#             [Cell(None, None), Cell(None, None), Cell(Item('gray'), None), Cell(None, None), Cell(None, None)],
#             [Cell(Item('red'), None), Cell(None, None), Cell(None, 'goal'), Cell(None, None), Cell(Item('blue'), None)]
#         ],
#         [
#             [Cell(None, None), Cell(Item('red'), None), Cell(None, None), Cell(None, 'goal'), Cell(None, None)],
#             [Cell(Item('gray'), None), Cell(None, None), Cell(None, None), Cell(None, None), Cell(None, None)],
#             [Cell(None, 'goal'), Cell(None, None), Cell(Item('gray'), None), Cell(None, None), Cell(None, None)],
#             [Cell(None, None), Cell(None, None), Cell(None, None), Cell(Item('gray'), None), Cell(None, None)],
#             [Cell(None, None), Cell(None, None), Cell(Item('blue'), None), Cell(None, 'goal'), Cell(None, None)]
#         ]
#     ],
#     (3, 2): [
#         [
#             [Cell(Item('blue'), None),  Cell(None, 'goal')],
#             [Cell(None, None), Cell(Item('gray'), None)],
#             [Cell(None, None), Cell(None, 'goal')]
#         ]
#     ]
# }

# class GameBoard:
#     def __init__(self, grid_layout):
#         self.grid = grid_layout
#         self.size = len(grid_layout)
#         self.num_cols = len(grid_layout[0]) if self.size > 0 else 0

#     def swap_item(self, x1, y1, item, new_x, new_y):
#         self.grid[x1][y1].item = None
#         self.grid[new_x][new_y].item = item
#         item.position = (new_x, new_y)

#         # حركة المغناطيس الأحمر
#         if item.hue == 'red':
#             for j in range(self.num_cols):
#                 if j != new_y:
#                     cell = self.grid[new_x][j]
#                     if cell and isinstance(cell.item, Item) and cell.item.hue == 'gray':
#                         if j < new_y and not self.grid[new_x][j + 1].item:
#                             self.swap_auto_item(new_x, j, cell.item, new_x, j + 1)
#                         elif j > new_y and not self.grid[new_x][j - 1].item:
#                             self.swap_auto_item(new_x, j, cell.item, new_x, j - 1)

#             for i in range(self.size):
#                 if i != new_x:
#                     cell = self.grid[i][new_y]
#                     if cell and isinstance(cell.item, Item) and cell.item.hue == 'gray':
#                         if i < new_x and not self.grid[i + 1][new_y].item:
#                             self.swap_auto_item(i, new_y, cell.item, i + 1, new_y)
#                         elif i > new_x and not self.grid[i - 1][new_y].item:
#                             self.swap_auto_item(i, new_y, cell.item, i - 1, new_y)

#         elif item.hue == 'blue':
#             for i in range(self.size):
#                 cell = self.grid[i][new_y]
#                 if cell and isinstance(cell.item, Item):
#                     if i > new_x and i < self.size - 1 and not self.grid[i + 1][new_y].item:
#                         self.swap_auto_item(i, new_y, cell.item, i + 1, new_y)
#                     elif i < new_x and i > 0 and not self.grid[i - 1][new_y].item:
#                         self.swap_auto_item(i, new_y, cell.item, i - 1, new_y)
#             for j in range(self.num_cols):
#                 cell = self.grid[new_x][j]
#                 if cell and isinstance(cell.item, Item):
#                     if j > new_y and j < self.num_cols - 1 and not self.grid[new_x][j + 1].item:
#                         self.swap_auto_item(new_x, j, cell.item, new_x, j + 1)
#                     elif j < new_y and j > 0 and not self.grid[new_x][j - 1].item:
#                         self.swap_auto_item(new_x, j, cell.item, new_x, j - 1)

#     def swap_auto_item(self, x1, y1, item, new_x, new_y):
#         self.grid[x1][y1].item = None
#         self.grid[new_x][new_y].item = item
#         item.position = (new_x, new_y)

#     def is_completed(self):
#         red_or_blue_found = False
#         for i in range(self.size):
#             for j in range(self.num_cols):
#                 cell = self.grid[i][j]
#                 if cell.target == "goal":
#                     if not cell.item:
#                         return False
#                     elif cell.item.hue == 'gray':
#                         continue
#                     elif cell.item.hue in ('red', 'blue'):
#                         red_or_blue_found = True
#                     else:
#                         return False
#         return red_or_blue_found

#     def bfs_solve(self):
#         """تقوم بالبحث عن حل تلقائي باستخدام خوارزمية BFS."""
#         initial_state = (self.grid, self.steps_remaining)
#         queue = Queue()
#         queue.put((initial_state, []))  # حالة البداية وخطوات المسار
#         visited = set()

#         while not queue.empty():
#             (current_grid, remaining_steps), path = queue.get()

#             # تحقق إذا تم الوصول للحل
#             if self.is_completed():
#                 return path  # مسار الحل للوصول للهدف

#             # إيقاف البحث إذا كانت الخطوات المتبقية صفر
#             if remaining_steps <= 0:
#                 continue

#             # حفظ حالة الشبكة الحالية
#             visited.add(tuple(map(tuple, current_grid)))

#             # جرب كل التحركات الممكنة لكل عنصر مغناطيسي
#             for i in range(self.size):
#                 for j in range(self.num_cols):
#                     cell = current_grid[i][j]
#                     if cell.item and cell.item.hue in ("red", "blue"):
#                         # جرب التحركات المتاحة
#                         for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
#                             new_x, new_y = i + dx, j + dy
#                             if 0 <= new_x < self.size and 0 <= new_y < self.num_cols and not current_grid[new_x][new_y].item:
#                                 new_grid = [row[:] for row in current_grid]  # نسخ الشبكة
#                                 new_grid[new_x][new_y].item = cell.item  # نقل العنصر
#                                 new_grid[i][j].item = None  # إزالة العنصر من الموقع القديم
#                                 new_state = (new_grid, remaining_steps - 1)

#                                 if tuple(map(tuple, new_grid)) not in visited:
#                                     queue.put((new_state, path + [(i, j, new_x, new_y)]))

#         return None  # إذا لم يتم العثور على حل

# class MagneticGameGUI:
#     def __init__(self, root, grid_layout):
#         self.root = root
#         self.root.title("Magnetic Item Game")
#         self.board = GameBoard(grid_layout)
#         self.steps_remaining = 3  # عدد الخطوات المسموحة
#         self.selected_item = None
#         self.selected_item_x = None
#         self.selected_item_y = None
#         self.create_board_ui()

#     def create_board_ui(self):
#         self.canvas = tk.Canvas(self.root, width=500, height=500, bg="white")
#         self.canvas.grid(row=0, column=0)
        
#         # عرض عدد الخطوات المتبقية
#         self.steps_label = tk.Label(self.root, text=f"remaning steps: {self.steps_remaining}", font=("Arial", 14))
#         self.steps_label.grid(row=1, column=0)
        
#         self.update_board_ui()
#         self.canvas.bind("<Button-1>", self.select_item)

#     def select_item(self, event):
#         x, y = event.x // 100, event.y // 100
#         cell = self.board.grid[y][x]
#         if isinstance(cell.item, Item):
#             if cell.item.hue == "gray":
#                 messagebox.showwarning("تحذير", "لا يمكنك اختيار العناصر الرمادية.")
#             else:
#                 self.selected_item = cell.item
#                 self.selected_item_x = y
#                 self.selected_item_y = x
#         elif self.selected_item:
#             self.board.swap_item(self.selected_item_x, self.selected_item_y, self.selected_item, y, x)
#             self.steps_remaining -= 1
#             self.steps_label.config(text=f"remaining steps: {self.steps_remaining}")
#             self.selected_item = None
#             self.update_board_ui()
#             if self.board.is_completed():
#                 messagebox.showinfo("تهانينا!", "لقد انتهيت من اللعبة!")
#                 self.root.quit()
#             elif self.steps_remaining <= 0:
#                 messagebox.showinfo("انتهت اللعبة", "لم تقم بحل اللعبة في الوقت المحدد!")
#                 self.root.quit()

#     def update_board_ui(self):
#         self.canvas.delete("all")
#         for i in range(self.board.size):
#             for j in range(self.board.num_cols):
#                 cell = self.board.grid[i][j]
#                 color = "white"
#                 if cell.target == "goal":
#                     color = "yellow"
#                 self.canvas.create_rectangle(j*100, i*100, (j+1)*100, (i+1)*100, fill=color)
#                 if cell.item:
#                     item_color = "gray" if cell.item.hue == "gray" else cell.item.hue
#                     self.canvas.create_oval(j*100+25, i*100+25, (j+1)*100-25, (i+1)*100-25, fill=item_color)

#     def auto_solve(self):
#         """تطبيق حل BFS تلقائيًا وعرض الحل"""
#         solution_path = self.board.bfs_solve()
#         if solution_path is None:
#             messagebox.showinfo("نتيجة", "لم يتم العثور على حل.")
#         else:
#             for (x1, y1, x2, y2) in solution_path:
#                 self.board.swap_item(x1, y1, self.board.grid[x1][y1].item, x2, y2)
#                 self.update_board_ui()
#                 self.root.update()  # لتحديث الشاشة تلقائيًا بعد كل خطوة

# # تعديل تشغيل اللعبة بحيث يطلب من المستخدم اختيار نمط اللعب

# # إدخال عدد الصفوف والأعمدة من المستخدم
# try:
#     num_rows = int(input("Enter your rows: "))
#     num_cols = int(input("Enter your columns: "))
# except ValueError:
#     print("Please enter an integer number.")
#     exit()

# # التحقق من وجود رقع متوافقة
# available_grids = grids.get((num_rows, num_cols), [])
# if not available_grids:
#     print("No grid available with the entered dimensions.")
#     exit()

# # إذا كان هناك أكثر من رقعة، نطلب من المستخدم اختيار واحدة
# if len(available_grids) > 1:
#     print("Please select a grid:")
#     for i, grid in enumerate(available_grids, start=1):
#         print(f"Grid {i}")
#     grid_index = int(input("Enter the grid number: ")) - 1
# else:
#     grid_index = 0

# selected_grid = available_grids[grid_index]

# # طلب نمط التشغيل من المستخدم
# mode = input("Select mode: (1) Manual, (2) Automatic BFS: ")

# # تشغيل اللعبة
# root = tk.Tk()
# game = MagneticGameGUI(root, selected_grid)

# if mode == '2':
#     game.auto_solve()  # تنفيذ الحل التلقائي باستخدام BFS
# else:
#     root.mainloop()  # تشغيل الوضع اليدوي كما هو في الكود الأصلي
































































# import tkinter as tk
# from tkinter import messagebox
# from queue import Queue

# class Item:
#     def __init__(self, hue):
#         self.hue = hue  # "red", "blue", "gray"
#         self.position = None

#     def __str__(self):
#         return self.hue[0].upper()

# class Cell:
#     def __init__(self, item, target):
#         self.item = item  # عنصر المغناطيس أو None
#         self.target = target  # هدف إذا كانت الخلية هدفا
#         self.position = None

#     def __str__(self):
#         return "G" if self.target == "goal" else ""

# # تعريف الرقع المتاحة
# grids = {
#     (5, 5): [
#         [
#             [Cell(None, None), Cell(None, None), Cell(None, 'goal'), Cell(None, None), Cell(None, None)],
#             [Cell(None, None), Cell(None, None), Cell(Item('gray'), None), Cell(None, None), Cell(None, None)],
#             [Cell(None, 'goal'), Cell(Item('gray'), None), Cell(None, 'goal'), Cell(Item('gray'), None), Cell(None, 'goal')],
#             [Cell(None, None), Cell(None, None), Cell(Item('gray'), None), Cell(None, None), Cell(None, None)],
#             [Cell(Item('red'), None), Cell(None, None), Cell(None, 'goal'), Cell(None, None), Cell(Item('blue'), None)]
#         ],
#         [
#             [Cell(None, None), Cell(Item('red'), None), Cell(None, None), Cell(None, 'goal'), Cell(None, None)],
#             [Cell(Item('gray'), None), Cell(None, None), Cell(None, None), Cell(None, None), Cell(None, None)],
#             [Cell(None, 'goal'), Cell(None, None), Cell(Item('gray'), None), Cell(None, None), Cell(None, None)],
#             [Cell(None, None), Cell(None, None), Cell(None, None), Cell(Item('gray'), None), Cell(None, None)],
#             [Cell(None, None), Cell(None, None), Cell(Item('blue'), None), Cell(None, 'goal'), Cell(None, None)]
#         ]
#     ],
#     (3, 2): [
#         [
#             [Cell(Item('blue'), None),  Cell(None, 'goal')],
#             [Cell(None, None), Cell(Item('gray'), None)],
#             [Cell(None, None), Cell(None, 'goal')]
#         ]
#     ]
# }

# class GameBoard:
#     def __init__(self, grid_layout):
#         self.grid = grid_layout
#         self.size = len(grid_layout)
#         self.num_cols = len(grid_layout[0]) if self.size > 0 else 0

#     def swap_item(self, x1, y1, item, new_x, new_y):
#         self.grid[x1][y1].item = None
#         self.grid[new_x][new_y].item = item
#         item.position = (new_x, new_y)

#         # حركة المغناطيس الأحمر
#         if item.hue == 'red':
#             for j in range(self.num_cols):
#                 if j != new_y:
#                     cell = self.grid[new_x][j]
#                     if cell and isinstance(cell.item, Item) and cell.item.hue == 'gray':
#                         if j < new_y and not self.grid[new_x][j + 1].item:
#                             self.swap_auto_item(new_x, j, cell.item, new_x, j + 1)
#                         elif j > new_y and not self.grid[new_x][j - 1].item:
#                             self.swap_auto_item(new_x, j, cell.item, new_x, j - 1)

#             for i in range(self.size):
#                 if i != new_x:
#                     cell = self.grid[i][new_y]
#                     if cell and isinstance(cell.item, Item) and cell.item.hue == 'gray':
#                         if i < new_x and not self.grid[i + 1][new_y].item:
#                             self.swap_auto_item(i, new_y, cell.item, i + 1, new_y)
#                         elif i > new_x and not self.grid[i - 1][new_y].item:
#                             self.swap_auto_item(i, new_y, cell.item, i - 1, new_y)

#         elif item.hue == 'blue':
#             for i in range(self.size):
#                 cell = self.grid[i][new_y]
#                 if cell and isinstance(cell.item, Item):
#                     if i > new_x and i < self.size - 1 and not self.grid[i + 1][new_y].item:
#                         self.swap_auto_item(i, new_y, cell.item, i + 1, new_y)
#                     elif i < new_x and i > 0 and not self.grid[i - 1][new_y].item:
#                         self.swap_auto_item(i, new_y, cell.item, i - 1, new_y)
#             for j in range(self.num_cols):
#                 cell = self.grid[new_x][j]
#                 if cell and isinstance(cell.item, Item):
#                     if j > new_y and j < self.num_cols - 1 and not self.grid[new_x][j + 1].item:
#                         self.swap_auto_item(new_x, j, cell.item, new_x, j + 1)
#                     elif j < new_y and j > 0 and not self.grid[new_x][j - 1].item:
#                         self.swap_auto_item(new_x, j, cell.item, new_x, j - 1)

#     def swap_auto_item(self, x1, y1, item, new_x, new_y):
#         self.grid[x1][y1].item = None
#         self.grid[new_x][new_y].item = item
#         item.position = (new_x, new_y)

#     def is_completed(self):
#         red_or_blue_found = False
#         for i in range(self.size):
#             for j in range(self.num_cols):
#                 cell = self.grid[i][j]
#                 if cell.target == "goal":
#                     if not cell.item:
#                         return False
#                     elif cell.item.hue == 'gray':
#                         continue
#                     elif cell.item.hue in ('red', 'blue'):
#                         red_or_blue_found = True
#                     else:
#                         return False
#         return red_or_blue_found

#     def bfs_solve(self):
#         """تقوم بالبحث عن حل تلقائي باستخدام خوارزمية BFS بدون حد للخطوات."""
#         initial_state = self.grid
#         queue = Queue()
#         queue.put((initial_state, []))  # حالة البداية وخطوات المسار
#         visited = set()

#         while not queue.empty():
#             current_grid, path = queue.get()

#             # تحقق إذا تم الوصول للحل
#             if self.is_completed():
#                 return path  # مسار الحل للوصول للهدف

#             # حفظ حالة الشبكة الحالية
#             visited.add(tuple(map(tuple, current_grid)))

#             # جرب كل التحركات الممكنة لكل عنصر مغناطيسي
#             for i in range(self.size):
#                 for j in range(self.num_cols):
#                     cell = current_grid[i][j]
#                     if cell.item and cell.item.hue in ("red", "blue"):
#                         # جرب التحركات المتاحة
#                         for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
#                             new_x, new_y = i + dx, j + dy
#                             if 0 <= new_x < self.size and 0 <= new_y < self.num_cols and not current_grid[new_x][new_y].item:
#                                 new_grid = [row[:] for row in current_grid]  # نسخ الشبكة
#                                 new_grid[new_x][new_y].item = cell.item  # نقل العنصر
#                                 new_grid[i][j].item = None  # إزالة العنصر من الموقع القديم
                                
#                                 if tuple(map(tuple, new_grid)) not in visited:
#                                     queue.put((new_grid, path + [(i, j, new_x, new_y)]))

#         return None  # إذا لم يتم العثور على حل

# class MagneticGameGUI:
#     def __init__(self, root, grid_layout):
#         self.root = root
#         self.root.title("Magnetic Item Game")
#         self.board = GameBoard(grid_layout)
#         self.steps_remaining = 3  # عدد الخطوات المسموحة
#         self.selected_item = None
#         self.selected_item_x = None
#         self.selected_item_y = None
#         self.create_board_ui()

#     def create_board_ui(self):
#         self.canvas = tk.Canvas(self.root, width=500, height=500, bg="white")
#         self.canvas.grid(row=0, column=0)
        
#         # عرض عدد الخطوات المتبقية
#         self.steps_label = tk.Label(self.root, text=f"remaning steps: {self.steps_remaining}", font=("Arial", 14))
#         self.steps_label.grid(row=1, column=0)
        
#         self.update_board_ui()
#         self.canvas.bind("<Button-1>", self.select_item)

#     def select_item(self, event):
#         x, y = event.x // 100, event.y // 100
#         cell = self.board.grid[y][x]
#         if isinstance(cell.item, Item):
#             if cell.item.hue == "gray":
#                 messagebox.showwarning("تحذير", "لا يمكنك اختيار العناصر الرمادية.")
#             else:
#                 self.selected_item = cell.item
#                 self.selected_item_x = y
#                 self.selected_item_y = x
#         elif self.selected_item:
#             self.board.swap_item(self.selected_item_x, self.selected_item_y, self.selected_item, y, x)
#             self.steps_remaining -= 1
#             self.selected_item = None
#             self.update_board_ui()

#             if self.board.is_completed():
#                 messagebox.showinfo("تهانينا", "لقد نجحت في إنهاء اللعبة!")
#             elif self.steps_remaining <= 0:
#                 messagebox.showwarning("انتهاء الخطوات", "انتهت عدد الخطوات المسموحة.")

#     def update_board_ui(self):
#         self.canvas.delete("all")
#         for i in range(self.board.size):
#             for j in range(self.board.num_cols):
#                 cell = self.board.grid[i][j]
#                 color = "white" if cell.item is None else cell.item.hue
#                 self.canvas.create_rectangle(j*100, i*100, (j+1)*100, (i+1)*100, fill=color)
#                 if cell.target == "goal":
#                     self.canvas.create_text(j*100 + 50, i*100 + 50, text="G", font=("Arial", 20), fill="black")

#         self.steps_label.config(text=f"Remaining Steps: {self.steps_remaining}")

# root = tk.Tk()
# game = MagneticGameGUI(root, grids[(3, 2)][0])  # تهيئة اللعبة باستخدام التخطيط الأول
# root.mainloop()







































































































# import tkinter as tk
# from tkinter import messagebox

# class Item:
#     def __init__(self, hue):
#         self.hue = hue  # "red", "blue", "gray"
#         self.position = None

#     def __str__(self):
#         return self.hue[0].upper()

# class Cell:
#     def __init__(self, item, target):
#         self.item = item  # عنصر المغناطيس أو None
#         self.target = target  # هدف إذا كانت الخلية هدفا
#         self.position = None

#     def __str__(self):
#         return "G" if self.target == "goal" else ""

# # تعريف الرقع المتاحة
# grids = {
#     (5, 5): [
#         [
#             [Cell(None, None), Cell(None, None), Cell(None, 'goal'), Cell(None, None), Cell(None, None)],
#             [Cell(None, None), Cell(None, None), Cell(Item('gray'), None), Cell(None, None), Cell(None, None)],
#             [Cell(None, 'goal'), Cell(Item('gray'), None), Cell(None, 'goal'), Cell(Item('gray'), None), Cell(None, 'goal')],
#             [Cell(None, None), Cell(None, None), Cell(Item('gray'), None), Cell(None, None), Cell(None, None)],
#             [Cell(Item('red'), None), Cell(None, None), Cell(None, 'goal'), Cell(None, None), Cell(Item('blue'), None)]
#         ],
#         [
#             [Cell(None, None), Cell(Item('red'), None), Cell(None, None), Cell(None, 'goal'), Cell(None, None)],
#             [Cell(Item('gray'), None), Cell(None, None), Cell(None, None), Cell(None, None), Cell(None, None)],
#             [Cell(None, 'goal'), Cell(None, None), Cell(Item('gray'), None), Cell(None, None), Cell(None, None)],
#             [Cell(None, None), Cell(None, None), Cell(None, None), Cell(Item('gray'), None), Cell(None, None)],
#             [Cell(None, None), Cell(None, None), Cell(Item('blue'), None), Cell(None, 'goal'), Cell(None, None)]
#         ]
#     ],
#     (3, 2): [
#         [
#             [Cell(Item('blue'), None),  Cell(None, 'goal')],
#             [Cell(None, None), Cell(Item('gray'), None)],
#             [Cell(None, None), Cell(None, 'goal')]
#         ]
#     ]
# }

# class GameBoard:
#     def __init__(self, grid_layout):
#         self.grid = grid_layout
#         self.size = len(grid_layout)
#         self.num_cols = len(grid_layout[0]) if self.size > 0 else 0

#     def swap_item(self, x1, y1, item, new_x, new_y):
#         self.grid[x1][y1].item = None
#         self.grid[new_x][new_y].item = item
#         item.position = (new_x, new_y)

#         # حركة المغناطيس الأحمر
#         if item.hue == 'red':
#             for j in range(self.num_cols):
#                 if j != new_y:
#                     cell = self.grid[new_x][j]
#                     if cell and isinstance(cell.item, Item) and cell.item.hue == 'gray':
#                         if j < new_y and not self.grid[new_x][j + 1].item:
#                             self.swap_auto_item(new_x, j, cell.item, new_x, j + 1)
#                         elif j > new_y and not self.grid[new_x][j - 1].item:
#                             self.swap_auto_item(new_x, j, cell.item, new_x, j - 1)

#             for i in range(self.size):
#                 if i != new_x:
#                     cell = self.grid[i][new_y]
#                     if cell and isinstance(cell.item, Item) and cell.item.hue == 'gray':
#                         if i < new_x and not self.grid[i + 1][new_y].item:
#                             self.swap_auto_item(i, new_y, cell.item, i + 1, new_y)
#                         elif i > new_x and not self.grid[i - 1][new_y].item:
#                             self.swap_auto_item(i, new_y, cell.item, i - 1, new_y)

#         elif item.hue == 'blue':
#             for i in range(self.size):
#                 cell = self.grid[i][new_y]
#                 if cell and isinstance(cell.item, Item):
#                     if i > new_x and i < self.size - 1 and not self.grid[i + 1][new_y].item:
#                         self.swap_auto_item(i, new_y, cell.item, i + 1, new_y)
#                     elif i < new_x and i > 0 and not self.grid[i - 1][new_y].item:
#                         self.swap_auto_item(i, new_y, cell.item, i - 1, new_y)
#             for j in range(self.num_cols):
#                 cell = self.grid[new_x][j]
#                 if cell and isinstance(cell.item, Item):
#                     if j > new_y and j < self.num_cols - 1 and not self.grid[new_x][j + 1].item:
#                         self.swap_auto_item(new_x, j, cell.item, new_x, j + 1)
#                     elif j < new_y and j > 0 and not self.grid[new_x][j - 1].item:
#                         self.swap_auto_item(new_x, j, cell.item, new_x, j - 1)

#     def swap_auto_item(self, x1, y1, item, new_x, new_y):
#         self.grid[x1][y1].item = None
#         self.grid[new_x][new_y].item = item
#         item.position = (new_x, new_y)

#     def is_completed(self):
#         red_or_blue_found = False
#         for i in range(self.size):
#             for j in range(self.num_cols):
#                 cell = self.grid[i][j]
#                 if cell.target == "goal":
#                     if not cell.item:
#                         return False
#                     elif cell.item.hue == 'gray':
#                         continue
#                     elif cell.item.hue in ('red', 'blue'):
#                         red_or_blue_found = True
#                     else:
#                         return False
#         return red_or_blue_found

# class MagneticGameGUI:
#     def __init__(self, root, grid_layout):
#         self.root = root
#         self.root.title("Magnetic Item Game")
#         self.board = GameBoard(grid_layout)
#         self.steps_remaining = 3  # عدد الخطوات المسموحة
#         self.selected_item = None
#         self.selected_item_x = None
#         self.selected_item_y = None
#         self.create_board_ui()

#     def create_board_ui(self):
#         self.canvas = tk.Canvas(self.root, width=500, height=500, bg="white")
#         self.canvas.grid(row=0, column=0)
        
#         # عرض عدد الخطوات المتبقية
#         self.steps_label = tk.Label(self.root, text=f"remaning steps: {self.steps_remaining}", font=("Arial", 14))
#         self.steps_label.grid(row=1, column=0)
        
#         self.update_board_ui()
#         self.canvas.bind("<Button-1>", self.select_item)

#     def select_item(self, event):
#         x, y = event.x // 100, event.y // 100
#         cell = self.board.grid[y][x]
#         if isinstance(cell.item, Item):
#             if cell.item.hue == "gray":
#                 messagebox.showwarning("تحذير", "لا يمكنك اختيار العناصر الرمادية.")
#             else:
#                 self.selected_item = cell.item
#                 self.selected_item_x = y
#                 self.selected_item_y = x
#         elif self.selected_item:
#             self.board.swap_item(self.selected_item_x, self.selected_item_y, self.selected_item, y, x)
#             self.steps_remaining -= 1
#             self.steps_label.config(text=f"remaining steps: {self.steps_remaining}")
#             self.selected_item = None
#             self.update_board_ui()
#             if self.board.is_completed():
#                 messagebox.showinfo("تهانينا!", "لقد انتهيت من اللعبة!")
#                 self.root.quit()
#             elif self.steps_remaining <= 0:
#                 messagebox.showinfo("انتهت اللعبة", "لم تقم بحل اللعبة في الوقت المحدد!")
#                 self.root.quit()

#     def update_board_ui(self):
#         self.canvas.delete("all")
#         for i in range(self.board.size):
#             for j in range(self.board.num_cols):
#                 cell = self.board.grid[i][j]
#                 color = "white"
#                 if cell.target == "goal":
#                     color = "yellow"
#                 self.canvas.create_rectangle(j*100, i*100, (j+1)*100, (i+1)*100, fill=color)
#                 if cell.item:
#                     item_color = "gray" if cell.item.hue == "gray" else cell.item.hue
#                     self.canvas.create_oval(j*100+25, i*100+25, (j+1)*100-25, (i+1)*100-25, fill=item_color)

# # تعديل تشغيل اللعبة بحيث يطلب من المستخدم اختيار نمط اللعب

# # إدخال عدد الصفوف والأعمدة من المستخدم
# try:
#     num_rows = int(input("Enter your rows: "))
#     num_cols = int(input("Enter your columns: "))
# except ValueError:
#     print("Please enter an integer number.")
#     exit()

# # التحقق من وجود رقع متوافقة
# available_grids = grids.get((num_rows, num_cols), [])
# if not available_grids:
#     print("No grid available with the entered dimensions.")
#     exit()

# # إذا كان هناك أكثر من رقعة، نطلب من المستخدم اختيار واحدة
# if len(available_grids) > 1:
#     print("Please select a grid:")
#     for i, grid in enumerate(available_grids, start=1):
#         print(f"Grid {i}")
#     grid_index = int(input("Enter the grid number: ")) - 1
# else:
#     grid_index = 0

# selected_grid = available_grids[grid_index]

# # طلب نمط التشغيل من المستخدم
# mode = input("Select mode: (1) Manual: ")

# # تشغيل اللعبة
# root = tk.Tk()
# game = MagneticGameGUI(root, selected_grid)

# if mode == '1':
#     root.mainloop()  # تشغيل الوضع اليدوي كما هو في الكود الأصلي























# import tkinter as tk
# from tkinter import messagebox
# from collections import deque

# class Item:
#     def __init__(self, hue):
#         self.hue = hue  # "red", "blue", "gray"
#         self.position = None

#     def __str__(self):
#         return self.hue[0].upper()

# class Cell:
#     def __init__(self, item, target):
#         self.item = item  # العنصر الذي في الخلية (مغناطيس أو كرة حديدية أو لا شيء)
#         self.target = target  # هدف إذا كانت الخلية هدفا
#         self.position = None

#     def __str__(self):
#         return "G" if self.target == "goal" else ""

# # تعريف الرقع المتاحة
# grids = {
#     (5, 5): [
#         [
#             [Cell(None, None), Cell(None, None), Cell(None, 'goal'), Cell(None, None), Cell(None, None)],
#             [Cell(None, None), Cell(None, None), Cell(Item('gray'), None), Cell(None, None), Cell(None, None)],
#             [Cell(None, 'goal'), Cell(Item('gray'), None), Cell(None, 'goal'), Cell(Item('gray'), None), Cell(None, 'goal')],
#             [Cell(None, None), Cell(None, None), Cell(Item('gray'), None), Cell(None, None), Cell(None, None)],
#             [Cell(Item('red'), None), Cell(None, None), Cell(None, 'goal'), Cell(None, None), Cell(Item('blue'), None)]
#         ],
#         [
#             [Cell(None, None), Cell(Item('red'), None), Cell(None, None), Cell(None, 'goal'), Cell(None, None)],
#             [Cell(Item('gray'), None), Cell(None, None), Cell(None, None), Cell(None, None), Cell(None, None)],
#             [Cell(None, 'goal'), Cell(None, None), Cell(Item('gray'), None), Cell(None, None), Cell(None, None)],
#             [Cell(None, None), Cell(None, None), Cell(None, None), Cell(Item('gray'), None), Cell(None, None)],
#             [Cell(None, None), Cell(None, None), Cell(Item('blue'), None), Cell(None, 'goal'), Cell(None, None)]
#         ]
#     ],
#     (3, 2): [
#         [
#             [Cell(Item('blue'), None),  Cell(None, 'goal')],
#             [Cell(None, None), Cell(Item('gray'), None)],
#             [Cell(None, None), Cell(None, 'goal')]
#         ]
#     ]
# }

# class GameBoard:
#     def __init__(self, grid_layout):
#         self.grid = grid_layout
#         self.size = len(grid_layout)
#         self.num_cols = len(grid_layout[0]) if self.size > 0 else 0

#     def swap_item(self, x1, y1, item, new_x, new_y):
#         self.grid[x1][y1].item = None
#         self.grid[new_x][new_y].item = item
#         item.position = (new_x, new_y)

#         # حركة المغناطيس الأحمر
#         if item.hue == 'red':
#             for j in range(self.num_cols):
#                 if j != new_y:
#                     cell = self.grid[new_x][j]
#                     if cell and isinstance(cell.item, Item) and cell.item.hue == 'gray':
#                         if j < new_y and not self.grid[new_x][j + 1].item:
#                             self.swap_auto_item(new_x, j, cell.item, new_x, j + 1)
#                         elif j > new_y and not self.grid[new_x][j - 1].item:
#                             self.swap_auto_item(new_x, j, cell.item, new_x, j - 1)

#             for i in range(self.size):
#                 if i != new_x:
#                     cell = self.grid[i][new_y]
#                     if cell and isinstance(cell.item, Item) and cell.item.hue == 'gray':
#                         if i < new_x and not self.grid[i + 1][new_y].item:
#                             self.swap_auto_item(i, new_y, cell.item, i + 1, new_y)
#                         elif i > new_x and not self.grid[i - 1][new_y].item:
#                             self.swap_auto_item(i, new_y, cell.item, i - 1, new_y)

#         elif item.hue == 'blue':
#             for i in range(self.size):
#                 cell = self.grid[i][new_y]
#                 if cell and isinstance(cell.item, Item):
#                     if i > new_x and i < self.size - 1 and not self.grid[i + 1][new_y].item:
#                         self.swap_auto_item(i, new_y, cell.item, i + 1, new_y)
#                     elif i < new_x and i > 0 and not self.grid[i - 1][new_y].item:
#                         self.swap_auto_item(i, new_y, cell.item, i - 1, new_y)
#             for j in range(self.num_cols):
#                 cell = self.grid[new_x][j]
#                 if cell and isinstance(cell.item, Item):
#                     if j > new_y and j < self.num_cols - 1 and not self.grid[new_x][j + 1].item:
#                         self.swap_auto_item(new_x, j, cell.item, new_x, j + 1)
#                     elif j < new_y and j > 0 and not self.grid[new_x][j - 1].item:
#                         self.swap_auto_item(new_x, j, cell.item, new_x, j - 1)

#     def swap_auto_item(self, x1, y1, item, new_x, new_y):
#         self.grid[x1][y1].item = None
#         self.grid[new_x][new_y].item = item
#         item.position = (new_x, new_y)

#     def is_completed(self):
#         red_or_blue_found = False
#         for i in range(self.size):
#             for j in range(self.num_cols):
#                 cell = self.grid[i][j]
#                 if cell.target == "goal":
#                     if not cell.item:
#                         return False
#                     elif cell.item.hue == 'gray':
#                         continue
#                     elif cell.item.hue in ('red', 'blue'):
#                         red_or_blue_found = True
#                     else:
#                         return False
#         return red_or_blue_found

# class State:
#     def __init__(self, previous_state, board, x, y, item):
#         self.previous_state = previous_state
#         self.board = board
#         self.x = x
#         self.y = y
#         self.item = item

#     def has_previous(self):
#         return self.previous_state is not None
    
#     def get_previous_state(self):
#         return self.previous_state
    
#     def __str__(self):
#         return str(self.board)  # Represent the board as a string for debugging

# class BFS:
#     def __init__(self, game_board):
#         self.game_board = game_board
#         self.visited = set()  # Keep track of visited states
#         self.queue = deque()

#     def is_goal_state(self, board):
#         # تحقق من اكتمل اللعبة عندما جميع الأهداف مليئة بالمغناطيس أو الكرات الحديدية
#         for row in board:
#             for cell in row:
#                 if cell.target == "goal" and not cell.item:
#                     return False
#         return True

#     def get_next_states(self, current_state):
#         next_states = []
#         for i in range(self.game_board.size):
#             for j in range(self.game_board.num_cols):
#                 current_cell = current_state.board[i][j]
#                 if isinstance(current_cell.item, Item):
#                     for new_x, new_y in self.get_possible_moves(i, j):
#                         new_board = self.make_move(current_state.board, i, j, new_x, new_y)
#                         next_states.append(State(current_state, new_board, new_x, new_y, current_cell.item))
#         return next_states

#     def make_move(self, board, x1, y1, x2, y2):
#         # متحرك مغناطيس
#         new_board = [row[:] for row in board]
#         new_board[x2][y2].item = new_board[x1][y1].item
#         new_board[x1][y1].item = None
#         return new_board

#     def bfs_search(self):
#         initial_state = self.find_initial_state()
#         self.queue.append(initial_state)
#         self.visited.add(str(initial_state.board))  # Avoid revisiting the same board configuration

#         while self.queue:
#             current_state = self.queue.popleft()

#             # تحقق من اكتمل اللعبة
#             if self.is_goal_state(current_state.board):
#                 return current_state

#             next_states = self.get_next_states(current_state)
#             for next_state in next_states:
#                 board_str = str(next_state.board)
#                 if board_str not in self.visited:
#                     self.visited.add(board_str)
#                     self.queue.append(next_state)

#         return None  # Return None if no solution is found

#     def find_initial_state(self):
#         # البحث عن المغناطيس كحالة ابتداءية
#         for i in range(self.game_board.size):
#             for j in range(self.game_board.num_cols):
#                 cell = self.game_board.grid[i][j]
#                 if isinstance(cell.item, Item) and cell.item.hue != "gray":
#                     return State(None, self.game_board.grid, i, j, cell.item)
#         return None

# class MagneticGameGUI:
#     def __init__(self, root, grid_layout):
#         self.root = root
#         self.root.title("Magnetic Item Game")
#         self.board = GameBoard(grid_layout)
#         self.steps_remaining = 3
#         self.selected_item = None
#         self.selected_item_x = None
#         self.selected_item_y = None
#         self.create_board_ui()

#     def create_board_ui(self):
#         self.canvas = tk.Canvas(self.root, width=500, height=500, bg="white")
#         self.canvas.grid(row=0, column=0)

#         self.steps_label = tk.Label(self.root, text=f"remaining steps: {self.steps_remaining}", font=("Arial", 14))
#         self.steps_label.grid(row=1, column=0)

#         self.update_board_ui()
#         self.canvas.bind("<Button-1>", self.select_item)

#         # Add a button to run BFS
#         self.solve_button = tk.Button(self.root, text="Solve Automatically", command=self.solve_game)
#         self.solve_button.grid(row=2, column=0)

#     def solve_game(self):
#         bfs = BFS(self.board)
#         solution_state = bfs.bfs_search()

#         if solution_state:
#             self.show_solution(solution_state)
#         else:
#             messagebox.showinfo("No Solution", "No solution found.")

#     def show_solution(self, solution_state):
#         state = solution_state
#         while state:
#             self.update_board_ui(state.board)
#             state = state.get_previous_state()

#     def update_board_ui(self, board=None):
#         self.canvas.delete("all")
#         board = board or self.board.grid  # Use the current board if no solution state
#         for i in range(self.board.size):
#             for j in range(self.board.num_cols):
#                 cell = board[i][j]
#                 color = "white"
#                 if cell.target == "goal":
#                     color = "yellow"
#                 self.canvas.create_rectangle(j*100, i*100, (j+1)*100, (i+1)*100, fill=color)
#                 if cell.item:
#                     item_color = "gray" if cell.item.hue == "gray" else cell.item.hue
#                     self.canvas.create_oval(j*100+25, i*100+25, (j+1)*100-25, (i+1)*100-25, fill=item_color)

#     def select_item(self, event):
#         x, y = event.x // 100, event.y // 100
#         cell = self.board.grid[y][x]
#         if isinstance(cell.item, Item):
#             if cell.item.hue == "gray":
#                 messagebox.showwarning("Warning", "Cannot select gray items.")
#             else:
#                 self.selected_item = cell.item
#                 self.selected_item_x = y
#                 self.selected_item_y = x
#         elif self.selected_item:
#             self.board.swap_item(self.selected_item_x, self.selected_item_y, self.selected_item, y, x)
#             self.steps_remaining -= 1
#             self.steps_label.config(text=f"remaining steps: {self.steps_remaining}")
#             self.selected_item = None
#             self.update_board_ui()
#             if self.board.is_completed():
#                 messagebox.showinfo("Congratulations!", "You completed the game!")
#                 self.root.quit()
#             elif self.steps_remaining <= 0:
#                 messagebox.showinfo("Game Over", "You ran out of steps!")
#                 self.root.quit()

# # إنشاء واجهة المستخدم
# root = tk.Tk()
# game = MagneticGameGUI(root, grids[(5, 5)][0])
# root.mainloop()



















































































































import tkinter as tk
from tkinter import messagebox
from collections import deque

class Item:
    def __init__(self, hue):
        self.hue = hue  # "red", "blue", "gray"
        self.position = None

    def __str__(self):
        return self.hue[0].upper()

class Cell:
    def __init__(self, item, target):
        self.item = item  # عنصر المغناطيس أو None
        self.target = target  # هدف إذا كانت الخلية هدفا
        self.position = None

    def __str__(self):
        return "G" if self.target == "goal" else ""

# تعريف الرقع المتاحة
grids = {
    (5, 5): [
        [
            [Cell(None, None), Cell(None, None), Cell(None, 'goal'), Cell(None, None), Cell(None, None)],
            [Cell(None, None), Cell(None, None), Cell(Item('gray'), None), Cell(None, None), Cell(None, None)],
            [Cell(None, 'goal'), Cell(Item('gray'), None), Cell(None, 'goal'), Cell(Item('gray'), None), Cell(None, 'goal')],
            [Cell(None, None), Cell(None, None), Cell(Item('gray'), None), Cell(None, None), Cell(None, None)],
            [Cell(Item('red'), None), Cell(None, None), Cell(None, 'goal'), Cell(None, None), Cell(Item('blue'), None)]
        ],
        [
            [Cell(None, None), Cell(Item('red'), None), Cell(None, None), Cell(None, 'goal'), Cell(None, None)],
            [Cell(Item('gray'), None), Cell(None, None), Cell(None, None), Cell(None, None), Cell(None, None)],
            [Cell(None, 'goal'), Cell(None, None), Cell(Item('gray'), None), Cell(None, None), Cell(None, None)],
            [Cell(None, None), Cell(None, None), Cell(None, None), Cell(Item('gray'), None), Cell(None, None)],
            [Cell(None, None), Cell(None, None), Cell(Item('blue'), None), Cell(None, 'goal'), Cell(None, None)]
        ]
    ],
    (3, 2): [
        [
            [Cell(Item('blue'), None),  Cell(None, 'goal')],
            [Cell(None, None), Cell(Item('gray'), None)],
            [Cell(None, None), Cell(None, 'goal')]
        ]
    ]
}

class GameBoard:
    def __init__(self, grid_layout):
        self.grid = grid_layout
        self.size = len(grid_layout)
        self.num_cols = len(grid_layout[0]) if self.size > 0 else 0

    def swap_item(self, x1, y1, item, new_x, new_y):
        self.grid[x1][y1].item = None
        self.grid[new_x][new_y].item = item
        item.position = (new_x, new_y)

        # حركة المغناطيس الأحمر
        if item.hue == 'red':
            for j in range(self.num_cols):
                if j != new_y:
                    cell = self.grid[new_x][j]
                    if cell and isinstance(cell.item, Item) and cell.item.hue == 'gray':
                        if j < new_y and not self.grid[new_x][j + 1].item:
                            self.swap_auto_item(new_x, j, cell.item, new_x, j + 1)
                        elif j > new_y and not self.grid[new_x][j - 1].item:
                            self.swap_auto_item(new_x, j, cell.item, new_x, j - 1)

            for i in range(self.size):
                if i != new_x:
                    cell = self.grid[i][new_y]
                    if cell and isinstance(cell.item, Item) and cell.item.hue == 'gray':
                        if i < new_x and not self.grid[i + 1][new_y].item:
                            self.swap_auto_item(i, new_y, cell.item, i + 1, new_y)
                        elif i > new_x and not self.grid[i - 1][new_y].item:
                            self.swap_auto_item(i, new_y, cell.item, i - 1, new_y)

        elif item.hue == 'blue':
            for i in range(self.size):
                cell = self.grid[i][new_y]
                if cell and isinstance(cell.item, Item):
                    if i > new_x and i < self.size - 1 and not self.grid[i + 1][new_y].item:
                        self.swap_auto_item(i, new_y, cell.item, i + 1, new_y)
                    elif i < new_x and i > 0 and not self.grid[i - 1][new_y].item:
                        self.swap_auto_item(i, new_y, cell.item, i - 1, new_y)
            for j in range(self.num_cols):
                cell = self.grid[new_x][j]
                if cell and isinstance(cell.item, Item):
                    if j > new_y and j < self.num_cols - 1 and not self.grid[new_x][j + 1].item:
                        self.swap_auto_item(new_x, j, cell.item, new_x, j + 1)
                    elif j < new_y and j > 0 and not self.grid[new_x][j - 1].item:
                        self.swap_auto_item(new_x, j, cell.item, new_x, j - 1)

    def swap_auto_item(self, x1, y1, item, new_x, new_y):
        self.grid[x1][y1].item = None
        self.grid[new_x][new_y].item = item
        item.position = (new_x, new_y)

    def is_completed(self):
        red_or_blue_found = False
        for i in range(self.size):
            for j in range(self.num_cols):
                cell = self.grid[i][j]
                if cell.target == "goal":
                    if not cell.item:
                        return False
                    elif cell.item.hue == 'gray':
                        continue
                    elif cell.item.hue in ('red', 'blue'):
                        red_or_blue_found = True
                    else:
                        return False
        return red_or_blue_found

class MagneticGameSolver:
    def __init__(self, game_board):
        self.game_board = game_board

    def bfs(self):
        start_positions = []
        
        # البحث عن مواقع المغناطيسات (الأحمر والأزرق)
        for i in range(self.game_board.size):
            for j in range(self.game_board.num_cols):
                cell = self.game_board.grid[i][j]
                if isinstance(cell.item, Item) and cell.item.hue in ('red', 'blue'):
                    start_positions.append((i, j, cell.item))
        
        # قائمة الحركات الممكنة (أعلى، أسفل، يمين، يسار)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        # تعيين قائمة للحركات التي يتم تنفيذها
        moves = deque()
        
        # تهيئة الصفوف في BFS مع إضافة جميع مواقع المغناطيسات
        visited = set()
        for x, y, item in start_positions:
            visited.add((x, y, item.hue))
            moves.append((x, y, item))
        
        # خوارزمية BFS
        while moves:
            x, y, item = moves.popleft()
            
            # نفذ الحركات الممكنة (أعلى، أسفل، يسار، يمين)
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < self.game_board.size and 0 <= new_y < self.game_board.num_cols:
                    cell = self.game_board.grid[new_x][new_y]
                    
                    # تحريك العنصر إلى الخلية الجديدة إذا لم تكن محجوزة
                    if not cell.item and (new_x, new_y, item.hue) not in visited:
                        self.game_board.swap_item(x, y, item, new_x, new_y)
                        visited.add((new_x, new_y, item.hue))
                        moves.append((new_x, new_y, item))

                        # التحقق مما إذا كانت اللعبة قد اكتملت بعد الحركة
                        if self.game_board.is_completed():
                            return True
        
        return False  # إذا لم يتم الوصول إلى الحل

class MagneticGameGUI:
    def __init__(self, root, grid_layout):
        self.root = root
        self.root.title("Magnetic Item Game")
        self.board = GameBoard(grid_layout)
        self.steps_remaining = 1000  # عدد الخطوات المسموحة
        self.selected_item = None
        self.selected_item_x = None
        self.selected_item_y = None
        self.create_board_ui()

    def create_board_ui(self):
        self.canvas = tk.Canvas(self.root, width=500, height=500, bg="white")
        self.canvas.grid(row=0, column=0)
        
        # عرض عدد الخطوات المتبقية
        self.steps_label = tk.Label(self.root, text=f"remaning steps: {self.steps_remaining}", font=("Arial", 14))
        self.steps_label.grid(row=1, column=0)
        
        self.update_board_ui()
        self.canvas.bind("<Button-1>", self.select_item)

    def select_item(self, event):
        x, y = event.x // 100, event.y // 100
        cell = self.board.grid[y][x]
        if isinstance(cell.item, Item):
            if cell.item.hue == "gray":
                messagebox.showwarning("تحذير", "لا يمكنك اختيار العناصر الرمادية.")
            else:
                self.selected_item = cell.item
                self.selected_item_x = y
                self.selected_item_y = x
        elif self.selected_item:
            self.board.swap_item(self.selected_item_x, self.selected_item_y, self.selected_item, y, x)
            self.steps_remaining -= 1
            self.steps_label.config(text=f"remaining steps: {self.steps_remaining}")
            self.selected_item = None
            self.update_board_ui()
            if self.board.is_completed():
                messagebox.showinfo("تهانينا!", "لقد انتهيت من اللعبة!")
                self.root.quit()
            elif self.steps_remaining <= 0:
                messagebox.showinfo("انتهت اللعبة", "لم تقم بحل اللعبة في الوقت المحدد!")
                self.root.quit()

    def update_board_ui(self):
        self.canvas.delete("all")
        for i in range(self.board.size):
            for j in range(self.board.num_cols):
                cell = self.board.grid[i][j]
                color = "white"
                if cell.target == "goal":
                    color = "yellow"
                self.canvas.create_rectangle(j*100, i*100, (j+1)*100, (i+1)*100, fill=color)
                if cell.item:
                    item_color = "gray" if cell.item.hue == "gray" else cell.item.hue
                    self.canvas.create_oval(j*100+25, i*100+25, (j+1)*100-25, (i+1)*100-25, fill=item_color)

    def auto_solve(self):
        solver = MagneticGameSolver(self.board)
        if solver.bfs():
            messagebox.showinfo("تهانينا!", "تم حل اللعبة تلقائيًا!")
            self.root.quit()
        else:
            messagebox.showinfo("فشل", "لم يتمكن من حل اللعبة.")
            self.root.quit()

# تعديل تشغيل اللعبة بحيث يطلب من المستخدم اختيار نمط اللعب

# إدخال عدد الصفوف والأعمدة من المستخدم
try:
    num_rows = int(input("Enter your rows: "))
    num_cols = int(input("Enter your columns: "))
except ValueError:
    print("Please enter an integer number.")
    exit()

# التحقق من وجود رقع متوافقة
available_grids = grids.get((num_rows, num_cols), [])
if not available_grids:
    print("No grid available with the entered dimensions.")
    exit()

# إذا كان هناك أكثر من رقعة، نطلب من المستخدم اختيار واحدة
if len(available_grids) > 1:
    print("Please select a grid:")
    for i, grid in enumerate(available_grids, start=1):
        print(f"Grid {i}")
    grid_index = int(input("Enter the grid number: ")) - 1
else:
    grid_index = 0

selected_grid = available_grids[grid_index]

# طلب نمط التشغيل من المستخدم
mode = input("Select mode: (1) Manual, (2) Auto-solve: ")

# تشغيل اللعبة
root = tk.Tk()
game = MagneticGameGUI(root, selected_grid)

if mode == '1':
    root.mainloop()  # تشغيل الوضع اليدوي كما هو في الكود الأصلي
elif mode == '2':
    game.auto_solve()  # تشغيل الوضع التلقائي لحل اللعبة




















































import tkinter as tk
from tkinter import messagebox, ttk
import random
import time

class TicTacToeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("井字棋游戏")
        self.root.resizable(False, False)
        
        # 首先显示开始界面
        self.show_start_screen()
    
    def show_start_screen(self):
        # 清除窗口中的所有组件
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # 创建开始界面
        start_frame = tk.Frame(self.root, padx=20, pady=20)
        start_frame.pack(expand=True, fill='both')
        
        # 游戏标题
        title_label = tk.Label(start_frame, text="井字棋游戏", font=('Arial', 24, 'bold'))
        title_label.pack(pady=20)
        
        # 游戏模式选择
        mode_frame = tk.Frame(start_frame)
        mode_frame.pack(pady=20)
        
        # 对战模式选择
        self.game_mode = tk.StringVar(value="pvp")
        
        pvp_radio = tk.Radiobutton(mode_frame, text="双人对战", variable=self.game_mode, 
                                   value="pvp", font=('Arial', 12))
        pvp_radio.grid(row=0, column=0, padx=10)
        
        pvc_radio = tk.Radiobutton(mode_frame, text="人机对战", variable=self.game_mode, 
                                   value="pvc", font=('Arial', 12))
        pvc_radio.grid(row=0, column=1, padx=10)
        
        # AI难度选择（仅在人机对战时有效）
        difficulty_frame = tk.Frame(start_frame)
        difficulty_frame.pack(pady=10)
        
        tk.Label(difficulty_frame, text="AI难度:", font=('Arial', 12)).grid(row=0, column=0, padx=5)
        self.difficulty = tk.StringVar(value="中等")
        difficulty_combo = ttk.Combobox(difficulty_frame, textvariable=self.difficulty, 
                                        values=["简单", "中等", "困难"], state="readonly", width=10)
        difficulty_combo.grid(row=0, column=1, padx=5)
        
        # 先手选择
        first_move_frame = tk.Frame(start_frame)
        first_move_frame.pack(pady=10)
        
        tk.Label(first_move_frame, text="先手:", font=('Arial', 12)).grid(row=0, column=0, padx=5)
        self.first_player = tk.StringVar(value="玩家")
        first_combo = ttk.Combobox(first_move_frame, textvariable=self.first_player, 
                                   values=["玩家", "电脑"], state="readonly", width=10)
        first_combo.grid(row=0, column=1, padx=5)
        
        # 开始游戏按钮
        start_button = tk.Button(start_frame, text="开始游戏", font=('Arial', 14),
                                command=self.start_game, width=15, height=2)
        start_button.pack(pady=20)
        
        # 显示游戏规则
        rules_button = tk.Button(start_frame, text="游戏规则", font=('Arial', 10),
                                command=self.show_rules)
        rules_button.pack(pady=5)
    
    def start_game(self):
        # 初始化游戏变量
        self.current_player = "X"  # 人类玩家总是X，AI是O
        self.board = [""] * 9
        self.moves_history = []
        self.game_over = False
        self.x_score = 0
        self.o_score = 0
        self.game_mode = self.game_mode.get()
        self.ai_difficulty = self.difficulty.get()
        
        # 如果是人机模式且电脑先手
        self.ai_plays_first = self.game_mode == "pvc" and self.first_player.get() == "电脑"
        
        # 设置游戏界面
        self.setup_game_ui()
        
        # 如果是AI先手，让AI走第一步
        if self.ai_plays_first:
            self.ai_make_move()
    
    def setup_game_ui(self):
        # 清除窗口中的所有组件
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # 创建UI元素
        self.create_menu_bar()
        self.create_info_frame()
        self.create_board_frame()
        self.create_control_frame()
    
    def create_menu_bar(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        
        game_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="游戏", menu=game_menu)
        game_menu.add_command(label="主菜单", command=self.show_start_screen)
        game_menu.add_command(label="新游戏", command=self.new_game)
        game_menu.add_command(label="退出", command=self.root.quit)
        
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="游戏规则", command=self.show_rules)
    
    def create_info_frame(self):
        info_frame = tk.Frame(self.root, pady=10)
        info_frame.pack()
        
        # 游戏模式显示
        game_mode_text = "双人对战" if self.game_mode == "pvp" else "人机对战"
        mode_label = tk.Label(info_frame, text=f"游戏模式: {game_mode_text}", font=('Arial', 10))
        mode_label.grid(row=0, column=0, padx=20, columnspan=2)
        
        # 玩家回合提示
        self.player_label = tk.Label(info_frame, text="当前玩家: X", font=('Arial', 12))
        self.player_label.grid(row=1, column=0, padx=20)
        
        # 分数显示
        score_frame = tk.Frame(info_frame)
        score_frame.grid(row=1, column=1, padx=20)
        
        player_text = "玩家" if self.game_mode == "pvc" else "X"
        ai_text = "电脑" if self.game_mode == "pvc" else "O"
        
        tk.Label(score_frame, text="分数:", font=('Arial', 12)).grid(row=0, column=0)
        self.score_label = tk.Label(score_frame, 
                                  text=f"{player_text}: 0 | {ai_text}: 0", 
                                  font=('Arial', 12))
        self.score_label.grid(row=0, column=1)
        
    def create_board_frame(self):
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(pady=10)
        
        self.buttons = []
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.board_frame, text="", font=('Arial', 20, 'bold'),
                                  width=5, height=2, 
                                  command=lambda row=i, col=j: self.make_move(row * 3 + col))
                button.grid(row=i, column=j, padx=2, pady=2)
                self.buttons.append(button)
    
    def create_control_frame(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        
        undo_button = tk.Button(control_frame, text="悔棋", font=('Arial', 10),
                             command=self.undo_move)
        undo_button.grid(row=0, column=0, padx=10)
        
        new_game_button = tk.Button(control_frame, text="新游戏", font=('Arial', 10),
                                 command=self.new_game)
        new_game_button.grid(row=0, column=1, padx=10)
        
        menu_button = tk.Button(control_frame, text="主菜单", font=('Arial', 10),
                               command=self.show_start_screen)
        menu_button.grid(row=0, column=2, padx=10)
    
    def make_move(self, index):
        if self.board[index] == "" and not self.game_over:
            # 记录移动历史
            self.moves_history.append((index, self.current_player))
            
            # 更新棋盘
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player, 
                                     fg="blue" if self.current_player == "X" else "red")
            
            # 检查游戏状态
            if self.check_winner():
                self.game_over = True
                if self.current_player == "X":
                    self.x_score += 1
                else:
                    self.o_score += 1
                self.update_score()
                
                winner_text = "玩家" if self.current_player == "X" and self.game_mode == "pvc" else \
                             "电脑" if self.current_player == "O" and self.game_mode == "pvc" else \
                             self.current_player
                             
                messagebox.showinfo("游戏结束", f"{winner_text} 获胜!")
            elif "" not in self.board:  # 平局
                self.game_over = True
                messagebox.showinfo("游戏结束", "平局!")
            else:
                # 切换玩家
                self.current_player = "O" if self.current_player == "X" else "X"
                self.player_label.config(text=f"当前玩家: {self.current_player}")
                
                # 如果是人机模式且当前是电脑回合（O），让AI下棋
                if self.game_mode == "pvc" and self.current_player == "O":
                    # 为了UI更新的效果，使用after方法延迟一点AI的操作
                    self.root.after(500, self.ai_make_move)
    
    def ai_make_move(self):
        if not self.game_over:
            # 根据难度选择不同的AI策略
            if self.ai_difficulty == "简单":
                index = self.ai_easy_move()
            elif self.ai_difficulty == "困难":
                index = self.ai_hard_move()
            else:  # 中等难度
                index = self.ai_medium_move()
                
            # 模拟AI点击
            self.make_move(index)
    
    def ai_easy_move(self):
        """简单AI：随机选择一个空位置"""
        empty_cells = [i for i, cell in enumerate(self.board) if cell == ""]
        return random.choice(empty_cells)
    
    def ai_medium_move(self):
        """中等AI：有70%概率使用困难策略，30%概率随机下棋"""
        if random.random() < 0.7:
            return self.ai_hard_move()
        else:
            return self.ai_easy_move()
    
    def ai_hard_move(self):
        """困难AI：使用Minimax算法找出最佳位置"""
        # 首先检查是否有立即获胜的位置
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"  # 尝试在此位置下棋
                if self.check_winner(False):  # 检查但不高亮
                    self.board[i] = ""  # 恢复
                    return i  # 找到能立即获胜的位置
                self.board[i] = ""  # 恢复
        
        # 检查是否需要阻止玩家获胜
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "X"  # 尝试玩家在此位置下棋
                if self.check_winner(False):  # 检查但不高亮
                    self.board[i] = ""  # 恢复
                    return i  # 阻止玩家获胜
                self.board[i] = ""  # 恢复
        
        # 尝试占据中心
        if self.board[4] == "":
            return 4
        
        # 尝试占据角落
        corners = [0, 2, 6, 8]
        empty_corners = [i for i in corners if self.board[i] == ""]
        if empty_corners:
            return random.choice(empty_corners)
        
        # 尝试占据边
        edges = [1, 3, 5, 7]
        empty_edges = [i for i in edges if self.board[i] == ""]
        if empty_edges:
            return random.choice(empty_edges)
        
        # 不应该到达这里，但为了安全，返回一个随机空位
        return self.ai_easy_move()
    
    def check_winner(self, highlight=True):
        # 检查所有获胜可能性
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # 横行
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # 纵列
            [0, 4, 8], [2, 4, 6]              # 对角线
        ]
        
        for pattern in win_patterns:
            if (self.board[pattern[0]] == self.board[pattern[1]] == self.board[pattern[2]] != ""):
                # 高亮显示获胜组合
                if highlight:
                    for pos in pattern:
                        self.buttons[pos].config(bg="light green")
                return True
        return False
    
    def update_score(self):
        if self.game_mode == "pvc":
            player_text = "玩家"
            ai_text = "电脑"
        else:
            player_text = "X"
            ai_text = "O"
        self.score_label.config(text=f"{player_text}: {self.x_score} | {ai_text}: {self.o_score}")
    
    def undo_move(self):
        if not self.moves_history:
            return
        
        if self.game_mode == "pvc" and len(self.moves_history) >= 2 and not self.game_over:
            # 在人机模式下，需要撤销两步（玩家的和电脑的）
            for _ in range(2):
                if self.moves_history:
                    last_move = self.moves_history.pop()
                    index = last_move[0]
                    self.board[index] = ""
                    self.buttons[index].config(text="", bg="SystemButtonFace")
            
            # 重置为玩家的回合
            self.current_player = "X"
            self.player_label.config(text="当前玩家: X")
        elif self.game_mode == "pvp" or self.game_over:
            # 双人模式或游戏结束后的撤销
            last_move = self.moves_history.pop()
            index = last_move[0]
            
            # 更新棋盘
            self.board[index] = ""
            self.buttons[index].config(text="", bg="SystemButtonFace")
            
            # 切换回上一个玩家
            self.current_player = last_move[1]
            self.player_label.config(text=f"当前玩家: {self.current_player}")
        
        # 如果游戏已结束但进行了悔棋，则继续游戏
        self.game_over = False
        
        # 重置高亮背景（如果有）
        for button in self.buttons:
            button.config(bg="SystemButtonFace")
    
    def new_game(self):
        # 重置棋盘
        self.board = [""] * 9
        for button in self.buttons:
            button.config(text="", bg="SystemButtonFace")
            
        # 重置游戏状态
        self.current_player = "X"
        self.moves_history = []
        self.game_over = False
        self.player_label.config(text="当前玩家: X")
        
        # 如果是人机模式且电脑先手
        if self.game_mode == "pvc" and self.ai_plays_first:
            self.root.after(500, self.ai_make_move)
    
    def show_rules(self):
        rules = """
        井字棋游戏规则:
        
        1. 两名玩家轮流在3x3网格上放置X和O标记
        2. 第一个在水平、垂直或对角线上连成一行的玩家获胜
        3. 如果所有格子都被填满且没有玩家获胜，游戏结束为平局
        4. 使用"悔棋"按钮可以撤销上一步操作
        5. 随时可以点击"新游戏"重新开始
        
        人机对战模式下：
        - 玩家始终使用X标记，电脑使用O标记
        - 有三种AI难度可选择
        - 可以选择谁先手
        """
        messagebox.showinfo("游戏规则", rules)

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGame(root)
    root.mainloop()

from PySide6.QtCore import Qt, Signal, Slot, QTimer
from PySide6.QtWidgets import QWidget, QGridLayout, QMessageBox, QLabel, QMainWindow, QPushButton \
, QApplication, QVBoxLayout, QHBoxLayout, QSpinBox, QComboBox, QSlider, QCheckBox, QGroupBox, QRadioButton, QButtonGroup
from PySide6.QtGui import QPainter, QPen, QColor, QBrush, QRadialGradient 

import sys


from menus.go.goboard import Player, Move, GoState
from menus.go.goplayer import Point
from menus.go.agent.mcts_agent import MCTsAgent

# Widget to display and interact with the Go board
class GoBoardGUI(QWidget):
    # Signal when a stone is placed 
    stone_placed = Signal(int,int)
    
    def __init__(self, board_size=9, parent=None):
        super().__init__(parent)
        self.board_size = board_size
        # Size of each cell in pixels 
        self.cell_size = 40
        self.board_margin = 40
        # Extra margin for coordinates  
        self.label_margin = 20
        # Adjustable stone size
        self.stone_radius = int(self.cell_size * 0.37)
        
        # Set fixed size for the board 
        board_pixels = (self.board_size - 1) * self.cell_size + 2 * (self.board_margin + self.label_margin)
        self.setMinimumSize(board_pixels, board_pixels)
        self.setMaximumSize(board_pixels, board_pixels)

        # point where the point is hovering
        self.hover_point = None
        
        # Set mouse tracking for hovering effects
        self.setMouseTracking(True)
        
    # Drawing the goboard and stones 
    def paintEvent(self, event):
        painter = QPainter(self)
        
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        # Draw the board backgrounnd
        painter.fillRect(self.rect(), QColor(236,197,125))
        
        # Draw board labels 
        self.draw_board_labels(painter)
        
        # Draw the grid lines
        pen = QPen(Qt.GlobalColor.black)
        pen.setWidth(1)
        painter.setPen(pen)
    
        
        # Gridlines positions
        grid_start = self.board_margin + self.label_margin
        grid_end = grid_start + (self.board_size - 1) * self.cell_size
        
        # Drawing the horizontal and vertical lines 
        for i in range(self.board_size):
            # Draw horizontal lines
            y = grid_start + i * self.cell_size
            painter.drawLine(grid_start, y, grid_end, y)
            
            # Draw vertical lines 
            x = grid_start + i * self.cell_size
            painter.drawLine(x, grid_start, x, grid_end)
        
        # Location of the star points (hoshi)
        star_points = [(2,2), (2,6), (6,2), (6,6), (4,4)]
        
        
        painter.setBrush(Qt.GlobalColor.black)
        # Draw the star points
        for row,col in star_points:
            x = grid_start + row * self.cell_size
            y = grid_start + col * self.cell_size
            painter.drawEllipse(x - 3.5, y - 3.5, 7, 7)
            
        
        # Draw points for the current board state     
        for row in range(1, self.board_size+1):
            for col in range(1, self.board_size+1):
                point = Point(row,col)
                player = self.game_state.board.get_player(point)
            
                if player is not None:
                    x = grid_start + (col -1) * self.cell_size
                    # Invert to match row numbering 
                    y = grid_start + (self.board_size - row) * self.cell_size
                    
                    if player == Player.black:
                        self.realistic_stones(painter, x, y, True)
                    else:
                        self.realistic_stones(painter, x, y, False)

         
        # Draw hover indicator for empty points
        if self.hover_point is not None:
            row, col = self.hover_point
            if 1 <= row <= self.board_size and 1 <= col <= self.board_size:
                point = Point(row,col)
                
                current_player = self.game_state.board.get_player(point)
                
                # only hover for empty points
                if current_player is None:
                    x = grid_start + (col -1) * self.cell_size
                    # Invert to match y-coordinate 
                    y = grid_start + (self.board_size - row) * self.cell_size
                    
                    # semi-transparent stones for hover effects 
                    if self.current_player == Player.black:
                        self.realistic_stones(painter, x, y, True, 100) # 100 for semitransparency
                    else: 
                        self.realistic_stones(painter, x, y, False, 200)
                    
             
    # Track mouse movement           
    def mouseMoveEvent(self, event):
        x = event.position().x() - (self.board_margin + self.label_margin)
        y = event.position().y() - (self.board_margin + self.label_margin)
        
        # the column correlates with x instead of y 
        col = round(x / self.cell_size) + 1
        # Invert to match with bottom -> 1 
        row = self.board_size - round(y/ self.cell_size)
        
        # Update hover points if changed 
        if self.hover_point != (row, col):
            self.hover_point = (row,col)
            self.update() # Repaint the hover
    
    # Place stone when mouse release    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.hover_point is not None:
            row, col = self.hover_point
            # Check boundaries
            if 1 <= row <= self.board_size and 1 <= col <= self.board_margin:
                self.stone_placed.emit(row,  col)
    
    # Draw board labels, (A-J for columns, 1-9 for rows)
    def draw_board_labels(self, painter):
        # set label font 
        font = painter.font()
        font.setPointSize(10)
        painter.setFont(font)
        
        # Calculate grid boundaries including label margins
        grid_start = self.board_margin + self.label_margin
        grid_end = grid_start + (self.board_size - 1) * self.cell_size
        
        # Draw column labels (letters)
        for col in range(self.board_size):
            label = chr(ord('A') + col)
            
            # Skip I since it is not used in Go 
            if ord(label) >= ord('I'):
                label = chr(ord(label)+1)
            # x-coordinates correlates to col   
            x = grid_start + col * self.cell_size
            
            # Bottom labels 
            painter.drawText(
                x - 5, grid_end + self.board_margin - 15, 12, 12, 
                Qt.AlignmentFlag.AlignCenter, label
            )
            
        # Draw row labels (numbers)
        for row in range(self.board_size):
            # Row numbers in ascending order
            label = str(self.board_size - row) 
                            
            y = grid_start + row * self.cell_size
            
            # Left labels 
            painter.drawText(
                self.board_margin - 15 , y -8, 12, 12, 
                Qt.AlignmentFlag.AlignVCenter, label
            )     
            
    # Draw a realistic stone using gradient and shadows        
    def realistic_stones(self, painter, x, y, is_black, alpha=255):
        diameter = self.stone_radius * 2
        
        # Save painter state
        painter.save()
        
        if alpha == 255:
            shadow_colour = QColor(0,0,0,30) # Transparent black
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(shadow_colour))
            # offset by 2 therefore shadow can be seen behind stones
            painter.drawEllipse(x - self.stone_radius + 2 , y - self.stone_radius + 2, diameter, diameter)
            
        # Create gradient for black stone
        if is_black:
            gradient = QRadialGradient(x - self.stone_radius * 0.3, y - self.stone_radius * 0.3, 
                                       self.stone_radius * 2)
            # Gradient affect
            gradient.setColorAt(0, QColor(90,90,90, alpha))
            gradient.setColorAt(0.4, QColor(30,30,30, alpha))
            gradient.setColorAt(1, QColor(0,0,0, alpha))
            
            # Drawing the stone 
            painter.setPen(QPen(QColor(0, 0, 0, alpha), 0.2))
            painter.setBrush(QBrush(gradient))
            painter.drawEllipse(x - self.stone_radius , y - self.stone_radius , diameter, diameter)
            
            # Add a highlight to simulate a reflection on the stone 
            highlight_gradient = QRadialGradient(x - self.stone_radius * 0.4, y - self.stone_radius * 0.4, 
                                     self.stone_radius * 0.8)
            # Fade from semi transparent white to fully transparent 
            highlight_gradient.setColorAt(0, QColor(255,255,255, int(alpha) * 0.35))
            highlight_gradient.setColorAt(1, QColor(255,255,255, 0))
            
            painter.setBrush(QBrush(highlight_gradient))
            painter.drawEllipse(x - self.stone_radius, y - self.stone_radius, diameter, diameter)
            
        else:
            gradient = QRadialGradient(x - self.stone_radius * 0.3, y - self.stone_radius * 0.3, 
                                       self.stone_radius * 2)
            # Gradient affect
            gradient.setColorAt(0, QColor(240,240,240, alpha))
            gradient.setColorAt(0.4, QColor(220,220,220, alpha))
            gradient.setColorAt(1, QColor(160,160,160, alpha))
            
            # Drawing the stone 
            painter.setPen(QPen(QColor(220, 220, 220, 155), 0.5)) # light border
            painter.setBrush(QBrush(gradient))
            painter.drawEllipse(x - self.stone_radius , y - self.stone_radius , diameter, diameter)
            
            # Add a highlight to simulate a reflection on the stone 
            highlight_gradient = QRadialGradient(x - self.stone_radius * 0.4, y - self.stone_radius * 0.4, 
                                    self.stone_radius * 0.8)
            
            # Fade from semi transparent white to fully transparent 
            highlight_gradient.setColorAt(0, QColor(255,255,255, int(alpha * 0.8))) # Shiny effect
            highlight_gradient.setColorAt(1, QColor(255,255,255, 0))
            
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(highlight_gradient))
            painter.drawEllipse(x - self.stone_radius, y - self.stone_radius, diameter, diameter)
            
        # Restore the painter state
        painter.restore()
    
    # Update board with a new state        
    def update_board(self, game_state, current_player=None):
        self.game_state = game_state
        if current_player is not None:
            self.current_player = current_player
            
        self.update()
   
# Main Window for the go game     
class GoGameGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Go Game")
        self.board_size = 9 
        self.game_mode = "PVP"
        
        # Initialise game state 
        self.game_state = GoState.new_game(self.board_size)
        self.bot = None
        
        # Set up the UI 
        self.init_ui()
        
        # Start a new game 
        self.new_game()
        
    # Setting up the user interface 
    def init_ui(self):
        # Main widget and layout 
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        
        # GO board widget
        self.board_widget = GoBoardGUI(board_size=self.board_size)
        self.board_widget.stone_placed.connect(self.place_stone)
        
        # Game controls widget 
        controls_widget = QWidget()
        controls_layout = QVBoxLayout(controls_widget)
        
        # Game mode layout
        mode_layout = QHBoxLayout()
        mode_label = QLabel("Game Mode: ")
        
        self.mode_box = QComboBox()
        self.mode_box.addItems(["Player vs Player", "Player vs Bot"])
        self.mode_box.currentTextChanged.connect(self.change_game_mode)
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_box)
        
        # Board size selection 
        size_layout = QHBoxLayout()
        
        # Player's turn 
        self.status_label = QLabel("Black's turn")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        # Capture display 
        self.capture_label = QLabel("Black: 0 captures | White: 0 captures (+6.5 komi)")
        self.capture_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Game control buttons 
        self.pass_button = QPushButton("Pass turn")
        self.pass_button.clicked.connect(self.handle_pass)
        
        # Add widgets to controls layout 
        controls_layout.addLayout(mode_layout)
        controls_layout.addLayout(size_layout)
        controls_layout.addWidget(self.status_label)
        controls_layout.addWidget(self.capture_label)
        controls_layout.addStretch(1)
        controls_layout.addWidget(self.pass_button)
        
        # Add widgets to main layout
        main_layout.addWidget(self.board_widget, 3) # 3:1 ratio to board controls 
        main_layout.addWidget(controls_widget, 1)
        
        # Set main widget as central
        self.setCentralWidget(main_widget)
        
        
        self.resize(800,600)
        
    # Start a new game 
    def new_game(self):
        self.game_state = GoState.new_game(self.board_size)
        self.update_ui()
        
        # Initialise bot for PVB mode 
        if self.game_mode == "PVB":
            self.bot = MCTsAgent(temperature=1.4, num_rounds=5000)
    
    # Update UI to display current game state    
    def update_ui(self):
        self.board_widget.update_board(self.game_state, self.game_state.next_player)
        
        # Update game status 
        if self.game_state.next_player == Player.black:
            player_name = "Black"
        else: 
            player_name = "White"
            
        self.status_label.setText(f"{player_name}'s turn")
        
        # Updating captures count 
        black_captures = self.game_state.captured[Player.black]
        white_captures = self.game_state.captured[Player.white]
        
        # Add komi variable 
        komi = 6.5
        
        # Update score display
        self.capture_label.setText(f"Black: {black_captures} | White: {white_captures} captures (+{komi})")
        
            
    # Defining method for bot's move
    def bots_move(self):
        if self.bot and not self.game_state.game_over():
            # Calculate bot move
            bot_move = self.bot.select_move(self.game_state)
            self.game_state = self.game_state.play_move(bot_move)
            
            # check if game is over 
            if self.game_state.game_over():
                self.game_over()
                return
                
            # Update UI after the bot has placed move
            self.update_ui()
            
    # Handle stone placement from board widget
    def place_stone(self, row, col):
        # Ignore if the game is over or it is the bot's turn next
        if self.game_state.game_over():
            return

        if self.game_mode == "PVB" and self.game_state.next_player == Player.white:
            return 
        
        # Create move 
        point = Point(row, col)
        move = Move.play(point)
        
        if self.game_state.valid_move(move):
            self.game_state = self.game_state.play_move(move)
            
            # Check if game over after move played
            if self.game_state.game_over():
                self.game_over()
                return
            
            # Update UI immediately after player's move 
            self.update_ui()
            
            # If its the bot's turn, make bot move 
            if (self.game_mode == "PVB" and 
                self.game_state.next_player == Player.white and 
                not self.game_state.game_over()):
                
                 # Show thinking indicator
                self.status_label.setText("White is thinking...")
                
                # Bot's move after UI update
                QTimer.singleShot(50, self.bots_move)
        else:
            self.timed_message("illegal move", "Please enter a legal move", 1500)
            # Update UI 
            self.update_ui()
        
    # Handle pass button 
    def handle_pass(self):
        if not self.game_state.game_over():
            # Player can't return if its bot's move 
            if self.game_mode == "PVB" and self.game_state.next_player == Player.white:
                return 
            
            # Obtain current player 
            current_player = "Black" if self.game_state.next_player == Player.black else "White"
            
            self.game_state = self.game_state.play_move(Move.pass_turn())
            
            # Check if game is over (if theres 2 passes in a row)
            if self.game_state.game_over():
                self.game_over()
                return 
            # If game over then pass noti. isnt displayed
            else: 
                # Display pass notification 
                self.timed_message("Pass", f"{current_player} passed their turn.", 1500)
            
            # Update UI 
            self.update_ui()
        
    # Handle UI when game is over     
    def game_over(self):
        self.update_ui()
        
        scores = self.game_state.final_score()
        
        # Komi 
        komi = 6.5
        
        # Calculating capture scores 
        black_captures = self.game_state.captured[Player.black]
        white_captures = self.game_state.captured[Player.white]
            
        # Calculate territory 
        black_territory = scores['Black'] - black_captures
        white_territory = scores['White'] - white_captures - komi
        
        # Game over messsage displaying the winner 
        if self.game_state.last_move.is_resign:
            if self.game_state.next_player == Player.black:
                winner = "White"
            else: 
                winner = "Black"
                
            display = f"{winner} wins by resignation! "
        
        else:
            if scores["Black"] > scores["White"]:
                display = f"Black wins by {scores['Black'] - scores['White']:.1f} points! \n ({black_captures} captures + {black_territory} territory)"
            elif scores["White"] > scores["Black"]:
                display = f"White wins by {scores['White'] - scores['Black']:.1f} points! \n ({white_captures} captures + {white_territory:} territory + {komi} komi)"
                
        # Display game over message
        QMessageBox.information(self, "Game Over", display)
        
        # Restart game once the display is closed 
        self.new_game()
        
    def timed_message(self, title, message, duration):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Close) # Close button for manual input
        
        # Set box to focus 
        msg_box.setModal(True)
        
        # Display box 
        msg_box.show()
        
        # Message closes after timer
        QTimer.singleShot(duration, msg_box.close)
        
        
    # Change between PVP & PVB 
    def change_game_mode(self, mode_text):
        if "Player VS Player" in mode_text:
            self.game_mode = "PVP"
        else:
            self.game_mode = "PVB"
            
        # Start new game with selection game mode
        self.new_game()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GoGameGUI()
    window.show()
    sys.exit(app.exec()) 
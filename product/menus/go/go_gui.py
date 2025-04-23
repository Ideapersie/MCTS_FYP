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
        self.min_cell_size = 48
        self.cell_size = self.min_cell_size
        
        # ratio to change during resizing
        self.board_margin_ratio = 0.1
        self.label_margin_ratio = 0.03
        
        # Extra margin for coordinates
        self.board_margin = int(400*self.board_margin_ratio)
        self.label_margin = int(400*self.label_margin_ratio)

        self.stone_radius = int(self.cell_size * 0.38)
        
        # Set fixed size for the board 
        self.setMinimumSize(400, 400)
        
        # Set size policy to expand
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

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
                        
        # Draw indicator for the last placed stone 
        if self.game_state.last_move is not None and self.game_state.last_move.is_play:
            last_point = self.game_state.last_move.point
            
            # get the coordinates of the last stone
            x = grid_start + (last_point.col - 1) * self.cell_size
            y = grid_start + (self.board_size - last_point.row) * self.cell_size
            
            # Player who placed the last stone
            last_player = self.game_state.board.get_player(last_point)
            
            painter.setPen(Qt.PenStyle.NoPen)
            # Calculat the size of the dot 
            dot_size = self.stone_radius * 0.65
            
            if last_player == Player.black:
                # semi-transparent white dot
                painter.setBrush(QBrush(QColor(255, 255, 255, 230)))
            else:
                # Draw a small black dot for white stone
                painter.setBrush(QBrush(QColor(0, 0, 0, 200)))
            
            # position relative to dot 
            dot_x = x - (dot_size / 2)
            dot_y = y - (dot_size / 2) 
                
            painter.drawEllipse(dot_x, dot_y, dot_size, dot_size)   
             
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
                x - 5, grid_end + 25, 12, 12, 
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
        main_widget.setStyleSheet(f"background-color: {"rgb(236, 197, 125)"};")
        
        # GO board widget
        self.board_widget = GoBoardGUI(board_size=self.board_size)
        self.board_widget.stone_placed.connect(self.place_stone)
        
        # Game controls widget 
        controls_widget = QWidget()
        controls_layout = QVBoxLayout(controls_widget)
        
        
        # Game mode layout 
        mode_group = QGroupBox("Game Mode")
        mode_group.setStyleSheet("QGroupBox { font-size: 16px; font-weight: bold;}")

        # Create radio buttons for game modes
        self.pvp_radio = QRadioButton("Player vs Player")
        self.pvb_radio = QRadioButton("Player vs Bot")
        self.pvp_radio.setStyleSheet("font-size: 14px; padding: 5px;")
        self.pvb_radio.setStyleSheet("font-size: 14px; padding: 5px;")

        # Create button group for radio buttons
        mode_button_group = QButtonGroup(self)
        mode_button_group.addButton(self.pvp_radio)
        mode_button_group.addButton(self.pvb_radio)
        mode_button_group.buttonClicked.connect(self.change_game_mode)

        # Set default selection
        self.pvp_radio.setChecked(True)
        
        mode_layout = QVBoxLayout(mode_group)
        # Add to layout
        mode_layout.addWidget(self.pvp_radio)
        mode_layout.addWidget(self.pvb_radio)

        # Add to the top of the controls layout
        controls_layout.addWidget(mode_group)
        
        # Board size selection 
        size_layout = QHBoxLayout()
        
        # Player's turn 
        self.status_label = QLabel("Black's turn")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        # Capture display 
        self.capture_label = QLabel("Black: 0 captures | White: 0 captures (+6.5 komi)")
        self.capture_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.capture_label.setStyleSheet("font-size: 14px;")

        wooden_style = """
            QPushButton {
                background-color: #b38c50;
                color: white;
                border: 2px solid #704214;
                border-radius: 5px;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c39c60;
            }
            """
            
        darken_wooden_style = """
            QPushButton {
                    background-color: #785114;
                    color: white;
                    border: 2px solid #704214;
                    border-radius: 5px;
                    padding: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #c39c60;
                }
            """
            
        # Game control buttons 
        self.pass_button = QPushButton("Pass turn")
        self.pass_button.clicked.connect(self.handle_pass)
        self.pass_button.setStyleSheet(wooden_style)
        
        # Resign button
        self.resign_button = QPushButton("Resign")
        self.resign_button.clicked.connect(self.handle_resign)
        self.resign_button.setStyleSheet(wooden_style)
        
        # New game button
        self.new_game_button = QPushButton("Start a new game!")
        self.new_game_button.clicked.connect(self.new_game)
        self.new_game_button.setStyleSheet(darken_wooden_style)
        
        # Hide new game button until game is over
        self.new_game_button.setVisible(False) 
        
        # Add widgets to controls layout 
        controls_layout.addLayout(size_layout)
        controls_layout.addWidget(self.status_label)
        controls_layout.addWidget(self.capture_label)
        controls_layout.addStretch(1)
        controls_layout.addWidget(self.new_game_button)
        
        #Add spacing between buttons
        controls_layout.addSpacing(20) 
        
        controls_layout.addWidget(self.pass_button)
        controls_layout.addWidget(self.resign_button)
        
        # Add widgets to main layout
        main_layout.addWidget(self.board_widget, 3) # 3:1 ratio to board controls 
        main_layout.addWidget(controls_widget, 1)
        
        # Set main widget as central
        self.setCentralWidget(main_widget)
        
        
        self.resize(800,600)
        
    # Start a new game 
    def new_game(self):
        # Initialise bot for PVB mode 
        if self.game_mode == "PVB":
            self.bot = MCTsAgent(temperature=1.4, num_rounds=5000)
        else: 
            self.bot = None
        # Reset game state
        self.game_state = GoState.new_game(self.board_size)
        self.update_ui()
        # Hide new game button until game is over
        self.new_game_button.setVisible(False)
    
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
        if self.bot and self.game_mode == "PVB" and not self.game_state.game_over():
            # Calculate bot move
            bot_move = self.bot.select_move(self.game_state)
            # Check if the bot's move is a pass 
            is_pass = bot_move.is_pass
            
            self.game_state = self.game_state.play_move(bot_move)
            
            # Display popup message if the bot passes
            if is_pass:
                self.timed_message("Pass"," White passed their turn.", 1500)
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
            # Ignore player input if it's the bot's turn
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
            self.schedule_bot_move()
                
        # Specify the error message, hide hover point         
        elif self.game_state.ko_rule(self.game_state.next_player, move):
            self.board_widget.hover_point = None
            # Update UI 
            self.board_widget.update()
            
            self.timed_message("Please enter a legal move", "This move violates the Ko-rule", 2000)
        
        elif self.game_state.self_capture(self.game_state.next_player, move):
            self.board_widget.hover_point = None
            # Update UI 
            self.board_widget.update()
            
            self.timed_message("Please enter a legal move", "This move is a self-capture move", 2000)
        # Incase some other error 
        else: 
            self.board_widget.hover_point = None
            # Update UI 
            self.board_widget.update()
            
            self.timed_message("illegal move", "Please enter a legal move", 2000)
        
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
            
            if self.game_mode == "PVB" and self.bot is not None:
                # Trigger bot's move even after player passes
                QTimer.singleShot(1500, self.schedule_bot_move)
            
    def handle_resign(self):
        if not self.game_state.game_over():
            # Create resign move
            resign_move = Move.resign()
            
            # Play resign move
            self.game_state = self.game_state.play_move(resign_move)

            # call game over method to handle UI            
            self.game_over()
            
                
    # Schedule bot's turn while display indicator             
    def schedule_bot_move(self):
        if (self.game_mode == "PVB" and
                self.bot is not None and # Check if bot is initialised
                self.game_state.next_player == Player.white and 
                not self.game_state.game_over()):
                
                # Show thinking indicator
                self.status_label.setText("White is thinking...")
                
                # Bot's move after UI update
                QTimer.singleShot(50, self.bots_move)
        
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
                winner = "Black"
            else: 
                winner = "White"
                
            display = f"{winner} wins by resignation! "
        
        else:
            if scores["Black"] > scores["White"]:
                display = f"Black wins by {scores['Black'] - scores['White']:.1f} points! \n ({black_captures} captures + {black_territory} territory)"
            elif scores["White"] > scores["Black"]:
                display = f"White wins by {scores['White'] - scores['Black']:.1f} points! \n ({white_captures} captures + {white_territory:} territory + {komi} komi)"
                
        # Display game over message
        self.game_over_message(display)
        
    # Display message box for a certain duration and closes after
    def timed_message(self, title, message, duration):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Close) # Close button for manual input
        
        # Makes dialog resizable
        msg_box.setWindowFlags(msg_box.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint)
        
        # Set min. size for scalability     
        msg_box.setMinimumSize(400, 200)
        msg_box.resize(400, 200)
        
        # Set box to focus 
        msg_box.setModal(True)
        
        # Display box 
        msg_box.show()
        
        # Message closes after timer
        QTimer.singleShot(duration, msg_box.close)
        
    # Game over message when the new game only starts if the button is clicked
    def game_over_message(self, message):
        game_over_box = QMessageBox(self)
        game_over_box.setText(message)
        # Display game over message
        game_over_box.setWindowTitle("Game Over!")
        game_over_box.setInformativeText("Click New Game to start a new game.")
        
        new_game_button = game_over_box.addButton("New Game", QMessageBox.ButtonRole.AcceptRole)
        exit_button = game_over_box.addButton("Exit", QMessageBox.ButtonRole.RejectRole)
        
        # Make dialog resizable
        game_over_box.setWindowFlags(game_over_box.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint)
        
        # Set min. size for scalability     
        game_over_box.setMinimumSize(1000, 500)
        game_over_box.resize(1000, 500)
        
        # Set box to focus but allow interaction with the main window
        game_over_box.setModal(False)
        
        game_over_box.finished.connect( 
            lambda result: self.handle_game_over(game_over_box, new_game_button))
        
        # Display box 
        game_over_box.show()
        
        # Display new game button when game is over
        self.new_game_button.setVisible(True)
                
    # only start new game if the button is clicked
    def handle_game_over(self, dialog, new_game_button):
        if dialog.clickedButton() == new_game_button:
            self.new_game()
        
    # Change between PVP & PVB 
    def change_game_mode(self, mode_text):
        #if "Player vs Player" in mode_text:
        if mode_text.text() == "Player vs Player":
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
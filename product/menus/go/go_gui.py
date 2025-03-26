from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QMainWindow, QPushButton, QApplication, QVBoxLayout, QHBoxLayout, QSpinBox, QComboBox, QSlider, QCheckBox, QGroupBox, QRadioButton, QButtonGroup
from PySide6.QtGui import QPainter, QPen, QColor, QBrush

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
        self.stone_radius = int(self.cell_size * 0.4)
        
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
                player = GoState.game_state.board.get_player(point)
            
                if player is not None:
                    x = grid_start + (row -1) * self.cell_size
                    y = grid_start + (col -1) * self.cell_size
                    
                    if player == Player.black:
                        painter.setBrush(Qt.GlobalColor.black)
                    else:
                        painter.setBrush(Qt.GlobalColor.white)
                        
                    painter.setPen(Qt.GlobalColor.black)
                    painter.drawEllipse(x - self.stone_radius, y - self.stone_radius,
                                        self.stone_radius * 2, self.stone_radius * 2)
         
        # Draw hover indicator for empty points
        if self.hover_point is not None:
            row, col = self.hover_point
            point = Point(row,col)
            
            current_player = GoState.game_state.board.get_player(point)
            
            # only hover for empty points
            if current_player is None:
                x = grid_start + (row -1) * self.cell_size
                y = grid_start + (col -1) * self.cell_size
                
                # semi-transparent stones for hover effects 
                if self.current_player == Player.black:
                    painter.setBrush(QColor(0,0,0, 100))
                else: 
                    painter.setBrush(QColor(255, 255, 255, 100))
                    
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(x - self.stone_radius, y - self.stone_radius,
                                        self.stone_radius * 2, self.stone_radius * 2)
                
             
    # Track mouse movement           
    def mouseMoveEvent(self, event):
        x = event.position().x() - (self.board_margin + self.label_margin)
        y = event.position().y() - (self.board_margin + self.label_margin)
        
        col = round(y / self.cell_size) + 1
        row = round(x/ self.cell_size) + 1
        
        # Update hover points if changed 
        if self.hover_point != (row, col):
            self.hover_point = (row,col)
            self.update() # Repaint the hover
    
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
                
            y = grid_start + col * self.cell_size
            
            # Bottom labels 
            painter.drawText(
                y , self.board.margin, 10, 10, 
                Qt.AlignmentFlag.AlignCenter, label
            )
            
        # Draw row labels (numbers)
        for row in range(self.board_size):
            label = row + 1 
                            
            x = grid_start + row * self.cell_size
            
            # Left labels 
            painter.drawText(
                self.board.margin , y , 10, 10, 
                Qt.AlignmentFlag.AlignVCenter, label
            )     
    
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
        
    # Start a new game 
    def new_game(self):
        self.game_state = GoState.new_game(self.board_size)
        self.update_ui()
        
        # Initialise bot for PVB mode 
        if self.game_mode == "PVB":
            self.bot = MCTsAgent(temperature=1.4, num_rounds=5000)
        
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GoGameGUI()
    window.show()
    sys.exit(app.exec()) 
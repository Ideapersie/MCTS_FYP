import PySide6.QtCore, PySide6.QtGui, PySide6.QtWidgets

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton


from menus.go.goboard import Player, Move, GoState
from menus.go.goplayer import Point
from menus.go.agent.random import MCTsAgent

print(PySide6.QtCore.__version__)

# Widget to display and interact with the Go board
class GoBoard(QWidget):
    # Signal when a stone is placed 
    stone_placed = Signal(int,int)
    
    def _init_(self, board_size=9, parent=None):
        super().__init__(parent)
        self.board_size = board_size
        # Size of each cell in pixels 
        self.cell_size = 40
        self.board_margin = 40 
        self.stone_radius = int(self.cell_size * 0.4)
        
        # Set fixed size for the board 
        board_pixels = (self.board_size - 1) * self.cell_size + 2 * self.board_margin
        self.setMinimumSize(board_pixels, board_pixels)
        self.setMaximumSize(board_pixels, board_pixels)

        # point where the point is hovering
        self.hover_point = None
        
        # Set mouse tracking for hovering effects
        self.setMouseTracking(True)
        
        
if __name__ == '__main__':
    pass
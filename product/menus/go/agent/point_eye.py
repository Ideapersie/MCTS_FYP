from go.goplayer import Point,Player
from go.goboard import Board

def is_point_eye(board, point, colour):
    # Check if point is empty
    if board.get_player(point) is not None:
        return False
    
    # Check if all surrounding points are of the same colour
    for neighbour in point.neighbours():
        if board.in_grid(neighbour):
            if board.get_player(neighbour).value != colour.value:
                return False
        
    # Check adjacent corners
    corners = [
        Point(point.row - 1, point.col - 1),
        Point(point.row - 1, point.col + 1),
        Point(point.row + 1, point.col - 1),
        Point(point.row + 1, point.col + 1),
    ]    
    
    # Count the friendly adjacent corners
    friendly_corners = 0
    off_board_corners = 0
    # For empty corners
    empty_corners = 0
    
    for corner in corners:
        if board.in_grid(corner):
            corner_player = board.get_player(corner)
            # Check if corner is empty, if empty then .value doesnt work 
            if corner_player is None:
                empty_corners += 1
            elif corner_player.value == colour.value:
                friendly_corners += 1
        else:
            off_board_corners += 1
    
    # If there are off board corners, then all corners must be friendly  
    if off_board_corners > 0:
        return off_board_corners + friendly_corners == 4
    # Else, at least 3 corners must be friendly
    return friendly_corners >= 3

from go.gotypes import Point

def is_point_an_eye(board, point, colour):
    if board.get(point) is not None:
        return False 
    
    # All adjacent points must contain friendly stones 
    for neighbour in point.neighbours():
        if board.is_on_grid(neighbour):
            neighbour_colour = board.get(neighbour)
            if neighbour_colour != colour:
                return False 
            
    friendly_corners = 0 
    off_board_corners = 0 
    corners = [
        Point(point.row - 1, point.col - 1),
        Point(point.row - 1, point.col + 1),
        Point(point.row + 1, point.col - 1),
        Point(point.row + 1, point.col + 1)
    ]
    
    for corner in corners:
        if board.is_on_grid(corner):
            corner_colour = board.get(corner)
            if corner_colour == colour:
                friendly_corners += 1 
            else:
                off_board_corners += 1 
                
        
    if off_board_corners > 0:
        return off_board_corners + friendly_corners == 4 # point is on the edge or corner 
    return friendly_corners >=3  # point is in the middle 
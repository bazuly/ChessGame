import pygame as pg
import chess_engine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def load_images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = pg.image.load('images/' + piece + '.png'), (SQUARE_SIZE, SQUARE_SIZE)  # set image size


""" main function """


def main():
    pg.init()
    # pygame documentation
    screen = pg.display.set_mode((HEIGHT, WIDTH))
    clock = pg.time.Clock()
    screen.fill(pg.Color('white'))
    gs = chess_engine.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False
    load_images()
    run_game = True
    sq_Selected = ()
    player_clicks = []
    while run_game:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run_game = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos()  # x, y mouse location
                col = location[0] // SQUARE_SIZE  # x
                row = location[1] // SQUARE_SIZE  # y
                if sq_Selected == (row, col):  # if user clicked the same square twice
                    sq_Selected = ()  # deselect square
                    player_clicks = []
                else:
                    sq_Selected = (row, col)
                    player_clicks.append(sq_Selected)
                if len(player_clicks) == 2:
                    move = chess_engine.Move(player_clicks[0], player_clicks[1], gs.board)
                    print(move.get_chess_notation())
                    # if move in valid_moves:
                    for each in range(len(valid_moves)):
                        if move == valid_moves[each]:
                            gs.make_move(move)
                            move_made = True
                            sq_Selected = ()
                            player_clicks = []
                    if not move_made:
                        player_clicks = [sq_Selected]

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    gs.undo_move()
                    move_made = True
        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        pg.display.flip()


""" Draw board and pieces """


def drawGameState(screen, gs):
    drawboard(screen)
    drawpieces(screen, gs.board)


def drawboard(screen):
    colors = [pg.Color('white'), pg.Color('brown')]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]
            pg.draw.rect(screen, color, pg.Rect(row * SQUARE_SIZE, column * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def drawpieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[column][row]
            if piece != '--':
                pg_rect = pg.Rect(row * SQUARE_SIZE, column * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                screen.blit(IMAGES[piece][0], pg_rect)


if __name__ == '__main__':
    main()

from ui import draw
from game import Game


def main() -> None:
    game = Game.new()

    while True:
        draw(game.player, game.enemy, game.game_over, game.screen)
        line = input("\n> ")

        game.step(line)

        if game.should_quit:
            draw(game.player, game.enemy, game.game_over, game.screen)
            break


if __name__ == "__main__":
    main()

import collections
import intcpu

import arcade
import pyglet


class Arcade:
    def __init__(self, src):
        self.cpu = intcpu.IntCpu()
        self.src = src
        self.cpu.load(src)

        self.world = {}
        self.score = 0

    def resume(self, d):
        self.cpu.add_input(d)
        self.cpu.resume()

    def step(self):
        ret = self.cpu.step()
        if self.cpu.pending_output() >= 3:
            x = self.cpu.pop_output()
            y = self.cpu.pop_output()
            d = self.cpu.pop_output()
            if x == -1 and y == 0:
                self.score = d
            else:
                self.world[(x, y)] = d
        if ret == 5:
            return 2
        if ret != 0:
            return 1
        return 0


class Game(arcade.Window):
    def __init__(self, width, height, title, src):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.AMAZON)
        self.dir = 0
        self.engine = Arcade(src)
        self.engine.cpu.write(0, 2)
        self.delta = 0

    def setup(self):
        while self.engine.step() == 0:
            pass

    def on_draw(self):
        arcade.start_render()
        w = 20
        cmap = {
            1: arcade.color.ASH_GREY,
            2: arcade.color.AUBURN,
            3: arcade.color.CYAN
        }
        for (x, y), d in self.engine.world.items():
            if d in [1, 2, 3]:
                arcade.draw_lrtb_rectangle_filled(w * x, w * x + (w - 1),
                                                  w * y, w * y - (w - 1),
                                                  cmap[d])
            if d == 4:
                arcade.draw_circle_filled(w * x, w * y, w // 2,
                                          arcade.color.YELLOW)

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.LEFT:
            self.dir = -1
        elif key == arcade.key.RIGHT:
            self.dir = 1

    def on_update(self, delta_time):
        self.delta += delta_time
        if self.delta > 1:
            self.delta = 0
            self.engine.resume(self.dir)
            self.dir = 0
            while True:
                r = self.engine.step()
                if r == 2:
                    break
                if self.engine.step() == 1:
                    pyglet.app.exit()
                    return


def part_1(src):
    src = intcpu.parse_tape(open(src).readline().strip())
    game = Arcade(src)
    while game.step() == 0:
        pass
    print("part 1:", collections.Counter(game.world.values())[2])


def part_2(src):
    w, h = 800, 600
    src = intcpu.parse_tape(open(src).readline().strip())
    game = Game(w, h, "Advent Breaker", src)
    game.setup()
    arcade.run()


def main():
    part_1('../assets/day13-input')
    part_2('../assets/day13-input')


if __name__ == "__main__":
    main()

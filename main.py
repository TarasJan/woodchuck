from collections import deque
from enum import Enum 
import random
import math
import pyxel

SCREEN_WIDTH = 255
SCREEN_HEIGHT = 255

FONT_WIDTH = 4
FONT_HEIGHT = 6

TITLE = "Woodchuck SIM"
SUBTITLE = "PRESS ENTER TO BEGIN"
TITLE_OFFSET_Y = -SCREEN_HEIGHT // 8
TITLE_X = (SCREEN_WIDTH - len(TITLE)*FONT_WIDTH) // 2
TITLE_Y = (SCREEN_HEIGHT- FONT_HEIGHT) // 2 + TITLE_OFFSET_Y

def multi_btnp(*keys):
    return any([pyxel.btnp(key) for key in keys])

def center_text(text, color =7, offset=None):
    if offset:
        offset_x, offset_y = offset
    else:
        offset_x, offset_y = (0, 0)
    
    x = (SCREEN_WIDTH - len(text)*FONT_WIDTH) // 2 + offset_x
    y = (SCREEN_HEIGHT- FONT_HEIGHT) // 2 + offset_y
    pyxel.text(x, y, text, color)


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, caption="Woodchuck")

        pyxel.image(0).load(0, 0, "assets/background.png")
        pyxel.image(1).load(0, 0, "assets/branch.png")
        pyxel.image(2).load(0, 0, "assets/axe.png")

        self.tree = False
        self.set_mode('start')

        # chuck 
        pyxel.sound(2).set(
            "g1g0rr", "p", "7532", "vfff", 25
        )

        #fail
        pyxel.sound(1).set(
            "g3a0a0", "t", "466", "nff", 25
        )

        pyxel.run(self.update, self.draw)

    def draw(self):
        self.disp_background()
        self.disp_game()
        self.disp_gui()

    def disp_background(self):
        pyxel.cls(8)
        if self.draw_background:
            pyxel.blt(0, 0, 0, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    def disp_game(self):
        if self.mode == 'playing':
            self.disp_tree()
            self.disp_axe()

    def disp_branch(self, right, height):
        if right:
            x = SCREEN_WIDTH//2-44
        else:
            x = -7
        pyxel.blt(x, height, 1, 0, 0, -186 + right * 372, 60, colkey=0)

    def disp_tree(self):
        tree_size = len(self.tree)
        for i in range(0, tree_size):
            self.disp_branch(self.tree[tree_size -i -1], -16 + 48 * i)

    def disp_axe(self):
        pyxel.blt(20 + self.axe_right*85, SCREEN_HEIGHT//2 + 18, 2, 0, 0, 140 - 280 * self.axe_right, 25, colkey=0)

    def disp_gui(self):
        if self.mode == 'start':
            center_text(TITLE, 7, offset=(0, TITLE_OFFSET_Y))
            center_text(SUBTITLE, pyxel.frame_count % 15 + 1)
        if self.mode == 'playing':
            self.disp_score()
            self.disp_bar()
        if self.mode == 'game_over':
            message = 'You scored {} points. Press ENTER to start again'.format(self.score)
            center_text('GAME OVER', 7, offset=(0, TITLE_OFFSET_Y))
            center_text(message, 7)
            center_text('Press Q to exit', 7, offset=(0, -TITLE_OFFSET_Y) )

    def disp_bar(self):
        delta = int(195 * self.percent/100)
        pyxel.rect(30, 200, 30 + delta, 220, 8)
        pyxel.text(30 + delta // 2, 207, '{:.2f}'.format(self.percent), 1)

    def disp_score(self):
        pyxel.text(5, 5, "Score: {}".format(self.score), 7)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.gameplay_inputs()
        self.gameplay_updates()
        self.gui_inputs()

    def gameplay_inputs(self):
        if self.mode == 'playing':
            if pyxel.btnp(pyxel.KEY_A):
                self.chop_left()
            if pyxel.btnp(pyxel.KEY_D):
                self.chop_right()

    def gui_inputs(self):
        for mode in ['game_over', 'start']:
            if self.mode == mode and pyxel.btnp(pyxel.KEY_ENTER):
                self.set_mode('playing')
    
    def gameplay_updates(self):
        self.percent -= 0.013 * math.sqrt(self.score)

    def chop(self, right):
        pyxel.play(1, 1)
        self.axe_right = right
        self.grow_tree()
        self.evaluate_axe()
    
    def chop_left(self):
        self.chop(False)
    
    def chop_right(self):
        self.chop(True)

    def grow_tree(self):
        self.tree.popleft()
        self.tree.append(random.choice([True, False]))
    
    def evaluate_axe(self):
        if self.tree[2] == self.axe_right:
            self.set_mode('game_over')
        else:
            self.score +=1

    def set_mode(self, mode):
        self.mode = mode
        if self.mode in ['start', 'playing']:
            self.draw_background = True
            self.score = 0
            self.percent = 100.0
            self.tree = deque([random.choice([True, False]) for i in range(0,6)])
            self.axe_right = not self.tree[2]
        elif self.mode == 'game_over':
            self.draw_background = False
            pyxel.play(2, 1)

if __name__ == '__main__':
    App()
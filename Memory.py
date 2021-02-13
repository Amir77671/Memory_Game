import functools
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore
import random

# number of images in game
NUMBER_OF_IMAGES = 8


class Game(QWidget):

    def __init__(self, number_of_buttons=16):
        super().__init__()

        self.window = QWidget()
        self.buttons = []
        self.buttons_images = {}
        self.number_of_buttons = number_of_buttons
        self.firstclick = 0
        self.secondclick = 0
        self.matches = 0
        self.clickedbuttons = []
        self.button1 = None
        self.button2 = None
        self.allowclick = True

    def init_window(self, game_name="Memory game", starting_x=100, starting_y=100, width=800, height=600):
        self.window.setWindowTitle(game_name)
        self.window.setGeometry(starting_x, starting_y, width, height)
        helloMsg = QLabel('<h1>Find the matching pairs</h1>', parent=self.window)
        helloMsg.move(250, 10)

    def create_buttons(self, number_of_buttons=16):
        row = 0
        col = 1
        for i in range(1, number_of_buttons + 1):
            button = QPushButton("", self.window)
            button.setGeometry(100+(col * 100) + 20,100+ (row * 100), 100, 100)
            self.buttons.append(button)

            if i % 4 == 0:
                row += 1
                col = 0
            col += 1
    # create single use function for assigning image
    def assign_images(self):
        # create indexes from 1 to 16
        image_list = [i for i in range(1, (NUMBER_OF_IMAGES) * 2 + 1)]

        # iterate over all buttons
        for button in self.buttons:

            # pick random index
            random_index = random.choice(image_list)

            # remove from list
            image_list.remove(random_index)

            # normalize index
            if random_index > 8:
                random_index -= 8

            # assign button to image index
            self.buttons_images[button] = random_index

    def hide_all_images(self):
        for i in range(0, self.number_of_buttons):
            self.buttons[i].setStyleSheet("background:silver;")

    def hide_image(self, button_index):
        if button_index == None:
            return
        button_index.setStyleSheet("background:silver;")

    def assignvalues(self, index):
        if self.allowclick:
            self.allowclick = False
            # button clicked
            current_button = self.buttons[index]

            # show image assigned to button
            current_button.setStyleSheet(
                f"border-image: url({self.buttons_images[current_button]}.jpg) 0 0 0 0 stretch stretch")

            self.clickedbuttons.append(current_button)

            if len(self.clickedbuttons) == 2:
                if self.clickedbuttons[0] == self.clickedbuttons[1]:
                    self.clickedbuttons.pop(-1)
                    self.allowclick = True
                    print("Don't push the same button!")
                    return
                loop = QtCore.QEventLoop()
                QtCore.QTimer.singleShot(500, loop.quit)
                loop.exec_()
                self.match()
                self.clickedbuttons = []
            self.allowclick = True

    def click(self):
        for i in range(self.number_of_buttons):
            self.buttons[i].clicked.connect(functools.partial(self.assignvalues, index=i))

    def match(self):
        if self.buttons_images[self.clickedbuttons[0]] == self.buttons_images[self.clickedbuttons[1]]:
            print("Match!")
            self.matches += 1

        else:
            # if unmatched , the buttons are re-hidden again
            self.hide_image(self.clickedbuttons[0])
            self.hide_image(self.clickedbuttons[1])

        if self.matches == 8:
            self.finished()

    def finished(self):
        if (self.matches == 8):
            self.app.exit(0)

    def run(self):

        self.init_window()
        self.create_buttons()
        self.assign_images()
        self.hide_all_images()
        self.click()
        self.window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    game.run()
    sys.exit(app.exec_())



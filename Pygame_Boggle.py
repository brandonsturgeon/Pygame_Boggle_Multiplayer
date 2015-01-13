# Python Boggle
# Brandon Sturgeon

import random
import string
import pygame


# Creates the tiles that display letters and respond to being hovered/clicked
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, letter, font):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 100))
        self.color = (182, 192, 210)
        self.pos = pos
        self.rect = pygame.Rect(((pos[0]*120)+10, (pos[1]*120)+10), self.image.get_size())
        self.letter = letter
        self.letter_image = font.render(self.letter.upper(), 1, (255, 255, 255))

        self.update()

    def update(self):
        # Fill and then blit the letter
        self.image.fill(self.color)
        blit_x = (self.image.get_width() / 2) - (self.letter_image.get_width() / 2)
        blit_y = (self.image.get_height() / 2) - (self.letter_image.get_height() / 2)
        self.image.blit(self.letter_image, (blit_x, blit_y))

    def rotate(self):
        self.pos =  4-self.pos[1], self.pos[0]
        self.rect = pygame.Rect(((self.pos[0]*120)+10, (self.pos[1]*120)+10), self.image.get_size())


class Game():
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.game_window = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Boggle")
        self.tile_container = pygame.Surface((600, 600))
        self.tile_container_rect = pygame.Rect((0, 0), self.tile_container.get_size())
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_pos = (0, 0)
        self.score = 0
        self.dictionary = open("2of12inf.txt")
        self.dictionary = set([x.strip() for x in self.dictionary])
        self.bound_box = pygame.Rect((0, 0), self.tile_container.get_size())

        # Lengthy surface creations
        self.word_container = pygame.Surface((400, 600))
        self.word_container_rect = pygame.Rect((0, 600), self.word_container.get_size())
        self.word_font = pygame.font.Font(None, 30)
        self.new_game_button = pygame.Surface((100, 25))
        self.new_game_button.fill((0, 0, 255))
        self.new_game_text = self.word_font.render("New Game", 1, (255, 0, 0))
        self.new_game_button.blit(self.new_game_text, ((self.new_game_button.get_width()/2) -
                                                       (self.new_game_text.get_width()/2),
                                                       (self.new_game_button.get_height()/2) -
                                                       (self.new_game_text.get_height()/2)))
        self.new_game_button_rect = pygame.Rect((self.game_window.get_width() - self.new_game_button.get_width(),
                                                 self.game_window.get_height() - self.new_game_button.get_height()),
                                                self.new_game_button.get_size())
        self.rotate_button = pygame.Surface((100, 25))
        self.rotate_button.fill((0, 0, 255))
        self.rotate_text = self.word_font.render("Rotate", 1, (255, 0, 0))
        self.rotate_button.blit(self.rotate_text, ((self.rotate_button.get_width()/2) -
                                                   (self.rotate_text.get_width()/2),
                                                   (self.rotate_button.get_height()/2) -
                                                   (self.rotate_text.get_height()/2)))
        self.rotate_button_rect = pygame.Rect((600, self.game_window.get_height() - self.new_game_button.get_height()),
                                               self.rotate_button.get_size())
        self.words = []

        self.tiles = pygame.sprite.Group()
        self.playing = True

        self.gen_tiles()
        self.game_loop()

    # Main game loop
    def game_loop(self):
        submit_word = []
        while self.playing:
            events = pygame.event.get()
            mousebutton = pygame.mouse.get_pressed()
            for event in events:

                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.playing = False
                    return

                if event.type == pygame.MOUSEMOTION:
                    self.mouse_x, self.mouse_y = event.pos
                    self.mouse_pos = (self.mouse_x, self.mouse_y)

                # Check for collisions and the update the color of the Tiles
                if mousebutton[0] == 1:
                    if self.tile_container_rect.collidepoint(self.mouse_pos):
                        for tile in self.tiles:
                            if tile.rect.collidepoint(self.mouse_pos) and self.bound_box.collidepoint(self.mouse_pos):
                                # Create bound_box to be 3x3 grid around the currently selected tile to prevent cheats
                                self.bound_box = pygame.Rect((tile.rect.x - tile.image.get_width() - 20,
                                                             tile.rect.y - tile.image.get_height() - 20),
                                                            (tile.image.get_width()*3 + (20*2),
                                                             tile.image.get_height()*3 + (20*2)))
                                if tile not in submit_word:
                                    submit_word.append(tile)
                                    tile.color = (132, 142, 160)

                    # New Game
                    if self.new_game_button_rect.collidepoint((self.mouse_x, self.mouse_y)):
                        self.score = 0
                        self.words = []
                        self.tiles = pygame.sprite.Group()
                        self.gen_tiles()
                        self.game_loop()

                    # Rotate board clockwise
                    elif self.rotate_button_rect.collidepoint((self.mouse_x, self.mouse_y)):
                        for t in self.tiles:
                          t.rotate()

                # Mouse is lifted up, check the word
                if event.type == pygame.MOUSEBUTTONUP:
                    self.bound_box = pygame.Rect((0, 0), self.tile_container.get_size())
                    for tile in self.tiles:
                        tile.color = (182, 192, 210)
                    self.check_word(submit_word)
                    submit_word = []

            # Blitting
            self.tile_container.fill((69, 82, 104))
            self.word_container.fill((28, 38, 60))
            self.game_window.fill((0, 0, 0))
            self.tiles.update()
            self.tiles.draw(self.tile_container)
            self.display_words()
            self.game_window.blit(self.tile_container, (0, 0))
            self.game_window.blit(self.word_container, (600, 0))
            self.game_window.blit(self.new_game_button, (self.new_game_button_rect.x, self.new_game_button_rect.y))
            self.game_window.blit(self.rotate_button, (self.rotate_button_rect.x, self.rotate_button_rect.y))
            pygame.display.flip()
            self.clock.tick(60)

    # Generates all of the tiles
    def gen_tiles(self):
        font = pygame.font.Font(None, 75)
        r_letter = ""
        print "Generating Tiles..."

        # Keeps track of all the letters we've used, puts a limit of 2 on each letter
        # Note that some consonants start at 1, so that we're even less likely to generate it
        letter_dict = {"q": 1, "x": 1, "a": -2, "e": -2, "i": -2, "o": -2, "u": -2}
        y_val = 0
        for y in range(5):
            x_val = 0
            for x in range(5):

                # Limit 2 of each consonant, uses dictionaries.
                while True:
                    # Approximate letter distribution based on a study of 500,000 English words
                    r_letter = random.choice(('eeeeeeeeeeeetttttttttaaaaaaaaooooooooiiiiiiinnnnnnn'
                                              'ssssssrrrrrrhhhhhhddddllluuucccmmmffyywwggppbvkxqjz'))

                    # If we haven't used the letter before, add it to the dictionary
                    if r_letter not in letter_dict.keys():
                        letter_dict[r_letter] = 1
                        break
                    # If we have, add 1
                    elif letter_dict[r_letter] < 2:
                        letter_dict[r_letter] += 1
                        break

                # Create the Tile
                self.tiles.add(Tile((x_val, y_val), r_letter, font))
                x_val += 1
            y_val += 1

        print "Generation Complete!"

    # Checks to see if the word is valid
    def check_word(self, tile_list):
        letter_list = [x.letter.lower() for x in tile_list]
        word = "".join(letter_list)

        # Adds word to the confirmed word list and updates score
        if word in self.dictionary and len(word) > 2:
            if word not in self.words:
                self.words.append(word)
                self.score += len(word)

    # Displays all of the valid words entered
    def display_words(self):
        y_value = 10
        x_value = 5

        # Gets the biggest words so we can highlight it
        if len(self.words) > 0:
            maxword = max(self.words, key=len)
        else:
            maxword = ""

        maxrender = self.word_font.render(maxword, 1, (0, 0, 0))
        for word in self.words:
            # Highlights the high-scores
            color = (255, 255, 255)
            if len(word) >= len(maxword):
                color = (0, 255, 0)

            render_font = self.word_font.render(word.capitalize()+": "+str(len(word)), 1, color)
            self.word_container.blit(render_font, (x_value, y_value))

            # Wraps the text over if it goes down too far -- Slightly buggy
            if (y_value + render_font.get_height() + 2) >= self.word_container.get_height():
                x_value += maxrender.get_width() + 40
                y_value = 10
            else:
                y_value += render_font.get_height() + 2

        # Blits the current score to the bottom-right of word_container
        score_font = self.word_font.render("Score: "+str(self.score), 1, (255, 255, 255))
        score_pos = (self.word_container.get_width() - score_font.get_width(),
                     self.word_container.get_height() - score_font.get_height()*2)
        self.word_container.blit(score_font, score_pos)


if __name__ == "__main__":
    Game()

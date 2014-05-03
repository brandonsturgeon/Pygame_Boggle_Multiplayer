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
        self.color = (175, 175, 175)
        self.rect = pygame.Rect(pos, self.image.get_size())
        self.letter = letter
        self.letter_image = font.render(self.letter.upper(), 1, (255, 255, 255))
        
        self.update()
        
    def update(self):
        # Fill and then blit the letter
        self.image.fill(self.color)
        blit_x = (self.image.get_width() / 2) - (self.letter_image.get_width() /2)
        blit_y = (self.image.get_height() /2) - (self.letter_image.get_height() /2)
        self.image.blit(self.letter_image, (blit_x, blit_y))



class Game():
    def __init__(self):
        pygame.init()
        self.CLOCK = pygame.time.Clock()
        self.game_window = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Boggle")
        self.tile_container = pygame.Surface((600, 600))
        self.tile_container_rect = pygame.Rect((0, 0), self.tile_container.get_size())
        self.mouse_x = 0
        self.mouse_y = 0
        self.score = 0
        self.dictionary = open("2of12inf.txt")
        self.dictionary = [x.strip().replace("%","") for x in self.dictionary]

        # Lengthy surface creations
        self.word_container = pygame.Surface((400, 600))
        self.word_container_rect = pygame.Rect((0, 600), self.word_container.get_size())
        self.word_font = pygame.font.Font(None, 30)
        self.new_game_button = pygame.Surface((100, 25))
        self.new_game_button.fill((0, 0, 255))
        self.new_game_text = self.word_font.render("New Game", 1, (255, 0, 0))
        self.new_game_button.blit(self.new_game_text, ((self.new_game_button.get_width()/2)-(self.new_game_text.get_width()/2),
                                                  (self.new_game_button.get_height()/2)-(self.new_game_text.get_height()/2)))
        self.new_game_button_rect = pygame.Rect((self.game_window.get_width() - self.new_game_button.get_width(),
                                                 self.game_window.get_height() - self.new_game_button.get_height()), self.new_game_button.get_size())
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
                    break

                if event.type == pygame.MOUSEMOTION:
                    self.mouse_x, self.mouse_y = event.pos

                # Check for collisions and thne update the color of the Tiles
                if mousebutton[0] == 1:
                    if self.tile_container_rect.collidepoint((self.mouse_x, self.mouse_y)):
                        for tile in self.tiles:
                            if tile.rect.collidepoint((self.mouse_x, self.mouse_y)):
                                if tile not in submit_word:
                                    submit_word.append(tile)
                                    tile.color = (125, 125, 125)

                    # New Game
                    if self.new_game_button_rect.collidepoint((self.mouse_x, self.mouse_y)):
                        self.score = 0
                        self.words = []
                        self.tiles = pygame.sprite.Group()
                        self.gen_tiles()
                        self.game_loop()

                # Mouse is lifted up, check the word
                if event.type == pygame.MOUSEBUTTONUP:
                    for tile in self.tiles:
                        tile.color = (175, 175, 175)
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
            pygame.display.flip()
            self.CLOCK.tick(60)

    # Generates all of the tiles
    def gen_tiles(self):
        font = pygame.font.Font(None, 75)
        print "Generating Tiles..."
        letter_dict = {"q":1, "x":1}
        y_val = 0
        for y in range(5):
            x_val = 0
            for x in range(5):

                # Limit 2 of each letter using dictionaries
                while True:
                    r_letter = random.choice(string.lowercase[:25])

                    if r_letter not in letter_dict.keys():
                        letter_dict[r_letter] = 1
                        break
                    elif letter_dict[r_letter] < 2:
                        letter_dict[r_letter] += 1
                        break
                    
                self.tiles.add(Tile((x_val, y_val), r_letter, font))
                x_val += 120
            y_val += 120

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

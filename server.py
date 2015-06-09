import PodSixNet.Channel
import PodSixNet.Server
import random
from time import sleep
class ClientChannel(PodSixNet.Channel.Channel):
    def Network(self, data):
        print data

class BoggleServer(PodSixNet.Server.Server):
    channelClass = ClientChannel
    def __init__(self, *args, **kwargs):
        PodSixNet.Server.Server.__init__(self, *args, **kwargs)
        self.games = []
        self.queue = None
        self.currentIndex = 0


    def Connected(self, channel, addr):
        if self.queue is None:
            self.currentIndex += 1
            channel.gameid=self.currentIndex
            self.queue=Game(channel, self.currentIndex)
        else:
            channel.gameid=self.currentIndex
            channel.board = self.gen_tiles()
            self.queue.player1=channel
            self.queue.player0.Send({"action": "startgame", "player": 0, "gameid": self.queue.gameid, "tiles": channel.board})
            self.queue.player1.Send({"action": "startgame", "player": 1, "gameid": self.queue.gameid, "tiles": channel.board})
            self.games.append(self.queue)
            self.queue = None

    # Generates all of the tiles
    def gen_tiles(self):
        r_letter = ""
        print "Generating Tiles..."
        tiles = []

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
                tiles.append([(x_val, y_val), r_letter])
                x_val += 1
            y_val += 1
        print "Generation Complete!"
        return tiles
class Game:
    def __init__(self, player0, currentIndex):
        self.p1_score = 0
        self.p2_score = 0
        self.player0 = player0
        self.player1 = None
        self.gameid = currentIndex
        self.board = []

print "STARTING SERVER ON LOCALHOST"
boggleServe=BoggleServer()
while True:
    boggleServe.Pump()
    sleep(0.01)




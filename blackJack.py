# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 22:05:13 2014

@author: adrianwoalmeida

"""
# imports
from random import shuffle


# global variables - defines
SUITE_NAMES = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
FACE_NAMES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
PLAYER_HUMAN = 1
PLAYER_CPU = 2

def get_input(msg, min_val=None, max_val=None):
    """ Print a message and waits for user input. 
    
    Check if is valid acording to min or max.
    Keep asking until it is valid.
    
    Args:
        msg: message to display
        min: default -1 - min accepted value (equal inclusive)
        max: default -1 - max accepted value (equal inclusive)
        -1 represent not needed. If any value is set, we only accept numbers, no letters
    """
    comp = ''
    # create auxiliary value range
    if min_val:    
        comp = 'min {0} '.format(min_val)

    if max_val:    
        comp += 'max {0} '.format(max_val)    
        
    if comp!='':
         comp = '( {0})'.format(comp)       
    
    # while the input is not valid
    while True:
        ok = True
        print msg + comp
        answer = raw_input()
        
        # if it has min or max, should be a number param
        if min_val!=-1 or min_val!=-1:
            
            # check if user input valid int
            try:
               answer = int(answer)
            except ValueError:
               print("Please insert a number")
               continue
            
            # check if it is inside the params passed
            if min_val and answer<min_val:
                print "Value should be bigger or equal to {0}".format(min_val)
                ok = False
            if max_val and answer>max_val:
                print "Value should be smaller or equal to {0}".format(max_val)
                ok= False
            
        if ok:
            break
    return answer

class Card(object):
    """ class to hold card face and suite.
    """
    
    def __init__(self, face, suite) :
        """ Init the card with face and suite.
        
        Args:
            face - the value of the card
            suite - one of the 4 suites
        """
        self.face = face
        self.suite = suite
    
    def __str__(self):
        """ Prety representation of the card. """
        return ('{0} of {1}'.format(self.face, self.suite))


class Deck(object):
    """ Class to hold the 52 cards. """
    
    def __init__(self, deck_num = 1):
        """ Initiate the class.
        
        Args:
            deckNum = create more than one deck of cards. Default = 1
        """
        self.stack = []
        self.deck_num = deck_num
        
    
    def createCards(self):
        """ Create the 52 cards. """  
        self.stack = []
        for deck in range(self.deck_num):
            for suite in SUITE_NAMES:
                self.stack += [ Card(face, suite) for face in FACE_NAMES] 
            
    def shuffle(self, restart=True):
        """ Shuffle Cards.
        
        Args:
            restart: If it should restart deck or shuffle the current deck
        """
        
        # put all cards back and shuffle
        if restart:
            self.createCards()
            
        shuffle(self.stack)
            
    def get_card(self):
        """ Get a card from the deck """
        return self.stack.pop()
        
class Player(object):
    """ Control player cards and moves. """

    
    # TODO: Fix param
    def __init__(self, player_name, player_type=PLAYER_HUMAN):
        """ Set inital vars 
        
        Args:
            player_type: Human prompts for play, CPU wil not
            player_name: Will print this name
        """
        self.player_type = player_type
        self.player_name = player_name
        self.hand = []
        self.chip = 100
    
    def add_card_to_hand(self, card):
        """ Add a card to player hand """       
        
        self.hand.append(card)
    
    def get_hand_total(self):
        """ calculate hands total """
        
        total = 0
        for c in self.hand:
            if c.face in ['Jack', 'Queen', 'King']:
                total += 10
            elif c.face == 'Ace':
                if (total+10)>21:
                    total += 1
                else:
                    total += 11
            else:
                total += int(c.face)
        return sum( total )
        
def Game(Object):
    """ game class that will control de game flow """
    players = []    
    
    # variables and defines   
    ST_INIT_GAME = 1
    ST_INIT_ROUND = 2
    ST_PLAY_HUMAN = 3
    ST_PLAY_CPU = 4
    ST_END_ROUND  = 5
    ST_QUIT = 6
    STATE = ST_INIT_GAME
    
    def __init__(self):
        """ Give the welcome, get no of player, init structures. """
        print "Welcome to the Black Jack Game \n\n"
        
        # ask amount of players and create them
        player_num = get_input('How many players?', 1,6)
        for p in range(player_num):
            player_name = get_input('Player {0} name:'.format(p))
            players.append(Player(player_name))
            
        # create dealer (cpu)
        players.append(Player('Dealer', PLAYER_CPU))
        
        # number of decks
        num_decks = get_input('How many decks should be used?', 1,8)
    
    def run(self):
        pass
    
    def end(self):
        pass
    
    
        
    

def main():   
    
    # create the class and init the game
    game = Game()
    #game.init()    
    
    

#    print 'Insert number of decks:'
#    deck_no = raw_input()
    # create deck
    deck = Deck()
    deck.shuffle()
    
    # ask player for his name and create CPU
    print 'Player Name'
    name = raw_input()
    player = Player(name)        
    dealer = Player('Dealer', Player.PLAYER_CPU)
    
    # TODO: Create game class
    # start the game and finish
    state = 'INIT'
    while 1:
        if state=='INIT':
            # one card for the dealer and two for the player
            dealer.add_card_to_hand(deck.get_card())
            player.add_card_to_hand(deck.get_card())
            player.add_card_to_hand(deck.get_card())
            
            # print the table
            print 'Cards on the table:'
            print dealer.player_name            
            for c in dealer.hand:
                print c
            print 'Total :{0}'.format(dealer.get_hand_total())
            
            print player.player_name            
            for c in player.hand:
                print c
            print 'Total :{0}'.format(player.get_hand_total())
            
            state = 'PLAY_HUMAN'
        if state=='PLAY_HUMAN':                    
            print 'Human Play'
            answer =  0
            
            # while the player does not quit
            while (answer<>'N' and player.get_hand_total() <21) :
                print 'Total :{0}'.format(player.get_hand_total())               
                print 'Want another card? (Y/N)'
                answer = raw_input()
                
                if answer=='Y':
                    card = deck.get_card()
                    print 'New card: {0}'.format(card)
                    player.add_card_to_hand(card)
                    print 'New total:{0}'.format(player.get_hand_total())
            
            state = 'PLAY_CPU'
                    
        if state=='PLAY_CPU':
            print 'Dealer Play'
            total = dealer.get_hand_total()
            print 'Total :{0}'.format(total)
            while total<17:
                card = deck.get_card()
                print 'New card: {0}'.format(card)
                dealer.add_card_to_hand(card)
                total = dealer.get_hand_total()
                print 'New total:{0}'.format(total)
            
            state='WIN_LOST'
        
        if state=='WIN_LOST':
            player_total = player.get_hand_total()
            dealer_total = dealer.get_hand_total()
            
            # client exploded
            if player_total>21:
                print '{0} WON!!!'.format(dealer.player_name)
            elif dealer_total >21:
                print '{0} WON!!!'.format(player.player_name)
            elif player_total>=dealer_total:
                print '{0} WON!!!'.format(player.player_name)
            else:
                print '{0} WON!!!'.format(dealer.player_name)
            
            print '{0} Total: {1}'.format(dealer.player_name, dealer.get_hand_total())            
            print '{0} Total: {1}'.format(player.player_name, player.get_hand_total())
            state = 'QUIT'
        
        if state=='RESTART':
            # TODO: restart game
            print 'Restarting'
        
        if state=='QUIT':
            print 'End of Game'
            break
        
    print 'Thanks for playing. Bye!'
        

if __name__=='__main__':
    main()
        
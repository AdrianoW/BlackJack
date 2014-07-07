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


class Card(object):
    """ class to hold card face and suite.
    """
    
    def __init__(self, face, suite, face_down = False) :
        """ Init the card with face and suite.
        
        Args:
            face - the value of the card
            suite - one of the 4 suites
        """
        self.face = face
        self.suite = suite
        self.face_down = face_down
    
    def __str__(self):
        """ Prety representation of the card. If the card is face_down, it will 
            show nothing        
        """
        if self.face_down:
            return "unknown card"
        else:
            return ('{0} of {1}'.format(self.face, self.suite))
    
    def flip_card(self):
        self.face_down = not self.face_down 


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
        self.chip = 0
        self.round_bet = 0
    
    def add_card_to_hand(self, card):
        """ Add a card to player hand """       
        self.hand.append(card)
    
    def clear_hand(self):
        self.hand[:]=[]
    
    def get_hand_total(self):
        """ calculate hands total of flipped cards"""
        
        total = 0
        for c in self.hand:
            if c.face_down:
                continue
            if c.face in ['Jack', 'Queen', 'King']:
                total += 10
            elif c.face == 'Ace':
                if (total+10)>21:
                    total += 1
                else:
                    total += 11
            else:
                total += int(c.face)
        return total
        
    def print_hand(self):
        print '-----------------' 
        print 'Player: {0}'.format(self.player_name)
        print '-----------------' 
        print 'Cards:'
        for c in self.hand:
            print '\t{0}'.format(c)
        print 'Total: {0}\n'.format(self.get_hand_total())
    
    def ask_bet_value(self):
        if self.player_type == PLAYER_CPU:
            return 
        
        line = '|  Player: {0}  |  Total Chips: ${1}  |'.format(
                                                self.player_name, self.chip) 
        print '-'*len(line)
        print line
        print '-'*len(line)                               
        self.round_bet = get_input('Amount to bet:',min_val = 1, max_val=self.chip, default = self.round_bet)
        
class Game(object):
    """ game class that will control de game flow """
     
    
    # variables
    players = [] # players list
    cur_player = 0 # current player
    player_standing = 0
    num_player_out = 0
    
    # game states
    ST_INIT_GAME = 1
    ST_INIT_ROUND = 2
    ST_PLAY_HUMAN = 3
    ST_PLAY_CPU = 4
    ST_END_ROUND  = 5
    ST_QUIT = 6
    
    def __init__(self):
        """ Give the welcome, get n. of player, init structures. """
        
        # print welcome
        self.welcome_screen()
        
        # ask amount of players and create them
        self.player_num = get_input('How many players?', min_val=1,max_val=6, default=1)
        for p in range(self.player_num):
            player_name = get_input('Player {0} name:'.format(p))
            self.players.append(Player(player_name))
            
        # create dealer (cpu)
        self.players.append(Player('Dealer', PLAYER_CPU))
        
        # number of decks
        num_decks = get_input('How many decks should be used?', min_val=1,max_val=8, default=2)
        self.deck = Deck(num_decks)
        
        # start the game when it is run
        self.state = self.ST_INIT_GAME
    
    def run(self):
        """ Game will run here acording to various states. """        
        
        while True:    
            # the begin of the game
            if self.state==self.ST_INIT_GAME:        
                # all players receive $100                
                for p in self.players:
                    p.chip = 100
                
                # start the round
                self.state = self.ST_INIT_ROUND

            # the begin of the round
            if self.state==self.ST_INIT_ROUND:        
                # first player again, shuffle cards and zero hands
                self.cur_player = 0
                self.player_standing = 0
                self.num_player_out = 0
                self.deck.shuffle()
                
                # bet time
                print '-------------------'
                print '|    BET TIME     |'
                print '-------------------'
                for p in self.players:    
                    p.clear_hand()
                    
                    # ask for the amount to bet
                    p.ask_bet_value()
                    
                # distribute cards. 2 per player.
                for i in range (2):
                    for p in self.players:
                        p.add_card_to_hand(self.deck.get_card())
                        
                # flip last card from the dealer
                self.players[-1].hand[-1].flip_card()
                        
                #print table
                print '-------------------'
                print '|      TABLE      |'
                print '-------------------'
                for p in self.players:
                    p.print_hand()
                
                # print play header
                print '\n\n-------------------'
                print '| PLAYERS ROUND   |'
                print '-------------------'
                
                # start the human play
                self.state = self.ST_PLAY_HUMAN
            
            # human play
            if self.state==self.ST_PLAY_HUMAN:
                # print player hand and ask what he wants to do                
                self.players[self.cur_player].print_hand()
                while True:                
                    ans = get_input('What do you wand to do? (N)ew Card, (S)tand'
                                    ,options=['N','S'], default='S')
                    
                    if ans=='S':
                        # stop
                        self.player_standing += 1
                        break
                    elif ans=='N':
                        # get another card, print new hand                       
                        self.players[self.cur_player].add_card_to_hand(
                                                        self.deck.get_card())
                        self.players[self.cur_player].print_hand()
                        
                        #and check if it has not bust  
                        total = self.players[self.cur_player].get_hand_total()
                        if total>21:
                            print 'You Lost!!!'
                            break
                
                # next player or dealer (dealer is always the last)?
                if self.cur_player < len(self.players)-2:
                    self.state = self.ST_PLAY_HUMAN
                else:
                    self.state = self.ST_PLAY_CPU
                
                self.cur_player += 1
            
            # CPU play
            if self.state==self.ST_PLAY_CPU:
                # check if the dealer needs to play
                if self.player_standing==0:
                    self.state = self.ST_END_ROUND
                else:
                    # flip dealer card and show the hands
                    self.players[-1].hand[-1].flip_card()
                    self.players[-1].print_hand()    
                    total = self.players[-1].get_hand_total()                   
                    
                    # keep getting cards until the dealer gets at least 17
                    while total<17:
                        card = self.deck.get_card()
                        print 'New card: {0}'.format(card)
                        self.players[-1].add_card_to_hand(card)
                        total = self.players[-1].get_hand_total()
                        print 'New total:{0}'.format(total)
                    
                    # close this round
                    self.state = self.ST_END_ROUND
            
            # finish the round giving or taking money.
            if self.state==self.ST_END_ROUND:
                # get the dealer total. If it bust, its like havin 0 at hand                
                dealer_total = self.players[-1].get_hand_total()
                if dealer_total>21:
                    dealer_total = 0
                    
                # show the banner for final results
                print ' ------------------'
                print '|  ROUND RESULTS   |'
                print ' ------------------'
                
                # do the maths for all human players
                for p in self.players[:-1]: 
                    player_total = p.get_hand_total()
                    print '-- Player: {0}'.format(p.player_name)
                    
                    if player_total == 21:
                        # blackjack                        
                        p.chip += p.round_bet*2
                        print '\t BLACK JACK!!!!'
                    elif player_total>21 or (
                        player_total<21 and player_total<dealer_total) :
                        # player bust or lost 
                        p.chip -= p.round_bet
                        
                        print '\t Hand {0} < {1} Dealer'.format(player_total, 
                                                                dealer_total)
                        print '\t YOU LOST!!!!'
                        
                        # out of game?                        
                        if p.chip<=0:
                            print "Player {0} is out!!!".format(p.player_name)
                            self.num_player_out += 1
                    else:
                        # player won   
                        print '\t Hand {0} > {1} Dealer'.format(player_total, 
                                                                dealer_total)
                        print '\t YOU WON!!!!'
                        p.chip += p.round_bet
                
                # check if there is anybody with money to play
                if self.num_player_out == self.player_num:
                    print 'All Players Lost !!!'
                    print ' ------- GAME OVER !!!! -------'
                    self.state = self.ST_QUIT
                else:
                    self.state = self.ST_INIT_ROUND
                        
            if self.state==self.ST_QUIT:
                break
            
    def end(self):
        pass
    
    def welcome_screen(self):
        """Prints the beaaautiful welcome screen. """
        print " _______________________________________"
        print "   WELCOME TO "
        print "             THE BLACK JACK GAME"
        self.get_input('Press enter to start')
    
    def get_input(msg, min_val=None, max_val=None, options=None, default= None):
    """ Print a message and waits for user input. 
    
    Check if is valid acording to min or max.
    Keep asking until it is valid.
    
    Args:
        msg: message to display /n
        min: default -1 - min accepted value (equal inclusive) /n
        max: default -1 - max accepted value (equal inclusive) /n
        options: array with possible options /n/n
        -1 represent not needed. If any value is set, we only accept numbers, no letters
    """
    comp = ''
    # create auxiliary value range
    if min_val:    
        comp = 'min {0} '.format(min_val)
    if max_val:    
        comp += 'max {0} '.format(max_val)    
    if comp!='':
         comp = ' ( {0})'.format(comp)
    if comp=='' and options:
        comp = ' ({0}) '.format(options)
    if default:
        comp += '- default {0}'.format(default)
    
    # while the input is not valid
    while True:
        ok = True
        print msg + comp
        answer = raw_input()
        
        # it there is no answer but there is a default, use the default.
        if answer=='' and default:
            answer = default
            print answer
        
        # if it has min or max, should be a number param
        if min_val or min_val:
            
            # check if user input valid int
            try:
               answer = int(answer)
            except ValueError:
               print("Please insert a number")
               continue
            
            # check if it is inside the params passed
            if min_val and answer<min_val:
                print "Value should be bigger or equal to {0}".format(min_val)
                continue
            if max_val and answer>max_val:
                print "Value should be smaller or equal to {0}".format(max_val)
                continue
                
        # if it has options, answer need to be inside the values
        if options and (answer.upper() not in options):
            print "Value should be in {0}".format(options)
            continue
        
        if ok:
            break
    return answer

def main():   
    
    # create the class and init the game
    game = Game()

    game.run()
    
    game.end()
    
#    # TODO: Create game class
#    # start the game and finish
#    state = 'INIT'
#    while 1:
#        if state=='INIT':
#            # one card for the dealer and two for the player
#            dealer.add_card_to_hand(deck.get_card())
#            player.add_card_to_hand(deck.get_card())
#            player.add_card_to_hand(deck.get_card())
#            
#            # print the table
#            print 'Cards on the table:'
#            print dealer.player_name            
#            for c in dealer.hand:
#                print c
#            print 'Total :{0}'.format(dealer.get_hand_total())
#            
#            print player.player_name            
#            for c in player.hand:
#                print c
#            print 'Total :{0}'.format(player.get_hand_total())
#            
#            state = 'PLAY_HUMAN'
#        if state=='PLAY_HUMAN':                    
#            print 'Human Play'
#            answer =  0
#            
#            # while the player does not quit
#            while (answer<>'N' and player.get_hand_total() <21) :
#                print 'Total :{0}'.format(player.get_hand_total())               
#                print 'Want another card? (Y/N)'
#                answer = raw_input()
#                
#                if answer=='Y':
#                    card = deck.get_card()
#                    print 'New card: {0}'.format(card)
#                    player.add_card_to_hand(card)
#                    print 'New total:{0}'.format(player.get_hand_total())
#            
#            state = 'PLAY_CPU'
#                    
#        if state=='PLAY_CPU':
#            print 'Dealer Play'
#            total = dealer.get_hand_total()
#            print 'Total :{0}'.format(total)
#            while total<17:
#                card = deck.get_card()
#                print 'New card: {0}'.format(card)
#                dealer.add_card_to_hand(card)
#                total = dealer.get_hand_total()
#                print 'New total:{0}'.format(total)
#            
#            state='WIN_LOST'
#        
#        if state=='WIN_LOST':
#            player_total = player.get_hand_total()
#            dealer_total = dealer.get_hand_total()
#            
#            # client exploded
#            if player_total>21:
#                print '{0} WON!!!'.format(dealer.player_name)
#            elif dealer_total >21:
#                print '{0} WON!!!'.format(player.player_name)
#            elif player_total>=dealer_total:
#                print '{0} WON!!!'.format(player.player_name)
#            else:
#                print '{0} WON!!!'.format(dealer.player_name)
#            
#            print '{0} Total: {1}'.format(dealer.player_name, dealer.get_hand_total())            
#            print '{0} Total: {1}'.format(player.player_name, player.get_hand_total())
#            state = 'QUIT'
#        
#        if state=='RESTART':
#            # TODO: restart game
#            print 'Restarting'
#        
#        if state=='QUIT':
#            print 'End of Game'
#            break
#        
#    print 'Thanks for playing. Bye!'
        

if __name__=='__main__':
    main()
        
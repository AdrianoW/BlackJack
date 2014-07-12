# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 22:05:13 2014

@author: adrianwoalmeida

"""
# imports
from random import shuffle
import os
from time import sleep
from math import ceil

# global variables - defines
SUITE_NAMES = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
FACE_NAMES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 
                                                  'Queen', 'King', 'Ace']
PLAYER_HUMAN = 1
PLAYER_CPU = 2


class Card(object):
    """ Class to hold card face and suite.
    """
    
    def __init__(self, face, suite, face_down = False) :
        """ Init the card with face and suite.
        
        Args:
            face (str): The value of the card.
            suite(str): One of the 4 suites.
            face_down (bool, optional): If the card is face down (True), 
                it will not be counted. Defaults to False.
                
        """
        self.face = face
        self.suite = suite
        self.face_down = face_down
    
    def __str__(self):
        """ Prety representation of the card. If the card is face_down, it will 
            show unknown card and it won't be counted on total.     
        """
        if self.face_down:
            return "unknown card"
        else:
            return ('{0} of {1}'.format(self.face, self.suite))
    
    def flip_card(self):
        """ Toggle the face_down property. """
        self.face_down = not self.face_down 


class Deck(object):
    """ Class to hold the 52 cards. """
    
    def __init__(self, deck_num = 1):
        """ Initiate the class.
        
        Args:
            deckNum (int, optional): create more than one deck of cards. 
                Defaults to 1.
                
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
            restart (bool, optional): If it should restart deck or just shuffle  
                current deck. Defaults to True.
            
        """
        
        # put all cards back and shuffle
        if restart:
            self.createCards()
            
        shuffle(self.stack)
            
    def get_card(self):
        """ Get a card from the deck. """
        return self.stack.pop()
        
class Player(object):
    """ Control player cards and moves. """

    def __init__(self, player_name, player_type=PLAYER_HUMAN):
        """ Set inital vars. 
        
        Args:
            player_name (str): Will print this name.
            player_type (int, optional): Human prompts for play, CPU wil not.
                defaults to PLAYER_HUMAN (1).
            
        """
        self.player_type = player_type
        self.player_name = player_name
        self.hand = []
        self.chip = 0
        self.round_bet = 0
        self.num_ace = 0
    
    def add_card_to_hand(self, card):
        """ Add a card to player hand. """       
        self.hand.append(card)
            
    def clear_hand(self):
        """ Clear players hand structure """
        self.hand[:]=[]
    
    def get_hand_total(self):
        """ calculate hands total of flipped cards"""
        
        total = 0
        
        # separate regular cards and aces
        regular = [c for c in self.hand if c.face != 'Ace']
        aces = [c for c in self.hand if c.face == 'Ace']
        
        # sum total without aces
        for c in regular:
            if c.face_down:
                continue
            if c.face in ['Jack', 'Queen', 'King']:
                total += 10
            else:
                total += int(c.face)
                
        # sum according to what is best Ace = 1 or Ace = 11
        num_ace = len(aces)
        if num_ace == 1:
            # check if one ace is face down
            if not aces[0].face_down:
                total += 11
        elif num_ace>1:            
            # check if there is a bust with one ace as 11
            if (total+11+(num_ace-1))<22:
                total += 11+(num_ace-1)
            else:                
                total += num_ace
            
        return total
        
    def print_hand(self, header=None):
        """Print formated player's hand.

        Args:
            header - string, optional
                Will print a header first. Ex: Players Turn
        """
        # print header
        if header:
            temp =  '|   {0}   |'.format(header)
            print '-'*len(temp)
            print temp
            print '-'*len(temp)
            print ' '
            
        # print player name, cards and total
        temp =  '|  Player: {0}   |'.format(self.player_name)
        print '-'*len(temp)
        print temp
        print '-'*len(temp)
        print 'Cards:'
        for c in self.hand:
            print '\t{0}'.format(c)
        print 'Total: {0}\n'.format(self.get_hand_total())
    
class Game(object):
    """ game class that will control de game flow """
     
    def __init__(self):   
         # variables
        self.players = [] # players list
        self.cur_player = 0 # current player
        self.player_standing = 0
        self.num_player_out = 0
        
        # game states
        self.ST_INIT_GAME = 1
        self.ST_INIT_ROUND = 2
        self.ST_PLAY = 3
        self.ST_END_ROUND  = 4
        self.ST_QUIT = 5
    
    def init(self):
        """ Give the welcome, get n. of player, init structures. """
        
        # print welcome
        self.welcome_screen()
        
        # ask amount of players and create them
        self.player_num = self.get_input('How many players?', 
                                         min_val=1,max_val=6, default=1)
        for p in range(self.player_num):
            player_name = self.get_input('Player {0} name:'.format(p))
            self.players.append(Player(player_name))
            
        # create dealer (cpu)
        self.players.append(Player('Dealer', PLAYER_CPU))
        
        # number of decks
        num_decks = self.get_input('How many decks should be used?', 
                                   min_val=1,max_val=8, default=2)
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
                # first player again, shuffle cards, zero hands, everybody in
                self.cur_player = 0
                self.player_standing = 0
                self.num_player_out = 0
                self.deck.shuffle()
                
                # bet time
                self.clear_scr()
                print '-------------------'
                print '|    BET TIME     |'
                print '-------------------'
                for p in self.players:    
                    p.clear_hand()
                    
                    # ask for the amount to bet
                    if p.chip>0:
                        self.ask_bet_value(p)
                    
                # distribute cards. 2 per player.
                for i in range (2):
                    for p in self.players:
                        # ask for the amount to bet
                        if p.chip>0:
                            p.add_card_to_hand(self.deck.get_card())
                        
                # flip last card from the dealer
                self.players[-1].hand[-1].flip_card()
                        
                #print table
                self.get_input("\n\nPress enter to continue...")
                self.clear_scr()
                print '-------------------'
                print '|      TABLE      |'
                print '-------------------'
                for p in self.players:
                    sleep(0.3)
                    p.print_hand()
                self.get_input("\n\nPress enter to start Players Round...")
                
                # start play round
                self.state = self.ST_PLAY
            
            # play time
            if self.state==self.ST_PLAY:        
                # all player play if they have money to
                for p in self.players:                    
                    # humans prompt, dealer is automatic play
                    if p.player_type == PLAYER_HUMAN:
                        # print player hand and ask what he wants to do                
                        while p.chip>0:                
                            self.clear_scr()
                            p.print_hand(header = 'PLAYERS ROUND')
                            
                            #and check if it has not bust  
                            total = p.get_hand_total()
                            if total>21:
                                print 'BUSTED!!!'
                                self.get_input("\nPress enter to continue...")
                                break
                                
                            # options
                            options=['H','S'] 
                            msg = 'What do you wand to do? (H)it, (S)tand'
                            
                            # check if player may split
                            if len(p.hand)==2 \
                                and (p.hand[0].face==p.hand[1].face):            
                                options += 'P'
                                msg += ' S(p)lit'
                                
                            ans = self.get_input(
                               msg, options=options, default='S')
                           
                            # switch according to answer
                            if ans=='S':
                                # stop
                                self.player_standing += 1
                                break
                            elif ans=='H':
                                # get another card, print new hand                       
                                p.add_card_to_hand(self.deck.get_card())
                    # dealer            
                    else:
                        # check if the dealer needs to play
                        if self.player_standing!=0:
                            self.get_input('End of PLAYERS ROUND. Press enter for Dealers Round...')                            
                            
                            # flip dealer card
                            self.players[-1].hand[-1].flip_card()
                            
                            # dealer play
                            while True:                      
                                # show hand. sleep 1 to give some tension.
                                self.clear_scr()
                                p.print_hand('DEALERS ROUND')    
                                total = p.get_hand_total()
                                
                                # keep getting cards until the dealer gets at least 17
                                if total<17:
                                    print 'Dealers Playing'
                                    sleep(1)               
                                    p.add_card_to_hand(self.deck.get_card())
                                else:
                                    sleep(1)
                                    print 'End of dealers round'
                                    self.get_input(
                                        "\nPress enter to continue...")
                                    break
                            
                # close this round
                self.state = self.ST_END_ROUND
            
            # finish the round giving or taking money.
            if self.state==self.ST_END_ROUND:
                # get the dealer total. If it bust, its like havin 0 at hand                
                dealer_total = self.players[-1].get_hand_total()
                dealer_num_cards = len(self.players[-1].hand)
                    
                # show the banner for final results
                self.clear_scr()
                print ' ------------------'
                print '|  ROUND RESULTS   |'
                print ' ------------------'
                
                # do the maths for all human players
                for p in self.players[:-1]: 
                    result = 0
                    player_total = p.get_hand_total()
                    print '-- Player: {0}'.format(p.player_name)
                    
                    if p.chip<=0:
                        print '\tPlayer Out!'
                    elif player_total == 21 and len(p.hand)==2:
                        # blackjack
                        if dealer_total==21 and dealer_num_cards==2:
                            # draw
                            result = p.round_bet
                            print '\tDRAW - YOU AND THE DEALER HAVE BLACKJACK!!'
                        else:
                            result = ceil(p.round_bet*2.5)
                            print '\tWIN - BLACK JACK!!!'
                    elif player_total>21:
                        # player busted
                        result = -p.round_bet
                        print '\tLOSE - BUSTED!!!'
                    elif dealer_total>21:
                        # dealer lost
                        result = p.round_bet
                        print '\tWON - DEALER BUSTED!!!'
                    elif dealer_total == player_total:
                        result = 0
                        print '\tDRAW - Player {0} = {1} Dealer'.format(
                                            player_total, dealer_total)
                    elif player_total<dealer_total or (
                                    dealer_total==2 and dealer_num_cards==2):
                        # player lost 
                        result = -p.round_bet
                        print '\tLOST - Player {0} < {1} Dealer'.format(
                                            player_total, dealer_total)
                    else:
                        # player won   
                        print '\tWON - Player {0} > {1} Dealer'.format(
                                            player_total, dealer_total)
                        result = p.round_bet
                        
                    print '\t ${0} Chips'.format(result)
                    p.chip += result
                    
                    # out of game?                        
                    if p.chip<=0:
                        print "\tPlayer {0} is out!!!".format(p.player_name)
                        self.num_player_out += 1
                
                # check if there is anybody with money to play
                if self.num_player_out == self.player_num:
                    print 'All Players Lost !!!'
                    print ' ------- GAME OVER !!!! -------' 
                    pa = self.get_input('Wanna play again?',options=['Y','N'])
                    if pa=='N':
                        self.state = self.ST_QUIT
                    else:
                        self.state = self.ST_INIT_GAME                        
                else:
                    self.get_input("\n\nPress enter to continue...")
                    self.state = self.ST_INIT_ROUND
                        
            if self.state==self.ST_QUIT:
                break
            
    def end(self):
        print 'Thanks for playing. Hope to see you soon!'
    
    def welcome_screen(self):
        """Prints the beaaautiful welcome screen. """
        self.clear_scr()
        print " _______________________________________"
        print "   WELCOME TO "
        print "             THE BLACK JACK GAME"
        print " _______________________________________"
        print " \n\nAt any time press CTRL+C to quit."
        self.get_input('Press enter to start')
    
    def get_input(self, msg, min_val=None, max_val=None, options=None, default= None):
        """ Print a message and waits for user input. 
        
        Check if is valid acording to min or max.
        Keep asking until it is valid.
        
        Args:
            @msg: message to display 
            @min: default -1 - min accepted value (equal inclusive)
            @max: default -1 - max accepted value (equal inclusive)
            @options: array with possible options, always capital 
            -1 represent not needed. If any value is set, we only accept numbers, no letters
        """
        comp = ''
        # create auxiliary value range
        if min_val:    
            comp = 'min {0} '.format(min_val)
        if max_val:    
            comp += 'max {0} '.format(max_val)    
        if comp!='':
             comp = ' ( {0}) '.format(comp)
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
            if options:
                answer = answer.upper()
                if answer not in options:
                    print "Value should be in {0}".format(options)
                    continue
            
            if ok:
                break
        return answer
        
    def clear_scr(self):
        """helper to clear screen."""
        if os.name=='nt':
            os.system('cls') #on windows
        else:
            os.system('clear') # on linux / os x
            
    def ask_bet_value(self, player):
        if player.player_type == PLAYER_CPU:
            return 
        
        line = '|  Player: {0}  |  Total Chips: ${1}  |'.format(
                                                player.player_name, player.chip) 
        print '-'*len(line)
        print line
        print '-'*len(line)                               
        player.round_bet = self.get_input('Amount to bet:',min_val = 1, max_val=player.chip, default = player.round_bet)
        

def main():   
    
    # create the class and init the game    
    game = Game()
    try:
        game.init()
        game.run()
    except KeyboardInterrupt:
        game.clear_scr()
        print 'Player QUIT!'
    finally:
        if game:
            game.end()
        

if __name__=='__main__':
    main()
        
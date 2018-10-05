
from random import shuffle
from sys import stdout


#Global varible
number_index = {"Two":2,"Three":3,"Four":4,"Five":5,"Six":6,"Seven":7,"Eight":8,"Nine":9,"Ten":10,"Jack":10,"Queen":10,"King":10,"Ace":11}
suits = ["Diamonds", "Hearts","Spades", "Clubs"]
numbers= {"Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Jack","Queen","King","Ace"}

class Deck():

    def __init__(self):
        # All the cards not in play are stored here

        self.card = []
        
        for i in suits:
            for num in numbers:
                self.card.append([i,num])
        shuffle(self.card) 
    def reset(self):
        #redos 
        suits = ["Diamonds", "Hearts","Spades", "Clubs"]
        numbers= {"Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Jack","Queen","King","Ace"}
        self.card = []
        for i in suits:
            for num in numbers:
                self.card.append([i,num])
        shuffle(self.card)     

    def draw(self):
        one_card = None
        if len(self.card) == 0:
            print("Error, no more cards in deck. EXITING\n")
            exit()
        else:
            one_card = self.card.pop()
        return one_card


class Hand():
    def __init__(self,card_one, card_two,name):
        #card one and two need to be cards from the deck. A list of a suit and a single entry dictionary
        # name : name of player. Player or Deal
        self.cards = [card_one,card_two]
        self.name = name
        #self.hidden_card = hidden

    def add_card(self,card):
        self.cards.append(card)

    def sum(self):
        total = 0
        n_ace = 0
        for index in self.cards:
            total += number_index[index[1]]
            if index[1] == "Ace" :
                n_ace += 1
        count = 0
        #if over 21 subract 10 for aces because aces can be 1 or 11
        while count < n_ace and total > 21:
            if total > 21:
                total -= 10
            count += 1
        return total

    def display(self,hidden = False):

        # number of aces
        n_ace = 0
        total = 0
        for index in self.cards:
            total += number_index[index[1]]
            if index[1] == "Ace" :
                n_ace += 1

        print("*"*50)
        print("Hand:{}".format(self.name))
        print("\nCards in hand:")
        for c in range(0,len(self.cards)) :
            if c == 0 and hidden:
                print("**Hidden Card**")
            else:
                print("{} of {}".format(self.cards[c][1],self.cards[c][0]))
        if(self.name != "Dealer"):
            if total > 21 and n_ace > 0 :
                stdout.write("\nsum = ")
            else :
                stdout.write("\nsum = {}".format(total))
            for i in range(0,n_ace):
                if (i == 0 and total > 21):
                    stdout.write("{}".format(total-10*(i+1)))
                elif total - 10*(i+1) > 0 and total-10*(i+1) <= 21:
                    stdout.write("(or {})".format(total-10*(i+1)))
            print("")
            if n_ace > 0:
                print("You many have multiple scores because your hand has one or more ace in it.")
                print("Highest score below 22 will always be chosen.")
        elif(hidden == False):
            print("\nsum = {}".format(self.sum()))      
        print("*"*50)
        

def display_game(dealer,player,hidden = True):
    print("\n"*100)
    dealer.display(hidden)
    print("")
    player.display(False)
#start main program




input("Ready to play Black Jack. Press any button to start.")
money = 100

while True:
    bet = ""
    while not bet.isnumeric():
        bet = input("Current balance ${}.\nHow much do you want to bet?".format(money))
        if(not bet.isnumeric()):
            print("Invalid input. Give an positive whole number.")
        elif int(bet) > money :
            print("Cannot bet more money than you have.")
            bet = ""
        else:
            money -= int(bet)

    #starting game
    deck = Deck()
    #dealers hand
    dealer = Hand(deck.draw(),deck.draw(),"Dealer")
    #players hand
    player = Hand(deck.draw(),deck.draw(),"Player")
    
    display_game(dealer,player)
            
    overtwentyone = False
    players_turn = True
    
    #drawing player cards
    while players_turn:
        user_input = ""
        while user_input != "Y" and user_input != "N" :
            user_input = input("Do you want to draw an other card[Y/N]").upper()
            if(user_input != "Y" and user_input != "N" ):
                print("Invalid Response.")
        if user_input == "Y" and player.sum() <= 21:
            player.add_card(deck.draw())
            display_game(dealer,player)
            if player.sum() > 21:
                display_game(dealer,player,False)
                print("You are over 21\n")
                overtwentyone = True
                players_turn = False
                input("Dealer wins.\nPress any button to continue.")
        elif user_input == "N":
            display_game(dealer,player,False)
            input("Dealer's hidden card is revealed.\nPress any button to continue.")
            players_turn = False
            
    ncard = 0
    while not players_turn and not overtwentyone:
        
        if player.sum() > dealer.sum() :
            dealer.add_card(deck.draw())
            display_game(dealer,player,False)
            if player.sum() > dealer.sum():
                input("Dealer draws a card. Press any button to continue.")

            ncard += 1

        # Player wins condition
        if dealer.sum() > 21:
            display_game(dealer,player,False)
            print("Dealer has drawn {} card(s)".format(ncard))
            print("Dealer cards total is over 21.")
            print("Player Wins. (YAY) You gain double your bet.\n")
            money += 2*int(bet)
            players_turn = True
        # Player loses condition
        elif player.sum() <= dealer.sum():
            display_game(dealer,player,False)
            print("Dealer has draw {} card(s)".format(ncard))
            print("Dealer's card total are greater or equal to Player's.")
            print("Dealer Wins.")
            players_turn = True
        user_input = ""

    if(money > 0):
        user_input = ""
        while user_input != "Y" and user_input != "N":
            user_input = input("Current balance is {}.\nDo you want to go again[Y/N]".format(money)).upper()
            if user_input != "Y" and user_input != "N":
                print("Invalid Response.")
            elif(user_input == "N") :
                print("GoodBye")
                exit()
            else:
                print("New Game\n")
    else:
        print("You're out of money. Goodbye")
        exit()
    #players hand
 #   player = Hand(deck.draw(),deck.draw(),"Player",hidden=False)
#    player.display()

#    break
    #print(player.sum())

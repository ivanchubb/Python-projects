##Ivan Chubb
import random
import os

global card_count
card_count= 0
# build the deck
def new_deck():
    deck = {}
    for i in range(4):
        suits = ["Diamonds", "Hearts", "Clubs", "Spades"]
        facecards = ["Jack", "Queen", "King", "Ace"]
        k = 0
        for j in range(13):
            if j < 9:
                cardname = "{number} of {suit}".format(number=j + 2, suit=suits[i])
                deck[cardname] = j + 2
            elif 9 <= j <= 11:
                cardname = "{number} of {suit}".format(number=facecards[k], suit=suits[i])
                deck[cardname] = 10
                k += 1
            elif j == 12:
                cardname = "{number} of {suit}".format(number=facecards[k], suit=suits[i])
                deck[cardname] = 11
                k += 1
    return deck


# shuffle the deck
def shuffle_deck(deck):
    lst = list(deck.items())
    random.shuffle(lst)
    shuffled_deck = dict(lst)
    print("Shuffling the deck")
    global card_count
    card_count = 0
    return shuffled_deck


# define player class
class Player:
    def __init__(self, name):
        self.points = 0
        self.split_points = 0
        self.cash = 1000
        self.chair = None
        self.name = name
        self.hand = []
        self.split_hand = []
        self.bet = 0
        self.split_bet = 0
        self.aces = 0
        self.split_aces = 0
        self.ai = "no"

    def __repr__(self):
        return "{name}".format(name=self.name)


# betting
def place_bets(gamblers):
    for i in range(len(gamblers)):
        while True:
            print("{player}, How much do you want to bet?".format(player=gamblers[i]))
            # spot for AI to place bets
            gamblers[i].bet = int(input())

            # ensure bet is positive and less than total funds
            if gamblers[i].cash >= gamblers[i].bet > 0 and gamblers[i].bet % 5 == 0:
                gamblers[i].cash -= gamblers[i].bet
                break
            else:
                print("Invalid bet, must be a positive number and multiple of 5. try again")


# set table with number of players and dealer
def get_players():
    print("The table has space for 5 players.  How many humans are playing?")
    while True:
        num_players = int(input())
        if num_players < 6:
            break
        else:
            print("There is only space for 5 people at the table")
    players = []
    classyplayers = []
    for i in range(int(num_players)):
        print("Enter name for player" + str(i + 1))
        temp = input()
        players.append(temp)

    # This is where AI players need to be created
    print("Would you like to play with any AI? you have space for " + str(5 - num_players) + ".")
    temp = input()
    while True:
        if "y" in temp.lower():
            # remove when AI is ready to be implemented
            print("This feature is not yet ready")
            break
            print("Who would you like to play with (Booker, Ace, or Both)?")
            choice = input()
            if "booker" == choice.lower():
                players.append("Booker")
            elif "ace" == choice.lower():
                players.append("Ace")
            elif "both" == choice.lower():
                players.append("Ace")
                players.append("Booker")
        else:
            print("No AI then.")
        break
    for i in range(len(players)):
        classyplayers.append(Player(players[i]))
        classyplayers[i].name = players[i]
        classyplayers[i].chair = i + 1
        # there is a better way to do this than by name, but i am not sure how i want to do it yet, probably
        # putting the AIs in after the classes are established so they start out with the ai attribute
        # leaving as it is will result in problems if a player chooses the names "booker" or "Ace"
        if classyplayers[i].name == "Booker" or classyplayers[i].name == "Ace":
            classyplayers[i].ai = "yes"
        print("{player} is sitting in chair {chair} and has ${cash}".format(player=classyplayers[i].name,
                                                                            chair=classyplayers[i].chair,
                                                                            cash=classyplayers[i].cash))
    # dealer
    dealer = Player("Dealer")
    dealer.chair = len(classyplayers)
    return classyplayers, dealer


# deal a single card, returns the card dealt and it's point value, removes the last item in the dictionary
def deal_card(deck, player):
    card, points = deck.popitem()
    get_count(points)
    player.hand.append(card)
    if "Ace" in card:
        player.aces += 1
    player.points += points
    player = check_ace(player)
    return player


# deal all the cards
def two_cards_each(players, dealer, deck):
    for j in range(len(players)):
        for i in range(2):
            players[j] = deal_card(deck, players[j])
        print("{player} has {cards} with a value of {points}".format(player=players[j].name, cards=players[j].hand,
                                                                     points=players[j].points))

    # dealer needs his cards too
    for i in range(2):
        dealer = deal_card(deck, dealer)
    print("{dealer} shows {card}".format(dealer=dealer.name, card=dealer.hand[0]))
    return players, dealer, deck


def get_count(value):
    global card_count
    if 2 <= value <= 6:
        card_count += 1
    if 10 <= value <= 11:
        card_count -= 1
    pass


# allow ai to hit/stand
def ai_play_hands(gamblers, dealer, deck, player_num):
    print("{name}, you have {points} HIT or STAND".format(name=gamblers[player_num].name, points=gamblers[player_num].points))
    print("The Card count is {count}".format(count=card_count))
    # decision matrix based on hi-lo
    # player new card isn't considered in the count?
    # would be better to put the running count in the deal_card function and have it ignore the dealer's second card
    while True:
        if gamblers[player_num].points == 12:
            if "2" in dealer.hand[0] and card_count < 3:
                print("{name} hits!".format(name=gamblers[player_num].name))
                gamblers[player_num] = deal_card(deck, gamblers[player_num])
                gamblers[player_num] = check_ace(gamblers[player_num])
            elif "3" in dealer.hand[0] and card_count < 1:
                print("{name} hits!".format(name=gamblers[player_num].name))
                gamblers[player_num] = deal_card(deck, gamblers[player_num])
                gamblers[player_num] = check_ace(gamblers[player_num])
            elif "4" in dealer.hand[0] and card_count < 0:
                print("{name} hits!".format(name=gamblers[player_num].name))
                gamblers[player_num] = deal_card(deck, gamblers[player_num])
                gamblers[player_num] = check_ace(gamblers[player_num])
            elif "5" in dealer.hand[0] and card_count < -1:
                print("{name} hits!".format(name=gamblers[player_num].name))
                gamblers[player_num] = deal_card(deck, gamblers[player_num])
                gamblers[player_num] = check_ace(gamblers[player_num])
            else:
                print("{name} hits!".format(name=gamblers[player_num].name))
                gamblers[player_num] = deal_card(deck, gamblers[player_num])
                gamblers[player_num] = check_ace(gamblers[player_num])
        elif gamblers[player_num].points == 13:
            if "2" in dealer.hand[0]:
                print("{name} hits!".format(name=gamblers[player_num].name))
                gamblers[player_num] = deal_card(deck, gamblers[player_num])
                gamblers[player_num] = check_ace(gamblers[player_num])
        elif gamblers[player_num].points == 14:
            if "Ace" in dealer.hand[0] and card_count < 9:
                print("{name} hits!".format(name=gamblers[player_num].name))
                gamblers[player_num] = deal_card(deck, gamblers[player_num])
                gamblers[player_num] = check_ace(gamblers[player_num])
        elif gamblers[player_num].points == 15:
            if "7" in dealer.hand[0] and card_count < 10:
                print("{name} hits!".format(name=gamblers[player_num].name))
                gamblers[player_num] = deal_card(deck, gamblers[player_num])
                gamblers[player_num] = check_ace(gamblers[player_num])
            elif "8" in dealer.hand[0] and card_count < 10:
                print("{name} hits!".format(name=gamblers[player_num].name))
                gamblers[player_num] = deal_card(deck, gamblers[player_num])
                gamblers[player_num] = check_ace(gamblers[player_num])
            elif "9" in dealer.hand[0] and card_count < 8:
                print("{name} hits!".format(name=gamblers[player_num].name))
                gamblers[player_num] = deal_card(deck, gamblers[player_num])
                gamblers[player_num] = check_ace(gamblers[player_num])
            elif "10" in dealer.hand[0] or "Jack" in dealer.hand[0] or "Queen" in dealer.hand[0] or "King" in dealer.hand:
                if card_count < 4:
                    print("{name} hits!".format(name=gamblers[player_num].name))
                    gamblers[player_num] = deal_card(deck, gamblers[player_num])
                    gamblers[player_num] = check_ace(gamblers[player_num])
            elif "Ace" in dealer.hand[0] and card_count < 9:
                print("{name} hits!".format(name=gamblers[player_num].name))
                gamblers[player_num] = deal_card(deck, gamblers[player_num])
                gamblers[player_num] = check_ace(gamblers[player_num])
        elif gamblers[player_num].points == 16:
            if "7" in dealer.hand[0] and card_count < 9:
                print("{name} hits!".format(name=gamblers[player_num].name))
                gamblers[player_num] = deal_card(deck, gamblers[player_num])
                gamblers[player_num] = check_ace(gamblers[player_num])
            elif "8" in dealer.hand[0] and card_count < 7:
                print("{name} hits!".format(name=gamblers[player_num].name))
                gamblers[player_num] = deal_card(deck, gamblers[player_num])
                gamblers[player_num] = check_ace(gamblers[player_num])
            elif "9" in dealer.hand[0] and card_count < 5:
                print("{name} hits!".format(name=gamblers[player_num].name))
                gamblers[player_num] = deal_card(deck, gamblers[player_num])
                gamblers[player_num] = check_ace(gamblers[player_num])
            elif "10" in dealer.hand[0] or "Jack" in dealer.hand[0] or "Queen" in dealer.hand[0] or "King" in dealer.hand:
                if card_count < 0:
                    print("{name} hits!".format(name=gamblers[player_num].name))
                    gamblers[player_num] = deal_card(deck, gamblers[player_num])
                    gamblers[player_num] = check_ace(gamblers[player_num])
            elif "Ace" in dealer.hand[0] and card_count < 8:
                print("{name} hits!".format(name=gamblers[player_num].name))
                gamblers[player_num] = deal_card(deck, gamblers[player_num])
                gamblers[player_num] = check_ace(gamblers[player_num])
        elif gamblers[player_num].points < 12:
            pass
        elif gamblers[player_num].points > 16:
            break
        break
    # return card_count, deck, gamblers
    pass


# allow user to hit/stand
def play_hands(gamblers, dealer, deck):
    for i in range(len(gamblers)):
        while True:
            if gamblers[i].ai == "no":
                choice = input("{name}, you have {points} HIT or STAND? \n".format(name=gamblers[i].name,
                                                                                   points=gamblers[i].points))
                if "h" in choice.lower():
                    gamblers[i] = deal_card(deck, gamblers[i])
                    gamblers[i] = check_ace(gamblers[i])
                    print("{card}, you have {points}".format(card=gamblers[i].hand[-1], name=gamblers[i].name,
                                                             points=gamblers[i].points))
                    if gamblers[i].points > 21:
                        print("BUST!")
                        break
                    elif gamblers[i].points == 21:
                        print("Blackjack!")
                        break
                elif "s" in choice.lower():
                    break
            elif gamblers[i].ai == "yes":
                ai_play_hands(gamblers, dealer, deck, i)
                break

    # compare scores to dealer
    print("Dealer shows {hand}. Dealer has {points}".format(hand=dealer.hand, points=dealer.points))
    while True:
        if dealer.points < 17:
            dealer = deal_card(deck, dealer)
            dealer = check_ace(dealer)
            print("Dealer takes a card, it's a {card}, Dealer has {points}".format(card=dealer.hand[-1],
                                                                                   points=dealer.points))
            if dealer.points > 21:
                print("DEALER BUSTS!")
                break
        elif dealer.points == 21:
            print("Dealer has Blackjack!")
            break
        elif 17 <= dealer.points <= 20:
            print("Dealer has {points}, dealer must stand".format(points=dealer.points))
            break
    return gamblers, dealer


# payout
def payout(gamblers, dealer):
    for i in range(len(gamblers)):
        if dealer.points > 21:
            if gamblers[i].points <= 21:
                gamblers[i].cash += 2 * gamblers[i].bet
                print("{player} won ${bet}. New total ${cash}".format(player=gamblers[i].name, bet=gamblers[i].bet,
                                                                      cash=gamblers[i].cash))
            elif gamblers[i].points > 21:
                print("{player} lost ${bet}. New total ${cash}".format(player=gamblers[i].name, cash=gamblers[i].cash,
                                                                       bet=gamblers[i].bet))
        elif dealer.points < gamblers[i].points <= 21:
            gamblers[i].cash += 2 * gamblers[i].bet
            print("{player} won ${bet}. New total ${cash}".format(player=gamblers[i].name, bet=gamblers[i].bet,
                                                                  cash=gamblers[i].cash))
        elif dealer.points == gamblers[i].points:
            gamblers[i].cash += gamblers[i].bet
            print("{player} ties dealer, cash still ${cash}".format(player=gamblers[i].name, cash=gamblers[i].cash))
        elif gamblers[i].points < dealer.points <= 21:
            print("{player} loses to dealer, New total ${cash}".format(player=gamblers[i].name, cash=gamblers[i].cash))
        elif gamblers[i].points > 21:
            print("{player} lost ${bet}. New total ${cash}".format(player=gamblers[i].name, cash=gamblers[i].cash,
                                                                   bet=gamblers[i].bet))
    return gamblers


def reset_hands(gamblers, dealer):
    for i in range(len(gamblers)):
        gamblers[i].points = 0
        gamblers[i].hand = []
        gamblers[i].aces = 0
    dealer.points = 0
    dealer.hand = []
    dealer.aces = 0
    return gamblers, dealer


# check for Ace
def check_ace(gambler):
    if gambler.points > 21 and gambler.aces > 0:
        gambler.points -= 10
        gambler.aces -= 1
    return gambler


def save_game(gamblers):
    print("What would you like to name the saved game?")
    save_name = input()
    with open("Saved_games/" + str(save_name), "w") as save_file:
        save_file.write(str(len(gamblers)) + "\n")
        for i in gamblers:
            save_file.write(i.name)
            save_file.write("\n" + str(i.cash) + "\n")
            save_file.write(str(i.chair) + "\n")
        save_file.close


def new_game():
    choice = input("Would you like to load a saved game? \n")
    choice = choice.lower()
    if "y" in choice:
        print("Please specify the name of the save file. Your choices are:")
        with os.scandir("Saved_games/") as entries:
            for i in entries:
                print(i.name)
        game = input()
        with open("Saved_games/" + game) as save_file:
            classyplayers = []
            for j in range(int(save_file.readline())):
                name = str(save_file.readline())
                player = Player(name)
                player.name = name.rstrip("\n")
                player.cash = int(save_file.readline())
                player.chair = int(save_file.readline())
                classyplayers.append(player)
                print("{player} is sitting in chair {chair} and has ${cash}".format(player=classyplayers[j].name,
                                                                                    chair=classyplayers[j].chair,
                                                                                    cash=classyplayers[j].cash))
            # dealer
            dealer = Player("Dealer")
            dealer.chair = len(classyplayers)
            save_file.close
            return classyplayers, dealer
    if "n" in choice:
        gamblers, dealer = get_players()
        return gamblers, dealer


# kicks people out if they run out of money and gives Game Over if no one is left
def play_again(gamblers):
    losers = []
    for i in range(len(gamblers)):
        if gamblers[i].cash <= 5:
            print("{player} ran out of money and has been kicked from the table".format(player=gamblers[i].name))
            losers.append(gamblers[i])
    for i in losers:
        gamblers.remove(i)
    if len(gamblers) == 0:
        print("GAME OVER!")
        return False
    choice = input("Play another hand? \n")
    if "y" in choice.lower():
        return True
    elif "n" in choice.lower():
        choice2 = input("would you like to save your game? \n")
        if "y" in choice2.lower():
            save_game(gamblers)
            print("Goodbye!")
            return False
        else:
            print("Goodbye!")
            return False
    else:
        play_again(gamblers)


# building the AI


# The actual game
def blackjack():
    playable_hands = 0
    gamblers, dealer = new_game()
    while True:
        if playable_hands == 0:
            current_deck = shuffle_deck(new_deck())
            playable_hands = 6 - len(gamblers)
        playable_hands -= 1
        gamblers, dealer = reset_hands(gamblers, dealer)
        place_bets(gamblers)
        gamblers, dealer, current_deck = two_cards_each(gamblers, dealer, current_deck)
        gamblers, dealer = play_hands(gamblers, dealer, current_deck)
        gamblers = payout(gamblers, dealer)
        choice = play_again(gamblers)
        if choice:
            continue
        else:
            break


blackjack()

# issues to solve:
# more input validation to prevent errors
# splitting
# robot that counts cards and makes decisions bets (ACE)
# robot that plays by the book (Booker)

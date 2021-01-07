import art
import cards
import os
import time
import sys
from random import shuffle


def deck_create():  # creates the deck of cards
    deck_of_cards = []
    for suit in cards.suits.keys():
        for number in cards.numbers:
            deck_of_cards.append((number, suit))
        for letter in cards.letters:
            deck_of_cards.append((letter, suit))
    shuffle(deck_of_cards)
    return deck_of_cards


def start_hand(deck: list):  # gives 2 cards from the deck and removes those cards from the deck
    hand = []
    for index in range(0, 2):
        hand.append(deck[0])
        deck.pop(0)
    return hand


def add_cart(deck: list, hand: list):  # adds a cart to a hand and removes the card from the deck
    hand.append(deck[0])
    deck.pop(0)
    return deck, hand


def turn_handler(deck: list, hand: list, dealer_hand: list):  # the logic behind each turn.
    score, lose = check_score(hand)  # checks the score to see if the player has lost
    time.sleep(2)
    if lose:
        draw_game(hand, dealer_hand, True)
        return deck, hand, score
    else:
        while True:
            action = input("Do you want another card (yes), or do you want to pass (pass)?\n").lower()
            if action == 'yes':
                print("Dealer is adding a card to your hand.")
                deck, hand = add_cart(deck, hand)
                draw_game(hand, dealer_hand, False)
                return turn_handler(deck, hand, dealer_hand)
            elif action == 'pass':
                draw_game(hand, dealer_hand, True)
                return deck, hand, score
            else:
                print("ERROR: Wrong input. Please use 'Yes' for another card or 'Pass' for passing your turn.")


def dealer_control(deck, hand, user_hand, user_score):  # logic for the machine gameplay
    score, lose = check_score(hand)
    time.sleep(3)
    if lose:
        draw_game(user_hand, hand, True)
        return deck, hand, score
    else:
        if score < 17:
            print("Dealer will take a card.")
            deck, hand = add_cart(deck, hand)
            draw_game(user_hand, hand, True)
            return dealer_control(deck, hand, user_hand, user_score)
        elif user_score > 21:
            print("Dealer will pass.")
            draw_game(user_hand, hand, True)
            return deck, hand, score
        elif user_score > score:
            print("Dealer will take a card.")
            deck, hand = add_cart(deck, hand)
            draw_game(user_hand, hand, True)
            return dealer_control(deck, hand, user_hand, user_score)
        elif user_score == score and score <= 11:
            print("Dealer will take a card.")
            deck, hand = add_cart(deck, hand)
            draw_game(user_hand, hand, True)
            return dealer_control(deck, hand, user_hand, user_score)
        elif user_score == score and score > 11:
            draw_game(user_hand, hand, True)
            return deck, hand, score
        else:
            draw_game(user_hand, hand, True)

            return deck, hand, score


def check_score(hand: list):  # the logic behind the score calculation
    score = 0
    ace_counter = 0
    for number, suite in hand:
        if type(number) == str:
            if number == 'J' or number == 'Q' or number == 'K':
                score += 10
            elif number == 'A':
                ace_counter += 1
        else:
            score += int(number)
    for ace in range(0, ace_counter):  # Counting the aces at the end to make sure they are used the best way possible
        if score > 10:
            score += 1
        else:
            score += 11
    if score > 21:
        print(f"Busted with {score} points.")
        lose = True
    elif score == 21:
        print("!!!21!!!")
        lose = False
    else:
        print(f"{score} points thus far.")
        lose = False
    return score, lose


def win_conditions(user_score, dealer_score):  # logic for deciding the end result
    if user_score > 21:
        print(f'You lose with a score of {user_score}')
    elif user_score > dealer_score or dealer_score > 21:
        print(f"You win with a score of {user_score} over the dealer's score of {dealer_score}")
    elif user_score == dealer_score:
        print(f"It is a tie. Both score {user_score}")
    else:
        print(f"You lose with a score of {user_score} over the dealer's score of {dealer_score}")


def draw_game(user_hand, dealer_hand, dealer_turn=False):  # draws the game
    os.system('cls')
    if not dealer_turn:
        print(f"Dealer's cards: ")
        print("\n")
        print(art.draw_card(dealer_hand[0][0], cards.suits[dealer_hand[0][1]]))
        print(art.face_down_card)
        print("\n\n\n")
        print(f"User's cards:")
        print("\n")
        for value, suit in user_hand:
            print(art.draw_card(value, cards.suits[suit]))
    else:
        print(f"User's cards")
        print("\n")
        for value, suit in user_hand:
            print(art.draw_card(value, cards.suits[suit]))
        print("\n\n\n")
        print(f"Dealer's cards:")
        print("\n")
        for value, suit in dealer_hand:
            print(art.draw_card(value, cards.suits[suit]))


def game():  # main method
    os.system('cls')
    print(art.logo)
    time.sleep(1)
    deck = deck_create()  # the deck for this game is created
    user_hand = start_hand(deck)  # the initial hand for the user is created
    dealer_hand = start_hand(deck)  # the initial hand for the dealer is created.
    draw_game(user_hand, dealer_hand)  # game is drawn for the first time
    deck, user_hand, user_score = turn_handler(deck, user_hand, dealer_hand)  # player start to play
    print("Dealer's turn...")
    time.sleep(2)
    deck, dealer_hand, dealer_score = dealer_control(deck, dealer_hand, user_hand, user_score)  # dealer starts to play
    win_conditions(user_score, dealer_score)  # end game results
    while True:  # quit or continue menu
        quit_game = input("Do you want to start another game? Yes/No.\n").lower()
        if quit_game == 'yes':
            game()
        elif quit_game == 'no':
            print("Good Bye!!!")
            time.sleep(1)
            sys.exit(0)
        else:
            print("ERROR: Wrong input. Please use 'Yes' or 'No'.")


game()

import art
import cards
import os
import time
import sys
from random import shuffle


def deck_create():
    deck_of_cards = []
    for suit in cards.suits.keys():
        for number in cards.numbers:
            deck_of_cards.append((number, suit))
        for letter in cards.letters:
            deck_of_cards.append((letter, suit))
    shuffle(deck_of_cards)
    return deck_of_cards


def start_hand(deck: list):
    hand = []
    for index in range(0, 2):
        hand.append(deck[0])
        deck.pop(0)
    return hand


def add_cart(deck: list, hand: list):
    hand.append(deck[0])
    deck.pop(0)
    return deck, hand


def turn_handler(deck: list, hand: list, dealer_hand: list):
    score, lose = check_score(hand)
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


def dealer_control(deck, hand, user_hand, user_score):
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
        elif user_score > score:
            print("Dealer will take a card.")
            deck, hand = add_cart(deck, hand)
            draw_game(user_hand, hand, True)
            return dealer_control(deck, hand, user_hand, user_score)
        elif user_score == score:
            draw_game(user_hand, hand, True)
            return deck, hand, score
        else:
            draw_game(user_hand, hand, True)

            return deck, hand, score


def check_score(hand: list):
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
    for ace in range(0, ace_counter):
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


def win_conditions(user_score, dealer_score):
    if user_score > 21:
        print(f'You lose with a score of {user_score}')
    elif user_score > dealer_score or dealer_score > 21:
        print(f"You win with a score of {user_score} over the dealer's score of {dealer_score}")
    elif user_score == dealer_score:
        print(f"It is a tie. Both score {user_score}")
    else:
        print(f"You lose with a score of {user_score} over the dealer's score of {dealer_score}")


def draw_game(user_hand, dealer_hand, dealer_turn=False):
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


def game():
    os.system('cls')
    print(art.logo)
    time.sleep(2)
    deck = deck_create()
    user_hand = start_hand(deck)
    dealer_hand = start_hand(deck)
    draw_game(user_hand, dealer_hand)
    deck, user_hand, user_score = turn_handler(deck, user_hand, dealer_hand)
    print("Dealer's turn...")
    time.sleep(2)
    deck, dealer_hand, dealer_score = dealer_control(deck, dealer_hand, user_hand, user_score)
    win_conditions(user_score, dealer_score)
    while True:
        quit_game = input("Do you want to star another game? Yes/No.\n").lower()
        if quit_game == 'yes':
            game()
        elif quit_game == 'no':
            print("Good Bye!!!")
            time.sleep(2)
            sys.exit(0)
        else:
            print("ERROR: Wrong input. Please use 'Yes' or 'No'.")


game()

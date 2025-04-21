import math

RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

def get_card_value_for_count(rank):
    if rank in ['2', '3', '4', '5', '6']:
        return 1
    elif rank in ['7', '8', '9']:
        return 0
    elif rank in ['10', 'J', 'Q', 'K', 'A']:
        return -1
    return 0

def get_card_value(rank):
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'A':
        return 11
    else:
        return int(rank)

def evaluate_hand(hand):
    value = 0
    aces = 0
    for card in hand:
        val = get_card_value(card)
        value += val
        if card == 'A':
            aces += 1
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def calculate_true_count(running_count, remaining_decks):
    return running_count / remaining_decks if remaining_decks > 0 else 0

def get_recommendation(player_hand, dealer_card, running_count, remaining_decks):
    player_value = evaluate_hand(player_hand)
    dealer_value = get_card_value(dealer_card)
    true_count = calculate_true_count(running_count, remaining_decks)

    if true_count > 3:
        if player_value in range(12, 17) and dealer_value in range(2, 7):
            return "Stand on 12-16 vs dealer 2-6 (True Count > +3)"
        elif player_value == 16 and dealer_value == 10 and true_count > 4:
            return "Stand on 16 vs 10 (True Count > +4)"
    if true_count < 0:
        if player_value in range(12, 16) and dealer_value >= 7:
            return "Hit on 12-16 vs dealer 7+ (True Count < 0)"
    if player_value >= 17:
        return "Stand (Player total >= 17)"
    return "Hit (Player total < 17)"

def get_bet_recommendation(true_count, min_bet=1, max_bet=8):
    if true_count < 1:
        return f"Bet {min_bet} unit(s)"
    # Scale bet linearly with count up to max_bet
    bet = min(max_bet, min_bet + math.floor(true_count))
    return f"Bet {bet} unit(s)"

def card_counting_assist():
    print("🔢 Blackjack Card Counting Assistant 🔢\n")
    decks_in_play = int(input("Enter the total number of decks in play: "))
    cards_per_deck = 52
    total_cards = decks_in_play * cards_per_deck
    cards_seen = 0
    running_count = 0
    dealt_cards = []

    while True:
        print("\n🎴 Deal cards (type 'done' to finish a round, or 'exit' to quit):")
        card = input("Enter card rank (e.g., '2', '10', 'J', 'A'): ").strip().upper()

        if card == 'EXIT':
            print("Exiting assistant.")
            break
        elif card == 'DONE':
            # Evaluate round state
            remaining_decks = (total_cards - cards_seen) / 52
            true_count = calculate_true_count(running_count, remaining_decks)
            adjusted_prob = 30.8 + (true_count * 2)

            print("\n🧮 Count Summary:")
            print(f"Running Count: {running_count}")
            print(f"True Count: {true_count:.2f}")
            print(f"Cards Seen: {cards_seen} / {total_cards}")
            print(f"Remaining Decks: {remaining_decks:.2f}")
            print(f"Estimated 10-Value Card Probability: {adjusted_prob:.2f}%")
            print(f"💸 Betting Recommendation: {get_bet_recommendation(true_count)}")
            
            # Optional: player hand evaluation
            evaluate = input("\nWould you like a hand recommendation? (y/n): ").strip().lower()
            if evaluate == 'y':
                player_hand = input("Enter player hand (comma separated): ").split(',')
                player_hand = [c.strip().upper() for c in player_hand]
                dealer_card = input("Enter dealer upcard: ").strip().upper()
                advice = get_recommendation(player_hand, dealer_card, running_count, remaining_decks)
                print(f"🧠 Strategy Suggestion: {advice}")
            print("-" * 40)
        elif card in RANKS:
            dealt_cards.append(card)
            running_count += get_card_value_for_count(card)
            cards_seen += 1
            print(f"Added {card}, Running Count: {running_count}")
        else:
            print("Invalid card. Please enter a valid rank like '5', '10', 'A', etc.")

if __name__ == "__main__":
    card_counting_assist()

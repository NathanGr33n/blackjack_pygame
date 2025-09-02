"""Provide simplified blackjack strategy recommendations."""

from __future__ import annotations

from deck import Card


def hand_value(hand: list[Card]) -> int:
    value = 0
    aces = 0
    for card in hand:
        value += card.value()
        if card.rank == "ace":
            aces += 1
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value


def is_soft(hand: list[Card]) -> bool:
    value = 0
    aces = 0
    for card in hand:
        value += card.value()
        if card.rank == "ace":
            aces += 1
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return aces > 0


def suggest_move(player_hand: list[Card], dealer_upcard: Card | None) -> str:
    """Return a basic strategy suggestion.

    Returns "Hit", "Stand", "Double", or "Split" recommendations.
    """
    if not dealer_upcard:
        return "Stand"

    player_total = hand_value(player_hand)
    dealer_val = dealer_upcard.value()
    
    # Check for pairs (split opportunity)
    if len(player_hand) == 2 and player_hand[0].rank == player_hand[1].rank:
        pair_rank = player_hand[0].rank
        
        # Always split aces and 8s
        if pair_rank in ["ace", "8"]:
            return "Split"
        
        # Never split 5s, 4s, or 10-value cards
        if pair_rank in ["5", "4", "10", "jack", "queen", "king"]:
            pass  # Continue to regular strategy
        
        # Split 2s, 3s, 6s, 7s based on dealer upcard
        elif pair_rank in ["2", "3"] and dealer_val in range(2, 8):
            return "Split"
        elif pair_rank == "6" and dealer_val in range(2, 7):
            return "Split"
        elif pair_rank == "7" and dealer_val in range(2, 8):
            return "Split"
        elif pair_rank == "9" and dealer_val in [2, 3, 4, 5, 6, 8, 9]:
            return "Split"
    
    # Check for double down opportunities (only on first two cards)
    if len(player_hand) == 2:
        if is_soft(player_hand):
            # Soft doubling strategy
            if player_total in [13, 14] and dealer_val in [5, 6]:
                return "Double"
            elif player_total in [15, 16] and dealer_val in [4, 5, 6]:
                return "Double"
            elif player_total == 17 and dealer_val in [3, 4, 5, 6]:
                return "Double"
            elif player_total == 18 and dealer_val in [2, 3, 4, 5, 6]:
                return "Double"
        else:
            # Hard doubling strategy
            if player_total == 9 and dealer_val in [3, 4, 5, 6]:
                return "Double"
            elif player_total == 10 and dealer_val in range(2, 10):
                return "Double"
            elif player_total == 11 and dealer_val in range(2, 11):
                return "Double"
    
    # Regular hit/stand strategy
    if is_soft(player_hand):
        if player_total >= 19:
            return "Stand"
        elif player_total == 18:
            return "Stand" if dealer_val in range(2, 9) else "Hit"
        else:
            return "Hit"
    else:
        if player_total >= 17:
            return "Stand"
        elif 13 <= player_total <= 16:
            return "Stand" if dealer_val in range(2, 7) else "Hit"
        elif player_total == 12:
            return "Stand" if dealer_val in range(4, 7) else "Hit"
        else:
            return "Hit"

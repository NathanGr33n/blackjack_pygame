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

    Only "Hit" and "Stand" recommendations are provided.
    """
    if not dealer_upcard:
        return "Stand"

    player_total = hand_value(player_hand)
    dealer_val = dealer_upcard.value()

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

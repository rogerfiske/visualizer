"""
Ticket generator for CA Fantasy 5 predictions.

Generates lottery tickets by combining:
1. Contact scores from matrix analysis
2. Position filters from optimal ranges
3. Configurable selection strategies
"""

import random
from typing import List, Dict, Set, Optional, Tuple
from itertools import combinations

from ..matrix import ContactMatrix, NumericalProximityMatrix
from .position_filter import PositionFilter


class TicketGenerator:
    """
    Generates prediction tickets using contact analysis and position filtering.
    """

    def __init__(
        self,
        matrix: Optional[ContactMatrix] = None,
        position_filter: Optional[PositionFilter] = None,
        seed: Optional[int] = None
    ):
        """
        Initialize the ticket generator.

        Args:
            matrix: ContactMatrix implementation for scoring
            position_filter: PositionFilter for range constraints
            seed: Random seed for reproducibility
        """
        self.matrix = matrix or NumericalProximityMatrix(window_size=3, use_wraparound=True)
        self.position_filter = position_filter or PositionFilter(capture_level='85')

        if seed is not None:
            random.seed(seed)

    def generate_tickets(
        self,
        recent_draws: List[int],
        num_tickets: int = 10,
        strategy: str = 'balanced'
    ) -> List[List[int]]:
        """
        Generate prediction tickets.

        Args:
            recent_draws: Numbers from recent draw(s) for contact analysis
            num_tickets: Number of tickets to generate
            strategy: Selection strategy:
                - 'balanced': Mix contact and position-weighted
                - 'contact_first': Prioritize high contact scores
                - 'position_first': Prioritize position compliance
                - 'random': Random selection within position constraints

        Returns:
            List of 5-number tickets (sorted)
        """
        # Calculate contact scores
        contact_scores = self.matrix.calculate_contact_scores(recent_draws)

        # Get candidates by position
        candidates = self.position_filter.get_candidates_by_position()

        if strategy == 'balanced':
            return self._generate_balanced(contact_scores, candidates, num_tickets)
        elif strategy == 'contact_first':
            return self._generate_contact_first(contact_scores, candidates, num_tickets)
        elif strategy == 'position_first':
            return self._generate_position_first(contact_scores, candidates, num_tickets)
        elif strategy == 'random':
            return self._generate_random(candidates, num_tickets)
        else:
            return self._generate_balanced(contact_scores, candidates, num_tickets)

    def _generate_balanced(
        self,
        contact_scores: Dict[int, float],
        candidates: Dict[str, List[int]],
        num_tickets: int
    ) -> List[List[int]]:
        """Generate tickets balancing contact scores and position compliance."""
        tickets = []
        seen = set()

        # Weight candidates by contact score within each position
        weighted_candidates = {}
        for pos, nums in candidates.items():
            weighted = [(n, contact_scores.get(n, 0) + 0.1) for n in nums]
            weighted_candidates[pos] = weighted

        attempts = 0
        max_attempts = num_tickets * 100

        while len(tickets) < num_tickets and attempts < max_attempts:
            attempts += 1
            ticket = []

            for pos in ['N_1', 'N_2', 'N_3', 'N_4', 'N_5']:
                pool = weighted_candidates[pos]

                # Remove already selected numbers
                available = [(n, w) for n, w in pool if n not in ticket]
                if not available:
                    break

                # Weighted random selection
                total_weight = sum(w for _, w in available)
                if total_weight == 0:
                    num = random.choice([n for n, _ in available])
                else:
                    r = random.random() * total_weight
                    cumulative = 0
                    num = available[0][0]
                    for n, w in available:
                        cumulative += w
                        if cumulative >= r:
                            num = n
                            break

                ticket.append(num)

            if len(ticket) == 5:
                ticket_tuple = tuple(sorted(ticket))
                if ticket_tuple not in seen:
                    seen.add(ticket_tuple)
                    tickets.append(list(ticket_tuple))

        return tickets

    def _generate_contact_first(
        self,
        contact_scores: Dict[int, float],
        candidates: Dict[str, List[int]],
        num_tickets: int
    ) -> List[List[int]]:
        """Generate tickets prioritizing high contact scores."""
        tickets = []
        seen = set()

        # Sort all numbers by contact score
        sorted_by_contact = sorted(
            range(1, 40),
            key=lambda n: contact_scores.get(n, 0),
            reverse=True
        )

        # Try combinations of high-contact numbers that satisfy position constraints
        in_contact = [n for n in sorted_by_contact if contact_scores.get(n, 0) > 0]

        # Generate from high-contact numbers
        for combo in combinations(in_contact[:20], 5):
            if len(tickets) >= num_tickets:
                break

            ticket = sorted(combo)
            is_valid, _ = self.position_filter.validate_ticket(ticket)

            if is_valid:
                ticket_tuple = tuple(ticket)
                if ticket_tuple not in seen:
                    seen.add(ticket_tuple)
                    tickets.append(list(ticket))

        # Fill remaining with balanced approach
        if len(tickets) < num_tickets:
            remaining = self._generate_balanced(
                contact_scores, candidates, num_tickets - len(tickets)
            )
            for t in remaining:
                if tuple(t) not in seen:
                    seen.add(tuple(t))
                    tickets.append(t)

        return tickets[:num_tickets]

    def _generate_position_first(
        self,
        contact_scores: Dict[int, float],
        candidates: Dict[str, List[int]],
        num_tickets: int
    ) -> List[List[int]]:
        """Generate tickets strictly following position constraints."""
        tickets = []
        seen = set()

        attempts = 0
        max_attempts = num_tickets * 50

        while len(tickets) < num_tickets and attempts < max_attempts:
            attempts += 1
            ticket = []

            for pos in ['N_1', 'N_2', 'N_3', 'N_4', 'N_5']:
                available = [n for n in candidates[pos] if n not in ticket]
                if not available:
                    break

                # Slight preference for contact numbers but mostly random
                in_contact = [n for n in available if contact_scores.get(n, 0) > 0]
                if in_contact and random.random() < 0.6:
                    num = random.choice(in_contact)
                else:
                    num = random.choice(available)

                ticket.append(num)

            if len(ticket) == 5:
                ticket_tuple = tuple(sorted(ticket))
                if ticket_tuple not in seen:
                    seen.add(ticket_tuple)
                    tickets.append(list(ticket_tuple))

        return tickets

    def _generate_random(
        self,
        candidates: Dict[str, List[int]],
        num_tickets: int
    ) -> List[List[int]]:
        """Generate random tickets within position constraints."""
        tickets = []
        seen = set()

        attempts = 0
        max_attempts = num_tickets * 50

        while len(tickets) < num_tickets and attempts < max_attempts:
            attempts += 1
            ticket = []

            for pos in ['N_1', 'N_2', 'N_3', 'N_4', 'N_5']:
                available = [n for n in candidates[pos] if n not in ticket]
                if not available:
                    break
                ticket.append(random.choice(available))

            if len(ticket) == 5:
                ticket_tuple = tuple(sorted(ticket))
                if ticket_tuple not in seen:
                    seen.add(ticket_tuple)
                    tickets.append(list(ticket_tuple))

        return tickets

    def score_tickets(
        self,
        tickets: List[List[int]],
        recent_draws: List[int]
    ) -> List[Dict]:
        """
        Score generated tickets.

        Returns list of dicts with ticket info and scores.
        """
        contact_scores = self.matrix.calculate_contact_scores(recent_draws)
        results = []

        for ticket in tickets:
            # Contact score = sum of individual contact scores
            total_contact = sum(contact_scores.get(n, 0) for n in ticket)

            # Position score
            pos_score = self.position_filter.score_ticket(ticket)

            results.append({
                'ticket': ticket,
                'contact_score': total_contact,
                'position_score': pos_score,
                'combined_score': total_contact * pos_score,
            })

        return sorted(results, key=lambda x: -x['combined_score'])


def create_default() -> TicketGenerator:
    """Create TicketGenerator with recommended settings."""
    return TicketGenerator()

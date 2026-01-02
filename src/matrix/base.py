"""
Base interface for contact matrix implementations.

All matrix approaches must implement this interface to enable
consistent comparison and interchangeable usage.
"""

from abc import ABC, abstractmethod
from typing import List, Dict


class ContactMatrix(ABC):
    """Abstract base class for contact matrix implementations."""

    POOL_SIZE = 39  # CA Fantasy 5: numbers 1-39

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of this matrix implementation."""
        pass

    @abstractmethod
    def get_neighbors(self, number: int) -> List[int]:
        """
        Return list of numbers considered 'adjacent' to given number.

        Args:
            number: A lottery number (1-39)

        Returns:
            List of adjacent/neighbor numbers
        """
        pass

    @abstractmethod
    def get_neighbor_count(self, number: int) -> int:
        """
        Return the number of neighbors for a given number.

        Args:
            number: A lottery number (1-39)

        Returns:
            Count of neighbors
        """
        pass

    @abstractmethod
    def get_bias_factor(self, number: int) -> float:
        """
        Return bias correction factor for a number.

        1.0 means no bias/correction needed.
        >1.0 means number is underweighted and needs boosting.
        <1.0 means number is overweighted and needs reduction.

        Args:
            number: A lottery number (1-39)

        Returns:
            Bias correction factor
        """
        pass

    def calculate_contact_scores(self, recent_draws: List[int]) -> Dict[int, float]:
        """
        Calculate contact score for all numbers 1-39 based on recent draws.

        A number's contact score = count of how many recent draw numbers
        it is adjacent to, multiplied by its bias correction factor.

        Args:
            recent_draws: List of recently drawn numbers

        Returns:
            Dict mapping each number (1-39) to its contact score
        """
        scores = {}
        for n in range(1, self.POOL_SIZE + 1):
            neighbors = set(self.get_neighbors(n))
            raw_score = len(neighbors.intersection(recent_draws))
            corrected_score = raw_score * self.get_bias_factor(n)
            scores[n] = corrected_score
        return scores

    def get_in_contact_numbers(self, recent_draws: List[int]) -> List[int]:
        """
        Return all numbers that are 'in contact' with recent draws.

        Args:
            recent_draws: List of recently drawn numbers

        Returns:
            List of numbers adjacent to at least one recent draw
        """
        in_contact = set()
        for draw in recent_draws:
            if 1 <= draw <= self.POOL_SIZE:
                in_contact.update(self.get_neighbors(draw))
        # Also include the drawn numbers themselves
        in_contact.update(d for d in recent_draws if 1 <= d <= self.POOL_SIZE)
        return sorted(in_contact)

    def analyze_bias(self) -> Dict[str, any]:
        """
        Analyze the bias characteristics of this matrix.

        Returns:
            Dict with bias analysis metrics
        """
        neighbor_counts = [self.get_neighbor_count(n) for n in range(1, self.POOL_SIZE + 1)]
        bias_factors = [self.get_bias_factor(n) for n in range(1, self.POOL_SIZE + 1)]

        # Effective contacts = neighbor_count * bias_factor
        effective_contacts = [
            self.get_neighbor_count(n) * self.get_bias_factor(n)
            for n in range(1, self.POOL_SIZE + 1)
        ]

        return {
            'name': self.name,
            'min_neighbors': min(neighbor_counts),
            'max_neighbors': max(neighbor_counts),
            'avg_neighbors': sum(neighbor_counts) / len(neighbor_counts),
            'neighbor_variance': max(neighbor_counts) - min(neighbor_counts),
            'min_effective': min(effective_contacts),
            'max_effective': max(effective_contacts),
            'avg_effective': sum(effective_contacts) / len(effective_contacts),
            'effective_variance': max(effective_contacts) - min(effective_contacts),
            'is_uniform': max(effective_contacts) - min(effective_contacts) < 0.5,
        }

    def _validate_number(self, number: int) -> None:
        """Validate that a number is in the valid pool range."""
        if not 1 <= number <= self.POOL_SIZE:
            raise ValueError(f"Number must be between 1 and {self.POOL_SIZE}, got {number}")

"""
Matrix implementations for lottery contact analysis.

This module provides different approaches to defining "contact" between
lottery numbers, addressing the structural bias in VLA's standard grid.

Available implementations:
- VLAStandardMatrix: Original VLA 6x7 grid (baseline, exhibits bias)
- WeightedAdjacencyMatrix: VLA grid with bias correction factors
- NumericalProximityMatrix: Non-geometric, uses numerical distance

Usage:
    from src.matrix import NumericalProximityMatrix, WeightedAdjacencyMatrix

    # Create matrix instances
    proximity = NumericalProximityMatrix(window_size=3, use_wraparound=True)
    weighted = WeightedAdjacencyMatrix(apply_correction=True)

    # Get neighbors for a number
    neighbors = proximity.get_neighbors(15)

    # Calculate contact scores for recent draws
    recent_draws = [3, 15, 22, 28, 37]
    scores = proximity.calculate_contact_scores(recent_draws)

    # Analyze bias characteristics
    bias_info = proximity.analyze_bias()
"""

from .base import ContactMatrix
from .vla_standard import VLAStandardMatrix
from .weighted_adjacency import WeightedAdjacencyMatrix
from .numerical_proximity import NumericalProximityMatrix
from .csv_matrix import CSVGridMatrix, analyze_matrix


# Factory functions for easy creation
def create_matrix(matrix_type: str, **kwargs) -> ContactMatrix:
    """
    Factory function to create matrix instances by type name.

    Args:
        matrix_type: One of 'vla', 'weighted', 'proximity'
        **kwargs: Additional arguments passed to constructor

    Returns:
        ContactMatrix instance
    """
    if matrix_type == 'vla' or matrix_type == 'vla_standard':
        return VLAStandardMatrix()
    elif matrix_type == 'weighted' or matrix_type == 'weighted_adjacency':
        return WeightedAdjacencyMatrix(**kwargs)
    elif matrix_type == 'proximity' or matrix_type == 'numerical_proximity':
        return NumericalProximityMatrix(**kwargs)
    else:
        raise ValueError(f"Unknown matrix type: {matrix_type}")


__all__ = [
    'ContactMatrix',
    'VLAStandardMatrix',
    'WeightedAdjacencyMatrix',
    'NumericalProximityMatrix',
    'CSVGridMatrix',
    'analyze_matrix',
    'create_matrix',
]

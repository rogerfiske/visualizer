"""
Main predictor module for CA Fantasy 5.

Combines all components into a unified prediction interface.
"""

from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple

from ..matrix import ContactMatrix, NumericalProximityMatrix, WeightedAdjacencyMatrix
from .data_loader import DrawHistory
from .position_filter import PositionFilter
from .ticket_generator import TicketGenerator


class CA5Predictor:
    """
    Complete prediction system for CA Fantasy 5.

    Combines:
    - Historical draw data
    - Bias-corrected contact matrix
    - Position-based filtering
    - Ticket generation

    Usage:
        predictor = CA5Predictor()
        tickets = predictor.predict(target_date=datetime(2025, 12, 31), num_tickets=20)
    """

    def __init__(
        self,
        matrix_type: str = 'proximity',
        capture_level: str = '85',
        lookback_draws: int = 1,
        data_path: Optional[Path] = None
    ):
        """
        Initialize the predictor.

        Args:
            matrix_type: 'proximity' or 'weighted' (VLA-style with correction)
            capture_level: '80', '85', or '90' for position filter stringency
            lookback_draws: Number of previous draws to use for contact analysis
            data_path: Optional custom path to CA5_date.csv
        """
        # Initialize components
        self.history = DrawHistory(data_path)
        self.position_filter = PositionFilter(capture_level)
        self.lookback_draws = lookback_draws

        # Select matrix type
        if matrix_type == 'weighted':
            self.matrix = WeightedAdjacencyMatrix(apply_correction=True)
        else:
            self.matrix = NumericalProximityMatrix(window_size=3, use_wraparound=True)

        self.generator = TicketGenerator(
            matrix=self.matrix,
            position_filter=self.position_filter
        )

        self.matrix_type = matrix_type
        self.capture_level = capture_level

    def predict(
        self,
        target_date: Optional[datetime] = None,
        num_tickets: int = 20,
        strategy: str = 'balanced'
    ) -> Dict:
        """
        Generate predictions for a target date.

        Args:
            target_date: Date to predict for. Uses draws BEFORE this date.
                        Defaults to day after last draw in dataset.
            num_tickets: Number of tickets to generate
            strategy: Generation strategy ('balanced', 'contact_first',
                     'position_first', 'random')

        Returns:
            Dict containing:
            - target_date: The date being predicted
            - previous_draw: The draw used for contact analysis
            - tickets: List of generated tickets
            - config: Configuration used
        """
        # Determine target date
        if target_date is None:
            last_draw = self.history.get_last_draw()
            if last_draw:
                target_date = last_draw['date'] + timedelta(days=1)
            else:
                raise ValueError("No draw data available")

        # Get recent draws for contact analysis
        recent_draws = self.history.get_draws_before(target_date, self.lookback_draws)
        if not recent_draws:
            raise ValueError(f"No draws found before {target_date}")

        # Extract numbers from recent draws
        recent_numbers = []
        for draw in recent_draws:
            recent_numbers.extend(draw['numbers'])

        # Generate tickets
        tickets = self.generator.generate_tickets(
            recent_draws=recent_numbers,
            num_tickets=num_tickets,
            strategy=strategy
        )

        # Score tickets
        scored = self.generator.score_tickets(tickets, recent_numbers)

        return {
            'target_date': target_date,
            'target_date_str': target_date.strftime('%Y-%m-%d'),
            'previous_draws': [d['numbers'] for d in recent_draws],
            'previous_dates': [d['date_str'] for d in recent_draws],
            'tickets': tickets,
            'scored_tickets': scored,
            'config': {
                'matrix_type': self.matrix_type,
                'capture_level': self.capture_level,
                'lookback_draws': self.lookback_draws,
                'strategy': strategy,
                'num_tickets': num_tickets,
            }
        }

    def backtest_single(
        self,
        test_date: datetime,
        num_tickets: int = 20,
        strategy: str = 'balanced'
    ) -> Dict:
        """
        Run backtest for a single date.

        Args:
            test_date: Date to test (must have actual results)
            num_tickets: Number of tickets to generate
            strategy: Generation strategy

        Returns:
            Dict with prediction results and scoring
        """
        # Generate predictions
        result = self.predict(
            target_date=test_date,
            num_tickets=num_tickets,
            strategy=strategy
        )

        # Get actual result
        actual_draw = self.history.get_draw_by_date(test_date)
        if not actual_draw:
            result['actual'] = None
            result['scores'] = None
            result['best_match'] = 0
            return result

        actual_numbers = set(actual_draw['numbers'])
        result['actual'] = actual_draw['numbers']
        result['actual_date_str'] = actual_draw['date_str']

        # Score each ticket
        scores = []
        for ticket in result['tickets']:
            matches = len(set(ticket) & actual_numbers)
            matching_nums = list(set(ticket) & actual_numbers)
            scores.append({
                'ticket': ticket,
                'matches': matches,
                'matching_numbers': matching_nums
            })

        result['scores'] = sorted(scores, key=lambda x: -x['matches'])
        result['best_match'] = max(s['matches'] for s in scores) if scores else 0

        # Summary statistics
        match_dist = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for s in scores:
            match_dist[s['matches']] = match_dist.get(s['matches'], 0) + 1

        result['match_distribution'] = match_dist
        result['tickets_with_3plus'] = sum(match_dist.get(i, 0) for i in [3, 4, 5])

        return result

    def backtest_range(
        self,
        start_date: datetime,
        end_date: datetime,
        num_tickets: int = 20,
        strategy: str = 'balanced'
    ) -> Dict:
        """
        Run backtest over a date range.

        Args:
            start_date: First date to test
            end_date: Last date to test
            num_tickets: Tickets per day
            strategy: Generation strategy

        Returns:
            Dict with aggregated results
        """
        results = []
        total_best = []
        total_3plus = 0

        for draw, _ in self.history.iterate_from_date(start_date):
            if draw['date'].date() > end_date.date():
                break

            result = self.backtest_single(
                test_date=draw['date'],
                num_tickets=num_tickets,
                strategy=strategy
            )

            if result['actual']:
                results.append(result)
                total_best.append(result['best_match'])
                total_3plus += result['tickets_with_3plus']

        # Aggregate statistics
        if results:
            avg_best = sum(total_best) / len(total_best)
            match_5 = sum(1 for b in total_best if b == 5)
            match_4 = sum(1 for b in total_best if b >= 4)
            match_3 = sum(1 for b in total_best if b >= 3)
        else:
            avg_best = 0
            match_5 = match_4 = match_3 = 0

        return {
            'start_date': start_date,
            'end_date': end_date,
            'days_tested': len(results),
            'config': {
                'matrix_type': self.matrix_type,
                'capture_level': self.capture_level,
                'strategy': strategy,
                'num_tickets': num_tickets,
            },
            'summary': {
                'avg_best_match': avg_best,
                'days_with_5_match': match_5,
                'days_with_4plus_match': match_4,
                'days_with_3plus_match': match_3,
                'total_3plus_tickets': total_3plus,
            },
            'daily_results': results,
        }

    def export_predictions(
        self,
        tickets: List[List[int]],
        output_path: Path,
        format: str = 'csv'
    ) -> None:
        """
        Export predictions to file.

        Args:
            tickets: List of tickets to export
            output_path: Output file path
            format: 'csv' or 'txt'
        """
        output_path = Path(output_path)

        with open(output_path, 'w') as f:
            if format == 'csv':
                f.write("N_1,N_2,N_3,N_4,N_5\n")
                for ticket in tickets:
                    f.write(",".join(str(n) for n in ticket) + "\n")
            else:
                for ticket in tickets:
                    f.write(" ".join(str(n) for n in ticket) + "\n")

    def get_info(self) -> Dict:
        """Get predictor configuration info."""
        start, end = self.history.get_date_range()
        return {
            'matrix': self.matrix.name,
            'position_filter': str(self.position_filter),
            'lookback_draws': self.lookback_draws,
            'data_range': f"{start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}",
            'total_draws': len(self.history),
        }


def create_default() -> CA5Predictor:
    """Create CA5Predictor with recommended settings."""
    return CA5Predictor(
        matrix_type='proximity',
        capture_level='85',
        lookback_draws=1
    )

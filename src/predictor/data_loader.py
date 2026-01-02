"""
Data loader for CA Fantasy 5 historical draws.

Loads draw history from CSV and provides methods for accessing
recent draws for contact analysis.
"""

import csv
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple


class DrawHistory:
    """Manages historical lottery draw data."""

    def __init__(self, data_path: Optional[Path] = None):
        """
        Initialize with path to CA5_date.csv.

        Args:
            data_path: Path to CSV file. Defaults to project data location.
        """
        if data_path is None:
            # Default to project data location
            project_root = Path(__file__).parent.parent.parent
            data_path = project_root / "data" / "raw" / "CA5_date.csv"

        self.data_path = Path(data_path)
        self.draws: List[Dict] = []
        self._date_index: Dict[str, int] = {}
        self._load_data()

    def _parse_date(self, date_str: str) -> datetime:
        """Parse date from M/D/YYYY format."""
        for fmt in ["%m/%d/%Y", "%Y-%m-%d", "%m-%d-%Y"]:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue
        raise ValueError(f"Cannot parse date: {date_str}")

    def _load_data(self) -> None:
        """Load all draws from CSV file."""
        with open(self.data_path, 'r') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                try:
                    draw = {
                        'date': self._parse_date(row['date']),
                        'date_str': row['date'],
                        'numbers': [
                            int(row['N_1']),
                            int(row['N_2']),
                            int(row['N_3']),
                            int(row['N_4']),
                            int(row['N_5']),
                        ]
                    }
                    self.draws.append(draw)
                    self._date_index[row['date']] = len(self.draws) - 1
                except (KeyError, ValueError) as e:
                    continue

        # Sort by date (oldest first)
        self.draws.sort(key=lambda x: x['date'])

        # Rebuild index after sorting
        self._date_index = {}
        for i, draw in enumerate(self.draws):
            self._date_index[draw['date_str']] = i

    def __len__(self) -> int:
        return len(self.draws)

    def get_draw_by_date(self, date: datetime) -> Optional[Dict]:
        """Get draw for a specific date."""
        # Direct search by date comparison (most reliable)
        for draw in self.draws:
            if draw['date'].date() == date.date():
                return draw
        return None

    def get_draws_before(self, date: datetime, count: int = 1) -> List[Dict]:
        """
        Get the most recent draws BEFORE a given date.

        Args:
            date: Reference date
            count: Number of draws to retrieve

        Returns:
            List of draws, most recent first
        """
        results = []
        for draw in reversed(self.draws):
            if draw['date'].date() < date.date():
                results.append(draw)
                if len(results) >= count:
                    break
        return results

    def get_recent_numbers(self, before_date: datetime, num_draws: int = 1) -> List[int]:
        """
        Get numbers from recent draws before a date.

        Args:
            before_date: Reference date
            num_draws: Number of draws to include

        Returns:
            Flat list of all numbers from recent draws
        """
        draws = self.get_draws_before(before_date, num_draws)
        numbers = []
        for draw in draws:
            numbers.extend(draw['numbers'])
        return numbers

    def get_last_draw(self) -> Optional[Dict]:
        """Get the most recent draw in the dataset."""
        return self.draws[-1] if self.draws else None

    def get_date_range(self) -> Tuple[datetime, datetime]:
        """Get the date range of the dataset."""
        if not self.draws:
            return None, None
        return self.draws[0]['date'], self.draws[-1]['date']

    def iterate_from_date(self, start_date: datetime):
        """
        Iterate through draws starting from a date.

        Yields:
            (draw_dict, previous_draws) tuples for backtesting
        """
        for i, draw in enumerate(self.draws):
            if draw['date'].date() >= start_date.date():
                previous = self.draws[:i]
                yield draw, previous


def create_default() -> DrawHistory:
    """Create DrawHistory with default data path."""
    return DrawHistory()

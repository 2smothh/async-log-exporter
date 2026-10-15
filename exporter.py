import asyncio
import json
import csv
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@dataclass
class LogEntry:
    timestamp: str
    level: str
    message: str
    service: str

class AsyncLogProcessor:
    """Asynchronous log processing and exporting utility for microservices."""
    
    def __init__(self, batch_size: int = 100):
        self.batch_size = batch_size
        self._buffer: List[LogEntry] = []

    async def ingest_log(self, level: str, message: str, service: str = "default") -> None:
        """Simulates ingestion of a log entry."""
        entry = LogEntry(
            timestamp=datetime.utcnow().isoformat(),
            level=level.upper(),
            message=message,
            service=service
        )
        self._buffer.append(entry)
        logging.debug(f"Ingested log from {service}: {message}")

    async def export_to_json(self, output_filepath: str) -> None:
        """Exports buffered logs asynchronously to a JSON file."""
        if not self._buffer:
            logging.warning("No logs to export.")
            return

        data = [asdict(entry) for entry in self._buffer]
        await asyncio.sleep(0.1)
        
        with open(output_filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        
        logging.info(f"Successfully exported {len(data)} logs to {output_filepath}")

    async def export_to_csv(self, output_filepath: str) -> None:
        """Exports buffered logs asynchronously to a CSV file."""
        if not self._buffer:
            logging.warning("No logs to export.")
            return

        await asyncio.sleep(0.1)
        
        fieldnames = ["timestamp", "level", "message", "service"]
        with open(output_filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for entry in self._buffer:
                writer.writerow(asdict(entry))

        logging.info(f"Successfully exported {len(self._buffer)} logs to {output_filepath}")

    def filter_by_level(self, level: str) -> List[LogEntry]:
        """Filters in-memory logs by severity level."""
        return [entry for entry in self._buffer if entry.level == level.upper()]

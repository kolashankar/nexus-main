"""Background Karma Processing Task"""

import logging
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class KarmaProcessor:
    """Processes karma evaluations in background"""

    def __init__(self):
        self.queue: List[Dict[str, Any]] = []
        self.processing = False

    def add_to_queue(self, evaluation_data: Dict[str, Any]) -> None:
        """Add evaluation to processing queue"""
        self.queue.append({
            **evaluation_data,
            "queued_at": datetime.utcnow().isoformat()
        })
        logger.info(
            f"Added karma evaluation to queue. Queue size: {len(self.queue)}")

    async def process_queue(self) -> None:
        """Process all queued karma evaluations"""

        if self.processing:
            logger.info("Karma processor already running")
            return

        self.processing = True
        logger.info(
            f"Starting karma queue processing. Queue size: {len(self.queue)}")

        try:
            while self.queue:
                item = self.queue.pop(0)
                await self._process_item(item)

        except Exception as e:
            logger.error(f"Error processing karma queue: {e}")

        finally:
            self.processing = False
            logger.info("Karma queue processing complete")

    async def _process_item(self, item: Dict[str, Any]) -> None:
        """Process a single karma evaluation"""
        try:
            # Import here to avoid circular imports
            from ..services.ai.karma_arbiter.arbiter import karma_arbiter

            result = await karma_arbiter.evaluate_action(
                action_type=item["action_type"],
                action_details=item["action_details"],
                actor=item["actor"],
                target=item.get("target"),
                additional_context=item.get("context")
            )

            logger.info(
                f"Processed karma evaluation: {result.karma_change} karma")

        except Exception as e:
            logger.error(f"Error processing karma item: {e}")


# Global karma processor instance
karma_processor = KarmaProcessor()


async def process_karma_queue() -> None:
    """Background task to process karma queue"""
    await karma_processor.process_queue()

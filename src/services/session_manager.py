"""
Session Manager
Manages synthesis sessions and progress tracking
"""
from queue import Queue, Empty
from threading import Thread, Lock
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from src.config.logging_config import get_logger

logger = get_logger(__name__)


class SessionManager:
    """Manages synthesis sessions and progress tracking"""

    def __init__(self, timeout_seconds: int = 300):
        """
        Initialize session manager

        Args:
            timeout_seconds: Timeout for inactive sessions
        """
        self.timeout_seconds = timeout_seconds
        self._sessions: Dict[str, Queue] = {}
        self._session_timestamps: Dict[str, datetime] = {}
        self._lock = Lock()

    def create_session(self, session_id: str) -> Queue:
        """
        Create a new session

        Args:
            session_id: Unique session identifier

        Returns:
            Progress queue for the session
        """
        with self._lock:
            queue = Queue()
            self._sessions[session_id] = queue
            self._session_timestamps[session_id] = datetime.now()
            logger.info(f"Created session: {session_id}")
            return queue

    def get_session(self, session_id: str) -> Optional[Queue]:
        """
        Get session queue

        Args:
            session_id: Session identifier

        Returns:
            Queue if session exists, None otherwise
        """
        with self._lock:
            return self._sessions.get(session_id)

    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session

        Args:
            session_id: Session identifier

        Returns:
            True if session was deleted, False if not found
        """
        with self._lock:
            if session_id in self._sessions:
                del self._sessions[session_id]
                del self._session_timestamps[session_id]
                logger.info(f"Deleted session: {session_id}")
                return True
            return False

    def send_progress(
        self,
        session_id: str,
        step: int,
        message: str,
        progress: int
    ) -> bool:
        """
        Send progress update to session

        Args:
            session_id: Session identifier
            step: Current step number
            message: Progress message
            progress: Progress percentage (0-100)

        Returns:
            True if sent successfully, False if session not found
        """
        queue = self.get_session(session_id)
        if queue is None:
            logger.warning(f"Attempted to send progress to non-existent session: {session_id}")
            return False

        queue.put({
            'step': step,
            'message': message,
            'progress': progress
        })
        return True

    def send_completion(
        self,
        session_id: str,
        output_file: str,
        chunks_processed: int = 1
    ) -> bool:
        """
        Send completion message to session

        Args:
            session_id: Session identifier
            output_file: Generated output filename
            chunks_processed: Number of chunks processed

        Returns:
            True if sent successfully, False if session not found
        """
        queue = self.get_session(session_id)
        if queue is None:
            logger.warning(f"Attempted to send completion to non-existent session: {session_id}")
            return False

        queue.put({
            'complete': True,
            'output_file': output_file,
            'message': f'Speech synthesized successfully! ({chunks_processed} chunk{"s" if chunks_processed > 1 else ""})'
        })
        logger.info(f"Session completed: {session_id}")
        return True

    def send_error(self, session_id: str, error_message: str) -> bool:
        """
        Send error message to session

        Args:
            session_id: Session identifier
            error_message: Error description

        Returns:
            True if sent successfully, False if session not found
        """
        queue = self.get_session(session_id)
        if queue is None:
            logger.warning(f"Attempted to send error to non-existent session: {session_id}")
            return False

        queue.put({
            'error': True,
            'message': error_message
        })
        logger.error(f"Session error: {session_id} - {error_message}")
        return True

    def get_progress(self, session_id: str, timeout: int = 30) -> Optional[Dict[str, Any]]:
        """
        Get next progress update from session

        Args:
            session_id: Session identifier
            timeout: Timeout in seconds

        Returns:
            Progress update dict or None if timeout
        """
        queue = self.get_session(session_id)
        if queue is None:
            return {"error": "Invalid session ID"}

        try:
            return queue.get(timeout=timeout)
        except Empty:
            # Timeout - send keepalive
            return {"keepalive": True}

    def cleanup_old_sessions(self) -> int:
        """
        Clean up old/inactive sessions

        Returns:
            Number of sessions cleaned up
        """
        cutoff_time = datetime.now() - timedelta(seconds=self.timeout_seconds)
        cleaned = 0

        with self._lock:
            session_ids = list(self._session_timestamps.keys())
            for session_id in session_ids:
                if self._session_timestamps[session_id] < cutoff_time:
                    del self._sessions[session_id]
                    del self._session_timestamps[session_id]
                    cleaned += 1
                    logger.info(f"Cleaned up inactive session: {session_id}")

        if cleaned > 0:
            logger.info(f"Cleaned up {cleaned} inactive sessions")

        return cleaned

    def get_active_session_count(self) -> int:
        """Get number of active sessions"""
        with self._lock:
            return len(self._sessions)


# Global session manager instance
_session_manager: Optional[SessionManager] = None


def get_session_manager(timeout_seconds: int = 300) -> SessionManager:
    """
    Get or create global session manager instance

    Args:
        timeout_seconds: Session timeout

    Returns:
        SessionManager instance
    """
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager(timeout_seconds)
    return _session_manager

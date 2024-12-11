class JobError(Exception):
    """Job returns an error state"""

class JobTimeoutError(Exception):
    """Job doesn't complete within the expected time"""

class CancellationError(Exception):
    """User cancels the polling"""

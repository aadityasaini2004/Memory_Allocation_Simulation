class MemorySimulatorError(Exception):
    """Base exception for all domain errors."""
    pass

class InvalidMemoryRequestError(MemorySimulatorError):
    pass

class DuplicateProcessError(MemorySimulatorError):
    pass

class ProcessNotFoundError(MemorySimulatorError):
    pass

class InsufficientMemoryError(MemorySimulatorError):
    pass

class ExternalFragmentationError(MemorySimulatorError):
    pass

class MemoryIntegrityError(MemorySimulatorError):
    pass

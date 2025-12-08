"""
Database utility functions with transaction handling and error logging.
"""
import logging
from django.db import transaction, IntegrityError, DatabaseError
from typing import Callable, Any, Optional

logger = logging.getLogger(__name__)


def atomic_operation(operation: Callable, *args, **kwargs) -> tuple[bool, Optional[Any], Optional[str]]:
    """
    Execute a database operation within an atomic transaction.
    
    Args:
        operation: The callable to execute within the transaction
        *args: Positional arguments to pass to the operation
        **kwargs: Keyword arguments to pass to the operation
    
    Returns:
        A tuple of (success: bool, result: Any, error_message: Optional[str])
    """
    try:
        with transaction.atomic():
            result = operation(*args, **kwargs)
            return True, result, None
    except IntegrityError as e:
        error_msg = f"Integrity error in database operation: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, None, error_msg
    except DatabaseError as e:
        error_msg = f"Database error in operation: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, None, error_msg
    except Exception as e:
        error_msg = f"Unexpected error in database operation: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, None, error_msg


def safe_bulk_create(model_class, instances: list, batch_size: Optional[int] = None) -> tuple[bool, list, Optional[str]]:
    """
    Safely perform bulk create operation with transaction handling.
    
    Args:
        model_class: The Django model class
        instances: List of model instances to create
        batch_size: Optional batch size for bulk creation
    
    Returns:
        A tuple of (success: bool, created_instances: list, error_message: Optional[str])
    """
    try:
        with transaction.atomic():
            created = model_class.objects.bulk_create(instances, batch_size=batch_size)
            return True, created, None
    except IntegrityError as e:
        error_msg = f"Integrity error during bulk create: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, [], error_msg
    except DatabaseError as e:
        error_msg = f"Database error during bulk create: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, [], error_msg
    except Exception as e:
        error_msg = f"Unexpected error during bulk create: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, [], error_msg


def safe_update(instance, **fields) -> tuple[bool, Optional[Any], Optional[str]]:
    """
    Safely update a model instance with transaction handling.
    
    Args:
        instance: The model instance to update
        **fields: Field names and values to update
    
    Returns:
        A tuple of (success: bool, updated_instance: Optional[Any], error_message: Optional[str])
    """
    try:
        with transaction.atomic():
            for field, value in fields.items():
                setattr(instance, field, value)
            instance.save()
            return True, instance, None
    except IntegrityError as e:
        error_msg = f"Integrity error during update: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, None, error_msg
    except DatabaseError as e:
        error_msg = f"Database error during update: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, None, error_msg
    except Exception as e:
        error_msg = f"Unexpected error during update: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, None, error_msg


def safe_delete(instance) -> tuple[bool, Optional[str]]:
    """
    Safely delete a model instance with transaction handling.
    
    Args:
        instance: The model instance to delete
    
    Returns:
        A tuple of (success: bool, error_message: Optional[str])
    """
    try:
        with transaction.atomic():
            instance.delete()
            return True, None
    except DatabaseError as e:
        error_msg = f"Database error during delete: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, error_msg
    except Exception as e:
        error_msg = f"Unexpected error during delete: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, error_msg

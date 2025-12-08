from django.db import models, transaction, IntegrityError
from django.utils.text import slugify
import uuid
import logging

logger = logging.getLogger(__name__)


class Project(models.Model):
    """
    Portfolio project entry with title, description, and featured status.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    description = models.TextField()
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        """
        Save the project with automatic slug generation.
        Wraps the save operation in error handling for integrity errors.
        """
        if not self.slug:
            base_slug = slugify(self.title)
            # Handle edge case where slugify returns empty string
            if not base_slug:
                base_slug = f'project-{uuid.uuid4().hex[:8]}'
            self.slug = base_slug
        
        try:
            super().save(*args, **kwargs)
        except IntegrityError as e:
            logger.error(f"Integrity error saving Project '{self.title}': {str(e)}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Error saving Project '{self.title}': {str(e)}", exc_info=True)
            raise
    
    def __str__(self):
        return self.title


class Devlog(models.Model):
    """
    Development log entry containing title, tagline, markdown content, and publication status.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    tagline = models.CharField(max_length=300)
    content = models.TextField()  # Markdown content
    is_published = models.BooleanField(default=False)
    project = models.ForeignKey(
        'Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='devlogs'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        """
        Save the devlog with automatic slug generation.
        Wraps the save operation in error handling for integrity errors.
        """
        if not self.slug:
            base_slug = slugify(self.title)
            # Handle edge case where slugify returns empty string
            if not base_slug:
                base_slug = f'devlog-{uuid.uuid4().hex[:8]}'
            self.slug = base_slug
        
        try:
            super().save(*args, **kwargs)
        except IntegrityError as e:
            logger.error(f"Integrity error saving Devlog '{self.title}': {str(e)}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Error saving Devlog '{self.title}': {str(e)}", exc_info=True)
            raise
    
    def __str__(self):
        return self.title

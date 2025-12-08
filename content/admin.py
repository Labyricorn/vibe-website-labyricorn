from django.contrib import admin
from django.db import transaction, IntegrityError
from django.contrib import messages
import logging
from .models import Devlog, Project

logger = logging.getLogger(__name__)


@admin.register(Devlog)
class DevlogAdmin(admin.ModelAdmin):
    """
    Admin configuration for Devlog model.
    """
    list_display = ['title', 'is_published', 'project', 'created_at']
    list_filter = ['is_published', 'created_at', 'project']
    search_fields = ['title', 'tagline', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    
    def save_model(self, request, obj, form, change):
        """
        Save the model with transaction handling and error logging.
        """
        try:
            with transaction.atomic():
                super().save_model(request, obj, form, change)
                messages.success(request, f"Devlog '{obj.title}' saved successfully.")
        except IntegrityError as e:
            logger.error(f"Integrity error saving Devlog in admin: {str(e)}", exc_info=True)
            messages.error(request, f"Error saving devlog: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error saving Devlog in admin: {str(e)}", exc_info=True)
            messages.error(request, f"Unexpected error: {str(e)}")
            raise
    
    def delete_model(self, request, obj):
        """
        Delete the model with transaction handling and error logging.
        """
        try:
            with transaction.atomic():
                super().delete_model(request, obj)
                messages.success(request, f"Devlog '{obj.title}' deleted successfully.")
        except Exception as e:
            logger.error(f"Error deleting Devlog in admin: {str(e)}", exc_info=True)
            messages.error(request, f"Error deleting devlog: {str(e)}")
            raise
    
    def delete_queryset(self, request, queryset):
        """
        Delete multiple objects with transaction handling.
        """
        try:
            with transaction.atomic():
                count = queryset.count()
                super().delete_queryset(request, queryset)
                messages.success(request, f"Successfully deleted {count} devlog(s).")
        except Exception as e:
            logger.error(f"Error bulk deleting Devlogs in admin: {str(e)}", exc_info=True)
            messages.error(request, f"Error deleting devlogs: {str(e)}")
            raise


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin configuration for Project model.
    """
    list_display = ['title', 'is_featured', 'created_at', 'devlog_count']
    list_filter = ['is_featured', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    
    def devlog_count(self, obj):
        """
        Display the count of devlogs associated with this project.
        """
        return obj.devlogs.count()
    devlog_count.short_description = 'Devlog Count'
    
    def save_model(self, request, obj, form, change):
        """
        Save the model with transaction handling and error logging.
        """
        try:
            with transaction.atomic():
                super().save_model(request, obj, form, change)
                messages.success(request, f"Project '{obj.title}' saved successfully.")
        except IntegrityError as e:
            logger.error(f"Integrity error saving Project in admin: {str(e)}", exc_info=True)
            messages.error(request, f"Error saving project: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error saving Project in admin: {str(e)}", exc_info=True)
            messages.error(request, f"Unexpected error: {str(e)}")
            raise
    
    def delete_model(self, request, obj):
        """
        Delete the model with transaction handling and error logging.
        """
        try:
            with transaction.atomic():
                super().delete_model(request, obj)
                messages.success(request, f"Project '{obj.title}' deleted successfully.")
        except Exception as e:
            logger.error(f"Error deleting Project in admin: {str(e)}", exc_info=True)
            messages.error(request, f"Error deleting project: {str(e)}")
            raise
    
    def delete_queryset(self, request, queryset):
        """
        Delete multiple objects with transaction handling.
        """
        try:
            with transaction.atomic():
                count = queryset.count()
                super().delete_queryset(request, queryset)
                messages.success(request, f"Successfully deleted {count} project(s).")
        except Exception as e:
            logger.error(f"Error bulk deleting Projects in admin: {str(e)}", exc_info=True)
            messages.error(request, f"Error deleting projects: {str(e)}")
            raise

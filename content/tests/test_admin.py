"""
Unit tests for Django admin configuration.
"""
from django.test import TestCase
from django.contrib import admin
from django.contrib.auth.models import User
from content.models import Devlog, Project
from content.admin import DevlogAdmin, ProjectAdmin


class DevlogAdminTest(TestCase):
    """
    Test cases for DevlogAdmin configuration.
    """
    
    def setUp(self):
        """Set up test data."""
        self.project = Project.objects.create(
            title="Test Project",
            slug="test-project",
            description="Test description"
        )
        self.devlog = Devlog.objects.create(
            title="Test Devlog",
            slug="test-devlog",
            tagline="Test tagline",
            content="Test content",
            is_published=True,
            project=self.project
        )
    
    def test_devlog_admin_registered(self):
        """Test that Devlog model is registered in admin."""
        self.assertIn(Devlog, admin.site._registry)
        self.assertIsInstance(admin.site._registry[Devlog], DevlogAdmin)
    
    def test_devlog_list_display_fields(self):
        """Test that DevlogAdmin has correct list_display fields."""
        devlog_admin = admin.site._registry[Devlog]
        expected_fields = ['title', 'is_published', 'project', 'created_at']
        self.assertEqual(devlog_admin.list_display, expected_fields)
    
    def test_devlog_list_filter_fields(self):
        """Test that DevlogAdmin has correct list_filter fields."""
        devlog_admin = admin.site._registry[Devlog]
        expected_filters = ['is_published', 'created_at', 'project']
        self.assertEqual(devlog_admin.list_filter, expected_filters)
    
    def test_devlog_search_fields(self):
        """Test that DevlogAdmin has correct search_fields."""
        devlog_admin = admin.site._registry[Devlog]
        expected_search = ['title', 'tagline', 'content']
        self.assertEqual(devlog_admin.search_fields, expected_search)
    
    def test_devlog_prepopulated_fields(self):
        """Test that DevlogAdmin has prepopulated_fields configured."""
        devlog_admin = admin.site._registry[Devlog]
        expected_prepopulated = {'slug': ('title',)}
        self.assertEqual(devlog_admin.prepopulated_fields, expected_prepopulated)


class ProjectAdminTest(TestCase):
    """
    Test cases for ProjectAdmin configuration.
    """
    
    def setUp(self):
        """Set up test data."""
        self.project = Project.objects.create(
            title="Test Project",
            slug="test-project",
            description="Test description",
            is_featured=True
        )
        # Create some devlogs for this project
        for i in range(3):
            Devlog.objects.create(
                title=f"Devlog {i}",
                slug=f"devlog-{i}",
                tagline=f"Tagline {i}",
                content=f"Content {i}",
                project=self.project
            )
    
    def test_project_admin_registered(self):
        """Test that Project model is registered in admin."""
        self.assertIn(Project, admin.site._registry)
        self.assertIsInstance(admin.site._registry[Project], ProjectAdmin)
    
    def test_project_list_display_fields(self):
        """Test that ProjectAdmin has correct list_display fields."""
        project_admin = admin.site._registry[Project]
        expected_fields = ['title', 'is_featured', 'created_at', 'devlog_count']
        self.assertEqual(project_admin.list_display, expected_fields)
    
    def test_project_list_filter_fields(self):
        """Test that ProjectAdmin has correct list_filter fields."""
        project_admin = admin.site._registry[Project]
        expected_filters = ['is_featured', 'created_at']
        self.assertEqual(project_admin.list_filter, expected_filters)
    
    def test_project_search_fields(self):
        """Test that ProjectAdmin has correct search_fields."""
        project_admin = admin.site._registry[Project]
        expected_search = ['title', 'description']
        self.assertEqual(project_admin.search_fields, expected_search)
    
    def test_project_prepopulated_fields(self):
        """Test that ProjectAdmin has prepopulated_fields configured."""
        project_admin = admin.site._registry[Project]
        expected_prepopulated = {'slug': ('title',)}
        self.assertEqual(project_admin.prepopulated_fields, expected_prepopulated)
    
    def test_project_devlog_count_method(self):
        """Test that devlog_count custom method works correctly."""
        project_admin = admin.site._registry[Project]
        devlog_count = project_admin.devlog_count(self.project)
        self.assertEqual(devlog_count, 3)
    
    def test_project_devlog_count_with_no_devlogs(self):
        """Test devlog_count returns 0 for project with no devlogs."""
        empty_project = Project.objects.create(
            title="Empty Project",
            slug="empty-project",
            description="No devlogs"
        )
        project_admin = admin.site._registry[Project]
        devlog_count = project_admin.devlog_count(empty_project)
        self.assertEqual(devlog_count, 0)

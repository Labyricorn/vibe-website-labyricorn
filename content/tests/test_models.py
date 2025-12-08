"""
Unit tests for model edge cases.
"""
from django.test import TestCase
from content.models import Project, Devlog


class ModelEdgeCaseTests(TestCase):
    """
    Unit tests for model edge cases.
    """
    
    def test_devlog_without_project(self):
        """
        Test creating a devlog without a project (null FK).
        """
        devlog = Devlog.objects.create(
            title="Standalone Devlog",
            tagline="A devlog without a project",
            content="# Test Content\n\nThis is a test."
        )
        
        self.assertIsNone(devlog.project)
        self.assertEqual(devlog.title, "Standalone Devlog")
        
        # Verify it can be retrieved
        retrieved = Devlog.objects.get(id=devlog.id)
        self.assertIsNone(retrieved.project)
    
    def test_project_string_representation(self):
        """
        Test model string representation for Project.
        """
        project = Project.objects.create(
            title="My Awesome Project",
            description="A great project"
        )
        
        self.assertEqual(str(project), "My Awesome Project")
    
    def test_devlog_string_representation(self):
        """
        Test model string representation for Devlog.
        """
        devlog = Devlog.objects.create(
            title="My First Devlog",
            tagline="Getting started",
            content="Content here"
        )
        
        self.assertEqual(str(devlog), "My First Devlog")
    
    def test_timestamp_auto_population(self):
        """
        Test that created_at and updated_at are automatically populated.
        """
        project = Project.objects.create(
            title="Test Project",
            description="Test description"
        )
        
        # Verify timestamps are set
        self.assertIsNotNone(project.created_at)
        self.assertIsNotNone(project.updated_at)
        
        # Verify they're approximately equal (created just now)
        time_diff = (project.updated_at - project.created_at).total_seconds()
        self.assertLess(time_diff, 1)  # Less than 1 second difference
        
        # Test for Devlog as well
        devlog = Devlog.objects.create(
            title="Test Devlog",
            tagline="Test tagline",
            content="Test content"
        )
        
        self.assertIsNotNone(devlog.created_at)
        self.assertIsNotNone(devlog.updated_at)
        
        time_diff = (devlog.updated_at - devlog.created_at).total_seconds()
        self.assertLess(time_diff, 1)

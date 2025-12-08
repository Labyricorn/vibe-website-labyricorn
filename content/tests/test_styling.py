"""
Integration tests for styling and frontend polish.
Tests that Tailwind CSS is loaded and markdown content has proper styling classes.
"""

from django.test import TestCase, Client
from django.urls import reverse
from content.models import Devlog, Project


class StylingIntegrationTests(TestCase):
    """Integration tests for styling and frontend polish."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        
        # Create a test project
        self.project = Project.objects.create(
            title="Test Project",
            slug="test-project",
            description="A test project description",
            is_featured=True
        )
        
        # Create a test devlog with markdown content
        self.devlog = Devlog.objects.create(
            title="Test Devlog",
            slug="test-devlog",
            tagline="A test devlog tagline",
            content="# Heading 1\n\n## Heading 2\n\nSome **bold** text and *italic* text.\n\n```python\nprint('Hello World')\n```\n\n- List item 1\n- List item 2",
            is_published=True,
            project=self.project
        )
    
    def test_tailwind_css_loaded_on_homepage(self):
        """Test that Tailwind CSS CDN is loaded on the homepage."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # Check that Tailwind CSS CDN script is present
        self.assertContains(response, 'cdn.tailwindcss.com')
    
    def test_custom_css_loaded_on_homepage(self):
        """Test that custom CSS file is loaded on the homepage."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # Check that custom CSS file is linked
        self.assertContains(response, 'static/css/styles.css')
    
    def test_custom_js_loaded_on_homepage(self):
        """Test that custom JavaScript file is loaded on the homepage."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # Check that custom JS file is linked
        self.assertContains(response, 'static/js/main.js')
    
    def test_markdown_content_has_styling_class(self):
        """Test that markdown content has the markdown-content styling class."""
        response = self.client.get(reverse('devlog_detail', args=[self.devlog.slug]))
        self.assertEqual(response.status_code, 200)
        
        # Check that markdown-content class is present
        self.assertContains(response, 'markdown-content')
    
    def test_card_styling_on_homepage(self):
        """Test that card styling classes are applied on homepage."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # Check that card class is present
        self.assertContains(response, 'class="card"')
    
    def test_responsive_navigation_elements(self):
        """Test that responsive navigation elements are present."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # Check for mobile menu button
        self.assertContains(response, 'mobile-menu-button')
        
        # Check for mobile menu
        self.assertContains(response, 'mobile-menu')
        
        # Check for desktop navigation
        self.assertContains(response, 'desktop-nav')
    
    def test_nav_links_present(self):
        """Test that navigation links are present."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # Check for nav-link class
        self.assertContains(response, 'nav-link')
    
    def test_devlog_card_has_proper_structure(self):
        """Test that devlog cards have proper structure on homepage."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # Check for card-title class
        self.assertContains(response, 'card-title')
        
        # Check that devlog title is present
        self.assertContains(response, self.devlog.title)
        
        # Check that devlog tagline is present
        self.assertContains(response, self.devlog.tagline)
    
    def test_project_card_has_proper_structure(self):
        """Test that project cards have proper structure on homepage."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # Check that project title is present
        self.assertContains(response, self.project.title)
        
        # Check that project description is present
        self.assertContains(response, self.project.description)
    
    def test_sticky_navigation(self):
        """Test that navigation has sticky positioning."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # Check for sticky positioning class
        self.assertContains(response, 'sticky top-0')
    
    def test_markdown_content_converted_to_html(self):
        """Test that markdown content is properly converted to HTML."""
        response = self.client.get(reverse('devlog_detail', args=[self.devlog.slug]))
        self.assertEqual(response.status_code, 200)
        
        # Check that markdown headings are converted to HTML
        self.assertContains(response, '<h1>Heading 1</h1>')
        self.assertContains(response, '<h2>Heading 2</h2>')
        
        # Check that bold and italic are converted
        self.assertContains(response, '<strong>bold</strong>')
        self.assertContains(response, '<em>italic</em>')
        
        # Check that code blocks are converted with codehilite
        self.assertContains(response, 'class="codehilite"')
        self.assertContains(response, '<pre')
        
        # Check that list items are converted
        self.assertContains(response, '<li>List item 1</li>')
    
    def test_project_link_in_devlog_card(self):
        """Test that project link is present in devlog card when devlog has a project."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # Check that project link is present
        self.assertContains(response, f'Project: <a href="/project/{self.project.slug}/"')

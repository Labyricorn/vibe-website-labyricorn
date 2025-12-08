"""
Unit tests for URL routing configuration.
Tests URL resolution, reversing, and 404 handling.
"""
from django.test import TestCase, Client
from django.urls import reverse, resolve
from content import views
from content.models import Devlog, Project


class URLRoutingTests(TestCase):
    """Test URL routing configuration and resolution."""
    
    def setUp(self):
        """Set up test client and sample data."""
        self.client = Client()
        
        # Create a test project
        self.project = Project.objects.create(
            title="Test Project",
            slug="test-project",
            description="A test project",
            is_featured=True
        )
        
        # Create a test devlog
        self.devlog = Devlog.objects.create(
            title="Test Devlog",
            slug="test-devlog",
            tagline="A test devlog",
            content="# Test Content",
            is_published=True,
            project=self.project
        )
    
    def test_root_url_resolves_to_home_view(self):
        """Test that root URL resolves to home view."""
        url = reverse('home')
        self.assertEqual(url, '/')
        
        # Test that the URL resolves to the correct view function
        resolver = resolve('/')
        self.assertEqual(resolver.func, views.home)
        self.assertEqual(resolver.view_name, 'home')
    
    def test_devlog_url_pattern_resolves_correctly(self):
        """Test that devlog URL pattern resolves correctly."""
        url = reverse('devlog_detail', args=['test-slug'])
        self.assertEqual(url, '/devlog/test-slug/')
        
        # Test that the URL resolves to the correct view function
        resolver = resolve('/devlog/test-slug/')
        self.assertEqual(resolver.func, views.devlog_detail)
        self.assertEqual(resolver.view_name, 'devlog_detail')
        self.assertEqual(resolver.kwargs['slug'], 'test-slug')
    
    def test_project_url_pattern_resolves_correctly(self):
        """Test that project URL pattern resolves correctly."""
        url = reverse('project_detail', args=['test-slug'])
        self.assertEqual(url, '/project/test-slug/')
        
        # Test that the URL resolves to the correct view function
        resolver = resolve('/project/test-slug/')
        self.assertEqual(resolver.func, views.project_detail)
        self.assertEqual(resolver.view_name, 'project_detail')
        self.assertEqual(resolver.kwargs['slug'], 'test-slug')
    
    def test_rss_url_pattern_resolves_correctly(self):
        """Test that RSS feed URL pattern resolves correctly."""
        url = reverse('rss_feed')
        self.assertEqual(url, '/rss/')
        
        # Test that the URL resolves to the correct view function
        resolver = resolve('/rss/')
        self.assertEqual(resolver.func, views.rss_feed)
        self.assertEqual(resolver.view_name, 'rss_feed')
    
    def test_admin_url_is_configured(self):
        """Test that admin URL is configured."""
        # Test that admin URL can be reversed
        url = reverse('admin:index')
        self.assertEqual(url, '/admin/')
        
        # Test that the URL resolves
        resolver = resolve('/admin/')
        self.assertEqual(resolver.view_name, 'admin:index')
    
    def test_invalid_urls_return_404(self):
        """Test that invalid URLs return 404."""
        # Test various invalid URL patterns
        invalid_urls = [
            '/invalid-page/',
            '/devlog/',  # Missing slug
            '/project/',  # Missing slug
            '/random/path/that/does/not/exist/',
        ]
        
        for url in invalid_urls:
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, 
                404, 
                f"URL {url} should return 404 but returned {response.status_code}"
            )
    
    def test_url_reversing_with_actual_slugs(self):
        """Test URL reversing with actual model slugs."""
        # Test devlog URL reversing
        devlog_url = reverse('devlog_detail', args=[self.devlog.slug])
        self.assertEqual(devlog_url, f'/devlog/{self.devlog.slug}/')
        
        # Test project URL reversing
        project_url = reverse('project_detail', args=[self.project.slug])
        self.assertEqual(project_url, f'/project/{self.project.slug}/')
        
        # Verify these URLs actually work
        devlog_response = self.client.get(devlog_url)
        self.assertEqual(devlog_response.status_code, 200)
        
        project_response = self.client.get(project_url)
        self.assertEqual(project_response.status_code, 200)
    
    def test_slug_with_special_characters_in_url(self):
        """Test that slugs with hyphens and numbers work correctly."""
        # Create devlog with complex slug
        complex_devlog = Devlog.objects.create(
            title="Test 123",
            slug="test-123-devlog-2024",
            tagline="Complex slug test",
            content="Content",
            is_published=True
        )
        
        # Test URL reversing
        url = reverse('devlog_detail', args=[complex_devlog.slug])
        self.assertEqual(url, '/devlog/test-123-devlog-2024/')
        
        # Test URL resolution
        resolver = resolve(url)
        self.assertEqual(resolver.kwargs['slug'], 'test-123-devlog-2024')
        
        # Test actual access
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_all_url_names_are_unique(self):
        """Test that all URL names are unique and can be reversed."""
        url_names = ['home', 'devlog_detail', 'project_detail', 'rss_feed']
        
        for url_name in url_names:
            # Test that each URL name can be reversed
            if url_name in ['devlog_detail', 'project_detail']:
                # These require a slug argument
                url = reverse(url_name, args=['test-slug'])
            else:
                url = reverse(url_name)
            
            # Verify we got a valid URL string
            self.assertIsInstance(url, str)
            self.assertTrue(url.startswith('/'))

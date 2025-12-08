"""
Unit tests for views in the Vibe Hub MVP.
"""
from django.test import TestCase, Client
from django.urls import reverse
from content.models import Devlog, Project


class HomepageViewTests(TestCase):
    """
    Unit tests for the homepage view.
    """
    
    def setUp(self):
        """Set up test client and test data."""
        self.client = Client()
        
        # Create test projects
        self.featured_project = Project.objects.create(
            title="Featured Project",
            description="A featured project",
            is_featured=True
        )
        self.non_featured_project = Project.objects.create(
            title="Non-Featured Project",
            description="A non-featured project",
            is_featured=False
        )
        
        # Create test devlogs
        self.published_devlog = Devlog.objects.create(
            title="Published Devlog",
            tagline="A published devlog",
            content="# Content",
            is_published=True,
            project=self.featured_project
        )
        self.unpublished_devlog = Devlog.objects.create(
            title="Unpublished Devlog",
            tagline="An unpublished devlog",
            content="# Content",
            is_published=False
        )
    
    def test_homepage_returns_200_status(self):
        """Test that homepage returns 200 status code."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_homepage_context_contains_latest_devlogs(self):
        """Test that homepage context contains latest_devlogs."""
        response = self.client.get(reverse('home'))
        self.assertIn('latest_devlogs', response.context)
    
    def test_homepage_context_contains_featured_projects(self):
        """Test that homepage context contains featured_projects."""
        response = self.client.get(reverse('home'))
        self.assertIn('featured_projects', response.context)
    
    def test_unpublished_devlogs_are_excluded(self):
        """Test that unpublished devlogs are excluded from homepage."""
        response = self.client.get(reverse('home'))
        latest_devlogs = response.context['latest_devlogs']
        
        # Published devlog should be in the list
        self.assertIn(self.published_devlog, latest_devlogs)
        
        # Unpublished devlog should not be in the list
        self.assertNotIn(self.unpublished_devlog, latest_devlogs)
    
    def test_featured_projects_are_displayed(self):
        """Test that featured projects are displayed on homepage."""
        response = self.client.get(reverse('home'))
        featured_projects = response.context['featured_projects']
        
        # Featured project should be in the list
        self.assertIn(self.featured_project, featured_projects)
        
        # Non-featured project should not be in the list
        self.assertNotIn(self.non_featured_project, featured_projects)
    
    def test_homepage_limits_devlogs_to_five(self):
        """Test that homepage displays at most 5 devlogs."""
        # Create 10 published devlogs
        for i in range(10):
            Devlog.objects.create(
                title=f"Devlog {i}",
                tagline=f"Tagline {i}",
                content=f"Content {i}",
                is_published=True
            )
        
        response = self.client.get(reverse('home'))
        latest_devlogs = response.context['latest_devlogs']
        
        # Should have at most 5 devlogs
        self.assertLessEqual(len(latest_devlogs), 5)


class DevlogDetailViewTests(TestCase):
    """
    Unit tests for the devlog detail view.
    """
    
    def setUp(self):
        """Set up test client and test data."""
        self.client = Client()
        
        # Create a test project
        self.project = Project.objects.create(
            title="Test Project",
            description="A test project",
            is_featured=True
        )
        
        # Create a published devlog
        self.published_devlog = Devlog.objects.create(
            title="Published Devlog",
            tagline="A published devlog",
            content="# Heading\n\nThis is **markdown** content with a [link](http://example.com).",
            is_published=True,
            project=self.project
        )
        
        # Create an unpublished devlog
        self.unpublished_devlog = Devlog.objects.create(
            title="Unpublished Devlog",
            tagline="An unpublished devlog",
            content="# Content",
            is_published=False
        )
    
    def test_published_devlog_returns_200(self):
        """Test that accessing a published devlog returns 200 status code."""
        response = self.client.get(
            reverse('devlog_detail', args=[self.published_devlog.slug])
        )
        self.assertEqual(response.status_code, 200)
    
    def test_unpublished_devlog_returns_404(self):
        """Test that accessing an unpublished devlog returns 404."""
        response = self.client.get(
            reverse('devlog_detail', args=[self.unpublished_devlog.slug])
        )
        self.assertEqual(response.status_code, 404)
    
    def test_non_existent_slug_returns_404(self):
        """Test that accessing a non-existent slug returns 404."""
        response = self.client.get(
            reverse('devlog_detail', args=['non-existent-slug'])
        )
        self.assertEqual(response.status_code, 404)
    
    def test_markdown_is_converted_to_html_in_response(self):
        """Test that markdown content is converted to HTML in the response."""
        response = self.client.get(
            reverse('devlog_detail', args=[self.published_devlog.slug])
        )
        
        # Check that HTML content is in the context
        self.assertIn('html_content', response.context)
        html_content = response.context['html_content']
        
        # Verify markdown was converted to HTML
        self.assertIn('<h1>', html_content)  # Heading converted
        self.assertIn('<strong>', html_content)  # Bold converted
        self.assertIn('<a href=', html_content)  # Link converted
        
        # Verify the HTML is in the response content
        self.assertContains(response, '<h1>')
        self.assertContains(response, 'markdown')
    
    def test_devlog_context_contains_correct_devlog(self):
        """Test that the devlog context contains the correct devlog."""
        response = self.client.get(
            reverse('devlog_detail', args=[self.published_devlog.slug])
        )
        
        self.assertEqual(response.context['devlog'].id, self.published_devlog.id)
        self.assertEqual(response.context['devlog'].title, self.published_devlog.title)
        self.assertEqual(response.context['devlog'].slug, self.published_devlog.slug)
    
    def test_devlog_with_project_shows_project_info(self):
        """Test that a devlog linked to a project shows project information."""
        response = self.client.get(
            reverse('devlog_detail', args=[self.published_devlog.slug])
        )
        
        # Check that the project is accessible in the context
        self.assertEqual(response.context['devlog'].project, self.project)
        
        # Check that the project title appears in the response
        self.assertContains(response, self.project.title)


class ProjectDetailViewTests(TestCase):
    """
    Unit tests for the project detail view.
    """
    
    def setUp(self):
        """Set up test client and test data."""
        self.client = Client()
        
        # Create a test project
        self.project = Project.objects.create(
            title="Test Project",
            description="A test project description",
            is_featured=True
        )
        
        # Create published devlogs linked to the project
        self.published_devlog_1 = Devlog.objects.create(
            title="Published Devlog 1",
            tagline="First published devlog",
            content="# Content 1",
            is_published=True,
            project=self.project
        )
        self.published_devlog_2 = Devlog.objects.create(
            title="Published Devlog 2",
            tagline="Second published devlog",
            content="# Content 2",
            is_published=True,
            project=self.project
        )
        
        # Create an unpublished devlog linked to the project
        self.unpublished_devlog = Devlog.objects.create(
            title="Unpublished Devlog",
            tagline="An unpublished devlog",
            content="# Content",
            is_published=False,
            project=self.project
        )
    
    def test_project_detail_returns_200(self):
        """Test that accessing a project detail page returns 200 status code."""
        response = self.client.get(
            reverse('project_detail', args=[self.project.slug])
        )
        self.assertEqual(response.status_code, 200)
    
    def test_related_devlogs_are_displayed(self):
        """Test that related devlogs are displayed on the project detail page."""
        response = self.client.get(
            reverse('project_detail', args=[self.project.slug])
        )
        
        # Check that related_devlogs is in the context
        self.assertIn('related_devlogs', response.context)
        related_devlogs = response.context['related_devlogs']
        
        # Published devlogs should be in the list
        self.assertIn(self.published_devlog_1, related_devlogs)
        self.assertIn(self.published_devlog_2, related_devlogs)
        
        # Check that devlog titles appear in the response
        self.assertContains(response, self.published_devlog_1.title)
        self.assertContains(response, self.published_devlog_2.title)
    
    def test_only_published_devlogs_are_shown(self):
        """Test that only published devlogs are shown on the project detail page."""
        response = self.client.get(
            reverse('project_detail', args=[self.project.slug])
        )
        
        related_devlogs = response.context['related_devlogs']
        
        # Published devlogs should be in the list
        self.assertIn(self.published_devlog_1, related_devlogs)
        self.assertIn(self.published_devlog_2, related_devlogs)
        
        # Unpublished devlog should not be in the list
        self.assertNotIn(self.unpublished_devlog, related_devlogs)
        
        # Unpublished devlog title should not appear in the response
        self.assertNotContains(response, self.unpublished_devlog.title)
    
    def test_non_existent_slug_returns_404(self):
        """Test that accessing a non-existent project slug returns 404."""
        response = self.client.get(
            reverse('project_detail', args=['non-existent-slug'])
        )
        self.assertEqual(response.status_code, 404)
    
    def test_project_context_contains_correct_project(self):
        """Test that the project context contains the correct project."""
        response = self.client.get(
            reverse('project_detail', args=[self.project.slug])
        )
        
        self.assertEqual(response.context['project'].id, self.project.id)
        self.assertEqual(response.context['project'].title, self.project.title)
        self.assertEqual(response.context['project'].slug, self.project.slug)
    
    def test_project_description_is_displayed(self):
        """Test that the project description is displayed."""
        response = self.client.get(
            reverse('project_detail', args=[self.project.slug])
        )
        
        self.assertContains(response, self.project.description)



class RSSFeedViewTests(TestCase):
    """
    Unit tests for the RSS feed view.
    """
    
    def setUp(self):
        """Set up test client and test data."""
        self.client = Client()
        
        # Create a test project
        self.project = Project.objects.create(
            title="Test Project",
            description="A test project",
            is_featured=True
        )
        
        # Create published devlogs
        self.published_devlog_1 = Devlog.objects.create(
            title="Published Devlog 1",
            tagline="First published devlog",
            content="# Content 1",
            is_published=True,
            project=self.project
        )
        self.published_devlog_2 = Devlog.objects.create(
            title="Published Devlog 2",
            tagline="Second published devlog",
            content="# Content 2",
            is_published=True
        )
        
        # Create an unpublished devlog
        self.unpublished_devlog = Devlog.objects.create(
            title="Unpublished Devlog",
            tagline="An unpublished devlog",
            content="# Content",
            is_published=False
        )
    
    def test_rss_feed_returns_valid_xml(self):
        """Test that RSS feed returns valid XML with correct content type."""
        response = self.client.get(reverse('rss_feed'))
        
        # Check status code
        self.assertEqual(response.status_code, 200)
        
        # Check content type
        self.assertEqual(response['Content-Type'], 'application/rss+xml')
        
        # Check that response contains XML declaration
        content = response.content.decode('utf-8')
        self.assertIn('<?xml', content)
        
        # Check that response contains RSS elements
        self.assertIn('<rss', content)
        self.assertIn('<channel>', content)
        self.assertIn('</channel>', content)
        self.assertIn('</rss>', content)
    
    def test_feed_contains_published_devlogs(self):
        """Test that feed contains published devlogs."""
        response = self.client.get(reverse('rss_feed'))
        content = response.content.decode('utf-8')
        
        # Check that published devlog titles are in the feed
        self.assertIn(self.published_devlog_1.title, content)
        self.assertIn(self.published_devlog_2.title, content)
        
        # Check that published devlog taglines are in the feed
        self.assertIn(self.published_devlog_1.tagline, content)
        self.assertIn(self.published_devlog_2.tagline, content)
    
    def test_feed_excludes_unpublished_devlogs(self):
        """Test that feed excludes unpublished devlogs."""
        response = self.client.get(reverse('rss_feed'))
        content = response.content.decode('utf-8')
        
        # Check that unpublished devlog title is not in the feed
        self.assertNotIn(self.unpublished_devlog.title, content)
        
        # Check that unpublished devlog tagline is not in the feed
        self.assertNotIn(self.unpublished_devlog.tagline, content)
    
    def test_feed_metadata_is_correct(self):
        """Test that feed metadata is correctly configured."""
        response = self.client.get(reverse('rss_feed'))
        content = response.content.decode('utf-8')
        
        # Check feed title
        self.assertIn('Vibe Hub Devlogs', content)
        
        # Check feed description
        self.assertIn('Latest development logs and technical insights', content)
    
    def test_feed_limits_to_20_devlogs(self):
        """Test that feed limits to 20 devlogs."""
        # Create 25 published devlogs
        for i in range(25):
            Devlog.objects.create(
                title=f"Devlog {i}",
                tagline=f"Tagline {i}",
                content=f"Content {i}",
                is_published=True
            )
        
        response = self.client.get(reverse('rss_feed'))
        content = response.content.decode('utf-8')
        
        # Count the number of <item> tags (each devlog is an item)
        item_count = content.count('<item>')
        
        # Should have at most 20 items
        self.assertLessEqual(item_count, 20)

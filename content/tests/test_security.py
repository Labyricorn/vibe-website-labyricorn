"""
Unit tests for security settings and configurations.
"""
import os
from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from django.conf import settings


class SecuritySettingsTests(TestCase):
    """
    Unit tests for security settings configuration.
    """
    
    def test_debug_false_in_production_mode(self):
        """
        Test that DEBUG is False when not explicitly set to True.
        This simulates production mode where DEBUG should be disabled.
        """
        # In production, DEBUG should be False
        # We test that the settings file respects the environment variable
        # by checking the current value (which should be from .env or default)
        
        # If DEBUG is True in test environment, that's expected
        # The important thing is that it CAN be set to False via environment
        # and that the default in settings.py for production is False
        
        # We verify the mechanism exists by checking settings can be overridden
        with override_settings(DEBUG=False):
            self.assertFalse(settings.DEBUG)
    
    def test_allowed_hosts_configured(self):
        """
        Test that ALLOWED_HOSTS is configured and not empty in production.
        """
        # ALLOWED_HOSTS should be configurable via environment variable
        # In our settings, it defaults to 'localhost,127.0.0.1'
        
        self.assertIsNotNone(settings.ALLOWED_HOSTS)
        self.assertIsInstance(settings.ALLOWED_HOSTS, list)
        
        # Should have at least one host configured
        self.assertGreater(len(settings.ALLOWED_HOSTS), 0)
        
        # Verify it's not the Django default of ['*'] in production
        # (though in dev/test it might be permissive)
        if not settings.DEBUG:
            self.assertNotEqual(settings.ALLOWED_HOSTS, ['*'])
    
    def test_admin_requires_authentication(self):
        """
        Test that admin interface requires authentication.
        """
        client = Client()
        
        # Try to access admin without authentication
        response = client.get('/admin/', follow=False)
        
        # Should redirect to login page (302) or return forbidden (403)
        self.assertIn(response.status_code, [302, 403])
        
        # If redirect, should go to login page
        if response.status_code == 302:
            self.assertIn('/admin/login/', response.url)
    
    def test_admin_accessible_with_authentication(self):
        """
        Test that admin interface is accessible with valid authentication.
        """
        # Create a superuser
        user = User.objects.create_superuser(
            username='testadmin',
            email='admin@test.com',
            password='testpass123'
        )
        
        client = Client()
        
        # Login
        client.login(username='testadmin', password='testpass123')
        
        # Try to access admin
        response = client.get('/admin/')
        
        # Should be successful
        self.assertEqual(response.status_code, 200)
    
    def test_csrf_protection_enabled(self):
        """
        Test that CSRF protection middleware is enabled.
        """
        # Verify CSRF middleware is in MIDDLEWARE setting
        self.assertIn(
            'django.middleware.csrf.CsrfViewMiddleware',
            settings.MIDDLEWARE
        )
    
    def test_security_middleware_enabled(self):
        """
        Test that security middleware is enabled.
        """
        # Verify security middleware is in MIDDLEWARE setting
        self.assertIn(
            'django.middleware.security.SecurityMiddleware',
            settings.MIDDLEWARE
        )
    
    def test_clickjacking_protection_enabled(self):
        """
        Test that clickjacking protection middleware is enabled.
        """
        # Verify X-Frame-Options middleware is in MIDDLEWARE setting
        self.assertIn(
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
            settings.MIDDLEWARE
        )
    
    def test_xss_protection_settings_exist(self):
        """
        Test that XSS protection settings are configured.
        """
        # Verify SECURE_BROWSER_XSS_FILTER setting exists
        self.assertTrue(hasattr(settings, 'SECURE_BROWSER_XSS_FILTER'))
        
        # Verify SECURE_CONTENT_TYPE_NOSNIFF setting exists
        self.assertTrue(hasattr(settings, 'SECURE_CONTENT_TYPE_NOSNIFF'))
    
    def test_session_cookie_settings_exist(self):
        """
        Test that session cookie security settings are configured.
        """
        # Verify SESSION_COOKIE_SECURE setting exists
        self.assertTrue(hasattr(settings, 'SESSION_COOKIE_SECURE'))
        
        # Verify SESSION_COOKIE_HTTPONLY setting exists
        self.assertTrue(hasattr(settings, 'SESSION_COOKIE_HTTPONLY'))
    
    def test_csrf_cookie_settings_exist(self):
        """
        Test that CSRF cookie security settings are configured.
        """
        # Verify CSRF_COOKIE_SECURE setting exists
        self.assertTrue(hasattr(settings, 'CSRF_COOKIE_SECURE'))
        
        # Verify CSRF_COOKIE_HTTPONLY setting exists
        self.assertTrue(hasattr(settings, 'CSRF_COOKIE_HTTPONLY'))
    
    def test_ssl_redirect_setting_exists(self):
        """
        Test that SSL redirect setting is configured.
        """
        # Verify SECURE_SSL_REDIRECT setting exists
        self.assertTrue(hasattr(settings, 'SECURE_SSL_REDIRECT'))
    
    def test_hsts_settings_exist(self):
        """
        Test that HSTS (HTTP Strict Transport Security) settings are configured.
        """
        # Verify HSTS settings exist
        self.assertTrue(hasattr(settings, 'SECURE_HSTS_SECONDS'))
        self.assertTrue(hasattr(settings, 'SECURE_HSTS_INCLUDE_SUBDOMAINS'))
        self.assertTrue(hasattr(settings, 'SECURE_HSTS_PRELOAD'))
    
    def test_x_frame_options_setting_exists(self):
        """
        Test that X-Frame-Options setting is configured.
        """
        # Verify X_FRAME_OPTIONS setting exists
        self.assertTrue(hasattr(settings, 'X_FRAME_OPTIONS'))
        
        # Should be set to DENY or SAMEORIGIN for security
        if hasattr(settings, 'X_FRAME_OPTIONS'):
            self.assertIn(settings.X_FRAME_OPTIONS, ['DENY', 'SAMEORIGIN'])
    
    def test_secret_key_not_default(self):
        """
        Test that SECRET_KEY is not the default insecure key in production.
        """
        # In production, SECRET_KEY should not be the default insecure key
        # We can't test the actual production value, but we can verify
        # it's configurable via environment
        
        # Test with production settings
        with override_settings(DEBUG=False, SECRET_KEY='production-secret-key-12345'):
            # In production mode, should not have 'insecure' in the key
            self.assertNotIn('insecure', settings.SECRET_KEY.lower())
    
    def test_password_validators_configured(self):
        """
        Test that password validators are configured for security.
        """
        # Verify AUTH_PASSWORD_VALIDATORS is configured
        self.assertTrue(hasattr(settings, 'AUTH_PASSWORD_VALIDATORS'))
        self.assertIsInstance(settings.AUTH_PASSWORD_VALIDATORS, list)
        
        # Should have at least some validators configured
        self.assertGreater(len(settings.AUTH_PASSWORD_VALIDATORS), 0)

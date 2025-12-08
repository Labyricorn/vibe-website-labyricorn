"""
Custom template tags for markdown processing.
"""
from django import template
import markdown as md
import bleach

register = template.Library()


@register.filter(name='markdown_to_html')
def markdown_to_html(text):
    """
    Convert markdown text to HTML with sanitization.
    
    Configures markdown extensions:
    - extra: Adds support for tables, footnotes, etc.
    - codehilite: Syntax highlighting for code blocks
    - fenced_code: Support for fenced code blocks (```)
    
    Sanitizes output to prevent XSS attacks using bleach.
    
    Args:
        text: Markdown formatted text string
        
    Returns:
        HTML string with sanitized output
    """
    if not text:
        return ''
    
    try:
        # Convert markdown to HTML with extensions
        html = md.markdown(
            text,
            extensions=['extra', 'codehilite', 'fenced_code']
        )
        
        # Sanitize HTML to prevent XSS
        # Allow common HTML tags that markdown generates
        allowed_tags = [
            'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'blockquote', 'code', 'pre', 'hr', 'div', 'span',
            'ul', 'ol', 'li', 'dd', 'dt', 'dl',
            'a', 'img',
            'table', 'thead', 'tbody', 'tr', 'th', 'td',
        ]
        
        allowed_attributes = {
            'a': ['href', 'title', 'rel'],
            'img': ['src', 'alt', 'title'],
            'code': ['class'],
            'pre': ['class'],
            'div': ['class'],
            'span': ['class'],
        }
        
        sanitized_html = bleach.clean(
            html,
            tags=allowed_tags,
            attributes=allowed_attributes,
            strip=True
        )
        
        return sanitized_html
        
    except Exception as e:
        # If markdown processing fails, return the original text as plain text
        # This handles malformed markdown gracefully
        return bleach.clean(text, tags=[], strip=True)

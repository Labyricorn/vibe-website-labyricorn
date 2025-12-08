"""
Hypothesis generators for property-based testing.
"""
from hypothesis import strategies as st
from hypothesis.extra.django import from_model
from content.models import Project, Devlog


# Basic text strategies
valid_titles = st.text(
    alphabet=st.characters(blacklist_categories=('Cs', 'Cc')),
    min_size=1,
    max_size=200
).filter(lambda x: x.strip())  # Ensure non-empty after stripping

valid_taglines = st.text(
    alphabet=st.characters(blacklist_categories=('Cs', 'Cc')),
    min_size=1,
    max_size=300
).filter(lambda x: x.strip())

valid_descriptions = st.text(
    alphabet=st.characters(blacklist_categories=('Cs', 'Cc')),
    min_size=0,
    max_size=1000
)

valid_markdown_content = st.text(
    alphabet=st.characters(blacklist_categories=('Cs', 'Cc')),
    min_size=0,
    max_size=5000
)


# Markdown-specific strategies for testing conversion
markdown_headings = st.builds(
    lambda level, text: f"{'#' * level} {text}\n",
    level=st.integers(min_value=1, max_value=6),
    text=st.text(min_size=1, max_size=50).filter(lambda x: '\n' not in x and x.strip())
)

markdown_lists = st.builds(
    lambda items: '\n'.join(f"- {item}" for item in items),
    items=st.lists(
        st.text(min_size=1, max_size=50).filter(lambda x: '\n' not in x and x.strip()),
        min_size=1,
        max_size=5
    )
)

markdown_code_blocks = st.builds(
    lambda lang, code: f"```{lang}\n{code}\n```",
    lang=st.sampled_from(['python', 'javascript', 'bash', '']),
    code=st.text(min_size=1, max_size=100)
)

markdown_links = st.builds(
    lambda text, url: f"[{text}]({url})",
    text=st.text(min_size=1, max_size=30).filter(lambda x: '[' not in x and ']' not in x),
    url=st.text(min_size=5, max_size=50).filter(lambda x: ' ' not in x and '(' not in x and ')' not in x)
)

markdown_images = st.builds(
    lambda alt, url: f"![{alt}]({url})",
    alt=st.text(min_size=1, max_size=30).filter(lambda x: '[' not in x and ']' not in x),
    url=st.text(min_size=5, max_size=50).filter(lambda x: ' ' not in x and '(' not in x and ')' not in x)
)

# Combined markdown content with various elements
structured_markdown = st.one_of(
    markdown_headings,
    markdown_lists,
    markdown_code_blocks,
    markdown_links,
    markdown_images,
    st.text(min_size=1, max_size=200)  # Plain text
)

# Malformed markdown for error handling tests
malformed_markdown = st.one_of(
    st.just("# Unclosed [link"),
    st.just("![Missing closing"),
    st.just("```\nUnclosed code block"),
    st.text(min_size=0, max_size=100)  # Any text should be handled
)

# XSS attack patterns
xss_patterns = st.sampled_from([
    '<script>alert("XSS")</script>',
    '<img src=x onerror="alert(1)">',
    '<a href="javascript:alert(1)">Click</a>',
    '"><script>alert(String.fromCharCode(88,83,83))</script>',
    '<iframe src="javascript:alert(1)">',
    '<body onload=alert(1)>',
    '<svg/onload=alert(1)>',
    '<input onfocus=alert(1) autofocus>',
])


# Model generators using from_model
project_strategy = from_model(
    Project,
    title=valid_titles,
    slug=st.just(''),  # Let the model generate it
)

devlog_strategy = from_model(
    Devlog,
    title=valid_titles,
    slug=st.just(''),  # Let the model generate it
    tagline=valid_taglines,
    content=valid_markdown_content,
)

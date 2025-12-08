from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
import markdown
from feedgen.feed import FeedGenerator
from .models import Devlog, Project


def home(request):
    """
    Assembles homepage context with latest devlogs and featured projects.
    """
    latest_devlogs = Devlog.objects.filter(is_published=True)[:5]
    featured_projects = Project.objects.filter(is_featured=True)
    
    context = {
        'latest_devlogs': latest_devlogs,
        'featured_projects': featured_projects,
    }
    return render(request, 'home.html', context)


def devlog_detail(request, slug):
    """
    Displays a single devlog with markdown content converted to HTML.
    """
    devlog = get_object_or_404(Devlog, slug=slug, is_published=True)
    
    # Convert markdown to HTML
    html_content = markdown.markdown(
        devlog.content,
        extensions=['extra', 'codehilite', 'fenced_code']
    )
    
    context = {
        'devlog': devlog,
        'html_content': html_content,
    }
    return render(request, 'devlog_detail.html', context)


def project_detail(request, slug):
    """
    Displays a single project with related published devlogs.
    """
    project = get_object_or_404(Project, slug=slug)
    related_devlogs = project.devlogs.filter(is_published=True)
    
    context = {
        'project': project,
        'related_devlogs': related_devlogs,
    }
    return render(request, 'project_detail.html', context)


def rss_feed(request):
    """
    Generates RSS feed for published devlogs.
    """
    fg = FeedGenerator()
    fg.title('Labyricorn Vibe Hub Devlogs')
    fg.link(href=request.build_absolute_uri('/'), rel='alternate')
    fg.description('Latest development logs and technical insights')
    
    devlogs = Devlog.objects.filter(is_published=True)[:20]
    for devlog in devlogs:
        fe = fg.add_entry()
        fe.title(devlog.title)
        fe.link(href=request.build_absolute_uri(
            reverse('devlog_detail', args=[devlog.slug])
        ))
        fe.description(devlog.tagline)
        fe.pubDate(devlog.created_at)
    
    return HttpResponse(fg.rss_str(), content_type='application/rss+xml')

"""
Django management command to generate sample devlogs and projects.

Usage:
    python manage.py generate_sample_data
    python manage.py generate_sample_data --projects 5 --devlogs 10
    python manage.py generate_sample_data --clear
"""

from django.core.management.base import BaseCommand, CommandError
from content.models import Devlog, Project
import random


class Command(BaseCommand):
    help = 'Generate sample devlogs and projects for testing and demonstration'
    
    PROJECT_TITLES = [
        "Django REST API Framework",
        "React Dashboard Application",
        "Python Data Pipeline",
        "Kubernetes Deployment Automation",
        "Machine Learning Model Trainer",
        "GraphQL API Gateway",
        "Microservices Architecture",
        "CI/CD Pipeline Implementation",
        "Docker Container Orchestration",
        "Serverless Function Framework"
    ]
    
    PROJECT_DESCRIPTIONS = [
        "A comprehensive REST API built with Django REST Framework, featuring authentication, pagination, and filtering capabilities.",
        "Modern dashboard application built with React and TypeScript, providing real-time data visualization and analytics.",
        "Scalable data pipeline processing millions of records daily using Python, Pandas, and Apache Airflow.",
        "Automated Kubernetes deployment system with Helm charts, monitoring, and auto-scaling configurations.",
        "End-to-end machine learning pipeline for training, evaluating, and deploying models to production.",
        "High-performance GraphQL API gateway handling complex queries with efficient data loading strategies.",
        "Distributed microservices architecture with service discovery, load balancing, and fault tolerance.",
        "Complete CI/CD pipeline using GitHub Actions, automated testing, and multi-environment deployments.",
        "Container orchestration platform managing Docker containers across multiple hosts with health monitoring.",
        "Serverless computing framework for deploying and managing AWS Lambda functions with API Gateway integration."
    ]

    DEVLOG_TITLES = [
        "Building a Scalable REST API", "Implementing JWT Authentication",
        "Optimizing Database Queries", "Setting Up Docker Compose",
        "Deploying to Production", "Writing Effective Unit Tests",
        "Debugging Memory Leaks", "Implementing Caching Strategies",
        "Refactoring Legacy Code", "Monitoring Application Performance",
        "Handling Async Operations", "Securing API Endpoints",
        "Migrating to PostgreSQL", "Implementing Rate Limiting",
        "Building a CLI Tool", "Automating Deployment Scripts",
        "Integrating Third-Party APIs", "Optimizing Frontend Performance",
        "Setting Up Logging Infrastructure", "Implementing Feature Flags"
    ]
    
    DEVLOG_TAGLINES = [
        "Lessons learned from building production-ready APIs",
        "A deep dive into modern authentication patterns",
        "Performance optimization techniques that actually work",
        "Containerization best practices for development",
        "Zero-downtime deployment strategies",
        "Testing approaches that catch bugs early",
        "Tools and techniques for finding memory issues",
        "When and how to implement caching effectively",
        "Strategies for improving code quality incrementally",
        "Observability patterns for modern applications",
        "Managing concurrency in Python applications",
        "Security best practices for web APIs",
        "Database migration without downtime",
        "Protecting your API from abuse",
        "Creating developer-friendly command-line interfaces",
        "Streamlining the deployment process",
        "Working with external services reliably",
        "Making web applications faster",
        "Centralized logging for distributed systems",
        "Gradual rollout techniques for new features"
    ]
    
    DEVLOG_CONTENT = """# Introduction

This devlog covers my experience building {topic}. The journey was full of interesting challenges and learning opportunities.

## The Challenge

When I started this project, I faced several key challenges:
- Understanding the requirements and constraints
- Choosing the right tools and technologies
- Balancing performance with maintainability

## The Solution

After researching various approaches, I settled on a practical architecture.

## Key Takeaways

1. Planning is crucial - Taking time upfront saves debugging time later
2. Test early and often - Automated tests catch issues before production
3. Document as you go - Future you will thank present you

## Conclusion

This project taught me valuable lessons about {topic} that I'll carry forward to future work."""
    
    def add_arguments(self, parser):
        parser.add_argument('--projects', type=int, default=3, help='Number of projects to create')
        parser.add_argument('--devlogs', type=int, default=8, help='Number of devlogs to create')
        parser.add_argument('--clear', action='store_true', help='Clear existing data first')

    
    def handle(self, *args, **options):
        num_projects = options['projects']
        num_devlogs = options['devlogs']
        clear_existing = options['clear']
        
        if num_projects < 0 or num_devlogs < 0:
            raise CommandError('Number of projects and devlogs must be non-negative')
        
        if num_projects > len(self.PROJECT_TITLES):
            self.stdout.write(self.style.WARNING(f'Only {len(self.PROJECT_TITLES)} project templates available'))
            num_projects = len(self.PROJECT_TITLES)
        
        if num_devlogs > len(self.DEVLOG_TITLES):
            self.stdout.write(self.style.WARNING(f'Only {len(self.DEVLOG_TITLES)} devlog templates available'))
            num_devlogs = len(self.DEVLOG_TITLES)
        
        if clear_existing:
            devlog_count = Devlog.objects.count()
            project_count = Project.objects.count()
            Devlog.objects.all().delete()
            Project.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Cleared {devlog_count} devlogs and {project_count} projects'))
        
        projects = []
        if num_projects > 0:
            self.stdout.write('Creating projects...')
            for i in range(num_projects):
                project = Project.objects.create(
                    title=self.PROJECT_TITLES[i],
                    description=self.PROJECT_DESCRIPTIONS[i],
                    is_featured=(i < num_projects // 2)
                )
                projects.append(project)
                self.stdout.write(f'  Created project: {project.title}')
            self.stdout.write(self.style.SUCCESS(f'Created {num_projects} projects'))
        
        if num_devlogs > 0:
            self.stdout.write('Creating devlogs...')
            for i in range(num_devlogs):
                project = None
                if projects and random.random() > 0.3:
                    project = random.choice(projects)
                
                content = self.DEVLOG_CONTENT.format(topic=self.DEVLOG_TITLES[i].lower())
                
                devlog = Devlog.objects.create(
                    title=self.DEVLOG_TITLES[i],
                    tagline=self.DEVLOG_TAGLINES[i],
                    content=content,
                    is_published=(i < num_devlogs - 2),
                    project=project
                )
                
                project_info = f' (linked to {project.title})' if project else ''
                self.stdout.write(f'  Created devlog: {devlog.title}{project_info}')
            self.stdout.write(self.style.SUCCESS(f'Created {num_devlogs} devlogs'))
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('Sample data generation complete!'))
        self.stdout.write('=' * 60)
        self.stdout.write(f'Total projects: {Project.objects.count()}')
        self.stdout.write(f'Total devlogs: {Devlog.objects.count()}')
        self.stdout.write(f'Published devlogs: {Devlog.objects.filter(is_published=True).count()}')
        self.stdout.write(f'Featured projects: {Project.objects.filter(is_featured=True).count()}')
        self.stdout.write('\nVisit http://localhost:8000 to view the site')

# Generated by Django 5.2.1 on 2025-06-11 19:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0003_alter_systemmetric_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="systemmodule",
            name="actual_dev_hours",
            field=models.IntegerField(
                blank=True, help_text="Actual development hours spent", null=True
            ),
        ),
        migrations.AddField(
            model_name="systemmodule",
            name="code_lines",
            field=models.PositiveIntegerField(
                default=0, help_text="Total lines of code"
            ),
        ),
        migrations.AddField(
            model_name="systemmodule",
            name="commit_count",
            field=models.PositiveIntegerField(default=0, help_text="Total Git commits"),
        ),
        migrations.AddField(
            model_name="systemmodule",
            name="daily_users",
            field=models.IntegerField(
                default=0, help_text="Average daily active users"
            ),
        ),
        migrations.AddField(
            model_name="systemmodule",
            name="estimated_completion_date",
            field=models.DateField(
                blank=True, help_text="Estimated project completion", null=True
            ),
        ),
        migrations.AddField(
            model_name="systemmodule",
            name="estimated_dev_hours",
            field=models.IntegerField(
                blank=True, help_text="Estimated development hours", null=True
            ),
        ),
        migrations.AddField(
            model_name="systemmodule",
            name="last_commit_date",
            field=models.DateTimeField(
                blank=True, help_text="Date of last Git commit", null=True
            ),
        ),
        migrations.AddField(
            model_name="systemmodule",
            name="response_time_ms",
            field=models.IntegerField(
                default=0, help_text="Average response time in milliseconds"
            ),
        ),
        migrations.AddField(
            model_name="systemmodule",
            name="team_size",
            field=models.IntegerField(default=1, help_text="Number of team members"),
        ),
        migrations.CreateModel(
            name="SystemDependency",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "dependency_type",
                    models.CharField(
                        choices=[
                            ("api", "API Dependency"),
                            ("database", "Database Dependency"),
                            ("service", "Service Dependency"),
                            ("library", "Library Dependency"),
                            ("integration", "Integration Dependency"),
                            ("data_flow", "Data Flow"),
                            ("authentication", "Authentication Dependency"),
                            ("infrastructure", "Infrastructure Dependency"),
                        ],
                        default="integration",
                        max_length=20,
                    ),
                ),
                (
                    "is_critical",
                    models.BooleanField(
                        default=False,
                        help_text="System cannot function without this dependency",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="Description of dependency relationship"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "depends_on",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dependents",
                        to="projects.systemmodule",
                    ),
                ),
                (
                    "system",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dependencies",
                        to="projects.systemmodule",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "System Dependencies",
                "unique_together": {("system", "depends_on")},
            },
        ),
    ]

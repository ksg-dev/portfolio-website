# Generated by Django 5.2.1 on 2025-06-16 19:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0009_systemlogentry_actual_hours_and_more"),
        ("core", "0005_contact_inquiry_category_contact_ip_address_and_more"),
        ("projects", "0005_remove_systemmodule_related_systems_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="systemmodule",
            name="learning_stage",
            field=models.CharField(
                choices=[
                    ("tutorial", "Following Tutorial"),
                    ("guided", "Guided Project"),
                    ("independent", "Independent Development"),
                    ("refactoring", "Refactoring/Improving"),
                    ("contributing", "Open Source Contributing"),
                    ("teaching", "Teaching/Sharing"),
                ],
                default="independent",
                help_text="What stage of learning was this project for you?",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="systemmodule",
            name="portfolio_ready",
            field=models.BooleanField(
                default=False,
                help_text="Is this project ready to show to potential employers?",
            ),
        ),
        migrations.CreateModel(
            name="LearningMilestone",
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
                    "milestone_type",
                    models.CharField(
                        choices=[
                            ("first_time", "First Time Using Technology"),
                            ("breakthrough", "Major Understanding Breakthrough"),
                            ("completion", "Project Completion"),
                            ("deployment", "First Successful Deployment"),
                            ("debugging", "Major Problem Solved"),
                            ("teaching", "First Time Teaching/Helping Others"),
                            ("contribution", "Open Source Contribution"),
                            ("recognition", "External Recognition"),
                        ],
                        help_text="Type of learning milestone",
                        max_length=20,
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text='Brief milestone title (e.g. "First successful API integration")',
                        max_length=200,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        help_text="What you achieved and why it was significant"
                    ),
                ),
                (
                    "date_achieved",
                    models.DateTimeField(
                        help_text="When did you achieve this milestone?"
                    ),
                ),
                (
                    "difficulty_level",
                    models.IntegerField(
                        choices=[
                            (1, "Level 1"),
                            (2, "Level 2"),
                            (3, "Level 3"),
                            (4, "Level 4"),
                            (5, "Level 5"),
                        ],
                        default=3,
                        help_text="How challenging was this to achieve? (1=Easy, 5=Very Hard)",
                    ),
                ),
                (
                    "confidence_boost",
                    models.IntegerField(
                        choices=[
                            (1, "1 stars"),
                            (2, "2 stars"),
                            (3, "3 stars"),
                            (4, "4 stars"),
                            (5, "5 stars"),
                        ],
                        default=3,
                        help_text="How much did this boost you confidence? (1-5 stars)",
                    ),
                ),
                (
                    "shared_publicly",
                    models.BooleanField(
                        default=False,
                        help_text="Did you share this achievement? (blog, social media, etc)",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "related_post",
                    models.ForeignKey(
                        blank=True,
                        help_text="DataLog entry about this milestone (optional)",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="documented_milestones",
                        to="blog.post",
                    ),
                ),
                (
                    "related_skill",
                    models.ForeignKey(
                        blank=True,
                        help_text="Primary skill this relates to (optional)",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="milestones",
                        to="core.skill",
                    ),
                ),
                (
                    "system",
                    models.ForeignKey(
                        help_text="Project/System this milestone is related to",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="milestones",
                        to="projects.systemmodule",
                    ),
                ),
            ],
            options={
                "verbose_name": "Learning Milestone",
                "verbose_name_plural": "Learning Milestones",
                "ordering": ["-date_achieved"],
            },
        ),
        migrations.CreateModel(
            name="SystemSkillGain",
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
                    "proficiency_gained",
                    models.IntegerField(
                        choices=[
                            (1, "First Exposure"),
                            (2, "Basic Understanding"),
                            (3, "Practical Application"),
                            (4, "Confident Usage"),
                            (5, "Teaching Level"),
                        ],
                        help_text="Level of proficiency gained",
                    ),
                ),
                (
                    "how_learned",
                    models.TextField(
                        blank=True,
                        help_text="Brief note on how this skill was used/learned in this project",
                    ),
                ),
                (
                    "skill_level_before",
                    models.IntegerField(
                        blank=True,
                        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                        help_text="Skill level before project (1-5, optional)",
                        null=True,
                    ),
                ),
                (
                    "skill_level_after",
                    models.IntegerField(
                        blank=True,
                        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                        help_text="Skill level after project (1-5, optional)",
                        null=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "skill",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="project_gains",
                        to="core.skill",
                    ),
                ),
                (
                    "system",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="skill_gains",
                        to="projects.systemmodule",
                    ),
                ),
            ],
            options={
                "verbose_name": "System Skill Gain",
                "verbose_name_plural": "System Skill Gains",
                "ordering": ["-created_at"],
                "unique_together": {("system", "skill")},
            },
        ),
        migrations.AddField(
            model_name="systemmodule",
            name="skills_developed",
            field=models.ManyToManyField(
                blank=True,
                help_text="Skills gained or improved through this project",
                related_name="developed_in_projects",
                through="projects.SystemSkillGain",
                to="core.skill",
            ),
        ),
    ]

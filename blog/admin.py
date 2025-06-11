from django.contrib import admin
from .models import Post, Category, Tag, Comment, Series, SeriesPost, SystemLogEntry, PostView
from django.utils.html import format_html


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "color_preview", "icon_preview")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}

    def color_preview(self, obj):
        if obj.color:
            return format_html(
                '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 3px; display: inline-block;"></div>',
                obj.color,
            )
        return "-"

    color_preview.short_description = "Color"

    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<i class="fas {}"></i> {}', obj.icon, obj.icon)
        return "-"

    icon_preview.short_description = "Icon"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "status",
        "featured",
        "reading_time",
        "created_at",
    )
    list_filter = ("status", "featured", "category", "tags", "created_at")
    search_fields = ("title", "content", "excerpt")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    readonly_fields = ("reading_time", "created_at", "updated_at")
    date_hierarchy = "created_at"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "post", "created_at", "approved")
    list_filter = ("approved", "created_at")
    search_fields = ("name", "email", "content")
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
        self.message_user(request, f"Approved {queryset.count()} comments.")

    approve_comments.short_description = "Approve selected comments"


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "post_count_display",
        "difficulty_level",
        "completion_status",
        "featured_status",
        "total_reading_time_display",
    )
    list_filter = ("difficulty_level", "is_complete", "is_featured", "created_at")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at", "post_count", "total_reading_time")
    actions = ["update_series_metrics", "mark_as_complete"]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("title", "slug", "description", "thumbnail")},
        ),
        (
            "Series Settings",
            {"fields": ("difficulty_level", "is_complete", "is_featured")},
        ),
        (
            "Metrics",
            {"fields": ("post_count", "total_reading_time"), "classes": ("collapse",)},
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def post_count_display(self, obj):
        count = obj.post_count
        if count == 0:
            color = "#808080"
        elif count < 3:
            color = "#ffbd2e"
        else:
            color = "#27c93f"
        return format_html('<span style="color: {};">{} posts</span>', color, count)

    post_count_display.short_description = "Posts"

    def completion_status(self, obj):
        if obj.is_complete:
            return format_html('<span style="color: #27c93f;">✓ Complete</span>')
        else:
            return format_html('<span style="color: #ffbd2e;">📝 Ongoing</span>')

    completion_status.short_description = "Status"

    def featured_status(self, obj):
        if obj.is_featured:
            return format_html('<span style="color: #27c93f;">⭐ Featured</span>')
        return "-"

    featured_status.short_description = "Featured"

    def total_reading_time_display(self, obj):
        minutes = obj.total_reading_time
        if minutes >= 60:
            hours = minutes // 60
            remaining_minutes = minutes % 60
            return f"{hours}h {remaining_minutes}m"
        return f"{minutes}m"

    total_reading_time_display.short_description = "Reading Time"

    def update_series_metrics(self, request, queryset):
        for series in queryset:
            series.update_metrics()
        self.message_user(request, f"Updated metrics for {queryset.count()} series.")

    update_series_metrics.short_description = "Update series metrics"

    def mark_as_complete(self, request, queryset):
        queryset.update(is_complete=True)
        self.message_user(request, f"Marked {queryset.count()} series as complete.")

    mark_as_complete.short_description = "Mark as complete"


@admin.register(SeriesPost)
class SeriesPostAdmin(admin.ModelAdmin):
    list_display = ("series", "post", "order")
    list_filter = ("series",)
    ordering = ("series", "order")


@admin.register(SystemLogEntry)
class SystemLogEntryAdmin(admin.ModelAdmin):
    list_display = (
        "log_entry_id",
        "post",
        "system",
        "connection_type",
        "impact_display",
        "hours_variance_display",
        "priority_display",
        "status_display",
    )
    list_filter = (
        "connection_type",
        "impact_level",
        "priority",
        "log_status",
        "system__system_type",
    )
    search_fields = (
        "post__title",
        "system__title",
        "log_entry_id",
        "affected_components",
    )
    readonly_fields = ("created_at", "updated_at", "hours_variance")

    fieldsets = (
        (
            "Connection Details",
            {
                "fields": (
                    "post",
                    "system",
                    "connection_type",
                    "log_entry_id",
                    "system_version",
                )
            },
        ),
        (
            "Impact Assessment",
            {
                "fields": (
                    "impact_level",
                    "priority",
                    "log_status",
                    "affected_components",
                )
            },
        ),
        (
            "Time Tracking",
            {"fields": ("estimated_hours", "actual_hours", "hours_variance")},
        ),
        ("Resolution", {"fields": ("resolution_notes",)}),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at", "resolved_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def impact_display(self, obj):
        colors = {
            "low": "#27c93f",
            "medium": "#ffbd2e",
            "high": "#ff8a80",
            "critical": "#f44336",
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.impact_level, "#808080"),
            obj.get_impact_level_display(),
        )

    impact_display.short_description = "Impact"

    def hours_variance_display(self, obj):
        variance = obj.hours_variance()
        if variance is not None:
            if variance > 0:
                return format_html(
                    '<span style="color: #ff8a80;">+{} hrs</span>', variance
                )
            elif variance < 0:
                return format_html(
                    '<span style="color: #27c93f;">{} hrs</span>', variance
                )
            else:
                return format_html('<span style="color: #27c93f;">On target</span>')
        return "-"

    hours_variance_display.short_description = "Hours Variance"

    def priority_display(self, obj):
        colors = {1: "#808080", 2: "#ffbd2e", 3: "#ff8a80", 4: "#f44336"}
        return format_html(
            '<span style="color: {};">Priority {}</span>',
            colors.get(obj.priority, "#808080"),
            obj.priority,
        )

    priority_display.short_description = "Priority"

    def status_display(self, obj):
        colors = {
            "draft": "#808080",
            "active": "#ffbd2e",
            "resolved": "#27c93f",
            "archived": "#b39ddb",
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.log_status, "#808080"),
            obj.get_log_status_display(),
        )

    status_display.short_description = "Status"


@admin.register(PostView)
class PostViewAdmin(admin.ModelAdmin):
    list_display = ("post", "ip_address", "viewed_on")
    list_filter = ("viewed_on",)
    search_fields = ("post__title", "ip_address")
    readonly_fields = ("viewed_on",)


# Customize admin site
admin.site.site_header = "AURA Portfolio Administration"
admin.site.site_title = "AURA Admin"
admin.site.index_title = "DataLogs Control Panel"

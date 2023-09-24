from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry, DELETION
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe

from .models import Profile, Post, Comment, Group

admin.site.site_header = 'Babushka'
admin.site.site_title = 'Админ Babushka'


def remove_delete_action(actions):
    if 'delete_selected' in actions:
        del actions['delete_selected']
    return actions


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    fields = ('description', 'site_url', 'gender', 'is_allow_recommends', 'profile_pic_preview', 'profile_pic')
    readonly_fields = ('profile_pic_preview', )
    extra = 0

    def profile_pic_preview(self, obj):
        return mark_safe('<img src="%s" width=200>' % (obj.profile_pic.url))

    profile_pic_preview.short_description = 'Предпросмотр'


class CommentsInline(admin.TabularInline):
    model = Comment
    readonly_fields = ('user', 'comment', 'get_str_time')
    fields = ('user', 'comment', 'get_str_time')
    can_delete = True
    extra = 0

    def has_add_permission(self, request, obj):
        return False


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'first_name', 'last_name', 'id')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        return remove_delete_action(super().get_actions(request))


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('user', '__str__', 'action_time')
    list_display_links = ('__str__',)
    list_filter = ('content_type',)
    readonly_fields = ['object_link', 'user', 'action_time', 'content_type', 'object_id', 'object_repr', 'action_flag',
                       'change_message']
    search_fields = ('action_time', 'user__first_name', 'user__last_name', 'object_id', 'object_repr')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_actions(self, request):
        return remove_delete_action(super().get_actions(request))

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return mark_safe(link)

    object_link.short_description = 'Ссылка на объект'


@admin.register(Post)
class PostAdmin (admin.ModelAdmin):
    list_display = ('id', 'get_publisher', 'get_str_time')
    fieldsets = [
        ('Основная информация', {'fields': ['get_publisher', 'title', 'image_preview'], 'classes': ['wide']}),
        ('Дополнительно', {'fields': ['is_archived', 'is_allow_comments', 'get_num_of_likes', 'get_num_of_comments', 'get_num_of_bookmarks', 'created'], 'classes': ['wide']}),
    ]
    list_filter = ('is_allow_comments', 'is_archived')
    inlines = [CommentsInline, ]
    readonly_fields = ['get_publisher', 'image_preview', 'get_num_of_likes', 'get_num_of_comments', 'get_num_of_bookmarks', 'get_str_time', 'created']
    search_fields = ('user_profile', 'group', 'title', 'image', 'created')
    list_per_page = 20
    ordering = ('-id',)

    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        return remove_delete_action(super().get_actions(request))

    def get_publisher(self, obj):
        if obj.user_profile:
            return mark_safe('<a href="%s"><i class="fas fa-user mr-1"></i> %s</a>' % (
                reverse('admin:auth_user_change', args=[obj.user_profile.user.pk]),
                f'{obj.user_profile.user}'
            ))
        elif obj.group:
            return mark_safe('<a href="%s"><i class="fas fa-user-friends mr-1"></i> %s</a>' % (
                reverse('admin:feeds_group_change', args=[obj.group.pk]),
                f'{obj.group}'
            ))
        else:
            return "-"

    def image_preview(self, obj):
        return mark_safe('<img src="%s" width=300>' % (obj.image.url))

    get_publisher.short_description = 'Автор'
    image_preview.short_description = 'Предпросмотр'


@admin.register(Group)
class GroupAdmin (admin.ModelAdmin):
    list_display = ('groupname', 'title', 'owner', 'id')
    fieldsets = [
        ('Основная информация', {'fields': ['groupname', 'owner', 'title', 'description', 'site_url', 'profile_pic_preview', 'profile_pic'], 'classes': ['wide']}),
        ('Дополнительно', {'fields': [], 'classes': ['wide']}),
    ]
    readonly_fields = ['groupname', 'owner', 'profile_pic_preview']
    search_fields = ('groupname', 'owner', 'title', 'description', 'site_url')
    list_per_page = 20
    ordering = ('-id',)

    def get_actions(self, request):
        return remove_delete_action(super().get_actions(request))

    def has_add_permission(self, request, obj=None):
        return False

    def profile_pic_preview(self, obj):
        return mark_safe('<img src="%s" width=200>' % (obj.profile_pic.url))

    profile_pic_preview.short_description = 'Предпросмотр'

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.home, name="home"),
    path("members/", views.members, name="members"),
    path("rules/", views.rules, name="rules"),
    path("join/", views.recruitment, name="recruitment"),
    path("admin-panel/", views.admin_panel, name="admin_panel"),
    path(
        "admin-panel/settings/",
        views.update_team_settings,
        name="update_team_settings",
    ),
    path("add-member/", views.add_member, name="add_member"),
    path("add-leader/", views.add_leader, name="add_leader"),
    path("add-rule/", views.add_rule, name="add_rule"),
    path("edit-rule/<int:pk>/", views.edit_rule, name="edit_rule"),
    path("edit-member/<int:pk>/", views.edit_member, name="edit_member"),
    path("edit-leader/<int:pk>/", views.edit_leader, name="edit_leader"),
    path("delete-member/<int:pk>/", views.delete_member, name="delete_member"),
    path("delete-leader/<int:pk>/", views.delete_leader, name="delete_leader"),
    path("delete-rule/<int:pk>/", views.delete_rule, name="delete_rule"),
    path(
        "applications/<int:pk>/delete/",
        views.delete_application,
        name="delete_application",
    ),
    path(
        "applications/<int:pk>/accept/",
        views.accept_application,
        name="accept_application",
    ),
    path(
        "applications/<int:pk>/reject/",
        views.reject_application,
        name="reject_application",
    ),
    path(
        "match-requests/<int:pk>/accept/",
        views.accept_match_request,
        name="accept_match_request",
    ),
    path(
        "match-requests/<int:pk>/reject/",
        views.reject_match_request,
        name="reject_match_request",
    ),
    path(
        "match-requests/<int:pk>/delete/",
        views.delete_match_request,
        name="delete_match_request",
    ),
    path("account/", views.member_account, name="member_account"),
    path("admin-panel/user-accounts/", views.user_accounts, name="user_accounts"),
    path(
        "admin-panel/user-accounts/<int:member_id>/create/",
        views.create_member_account,
        name="create_member_account",
    ),
    path(
        "admin-panel/user-accounts/<int:member_id>/",
        views.user_account_edit,
        name="user_account_edit",
    ),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
]

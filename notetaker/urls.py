from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("create", views.create, name="create"),
    path("create_team", views.create_team, name="create_team"),
    path("user_team", views.user_team, name="user_team"),
    path("create_invitation/<int:team_id>/", views.create_invitation, name="create_invitation"),
    path("join_team/<uuid:token>/", views.join_team, name="join_team"),
    path("team/<int:team_id>/create_task/", views.create_team_task, name="create_team_task"),
    path("team/<int:team_id>/", views.team_detail, name="team_detail"),
    path("team/<int:team_id>/task/<int:task_id>/", views.task_detail_api, name="task_detail_api"),
    path("task/<int:task_id>/", views.solo_task_detail, name="solo_task_detail"),
    path("team/<int:team_id>/task/<int:task_id>/assign/", views.assign_task, name="assign_task"),
    path("task/<int:task_id>/mark_done/", views.mark_task_done, name="mark_task_done"),
    path("task/<int:task_id>/delete/", views.delete_task, name="delete_task"),
    path("team/<int:team_id>/leave/", views.leave_team, name="leave_team"),
    path("task/<int:task_id>/edit", views.edit_task, name="edit_task"),
    path("team/<int:team_id>/delete/", views.delete_team, name="delete_team"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

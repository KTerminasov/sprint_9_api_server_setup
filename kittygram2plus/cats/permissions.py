"""Файл для описания собственных пермишенов для пользователей API."""

from rest_framework import permissions


class OwnerOrReadOnly(permissions.BasePermission):
    """Кастомный пермишен,
    который разрешает полный доступ к объекту только автору.

    При работе с вьюсетом при анонимном запроче позволяет
    получить только список котиков, но не возволяет получить
    информацию о конкретном котике.
    """

    def has_permission(self, request, view):
        """Определяет разрешение на уровне запроса."""
        return (
                request.method in permissions.SAFE_METHODS  # GET, HEAD или OPTIONS
                or request.user.is_authenticated
            )

    def has_object_permission(self, request, view, obj):
        """Определяет разрешение на уровне объекта."""
        return obj.owner == request.user


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS 
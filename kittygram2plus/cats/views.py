from rest_framework import viewsets, permissions
from rest_framework.pagination import (
    PageNumberPagination, LimitOffsetPagination
)
from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle

from .models import Achievement, Cat, User
from .pagination import CatsPagination
from .permissions import OwnerOrReadOnly, ReadOnly
from .serializers import AchievementSerializer, CatSerializer, UserSerializer
from .throttling import WorkingHoursRateThrottle


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    # Устанавливаем разрешение, теперь смотреть список
    # котиков можно без аутенфикации.
    permission_classes = (OwnerOrReadOnly,)

    # Устанавливаем лимит запросов для анонимов из settings
    # throttle_classes = (AnonRateThrottle,)

    # Если кастомный тротлинг-класс вернёт True - запросы будут обработаны
    # Если он вернёт False - все запросы будут отклонены
    # throttle_classes = (WorkingHoursRateThrottle, ScopedRateThrottle)

    # Для любых пользователей установим кастомный лимит 1 запрос в минуту
    throttle_scope = 'low_request'

    # Пагинация на уровне класса с помощью PageNumberPagination.
    # pagination_class = PageNumberPagination

    # Пагинация на уровне класса с помощью LimitOffsetPagination.
    # pagination_class = LimitOffsetPagination

    # Кастомная пагинация
    pagination_class = CatsPagination

    def get_permissions(self):
        """Определяет какой пермишен использовать."""
        # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
            # Вернём обновлённый перечень используемых пермишенов
            return (ReadOnly(),)
        # Для остальных ситуаций оставим текущий перечень пермишенов
        # без изменений
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer

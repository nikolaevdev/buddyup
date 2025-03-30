import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/pages/HomePage.vue'; // Предполагается, что это главная страница
import RequestsPage from '@/pages/Requests/RequestsPage.vue'; // Страница списка запросов
import ProfilePage from '@/pages/ProfilePage.vue'; // Страница профиля
import NewRequestPage from '@/pages/Requests/NewRequestPage.vue'; // Страница создания нового запроса
import RequestDetailPage from '@/pages/Requests/RequestDetailPage.vue'; // Страница детального просмотра запроса
import EditRequestPage from '@/pages/Requests/EditRequestPage.vue'; // Страница редактирования запроса
import NotFoundPage from '@/pages/NotFoundPage.vue'; // Страница 404


const routes = [
    {
        path: '/',
        name: 'Home',
        component: HomePage,
    },
    {
        path: '/requests',
        name: 'Requests',
        component: RequestsPage,
    },
    {
        path: '/requests/new',
        name: 'NewRequest',
        component: NewRequestPage,
    },
    {
        path: '/requests/:id',
        name: 'RequestDetail',
        component: RequestDetailPage,
        props: true, // Передаем параметры маршрута как props в компонент
    },
    {
        path: '/requests/:id/edit',
        name: 'EditRequest',
        component: EditRequestPage,
        props: true,
    },
    {
        path: '/profile',
        name: 'Profile',
        component: ProfilePage,
    },
    {
        path: '/:pathMatch(.*)*', // Обработка 404
        name: 'NotFound',
        component: NotFoundPage,
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
    // Добавляем поведение прокрутки для мобильного приложения
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) {
            return savedPosition; // Возвращаем сохраненную позицию при возврате назад
        }
        return { top: 0 }; // Прокрутка вверх при переходе на новую страницу
    },
});

export default router;
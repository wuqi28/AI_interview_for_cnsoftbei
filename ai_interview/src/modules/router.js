import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            redirect: '/index'
        },
        {
            path: "/index", component: () => import('@/pages/index.vue'),
            children: [
                { path: "/resume", component: () => import('@/pages/resume.vue') },
                { path: "/interview", component: () => import('@/pages/interview.vue') },
            ]
        },
        { path: "/register", component: () => import('@/pages/register.vue') },
        { path: "/mock", component: () => import('@/pages/mock.vue') },
        { path: "/report", component: () => import('@/pages/report.vue') },
        { path: "/test", component: () => import('@/pages/test.vue') },
        { path: "/test2", component: () => import('@/pages/test2.vue') },
    ],
});

export default router;
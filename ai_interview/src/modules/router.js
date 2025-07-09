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
                { path: "/record", component: () => import('@/pages/record.vue') },
                { path: "/exercise", component: () => import('@/pages/exercise.vue') },
                { path: "/resource", component: () => import('@/pages/resource.vue') },
                { path: "/question", component: () => import('@/pages/question.vue') },
            ]
        },
        { path: "/register", component: () => import('@/pages/register.vue') },
        { path: "/mock", component: () => import('@/pages/mock.vue') },
        { path: "/report", component: () => import('@/pages/report.vue') },
        { path: "/programming", component: () => import('@/pages/programming.vue') },
        { path: "/operation", component: () => import('@/pages/operation.vue') },
        { path: "/product", component: () => import('@/pages/product.vue') },
        { path: "/resume_draw", component: () => import('@/pages/resumeDraw.vue') },
        { path: "/test2", component: () => import('@/pages/test2.vue') },
    ],
});

export default router;
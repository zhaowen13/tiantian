import { createWebHistory, createRouter } from 'vue-router'
const history = createWebHistory()
const router = createRouter({
    history, // 路由模式
    routes: [
      {
        // 页面逻辑
        path: '/login',
        name: 'login',
        component: () => import('@/components/login')
      },
      {
        // 表格类
        path: '/table',
        name: 'table',
        component: () => import('@/components/table')
      },
      {
        // 
        path: '/test',
        name: 'test',
        component: () => import('@/components/test')
      },
      {
        // 基金
        path: '/fund',
        name: 'fund',
        meta: { 
          requireAuth: true // 配置此条，进入页面前判断是否需要登陆 
         }, 
        component: () => import('@/components/fund')
      },
      {
        // 股票
        path: '/',
        name: 'stock',
        meta: { 
          requireAuth: true // 配置此条，进入页面前判断是否需要登陆 
         }, 
        component: () => import('@/components/stock')
      }
    ]
  })

export default router


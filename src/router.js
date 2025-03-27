import HomeView from '@views/HomeView.vue'
import LoginView from '@views/LoginView.vue'
import RegisterView from '@views/RegisterView.vue'
import QuizDetailView from '@views/QuizDetailView.vue'

import UserHome from '@views/user/UserHome.vue'
import UserScores from '@views/user/UserScores.vue'
import UserSummary from '@views/user/UserSummary.vue'
import UserTakeQuiz from '@views/user/UserTakeQuiz.vue'

import AdminHome from '@views/admin/AdminHome.vue'
import AdminQuiz from '@views/admin/AdminQuiz.vue'
import AdminNewQuiz from '@views/admin/AdminNewQuiz.vue'
import AdminEditQuiz from '@views/admin/AdminEditQuiz.vue'
import AdminNewSubject from '@views/admin/AdminNewSubject.vue'

import { store } from '@/store'
import { createRouter, createWebHistory } from 'vue-router'
import AdminSummary from '@views/admin/AdminSummary.vue'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      name: 'home',
      path: '/',
      component: HomeView,
    },
    {
      name: 'login',
      path: '/login',
      component: LoginView,
    },
    {
      name: 'register',
      path: '/register',
      component: RegisterView,
    },
    {
      name: 'quizDetail',
      path: '/quiz/:id(\\d+)',
      component: QuizDetailView,
    },
    {
      path: '/user',
      beforeEnter(_to, from, next) {
        if (!store.state.authenticated && from.name !== 'login') {
          next({ name: 'login' })
        } else next()
      },
      children: [
        {
          name: 'userHome',
          path: '',
          component: UserHome,
        },
        {
          name: 'userScores',
          path: 'scores',
          component: UserScores,
        },
        {
          name: 'userSummary',
          path: 'summary',
          component: UserSummary,
        },
        {
          name: 'takeQuiz',
          path: 'quiz/take/:id(\\d+)',
          component: UserTakeQuiz,
        },
      ],
    },
    {
      path: '/admin',
      beforeEnter(_to, from, next) {
        if (!store.state.authenticated && from.name !== 'login') {
          next({ name: 'login' })
        } else next()
      },
      children: [
        {
          name: 'adminHome',
          path: '',
          component: AdminHome,
        },
        {
          name: 'adminSummary',
          path: 'summary',
          component: AdminSummary,
        },
        {
          name: 'quiz',
          path: 'quiz',
          component: AdminQuiz,
        },
        {
          name: 'addQuiz',
          path: 'quiz/add',
          component: AdminNewQuiz,
        },
        {
          name: 'editQuiz',
          path: 'quiz/edit/:id(\\d+)',
          component: AdminEditQuiz,
        },
        {
          name: 'addSubject',
          path: 'subject/add',
          component: AdminNewSubject,
        },
      ],
    },
  ],
})

router.beforeEach((_to, _from, next) => {
  document.startViewTransition(next)
})

export default router

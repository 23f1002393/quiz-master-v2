import Vuex from 'vuex'

const BACKEND_URL = 'http://127.0.0.1:5000/api'

export const store = new Vuex.Store({
  state: {
    currentUser: null,
    authenticated: false,
    activeQuiz: null,
    quizzes: [],
    subjects: [],
    scores: [],
    hideNavbar: false,
  },
  actions: {
    async registerUser(_, payload) {
      await fetch(`${BACKEND_URL}/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      })
    },
    async loginUser({ commit }, data) {
      await fetch(`${BACKEND_URL}/login`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
      const { current_user } = await fetch(`${BACKEND_URL}/users/me`, {
        credentials: 'include',
      }).then((response) => response.json())

      commit('setAuthentication', {
        currentUser: current_user,
        authenticated: true,
      })
    },
    async fetchSubjects({ commit, state }) {
      if (state.currentUser != null) {
        const { subjects } = await fetch(`${BACKEND_URL}/subjects`, {
          credentials: 'include',
        })
          .then((response) => response.json())
          .catch((error) => {
            console.error('[ERROR]:', error)
          })

        commit('setSubjects', subjects)
      } else console.warn('USER LOGIN REQUIRED')
    },
    async fetchQuizzes({ commit, state }) {
      if (state.currentUser != null) {
        const { quizzes } = await fetch(`${BACKEND_URL}/quizzes`, {
          credentials: 'include',
        })
          .then((response) => response.json())
          .catch((error) => {
            console.error('[ERROR]:', error)
          })
        commit('setQuizzes', quizzes)
      } else console.warn('USER LOGIN REQUIRED')
    },
    async fetchScores({ commit, state }) {
      if (state.currentUser != null) {
        const { scores } = await fetch(`${BACKEND_URL}/scores`, {
          credentials: 'include',
        })
          .then((response) => response.json())
          .catch((error) => console.error(error))
        commit('setScores', scores)
      } else console.warn('[WARN] user login required')
    },
    async fetchUserStats({ commit }) {
      const stats = await fetch(`${BACKEND_URL}/user/stats`, {
        credentials: 'include',
      })
        .then((response) => response.json())
        .catch((error) => console.error('[ERROR]', error))
      commit('setStats', stats)
    },
    async fetchAdminStats({ commit, state }) {
      if (state.currentUser.isAdmin) {
        const stats = await fetch(`${BACKEND_URL}/admin/stats`, {
          credentials: 'include',
        })
          .then((response) => response.json())
          .catch((error) => console.error('[ERROR]', error))
        commit('setStats', stats)
      }
    },
    async createSubject({ dispatch }, payload) {
      await fetch(`${BACKEND_URL}/subjects`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      })
        .then(() => dispatch('fetchSubjects'))
        .catch((error) => console.error('[ERROR]', error))
    },
    async createQuiz({ dispatch }, payload) {
      await fetch(`${BACKEND_URL}/quizzes`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      })
        .then(() => dispatch('fetchQuizzes'))
        .catch((error) => console.error('[ERROR]', error))
    },
    async deleteQuiz({ dispatch }, quiz_id) {
      await fetch(`${BACKEND_URL}/quizzes/${quiz_id}`, {
        method: 'DELETE',
        credentials: 'include',
      })
        .then(() => dispatch('fetchQuizzes'))
        .catch((error) => console.error(error))
    },
    async deleteSubject({ dispatch }, subject_id) {
      await fetch(`${BACKEND_URL}/subjects/${subject_id}`, {
        method: 'DELETE',
        credentials: 'include',
      })
        .then(() => dispatch('fetchSubjects'))
        .catch((error) => console.error('[ERROR]', error))
    },
    async submitQuiz({ commit, state }, payload) {
      await fetch(`${BACKEND_URL}/quiz/${state.activeQuiz}/submit`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      })
      commit('clearQuiz')
    },
  },
  mutations: {
    setAuthentication(state, { currentUser, authenticated }) {
      state.currentUser = currentUser
      state.authenticated = authenticated
    },
    setQuizzes(state, quizzes) {
      state.quizzes = quizzes
    },
    setSubjects(state, subjects) {
      state.subjects = subjects
    },
    logoutUser(state) {
      state.currentUser = null
    },
    startQuiz(state, quizId) {
      state.activeQuiz = quizId
    },
    clearQuiz(state) {
      state.activeQuiz = null
    },
    setScores(state, scores) {
      state.scores = scores
    },
    setStats(state, stats) {
      state.stats = stats
    },
  },
})

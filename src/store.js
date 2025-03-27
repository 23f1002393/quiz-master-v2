import Vuex, { createLogger } from 'vuex'

export const store = new Vuex.Store({
  plugins: [createLogger()],
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
    async loginUser({ commit }, data) {
      await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(data),
      })
      const { current_user } = await fetch('http://localhost:5000/users/me', {
        credentials: 'include',
      }).then((response) => response.json())

      commit('setAuthentication', {
        currentUser: current_user,
        authenticated: true,
      })
    },
    async fetchSubjects({ commit, state }) {
      if (state.currentUser != null) {
        const { subjects } = await fetch('http://localhost:5000/subjects', {
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
        const { quizzes } = await fetch('http://localhost:5000/quizzes', {
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
        const { scores } = await fetch('http://localhost:5000/scores', {
          credentials: 'include',
        })
          .then((response) => response.json())
          .catch((error) => console.error(error))
        commit('setScores', scores)
      } else console.warn('[WARN] user login required')
    },
    async fetchStats({ commit }) {
      const stats = await fetch('http://localhost:5000/stats', {
        credentials: 'include',
      })
        .then((response) => response.json())
        .catch((error) => console.error('[ERROR]', error))
      commit('setStats', stats)
    },
    async createSubject(_, payload) {
      await fetch('http://localhost:5000/subjects', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      }).catch((error) => console.error('[ERROR]', error))
    },
    async createQuiz(_, payload) {
      console.log(payload)
      await fetch('http://localhost:5000/quizzes', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      }).catch((error) => console.error('[ERROR]', error))
    },
    async deleteQuiz({ dispatch }, quiz_id) {
      await fetch(`http://localhost:5000/quizzes/${quiz_id}`, {
        method: 'DELETE',
        credentials: 'include',
      })
        .then((response) => response.json())
        .then(() => dispatch('fetchQuizzes'))
        .catch((error) => console.error(error))
    },
    async updateQuiz(_, payload) {
      await fetch(`http://localhost:5000/subjects/${payload.id}`, {
        method: 'PUT',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      })
        .then(() => store.dispatch('fetchSubjects'))
        .catch((error) => console.error('[ERROR]', error))
    },
  },
  async deleteSubject({ dispatch }, subject_id) {
    await fetch(`http://localhost:5000/subjects/${subject_id}`, {
      method: 'DELETE',
      credentials: 'include',
    })
      .then((response) => response.json())
      .then(() => dispatch('fetchSubjects'))
      .error((error) => console.error('[ERROR]', error))
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

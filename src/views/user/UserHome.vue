<script setup>
import QuizCard from '@components/QuizCard.vue';

import { computed } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

const store = useStore();
const router = useRouter();
await store.dispatch('fetchQuizzes');
const currentUser = computed(() => store.state.currentUser);

const quizzes = computed(() => store.state.quizzes);
const upcommingCount = computed(() => {
  return quizzes.value.filter((quiz) => !quiz.done).length;
});

function onStart(quiz_id) {
  store.commit('startQuiz', quiz_id);
  router.replace(`/user/quiz/take/${quiz_id}`);
}
function onView(quiz_id) {
  router.replace(`/quiz/${quiz_id}`);
}
</script>

<template>
  <div v-if="currentUser">
    <h1 class="display-6 text-center">Upcomming Quizzes</h1>
    <hr />
    <div v-if="quizzes && upcommingCount != 0" class="container-md">
      <QuizCard v-for="(quiz, key) in quizzes" v-show="!quiz.done" :quiz="quiz" :key @view="() => onView(key)"
        @start="onStart" />
    </div>
    <div v-else>
      <h1 class="display-6 text-center rounded bg-dark p-2">No Quizzes Available</h1>
    </div>
  </div>
</template>

<style>
ul {
  padding: 0;
  list-style: none;
}

button.btn {
  img {
    width: 1.25rem;
  }
}
</style>

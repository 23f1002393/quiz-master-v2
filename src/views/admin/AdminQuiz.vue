<script setup>
import { useStore } from 'vuex';
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import QuizCard from '@components/QuizCard.vue';

const store = useStore();
const currentUser = computed(() => store.state.currentUser);
const router = useRouter();

await store.dispatch('fetchQuizzes');
const quizzes = computed(() => store.state.quizzes);

function onDelete(quiz) {
  store.dispatch('deleteQuiz', quiz.quiz_id);
}

function onUpdate(quiz) {
  router.push(`/admin/quiz/${quiz.quiz_id}`);
}

function onView(quiz_id) {
  router.replace(`/quiz/${quiz_id}`);
}
</script>

<template>
  <div v-if="currentUser" class="text-center">
    <h1 class="display-6">Active Quizzes</h1>
    <button type="button" class="btn btn-primary ps-3 pe-3 my-3" @click.prevent="router.push('/admin/quiz/add')">
      add quiz <img src="@/assets/add.svg" alt="add" />
    </button>
    <div v-show="quizzes" class="p-0 d-flex flex-wrap flex-md-nowrap">
      <QuizCard v-for="(quiz, key) in quizzes.filter(quiz => !(quiz.date_of_quiz > Date.now()))" :key :quiz
        :admin="currentUser.isAdmin" @update="onUpdate" @delete="onDelete" @view="() => onView(key)" />
    </div>
    <hr />
    <h1 class="display-6">Past Quizzes</h1>
    <div class="container">
      <QuizCard v-for="(quiz, key) in quizzes.filter(quiz => quiz.date_of_quiz <= Date.now())" :key :quiz
        :admin="currentUser.isAdmin" @delete="onDelete" @update="onUpdate" @view="() => onView(key)" />
    </div>
  </div>
</template>
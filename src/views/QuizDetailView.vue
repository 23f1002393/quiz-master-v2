<script setup>
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useStore } from 'vuex';

const route = useRoute();
const store = useStore();
const router = useRouter();

const quiz = computed(() => store.state.quizzes.at(route.params.id));
const currentUser = computed(() => store.state.currentUser);

const attrs = [
  { name: 'Subject', value: quiz.value.subject },
  { name: 'Chapter', value: quiz.value.chapter },
  { name: 'No. of questions', value: quiz.value.questions.length },
  { name: 'Scheduled Date', value: new Date(quiz.value.date_of_quiz).toISOString().split('T')[0] },
  { name: 'Duration(hh:mm)', value: `01:00` },
];

function startQuiz() {
  store.commit('startQuiz', quiz.value.quiz_id);
  router.replace(`/user/quiz/take/${quiz.value.quiz_id}`);
}
</script>

<template>
  <div class="quiz container" v-if="currentUser">
    <h1 class="display-5">{{ quiz.name }}</h1>
    <div v-for="attr in attrs" class="row mt-2">
      <span class="col fs-5 bg-dark p-2 rounded">{{ attr.name }}</span>
      <span class="col fs-5 p-2 text-center bg-secondary text-dark rounded">
        {{ attr.value }}
      </span>
    </div>
    <button v-show="!currentUser.isAdmin" class="btn btn-primary mt-3 fs-5 w-100" @click.prevent="startQuiz">start
      quiz</button>
  </div>
</template>
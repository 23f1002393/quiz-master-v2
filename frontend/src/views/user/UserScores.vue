<script setup>
import { computed } from 'vue';
import { useStore } from 'vuex';

const store = useStore();
await store.dispatch('fetchScores');
const currentUser = computed(() => store.state.currentUser);

const scores = computed(() => store.state.scores);
</script>

<template>
  <div class="container" v-if="currentUser">
    <h1 class="display-4 text-center">Quiz Scores</h1>
    <hr />
    <div v-if="scores && scores.length !== 0">
      <div class="row text-center rounded bg-secondary lead text-white fw-bold p-2 mt-2">
        <span class="col">Quiz ID</span>|
        <span class="col">Date</span>|
        <span class="col">Score</span>
      </div>
      <div v-for="(score, key) in scores" :key>
        <div class="row text-center rounded bg-dark p-2 mt-2">
          <span class="col">{{ score.id }}</span>|
          <span class="col">{{ new Date(score.date_of_quiz).toISOString().split('T')[0] }}</span>|
          <span class="col">{{ score.correct }} / {{ score.total }}</span>
        </div>
      </div>
    </div>
    <div v-else class="lead bg-dark rounded p-2 text-center">No scores available</div>
  </div>
</template>
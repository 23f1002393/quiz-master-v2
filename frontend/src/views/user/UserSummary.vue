<script setup>
import { computed } from 'vue';
import { useStore } from 'vuex';

const store = useStore();
await store.dispatch('fetchUserStats');
const stats = computed(() => store.state.stats);
const { by_month, by_subject } = stats.value;
const currentUser = computed(() => store.state.currentUser);
</script>

<template>
  <div class="container" v-if="currentUser">
    <h1 class="display-3">User Summary</h1>
    <p class="lead">Subject wise:</p>
    <img :src="'/static/images/' + by_subject" alt="subject-wise summary" class="img-thumbnail">
    <p class="lead">Month wise no. of quizzes attempted:</p>
    <img :src="'/static/images/' + by_month" alt="month-wise summary" class="img-thumbnail">
  </div>
</template>
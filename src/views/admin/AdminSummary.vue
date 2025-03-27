<script setup>
import { computed } from 'vue';
import { useStore } from 'vuex';

const store = useStore();
await store.dispatch('fetchStats');
const stats = computed(() => store.state.stats);
const { user_count, by_subject } = stats.value;
const currentUser = computed(() => store.state.currentUser);
</script>

<template>
  <div class="container" v-if="currentUser != null">
    <h1 class="display-3">User Summary</h1>
    <p class="lead">Subject-wise Max Scores:</p>
    <img :src="'/images/' + by_subject" alt="subject-wise summary" class="img-thumbnail">
    <p class="lead">Subject-wise no. of user attempted:</p>
    <img :src="'/images/' + user_count" alt="month-wise summary" class="img-thumbnail">
  </div>
</template>
<script setup>
import { ref, onErrorCaptured, computed } from 'vue';
import { useStore } from 'vuex';
import { RouterView } from 'vue-router';
import NavBar from '@components/NavBar.vue';

const store = useStore();
const currentUser = computed(() => store.state.currentUser);
const hidden = computed(() => store.state.activeQuiz != null);

const links = computed(() => !currentUser.value ?
  [
    { name: 'Home', path: '/' },
    { name: 'Login', path: '/login' },
    { name: 'Register', path: '/register' },
  ] : currentUser.value.isAdmin ?
    [
      { name: "Home", path: "/admin" },
      { name: "Quiz", path: "/admin/quiz" },
      { name: "Summary", path: "/admin/summary" },
    ] : [
      { name: "Home", path: "/user" },
      { name: "Scores", path: "/user/scores" },
      { name: "Summary", path: "/user/summary" },
    ]);

const errMsg = ref(null);
onErrorCaptured(e => {
  errMsg.value = e.message;
  return true;
});
</script>

<template>
  <NavBar :links class="bg-dark" :hidden />
  <div v-if="errMsg" class="alert alert-danger" role="alert">
    {{ errMsg }}
  </div>
  <KeepAlive v-else>
    <Suspense>
      <template #default>
        <div class="page">
          <RouterView style="view-transition-name: route-view; grid-area: 2 / 2;" />
        </div>
      </template>
      <template #fallback>
        <div role="status">
          <span class="display-5 text-white" style="grid-area: 2 / 2">Loading...</span>
        </div>
      </template>
    </Suspense>
  </KeepAlive>
</template>
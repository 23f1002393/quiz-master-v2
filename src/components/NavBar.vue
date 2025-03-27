<script setup>
import { computed } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import ScrollWatcher from '@components/ScrollWatcher.vue';

const store = useStore();
const router = useRouter();
const currentUser = computed(() => store.state.currentUser);

const { links, hidden } = defineProps(['links', 'hidden']);

function logout() {
  store.commit('logoutUser');
  router.push('/login');
}
</script>

<template>
  <header v-show="!hidden">
    <nav class="bg-dark fixed-top">
      <span @click.prevent="() => { router.push(''); }" class="route-link ps-4 fs-5 lead">
        QuizMaster v2
      </span>
      <div class="space"></div>
      <ul class="navbar-links">
        <li v-for="link, i in links" :key="i">
          <span class="route-link col" @click.prevent="() => router.push(link.path)">
            {{ link.name }}
          </span>
        </li>
        <li v-show="!!currentUser">
          <span class="route-link col" @click.prevent="logout">Logout</span>
        </li>
      </ul>
      <ScrollWatcher />
    </nav>
  </header>
</template>

<style scoped>
nav {
  height: 3rem;
  display: flex;
  align-items: center;
  grid-template-columns: 150px auto 15%;

  .space {
    flex-grow: 1;
  }

  ul {
    display: flex;
    justify-content: space-between;
    align-items: center;
    list-style: none;
    height: 100%;
    padding: 0;
    margin: 0;
    gap: 1rem;
    padding-right: 1rem;
  }
}

span.route-link {
  cursor: pointer;
}
</style>

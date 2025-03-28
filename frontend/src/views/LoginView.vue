<script setup>
import { useStore } from 'vuex'
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()
const currentUser = computed(() => store.state.currentUser)

const email = ref('')
const password = ref('')

async function onSubmit() {
  try {
    await store.dispatch('loginUser', { email: email.value, password: password.value });

    if (currentUser.value.isAdmin)
      router.replace('/admin');
    else
      router.replace('/user');
  } catch (error) {
    console.error('[ERROR] login failed:', error);
  }
}
</script>

<template>
  <form @submit.prevent="onSubmit">
    <h1 class="display-5 text-center">Login</h1>
    <div class="form-floating mt-2">
      <input class="form-control" v-model="email" type="text" id="email" />
      <label for="email">Email</label>
    </div>
    <div class="form-floating mt-2">
      <input class="form-control" v-model="password" type="password" id="password" />
      <label for="password">Password</label>
    </div>
    <button class="btn btn-primary mt-3" type="submit">
      Login
    </button>
  </form>
</template>

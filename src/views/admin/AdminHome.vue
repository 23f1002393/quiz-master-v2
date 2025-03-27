<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router';
import SubjectCard from '@components/SubjectCard.vue'

const store = useStore()
await store.dispatch('fetchSubjects')
const router = useRouter();

const currentUser = computed(() => store.state.currentUser)
const subjects = computed(() => store.state.subjects)
</script>

<template>
  <div v-if="currentUser">
    <h1 class="display-5">Available Subjects</h1>

    <div v-if="currentUser.isAdmin">
      <button type="button" class="btn btn-primary ps-3 pe-3 text-center mt-3"
        @click.prevent=" router.push('/admin/subject/add')">
        Add Subject <img src="@assets/add.svg" alt="add subject" />
      </button>
    </div>

    <div class="d-flex p-0 flex-wrap flex-md-nowrap justify-content-start" style="height: 60dvh;">
      <SubjectCard v-for="(subject, i) in subjects" :subjectKey="i" :key="i" :subject="subject" />
    </div>
  </div>
</template>
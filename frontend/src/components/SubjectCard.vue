<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'

const store = useStore()
const currentUser = computed(() => store.state.currentUser)

const { subject, subjectKey } = defineProps(['subject', 'subjectKey'])
</script>

<template>
  <div class="bg-secondary rounded p-3 card me-3 mt-3">
    <h4 class="lead text-white">{{ subject.name }}</h4>

    <p class="text-dark">{{ subject.description }}</p>

    <div class="row px-2 gap-2">
      <button v-if="currentUser.isAdmin" class="col btn btn-danger"
        @click="() => { store.dispatch('deleteSubject', subject.id) }">
        <img src="@assets/remove.svg" alt="delete subject">
      </button>
    </div>

    <div class="accrdn rounded mt-2" :id="`subject${subjectKey}-chapters`">
      <div class="accrdn__item" v-for="(chapter, i) in subject.chapters" :key="i">
        <h2 class="accrdn__header">
          <button class="btn btn-dark text-muted fs-6 lead" data-bs-toggle="collapse" type="button"
            :data-bs-target="`#subject${subjectKey}-chapter${i}`" :id="`header-${i}`">
            {{ chapter.name }}
          </button>
        </h2>

        <div class="accrdn__body my-1" :data-bs-parent="`#subject${subjectKey}-chapter`">
          <div :id="`subject${subjectKey}-chapter${i}`" class="accordion-collapse collapse">
            {{ chapter.description }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
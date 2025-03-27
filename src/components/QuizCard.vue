<script setup>
const emit = defineEmits(['delete', 'update', 'start', 'view']);
const { quiz, admin } = defineProps(['quiz', 'admin']);
</script>

<template>
  <div class="card bg-dark mt-2 me-2" @click.prevent.stop="emit('view')">
    <div class="card-body d-flex flex-column">
      <h5 class="card-title text-white">{{ quiz.name }}</h5>
      <h6 class="card-subtitle mb-2 text-secondary">{{ quiz.chapter }}</h6>
      <hr />
      <p class="card-text text-white">{{ quiz.remarks }}</p>
      <div v-if="admin" class="gap-2 p-2 d-flex justify-content-center">
        <button v-show="admin" class="col btn btn-warning" @click.prevent.stop="() => emit('update', quiz)">
          <img src="@/assets/edit.svg" alt="edit quiz" />
        </button>
        <button v-show="admin" class="col btn btn-danger" @click.prevent.stop="() => emit('delete', quiz)">
          <img src="@/assets/remove.svg" alt="remove quiz" />
        </button>
      </div>
      <button v-else @click.prevent.stop="emit('start', quiz.quiz_id)" class="z-10 mt-3 btn btn-primary">
        Start Quiz
      </button>
    </div>
  </div>
</template>

<style scoped>
.card {
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.card:hover {
  transform: scale(1.02);
}
</style>
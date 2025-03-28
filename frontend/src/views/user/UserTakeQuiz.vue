<script setup>
import { computed, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex'

const store = useStore();
const router = useRouter();

const currentUser = computed(() => store.state.currentUser);
const quiz = computed(() =>
  store.state.quizzes.find(quiz =>
    quiz.quiz_id === store.state.activeQuiz));

const questionCount = ref(0);
const currentQuestion = ref(quiz.value.questions.at(0).id);
const selectedOption = ref(-1);
const questions = computed(() => quiz.value.questions);

const timer = ref(setTimeout(() => {
  alert('Time is up!');
  onSubmit();
}, (quiz.value.hh * 3600 + quiz.value.mm * 60) * 1000));

const hours = ref(quiz.value.hh);
const minutes = ref(quiz.value.mm);
const seconds = ref(0);

setInterval(() => {
  if (hours.value > 0 && minutes.value === 0) {
    --hours.value;
    minutes.value = 59;
  } else if (minutes.value > 0 && seconds.value === 0) {
    --minutes.value;
    seconds.value = 59;
  } else {
    --seconds.value;
  }
}, 1000);

const selected = reactive({});

function onNext() {
  if (selectedOption.value !== -1) {
    ++questionCount.value;
    selected[currentQuestion.value] = selectedOption.value;
    if (questionCount.value < questions.value.length)
      currentQuestion.value = questions.value[questionCount.value].id;
    else currentQuestion.value = -1;
    selectedOption.value = -1;
  }
}

async function onSubmit() {
  try {
    if (timer.value != null)
      clearTimeout(timer.value);

    store.dispatch('submitQuiz', {
      selected,
    }).then(() => router.push('/user'));
  } catch (error) {
    console.error('[ERROR] submitting answers:', error);
  } finally {
    selectedOption.value = -1;
  }
}
</script>

<template>
  <div v-if="quiz && currentUser" class="container-md">
    <p class="lead">{{ hours }}:{{ minutes }}:{{ seconds }}</p>
    <p class="lead bg-dark rounded d-inline p-2" v-if="questionCount < questions.length">{{ questionCount +
      1 }}/{{ questions.length }}</p>
    <h1 class="display-2 text-center">{{ quiz.name }}</h1>
    <div class="quiz">
      <div class="question" v-for="question in questions" :key="question.id" v-show="currentQuestion === question.id">
        <p class="question__statement lead fs-4">{{ question.statement }}</p>
        <div class="question__options">
          <div class="question__option" v-for="option in question.options" :key="option.id">
            <input class="question__optioninput btn-check" :checked="option.id === selectedOption"
              :id="`question${question.id}-option${option.id}`" autocomplete="off" />
            <label class="question__optionlabel btn btn-outline-primary" @click.prevent="selectedOption = option.id"
              :for="`question${question.id}-option${option.id}`">
              {{ option.statement }}
            </label>
          </div>
          <button class="question__submit btn btn-success" @click.prevent="onNext">next</button>
        </div>
      </div>
      <button v-show="questionCount === questions.length" class="quiz__submit btn btn-success" style="grid-area:  2 / 2"
        @click="onSubmit">Submit</button>
    </div>
  </div>
</template>

<style scoped>
.quiz {
  display: grid;
  grid-template-columns: 10px 1fr 10px;
  grid-template-rows: 10px 1fr 10px;
}

.question {
  grid-area: 2 / 2;

  .question__options {
    display: grid;
    grid-template-rows: repeat(4, 1fr);
    gap: 10px;

    .question__option {
      .question__optioninput[checked]~.question__optionlabel {
        background-color: var(--bs-primary);
      }

      .question__optionlabel {
        width: 100%;
        color: var(--bs-primary-text);
      }
    }
  }
}
</style>
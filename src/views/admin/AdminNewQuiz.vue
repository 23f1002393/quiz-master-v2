<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

const store = useStore();
const router = useRouter();
const subjects = computed(() => store.state.subjects);
const currentUser = computed(() => store.state.currentUser);

const subject = ref(null);
const chapter = ref(null);
const name = ref(null);
const remarks = ref(null);
const date = ref(new Date().toISOString().split('T')[0]);
const hours = ref(0);
const minutes = ref(0);
const questions = ref([]);

async function onSubmit() {
  try {
    if (questions.value.length === 0) {
      alert('Please add at least one question');
      return;
    }

    store.dispatch('createQuiz', {
      name: name.value,
      remarks: remarks.value,
      date_of_quiz: new Date(date.value).toISOString().split('T')[0],
      subject: subject.value.id,
      chapter: chapter.value.id,
      hh: hours.value,
      mm: minutes.value,
      questions: questions.value,
    });

    questions.value = [];
    name.value = '';
    remarks.value = '';
    date.value = new Date().toISOString().split('T')[0];
    hours.value = 0;
    minutes.value = 0;
    subject.value = null;
    chapter.value = null;

    await store.dispatch('fetchQuizzes');
    router.replace('/admin/quiz');
  } catch (error) {
    console.error('[ERROR] Failed to submit quiz:', error)
  }
};

function addQuestion() {
  const options = [];

  for (let i = 0; i < 4; ++i)
    options.push({ statement: '' });

  questions.value.push({
    statement: '',
    options: options,
    answer: 0,
  });
}

function removeQuestion(index) {
  questions.value.splice(index, 1);
}
</script>

<template>
  <div class="vw-25" v-if="currentUser">
    <h4 class="display-4 text-center">Add New Quiz</h4>
    <!-- New Quiz Form -->
    <form @submit.prevent.stop="onSubmit" class="container-md">
      <div class="form-floating my-2">
        <input type="text" v-model="name" id="name" class="form-control" autocomplete="off" required />
        <label for="name">Title</label>
      </div>

      <div class="form-floating my-2">
        <textarea style="min-height: 150px;" type="text" v-model="remarks" id="remarks" class="form-control"
          autocomplete="off" required></textarea>
        <label for="remarks">Description</label>
      </div>

      <select v-model="subject" id="subject" class="form-select" required>
        <option value="" disabled selected>Select Subject</option>
        <option v-for="(sub, key) in subjects" :key :value="sub">
          {{ sub.name }}
        </option>
      </select>

      <select v-if="subject" v-model="chapter" id="chapter" class="form-select mt-2" required>
        <option value="" disabled selected>Select Chapter</option>
        <option v-for="(chap, key) in subject.chapters" :key :value="chap">
          {{ chap.name }}
        </option>
      </select>

      <div class="row">
        <span class="lead col text-center align-self-center">Duration</span>
        <div class="col form-floating my-2">
          <input type="number" v-model="hours" id="hours" class="form-control" autocomplete="off" />
          <label for="hours">hh</label>
        </div>

        <div class="col form-floating my-2">
          <input type="minutes" v-model="minutes" id="minutes" class="form-control" autocomplete="off" />
          <label for="duration">mm</label>
        </div>
      </div>

      <div class="form-floating my-2">
        <input type="text" v-model="date" :type="getType('date_of_quiz')" id="date_of_quiz" class="form-control"
          autocomplete="off" />
        <label for="date_of_quiz">Date of Quiz</label>
      </div>

      <div class="bg-secondary p-4 rounded mt-3">
        <p class="text-start">Questions:</p>
        <ul class="d-flex flex-column align-items-center">
          <li v-for="(ques, key) in questions" :key class="d-flex flex-column w-100">
            <div>
              <div class="form-floating my-2">
                <textarea v-model="ques.statement" :id="`question-${key}-statement`" class="form-control"
                  autocomplete="off" />
                <label :for="`question-${key}-statement`">Question {{ key + 1 }} Statement</label>
              </div>

              <ul>
                <li v-for="(opt, j) in ques.options" :key="j" class="form-floating mt-2">
                  <textarea rows="5" cols="30" v-model="opt.statement" :id="`opt-${key}-${j}`" class="form-control"
                    autocomplete="off" />
                  <label :for="`opt-${key}-${j}`">{{ j + 1 }}.</label>
                </li>
              </ul>

              <div class="row mt-2">
                <label class="col align-self-center" for="answer">Answer [1-4]</label>
                <select v-model="ques.answer" :id="`question-${key}-answer`" class="col form-select" required>
                  <option v-for="(_, key) in ques.options" :key :value="key">
                    {{ key + 1 }}
                  </option>
                </select>
              </div>
            </div>

            <button @click.prevent="() => removeQuestion(key)"
              class="btn btn-danger align-self-center fs-5 my-2">-</button>
          </li>
          <button @click.prevent="addQuestion" class="btn btn-primary align-self-center mt-2 fs-5">+</button>
        </ul>

        <input type="submit" class="btn btn-success w-100 mt-2" value="add quiz" />
      </div>
    </form>
  </div>
</template>

<style scoped>
.btn-danger,
.btn-primary {
  width: 10rem;
}
</style>
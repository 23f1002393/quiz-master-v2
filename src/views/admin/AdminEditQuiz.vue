<script setup>
import { reactive } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

const store = useStore();
const router = useRouter();

const index = computed(() => router.params.id);
const subject = reactive(store.state.subjects[index.value]);

const addChapter = () => {
  subject.chapters.push({
    name: '',
    description: '',
  })
};
const removeChapter = (index) => subject.chapters.splice(index, 1);
function onSubmit() {
  store
    .dispatch('addSubject', subject)
    .then(() => router.push('/admin'));
}
</script>

<template>
  <div class="mx-5 px-5" v-if="currentUser">
    <h4 class="display-4 text-center">Add New Subject</h4>
    <form @submit.prevent.stop="onSubmit" class="container-md">
      <div v-for="(attr, key) in Object.keys(subject)" class="form-floating text-start my-2" :key>
        <textarea rows="10" cols="30" v-model="subject[attr]" v-if="attr === 'description'" :id="attr"
          class="form-control" autocomplete="off"></textarea>
        <input v-else v-model="subject[attr]" type="text" :id="attr" class="form-control" autocomplete="off" />
        <label :for="attr">{{ attr }}</label>
      </div>
      <ul class="rounded bg-dark p-3">
        <p class="text-start">Chapters:</p>
        <li v-for="(chapter, i) in subject.chapters" :key="i" class="col-md">
          <div class="form-floating my-2 row-sm" v-for="attr in Object.keys(chapter)" :key="attr">
            <textarea v-if="attr === 'description'" v-model="chapter[attr]" :id="`chapter-${i}-${attr}`"
              class="form-control" autocomplete="off"></textarea>
            <input v-else v-model="chapter[attr]" type="text" :id="`chapter-${i}-${attr}`" class="form-control"
              autocomplete="off" />
            <label :for="`chapter-${i}-name`">Chapter {{ i + 1 }} {{ attr }}</label>
          </div>
          <button @click.prevent.stop="() => removeChapter(i)" class="btn btn-danger fs-5 my-2 w-100">-</button>
        </li>
        <button @click.prevent.stop="addChapter" class="btn btn-primary fs-5 w-100">+</button>
      </ul>
      <input type="submit" class="btn btn-success w-100 mt-2" value="add subject" />
    </form>
  </div>
</template>
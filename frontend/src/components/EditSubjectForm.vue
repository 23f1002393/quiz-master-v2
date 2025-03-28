<script setup>
import { computed, ref } from 'vue';
import { useStore } from 'vuex';

const store = useStore()
const currentUser = computed(() => store.state.currentUser)

const emit = defineEmits(['refresh'])
const { name, description, chapters } = defineProps(['name', 'description', 'chapters'])

const subject = ref({
  name,
  description,
  chapters
})

const addChapter = () => {
  subject.value.chapters.push({
    name: '',
    description: '',
  })
}

const removeChapter = (index) => {
  subject.value.chapters.splice(index, 1)
}

const submit = async () => {
  if (currentUser.value == null) return

  store.dispatch('updateSubject', subject.value)
    .then(() => subject.value = {
      name: '',
      description: '',
      chapters: [],
    })
    .then(() => emit('refresh'))
    .catch(error => console.error('[ERROR]', error));
}
</script>

<template>
  <div class="modal fade" id="newSubjectModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title lead">Edit subject</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>

        <div class="modal-body">
          <form>
            <div v-for="attr in Object.keys(subject)" class="form-floating text-start my-2" :key="attr">

              <textarea rows="10" cols="30" v-model="subject[attr]" v-if="attr === 'description'" :id="attr"
                class="form-control" />

              <input v-else v-model="subject[attr]" type="text" :id="attr" class="form-control" />

              <label :for="attr">{{ attr }}</label>
            </div>

            <p class="text-start">Chapters:</p>

            <button @click.prevent.stop="addChapter" class="btn btn-secondary fs-5">+</button>

            <ul>
              <li v-for="(chapter, i) in subject.chapters" :key="i" class="d-flex flex-column">
                <div>
                  <div class="form-floating my-2" v-for="attr in Object.keys(chapter)" :key="attr">
                    <textarea v-if="attr === 'description'" v-model="chapter[attr]" :id="`chapter-${i}-${attr}`"
                      class="form-control" />

                    <input v-else v-model="chapter[attr]" type="text" :id="`chapter-${i}-${attr}`"
                      class="form-control" />

                    <label :for="`chapter-${i}-name`">Chapter {{ i + 1 }} {{ attr }}</label>
                  </div>
                </div>

                <button @click.prevent.stop="() => removeChapter(i)" class="btn btn-secondary fs-5 my-2">-</button>
              </li>
            </ul>
          </form>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">close</button>

          <button type="button" class="btn btn-primary" @click.prevent.stop="submit">add subject</button>
        </div>
      </div>
    </div>
  </div>
</template>
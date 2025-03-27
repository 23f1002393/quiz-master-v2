<script setup>
import { ref } from 'vue';
import { store } from '@/store';
import { useRouter } from 'vue-router';

const router = useRouter();

const user = ref({
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  qualification: '',
  dob: new Date().toISOString().split('T')[0],
});

const qualifications = [
  'Matriculation',
  'Senior Secondary',
  'Graduation',
  'Post Graduation',
  'PhD'
];

const getType = (attr) => {
  if (attr === 'password') return 'password'
  if (attr === 'dob') return 'date'
  return 'text'
};

async function onSubmit() {
  try {
    const { first_name, last_name } = user.value

    store.dispatch('registerUser', {
      name: `${first_name} ${last_name}`,
      ...user.value
    });
    user.value = {
      email: '',
      password: '',
      last_name: '',
      first_name: '',
      qualification: '',
      dob: new Date().toISOString().split('T')[0]
    };
    router.push('/login');
  } catch (error) {
    console.error('[ERROR]', error);
  }
}
const toLabel = (attr) => {
  return attr
    .split('_')
    .map((str) => `${str[0].toUpperCase()}${str.slice(1)}`)
    .join(' ');
};
</script>

<template>
  <form>
    <h1 class="display-5 text-center">Register</h1>
    <div v-for="attr in Object.keys(user)" :key="attr">
      <div class="form-floating mt-2" v-if="attr !== 'qualification'">
        <input class="form-control" v-model="user[attr]" :type="getType(attr)" :id="attr" required />
        <label :for="attr">{{ toLabel(attr) }}</label>
      </div>
      <div v-else>
        <select class="form-select mt-2" v-model="user[attr]" :id="attr" required>
          <option value="" disabled selected>Select your qualification</option>
          <option v-for="(qualification, i) in qualifications" :value="qualification" :key="i">{{ qualification }}
          </option>
        </select>
      </div>
    </div>
    <button @click.stop.prevent="onSubmit" class="btn btn-primary mt-3" type="submit">
      Register
    </button>
  </form>
</template>

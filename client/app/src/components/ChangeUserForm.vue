<script setup>
import { ref, reactive, watch, inject } from 'vue'
import axios from 'axios'

var API_host = import.meta.env.VITE_API_ENDPOINT

const access_token = inject('access_token')
const change_user = inject('change_user')
const getAllUsersList = inject('getAllUsersList')

const dirtyFlag = reactive({
  name: true
})

const validationError = reactive({
  name: '',
  form: false
})

const responseError = ref('')

const validationForm = () => {
  if (validationError.name || change_user.name < 3) {
    validationError.form = true
  } else {
    validationError.form = false
  }
}

const validationName = () => {
  if (change_user.name.length < 3 && dirtyFlag.name) {
    validationError.name = 'Некорректное имя. Минимальная длина имени — 3 символа'
  } else {
    validationError.name = ''
  }
}

const patchUser = async () => {
  event.preventDefault()
  console.log('Изменяю пользователя', change_user.id)
  try {
    const { data } = await axios({
      method: 'patch',
      url: `http://` + API_host + `/auth/change_user_by_id/${change_user.id}`,
      data: {
        name: change_user.name,
        role: change_user.role
      },
      headers: { Authorization: localStorage.access_token }
    })
    await getAllUsersList()
    return data
  } catch (err) {
    console.log(err)
  }
}

watch([() => dirtyFlag.name, () => change_user.name], validationName)

watch([() => dirtyFlag.name, () => change_user.name], validationForm)
</script>

<template>
  <form action="" class="registration_form">
    <h1>Редактирование пользователя {{ change_user.id }}</h1>
    <div class="input_box">
      <label class="label_name">ФИО</label>
      <input
        class="text_input"
        type="text"
        v-model="change_user.name"
        @blur="() => (dirtyFlag.name = true)"
      />
      <div class="error_box">{{ validationError.name }}</div>
    </div>

    <div class="input_box">
      <label class="label_name label_role">Права доступа</label>
      <div>
        <input
          class="radio_input"
          type="radio"
          id="staff"
          value="staff"
          v-model="change_user.role"
        />
        <label class="role_type" for="staff">Сотрудник</label>
      </div>
      <div>
        <input
          class="radio_input"
          type="radio"
          id="admin"
          value="admin"
          v-model="change_user.role"
        />
        <label class="role_type" for="admin">Администратор</label>
      </div>
      <div class="error_box">{{ responseError }}</div>
    </div>
    <button @click="patchUser" :disabled="validationError.form">Изменить</button>
  </form>
</template>

<style scoped>
.registration_form {
  margin-top: 20px;
  margin-left: 100px;
  display: flex;
  flex-direction: column;
  width: 520px;
  align-content: center;
  justify-content: center;
  align-items: center;
  padding: 10px;
}

.input_box {
  margin-bottom: 10px;
  width: 100%;
}

.input_box:nth-child(5) {
  margin-bottom: 30px;
}

.label_name {
  display: block;
  color: aliceblue;
}

.text_input {
  border: 2px solid black;
  border-radius: 5px;
  padding: 4px 10px;
  width: 100%;
}

.label_role {
  margin-bottom: 10px;
}

.role_type {
  color: aliceblue;
  padding-left: 5px;
}

h1 {
  font-size: 25px;
  margin-bottom: 20px;
  color: aliceblue;
}

.text_input:hover {
  border: 2px solid #009485;
}

input:focus {
  outline: #009485;
  border-color: #009485;
}

input[type='radio'] {
  accent-color: #009485;
}

button {
  border-radius: 8px;
  background: #009485;
  padding: 15px;
  font-size: 17px;
  transition: 0.2s;
  color: white;
}

button:hover {
  background: #04786c;
  transition: 0.2s;
  transition: 0.2s;
}
button:disabled {
  background: #5f6464;
  transition: 0.2s;
  transition: 0.2s;
}

.error_box {
  height: 20px;
  color: rgb(255, 115, 115);
  font-size: 15px;
}

.error_box:nth-child(4) {
  text-align: center;
}
</style>

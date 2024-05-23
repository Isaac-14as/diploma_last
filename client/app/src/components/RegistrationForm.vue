<script setup>
import { ref, reactive, watch, inject } from 'vue'
import axios from 'axios'

var API_host = import.meta.env.VITE_API_ENDPOINT

const getAllUsersList = inject('getAllUsersList')

const user = reactive({
  name: '',
  email: '',
  password: '',
  role: 'staff'
})

const dirtyFlag = reactive({
  name: false,
  email: false,
  password: false
})

const validationError = reactive({
  name: '',
  email: '',
  password: '',
  form: true
})

const responseError = ref('')

const validationForm = () => {
  if (
    validationError.name ||
    validationError.email ||
    validationError.password ||
    user.name < 3 ||
    !user.email ||
    user.password < 8
  ) {
    validationError.form = true
  } else {
    validationError.form = false
  }
}

const validationName = () => {
  if (user.name.length < 3 && dirtyFlag.name) {
    validationError.name = 'Некорректное имя. Минимальная длина имени — 3 символа'
  } else {
    validationError.name = ''
  }
}

const validationEmail = () => {
  const re = /^\S+@\S+\.\S+$/
  if (!re.test(String(user.email).toLocaleLowerCase()) && dirtyFlag.email) {
    validationError.email = 'Некорректный email'
  } else {
    validationError.email = ''
  }
}

const validationPassword = () => {
  if (user.password.length < 8 && dirtyFlag.password) {
    validationError.password = 'Некорректный пароль. Минимальная длина пароля — 8 символов'
  } else {
    validationError.password = ''
  }
}

watch([() => dirtyFlag.name, () => user.name], validationName)
watch([() => dirtyFlag.email, () => user.email], validationEmail)
watch([() => dirtyFlag.password, () => user.password], validationPassword)

watch([() => dirtyFlag.name, () => user.name], validationForm)
watch([() => dirtyFlag.email, () => user.email], validationForm)
watch([() => dirtyFlag.password, () => user.password], validationForm)

const createUser = async () => {
  // убирает перезагрузку страницы
  event.preventDefault()

  try {
    const { data } = await axios.post(`http://` + API_host + `/auth/register`, {
      name: user.name,
      email: user.email,
      password: user.password,
      role: user.role
    })
    await getAllUsersList()
    responseError.value = 'Пользователь успешно создан.'
    return data
  } catch (err) {
    console.log(err)
    responseError.value = err.response.data['detail']
  }
}
</script>

<template>
  <form action="" class="registration_form">
    <h1>Регистрация пользователя</h1>
    <div class="input_box">
      <label class="label_name">ФИО</label>
      <input
        class="text_input"
        type="text"
        v-model="user.name"
        @blur="() => (dirtyFlag.name = true)"
      />
      <div class="error_box">{{ validationError.name }}</div>
    </div>

    <div class="input_box">
      <label class="label_name">Email</label>
      <input
        class="text_input"
        type="email"
        v-model="user.email"
        @blur="() => (dirtyFlag.email = true)"
      />
      <div class="error_box">{{ validationError.email }}</div>
    </div>

    <div class="input_box">
      <label class="label_name">Пароль</label>
      <input
        class="text_input"
        type="password"
        v-model="user.password"
        @blur="() => (dirtyFlag.password = true)"
      />
      <div class="error_box">{{ validationError.password }}</div>
    </div>
    <div class="input_box">
      <label class="label_name label_role">Права доступа</label>
      <div>
        <input class="radio_input" type="radio" id="staff" value="staff" v-model="user.role" />
        <label class="role_type" for="staff">Сотрудник</label>
      </div>
      <div>
        <input class="radio_input" type="radio" id="admin" value="admin" v-model="user.role" />
        <label class="role_type" for="admin">Администратор</label>
      </div>
      <div class="error_box">{{ responseError }}</div>
    </div>
    <button @click="createUser()" :disabled="validationError.form">
      Зарегистрировать пользователя
    </button>
  </form>
</template>

<style scoped>
.label_name {
  display: block;
  color: aliceblue;
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
.text_input {
  border: 2px solid black;
  border-radius: 5px;
  padding: 4px 10px;
  width: 100%;
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

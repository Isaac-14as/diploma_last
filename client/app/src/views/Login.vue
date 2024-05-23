<script setup>
import { ref, reactive, watch, inject } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

var API_port = import.meta.env.VITE_API_ENDPOINT

const loginError = ref('')

const registrationCheck = inject('registrationCheck')

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

const validationForm = () => {
  if (
    validationError.name ||
    validationError.email ||
    validationError.password ||
    !user.email ||
    user.password < 5
  ) {
    validationError.form = true
  } else {
    validationError.form = false
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
  if (user.password.length < 5 && dirtyFlag.password) {
    validationError.password = 'Некорректный пароль. Минимальная длина пароля — 5 символов'
  } else {
    validationError.password = ''
  }
}

watch([() => dirtyFlag.email, () => user.email], validationEmail)
watch([() => dirtyFlag.password, () => user.password], validationPassword)
watch([() => dirtyFlag.email, () => user.email], validationForm)
watch([() => dirtyFlag.password, () => user.password], validationForm)

const login = async () => {
  event.preventDefault()
  try {
    const { data } = await axios.post(`http://` + API_port + `/auth/login`, {
      email: user.email,
      password: user.password
    })
    localStorage.access_token = data['access_token']
    await registrationCheck()
    router.push('/mnemo')
    return data
  } catch (err) {
    console.log(err)
    loginError.value = 'Неверный email или пароль'
  }
}
</script>

<template>
  <form action="" class="registration_form">
    <h1>Вход</h1>

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
    <div class="login_error_box">{{ loginError }}</div>
    <button @click="login" :disabled="validationError.form" type="button">Войти</button>
  </form>
</template>

<style scoped>
.label_name {
  display: block;
}
.label_role {
  margin-bottom: 10px;
}
h1 {
  font-size: 25px;
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

.error_box {
  height: 20px;
  color: rgb(255, 115, 115);
  font-size: 15px;
}

.login_error_box {
  height: 20px;
  color: rgb(255, 115, 115);
  font-size: 15px;
  margin-bottom: 10px;
}

form {
  margin: 0 auto;
  margin-top: 200px;
  display: flex;
  flex-direction: column;
  width: 25%;
  align-items: center;
  color: white;
}
</style>

<script setup>
import axios from 'axios'
import { ref, reactive, provide } from 'vue'
import UsersList from '../components/UsersList.vue'
import RegistrationForm from '../components/RegistrationForm.vue'
import ChangeUserForm from '../components/ChangeUserForm.vue'

var API_host = import.meta.env.VITE_API_ENDPOINT

const change_user = reactive({
  id: NaN,
  name: '',
  role: ''
})
const page_flag = ref(true)
const all_users = ref([])
const users = ref([])

const getAllUsersList = async () => {
  try {
    const { data } = await axios.get(`http://` + API_host + `/auth/get_all_users`, {
      headers: { Authorization: localStorage.access_token }
    })
    all_users.value = data
    users.value = data
  } catch (err) {
    console.log(err)
  }
}

provide('getAllUsersList', getAllUsersList)
provide('change_user', change_user)
provide('page_flag', page_flag)
provide('all_users', all_users)
provide('users', users)

const change_page = () => {
  page_flag.value = true
}
</script>

<template>
  <div class="main_box">
    <UsersList />
    <div class="right_box">
      <div class="flag" @click="change_page">Добавить</div>
      <div v-if="page_flag">
        <RegistrationForm />
      </div>
      <div v-else>
        <ChangeUserForm />
      </div>
    </div>
  </div>
</template>

<style scoped>
.main_box {
  display: flex;
}
.flag {
  border-radius: 8px;
  background: #009485;
  transition: 0.2s;
  color: white;
  width: 100px;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  position: absolute;
  right: 20px;
}

.flag:hover {
  background: #04786c;
  transition: 0.2s;
}
</style>

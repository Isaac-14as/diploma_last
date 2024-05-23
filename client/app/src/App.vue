<script setup>
import { ref, onMounted, provide, onUnmounted } from 'vue'
import { RouterView, useRouter } from 'vue-router'
import axios from 'axios'

import Header from './components/Header.vue'
import Sidebar from './components/Sidebar.vue'

var API_host = import.meta.env.VITE_API_ENDPOINT
const router = useRouter()
const sidebar_flag = ref(false)
const current_user = ref(NaN)
const access_token = ref(NaN)

// проверка того есть ли токен доступа к апи + редирект
const registrationCheck = async () => {
  console.log('Сработала проверка!')
  if (localStorage.access_token) {
    try {
      const { data } = await axios({
        method: 'get',
        url: `http://` + API_host + `/auth/get_me`,
        headers: { Authorization: localStorage.access_token }
      })
      current_user.value = data
      access_token.value = localStorage.access_token
      if (
        window.location.toString().split('/').length === 4 &&
        window.location.toString().split('/')[3] === ''
      ) {
        router.push('/mnemo')
      }
    } catch (err) {
      current_user.value = NaN
      access_token.value = NaN
      localStorage.removeItem('access_token')
      console.log(err)
    }
  } else {
    router.push('/')
    console.log('нет токена!')
  }
}

onMounted(() => registrationCheck())
provide('access_token', access_token)
provide('current_user', current_user)
provide('registrationCheck', registrationCheck)
provide('sidebar_flag', sidebar_flag)

const intervalId = [null]
const getWithiInterval = (interval) => {
  registrationCheck()
  intervalId[0] = setInterval(() => registrationCheck(), interval * 1000)
}
onMounted(() => getWithiInterval(20))
onUnmounted(() => {
  clearInterval(intervalId[0])
})
</script>

<template>
  <Header v-if="access_token" />
  <Sidebar v-if="sidebar_flag" />
  <!-- <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink> -->
  <RouterView />
</template>

<style scoped></style>

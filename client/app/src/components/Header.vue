<script setup>
import { inject } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

var API_host = import.meta.env.VITE_API_ENDPOINT
const current_user = inject('current_user')
const access_token = inject('access_token')
const registrationCheck = inject('registrationCheck')
const sidebar_flag = inject('sidebar_flag')
const router = useRouter()

const logout = async () => {
  try {
    await axios.post(`http://` + API_host + `/auth/logout`)
    localStorage.removeItem('access_token')
    current_user.value = NaN
    access_token.value = NaN
    await registrationCheck()
    router.push('/')
  } catch (err) {
    console.log(err)
  }
}

const sidebarChange = () => {
  sidebar_flag.value = !sidebar_flag.value
}
</script>

<template>
  <header>
    <div class="content_box">
      <div class="left_nav_menu">
        <img src="/icons8-menu.svg" alt="" class="sidebar" @click="sidebarChange" />
        <router-link class="link_router" to="/mnemo">Мнемосхема</router-link>
        <router-link class="link_router" v-if="current_user.role === 'admin'" to="/user_admin">
          Управление пользователями
        </router-link>
      </div>
      <div class="user_menu">
        <div class="name">{{ current_user.name }}</div>
        <div class="symbol">|</div>
        <div class="exit" @click="logout"><b>Выйти</b></div>
      </div>
    </div>
  </header>
</template>

<style scoped>
header {
  background-color: #009485;
  height: 70px;
  display: flex;
  justify-content: center;
  font-size: 20px;
}
.content_box {
  display: flex;
  justify-content: space-between;
  height: 100%;
  width: 95%;
  align-items: center;
}
.left_nav_menu {
  display: flex;
  align-items: center;
  width: 30%;
  justify-content: space-between;
}

.user_menu {
  display: flex;
  align-items: center;
  width: 20%;
}
.symbol {
  margin: 0px 10px;
}

.link_router,
.exit {
  cursor: pointer;
  transition: 0.2s;
}

.link_router:hover,
.exit:hover {
  color: white;
  transition: 0.2s;
}
</style>

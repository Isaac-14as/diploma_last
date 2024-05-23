<script setup>
import { inject } from 'vue'

const sidebar_flag = inject('sidebar_flag')

const sidebarChange = () => {
  sidebar_flag.value = !sidebar_flag.value
}
</script>

<template>
  <div class="sidebar">
    <router-link to="/devices" class="sidebar_box" @click="sidebarChange">
      <img src="/devices.png" alt="" class="icon" />
      <div class="sidebar_link">Устройства</div>
    </router-link>
    <router-link to="/graph" class="sidebar_box" @click="sidebarChange">
      <img src="/graph.png" alt="" class="icon" />
      <div class="sidebar_link">Аналитика</div>
    </router-link>
    <router-link to="/management_log" class="sidebar_box" @click="sidebarChange">
      <img src="/control.png" alt="" class="icon" />
      <div class="sidebar_link">Журнал управления</div>
    </router-link>
    <router-link to="/accident_log" class="sidebar_box" @click="sidebarChange">
      <img src="/accident.png" alt="" class="icon" />
      <div class="sidebar_link">Аварийные ситуации</div>
    </router-link>
  </div>
</template>

<style scoped>
.sidebar {
  position: absolute;
  background: #1c1c1c;
  width: 300px;
  display: flex;
  flex-direction: column;
  z-index: 200;
}
.sidebar_link {
  color: aliceblue;
  font-size: 20px;
  align-content: center;
}

.sidebar_box {
  display: flex;
  align-content: center;
  padding-left: 40px;
  padding-bottom: 10px;
  padding-top: 20px;
  border-bottom: 1px solid black;
}
.sidebar_box:hover {
  background: #009485;
}

.icon {
  margin-right: 10px;
}
</style>

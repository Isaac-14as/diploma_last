<script setup>
import axios from 'axios'
import { inject, ref, onMounted } from 'vue'

var API_host = import.meta.env.VITE_API_ENDPOINT

const access_token = inject('access_token')
const change_user = inject('change_user')
const page_flag = inject('page_flag')

const all_users = inject('all_users')
const users = inject('users')

const getAllUsersList = inject('getAllUsersList')

const changePage = () => {
  page_flag.value = false
}

const deleteUser = async (id) => {
  if (confirm('Вы дествительно хотите удалить пользователя?')) {
    try {
      const { data } = await axios.delete(`http://` + API_host + `/auth/delete_user_by_id/${id}`, {
        headers: { Authorization: localStorage.access_token }
      })
      await getAllUsersList()
      return data
    } catch (err) {
      console.log(err)
    }
  }
}

const search_text = ref('')

const onChangeSearchInput = async () => {
  let user_search = []

  if (search_text.value === '') {
    users.value = all_users.value
  }
  for (let i = 0; i < all_users.value.length; i++) {
    let id_search = all_users.value[i].id.toString().indexOf(search_text.value) != -1
    let name_search =
      all_users.value[i].name.toLowerCase().indexOf(search_text.value.toLowerCase()) != -1
    let email_search =
      all_users.value[i].email.toLowerCase().indexOf(search_text.value.toLowerCase()) != -1
    let role_search =
      all_users.value[i].role.toLowerCase().indexOf(search_text.value.toLowerCase()) != -1
    let role_ru =
      (all_users.value[i].role == 'staff' &&
        'сотрудник'.indexOf(search_text.value.toLowerCase()) != -1) ||
      (all_users.value[i].role == 'admin' &&
        'администратор'.indexOf(search_text.value.toLowerCase()) != -1)
    if (name_search || email_search || role_search || id_search || role_ru) {
      user_search.push(all_users.value[i])
    }
  }
  console.log(user_search)
  users.value = user_search
}

const changeUser = async (id, name, role) => {
  change_user.id = id
  change_user.name = name
  change_user.role = role
}

onMounted(() => getAllUsersList())
</script>

<template>
  <div class="users_list_main">
    <div class="title_search">
      <div class="title">Список пользователей</div>
      <input class="search" type="text" @input="onChangeSearchInput" v-model="search_text" />
    </div>
    <div class="users_list">
      <div class="user_box" v-for="user_i in users" :key="user_i.id">
        <div class="info_user">
          <div class="user_id">{{ user_i.id }}</div>
          <div class="user_name">{{ user_i.name }}</div>
          <div class="user_email">{{ user_i.email }}</div>
          <div class="user_role" v-if="user_i.role == 'admin'">администратор</div>
          <div class="user_role" v-if="user_i.role == 'staff'">сотрудник</div>
        </div>
        <div @click="deleteUser(user_i.id)" class="delete">Удалить</div>
        <div @click="[changeUser(user_i.id, user_i.name, user_i.role), changePage()]" class="patch">
          Изменить
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.title_search {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}
.title {
  padding-left: 20px;
  margin-bottom: 10px;
  font-size: 20px;
}

.search {
  width: 350px;
  border: 2px solid black;
  border-radius: 5px;
  padding: 4px 10px;
}

.search:hover {
  border: 2px solid #009485;
}

.search:focus {
  outline: #009485;
  border-color: #009485;
}

.users_list_main {
  width: 54%;
  margin-left: 25px;
  color: white;
  margin-top: 30px;
}

.users_list {
  overflow: scroll;
  overflow-x: hidden;
  height: 750px;
}

.user_box {
  display: flex;
  height: 30px;
  border: 1px solid white;
  border-radius: 5px;
  align-items: center;
  margin-bottom: 5px;
  width: 98%;
}
.info_user {
  display: flex;
}

.user_id {
  padding-left: 5px;
  width: 60px;
  border-right: 1px solid white;
}
.user_name {
  width: 320px;
  padding-left: 10px;
  border-right: 1px solid white;
}
.user_email {
  width: 250px;
  padding-left: 10px;
  border-right: 1px solid white;
}
.user_role {
  width: 150px;
  padding-left: 10px;
}

.delete {
  width: 70px;
  display: flex;
  justify-content: center;
  cursor: pointer;
  transition: 0.1s;
  border-left: 1px solid white;
  padding-left: 10px;
}

.patch {
  width: 80px;
  display: flex;
  justify-content: center;
  cursor: pointer;
  transition: 0.1s;
  padding-left: 20px;
}

.delete:hover,
.patch:hover {
  color: #009485;
  transition: 0.1s;
}

/* Define the scrollbar style */
.users_list::-webkit-scrollbar {
  width: 3px;
  height: 15px;
}

/* Define the thumb style */
.users_list::-webkit-scrollbar-thumb {
  background: #009485;
  border-radius: 1px;
}

/* Define the track style */
.users_list::-webkit-scrollbar-track:vertical {
  background-color: rgb(69, 67, 67);
  box-shadow: inset 0 0 2px 2px rgb(87, 86, 86);
}
</style>

<script setup>
import axios from 'axios'
import { inject, ref, onMounted } from 'vue'

import { useRouter } from 'vue-router'

const router = useRouter()

const routerPush = async (id) => {
  if (access_token.value) {
    router.push('/device_value/' + id.toString())
  }
}

var API_host = import.meta.env.VITE_API_ENDPOINT

const access_token = inject('access_token')
const current_user = inject('current_user')

const devices = ref([])
const devices_all = ref([])

const getAllDevices = async () => {
  try {
    const { data } = await axios.get(`http://` + API_host + `/device/get_all_devices`, {
      headers: { Authorization: localStorage.access_token }
    })
    devices.value = data.sort((a, b) => a.id - b.id)
    devices_all.value = data.sort((a, b) => a.id - b.id)
    return data
  } catch (err) {
    console.log(err)
  }
}

const deviceSwitch = async (id) => {
  try {
    const { data } = await axios({
      method: 'patch',
      url: `http://` + API_host + `/device/device_switch/${id}`,
      headers: { Authorization: localStorage.access_token }
    })
    // изменение одного из иустройст на стороне клиента
    let device_change = devices.value.find((item) => item.id === id)
    device_change.is_active = !device_change.is_active
    devices.value[devices.value.indexOf(devices.value.find((item) => item.id === id))] =
      device_change
    modelInfoOn()
    return data
  } catch (err) {
    console.log(err)
  }
}

const addManagementLog = async (device_id, action_text) => {
  try {
    const { data } = await axios({
      method: 'post',
      url: `http://` + API_host + `/device/add_management_log`,
      headers: { Authorization: localStorage.access_token },
      data: {
        info: info_test.value,
        action: action_text,
        user_id: current_user.value.id,
        device_id: device_id
      }
    })
    return data
  } catch (err) {
    console.log(err)
  }
}

const search_text = ref('')

const onChangeSearchInput = async () => {
  const devices_search = []
  if (search_text.value === '') {
    devices.value = devices_all.value
  }
  for (let i = 0; i < devices_all.value.length; i++) {
    let id_search = devices_all.value[i].id.toString().indexOf(search_text.value) != -1
    let name_search =
      devices_all.value[i].name.toLowerCase().indexOf(search_text.value.toLowerCase()) != -1
    let type_search =
      devices_all.value[i].type.toLowerCase().indexOf(search_text.value.toLowerCase()) != -1
    let status_search =
      devices_all.value[i].status.toLowerCase().indexOf(search_text.value.toLowerCase()) != -1
    let is_active_search =
      (devices_all.value[i].is_active &&
        'включен'.indexOf(search_text.value.toLowerCase()) != -1) ||
      (!devices_all.value[i].is_active && 'выключен'.indexOf(search_text.value.toLowerCase()) != -1)
    if (id_search || name_search || type_search || status_search || is_active_search) {
      devices_search.push(devices_all.value[i])
    }
    devices.value = devices_search
  }
}

const info_test = ref('')
const device_action = ref('')
const model_flag = ref(false)
const modelInfo = async (device) => {
  device_action.value = device
  model_flag.value = !model_flag.value
}

const modelInfoOn = async () => {
  model_flag.value = !model_flag.value
  info_test.value = ''
}

onMounted(() => getAllDevices())
</script>

<template>
  <div class="list_main">
    <div class="title_search">
      <div class="title">Список устройст</div>
      <input class="search" type="text" @input="onChangeSearchInput" v-model="search_text" />
    </div>

    <div class="list_name">
      <div class="box">
        <div class="info">
          <div class="id">id</div>
          <div class="name">Название</div>
          <div class="type">Тип</div>
          <div class="status">Статус</div>
          <div class="is_active">Включено/выключено</div>
          <div class="option_1">Опции</div>
        </div>
      </div>
    </div>

    <div class="list">
      <div class="box" v-for="device_i in devices" :key="device_i.id">
        <div class="info">
          <div class="id">{{ device_i.id }}</div>
          <div class="name">{{ device_i.name }}</div>
          <div class="type">{{ device_i.type }}</div>
          <div class="status">{{ device_i.status }}</div>
          <div class="is_active" style="color: greenyellow" v-if="device_i.is_active">включен</div>
          <div class="is_active" style="color: red" v-else>выключен</div>
        </div>
        <div
          class="option option_2"
          v-if="device_i.type == 'трансформатор'"
          @click="routerPush(device_i.id)"
        >
          Показания
        </div>
        <div
          @click="modelInfo(device_i)"
          class="option option_3"
          v-if="device_i.type === 'разъединитель' && device_i.is_active"
        >
          Выключить
        </div>
        <div
          @click="modelInfo(device_i)"
          class="option option_4"
          v-if="device_i.type === 'разъединитель' && !device_i.is_active"
        >
          Включить
        </div>
      </div>
    </div>
    <div v-if="model_flag" class="blur"></div>
    <div v-if="model_flag" class="model_window">
      <div class="title_model">
        Причинана
        <p v-if="device_action.is_active">выключения</p>
        <p v-else>включения</p>
        <p>устройства</p>
        <p>"{{ device_action.name }}":</p>
      </div>
      <textarea
        class="test_info"
        placeholder="Опишите причину действия..."
        v-model="info_test"
      ></textarea>
      <div class="button_box">
        <button @click="modelInfoOn">Отмена</button>
        <button
          v-if="device_action.is_active"
          @click="
            [deviceSwitch(device_action.id), addManagementLog(device_action.id, 'Выключение')]
          "
        >
          Выключить
        </button>
        <button
          v-else
          @click="[deviceSwitch(device_action.id), addManagementLog(device_action.id, 'Включение')]"
        >
          Включить
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.btn_action {
  transition: 0.2s;
}
.btn_action:hover {
  color: white;
  transition: 0.2s;
}
.button_box {
  display: flex;
  justify-content: space-around;
  width: 100%;
  margin-top: 20px;
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
.model_window {
  position: absolute;
  left: 33%;
  top: 30%;
  width: 550px;
  height: 350px;
  background: #1c1c1c;
  border: #009485 solid 2px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.test_info {
  padding: 10px;
  width: 85%;
  height: 50%;
  border: 2px solid black;
  border-radius: 5px;
  margin-top: 10px;
}

.test_info:hover {
  border: 2px solid #009485;
}

.test_info:focus {
  outline: #009485;
  border-color: #009485;
}

.title_model {
  color: white;
  background: #009485;
  text-align: center;
  font-size: 17px;
  padding-top: 10px;
  padding-bottom: 10px;
  width: 100%;
}
.title_model p {
  display: inline;
  margin-right: 5px;
}
.blur {
  position: fixed;
  background: #000000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  opacity: 0.7;
}

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
  color: #000000;
}

.search:hover {
  border: 2px solid #009485;
}

.search:focus {
  outline: #009485;
  border-color: #009485;
}

.list_main {
  width: 65%;
  margin-left: 25px;
  color: white;
  margin-top: 30px;
  margin: 0 auto;
  margin-top: 30px;
}
.is_active {
  border-left: 1px solid white;
  padding-left: 10px;
  width: 250px;
}

.list {
  overflow: scroll;
  overflow-x: hidden;
  height: 700px;
}
.list_name {
  margin-bottom: 20px;
}

.box {
  display: flex;
  height: 30px;
  border: 1px solid white;
  border-radius: 5px;
  align-items: center;
  margin-bottom: 5px;
  width: 98%;
}
.info {
  display: flex;
}

.id {
  padding-left: 5px;
  width: 60px;
  border-right: 1px solid white;
}
.name {
  width: 320px;
  padding-left: 10px;
  border-right: 1px solid white;
}
.type {
  width: 250px;
  padding-left: 10px;
  border-right: 1px solid white;
}
.status {
  width: 150px;
  padding-left: 10px;
}

.option_1 {
  width: 150px;
  border-left: 1px solid white;
  padding-left: 10px;
}

.option {
  width: 150px;
  border-left: 1px solid white;
  padding-left: 10px;
  transition: 0.1s;
  cursor: pointer;
}
.option:hover {
  color: white;
  transition: 0.1s;
}

.option_2 {
  color: rgb(230, 246, 15);
}

.option_3 {
  color: red;
}
.option_4 {
  color: greenyellow;
}
.list::-webkit-scrollbar {
  width: 3px;
  height: 15px;
}

.list::-webkit-scrollbar-thumb {
  background: #009485;
  border-radius: 1px;
}
.list::-webkit-scrollbar-track:vertical {
  background-color: rgb(69, 67, 67);
  box-shadow: inset 0 0 2px 2px rgb(87, 86, 86);
}
</style>

<script setup>
import axios from 'axios'
import { ref, onMounted, watch } from 'vue'

var API_host = import.meta.env.VITE_API_ENDPOINT

const log = ref([])
const main_log = ref([])
const format = ref('')

const getLog = async () => {
  date_value.value = null
  time_1_value.value = '00:00:00'
  time_2_value.value = '23:59:59'
  device_value.value = null
  try {
    const { data } = await axios({
      method: 'get',
      url: `http://` + API_host + `/device/get_accident_log`,
      headers: { Authorization: localStorage.access_token }
    })
    log.value = data.reverse()
    for (let i = 0; i < log.value.length; i++) {
      const data = log.value[i].date_of_origin.toString().slice(0, 10)
      const time = log.value[i].date_of_origin.toString().slice(11, 19)
      log.value[i].date_of_origin = data + ' (' + time + ')'
    }
    main_log.value = log.value
    console.log(main_log.value)
    return data
  } catch (err) {
    console.log(err)
  }
}

onMounted(getLog)

const search_text = ref('')

const onChangeSearchInput = async () => {
  const log_search = []

  if (search_text.value === '') {
    main_log.value = log.value
  }
  for (let i = 0; i < log.value.length; i++) {
    let info_search = log.value[i].info.indexOf(search_text.value) != -1
    let date_of_origin_search =
      log.value[i].date_of_origin.toString().indexOf(search_text.value.toLowerCase()) != -1
    let device_search =
      log.value[i]['device_id.name'].toLowerCase().indexOf(search_text.value.toLowerCase()) != -1
    if (info_search || device_search || date_of_origin_search) {
      log_search.push(log.value[i])
    }
  }
  main_log.value = log_search
  console.log(main_log.value)
}

const date_value = ref(null)
const time_1_value = ref('00:00:00')
const time_2_value = ref('23:59:59')
const device_value = ref(null)
const getLogDateTime = async () => {
  if ((date_value.value && time_1_value.value && time_2_value.value) || device_value.value) {
    try {
      const { data } = await axios.get(
        `http://` +
          API_host +
          `/device/get_accident_log?device_id=${device_value.value}&date=${date_value.value}&time_from=${time_1_value.value}&time_to=${time_2_value.value}`,
        {
          headers: { Authorization: localStorage.access_token }
        }
      )
      console.log(data)
      log.value = data.reverse()
      for (let i = 0; i < log.value.length; i++) {
        const data = log.value[i].date_of_origin.toString().slice(0, 10)
        const time = log.value[i].date_of_origin.toString().slice(11, 19)
        log.value[i].date_of_origin = data + ' (' + time + ')'
      }
      main_log.value = log.value
    } catch (err) {
      console.log(err)
    }
  }
}

const getReporting = async () => {
  const params = {
    device_id: device_value.value,
    date: date_value.value,
    time_from: time_1_value.value,
    time_to: time_2_value.value
  }
  try {
    const { data } = await axios({
      method: 'get',
      url:
        `http://` +
        API_host +
        `/device/get_reporting_accident_log/${format.value}?device_id=${device_value.value}&date=${date_value.value}&time_from=${time_1_value.value}&time_to=${time_2_value.value}`,
      headers: { Authorization: localStorage.access_token },
      responseType: 'blob',
      params
    })
    const url = window.URL.createObjectURL(new Blob([data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'отчет.xlsx') // Указываем имя файла
    document.body.appendChild(link)
    link.click()
    format.value = ''
    return data
  } catch (err) {
    console.log(err)
  }
}

watch(
  [
    () => date_value.value,
    () => time_1_value.value,
    () => time_2_value.value,
    () => device_value.value
  ],
  getLogDateTime
)
watch([() => format.value], getReporting)
</script>

<template>
  <div class="list_main">
    <div class="title">Журнал аварийных ситуаций</div>
    <div class="title_search">
      <label for="mySelect">Устройство:</label>
      <select class="input_input select_device" id="mySelect" v-model="device_value">
        <option value="null">--Выберите--</option>
        <option value="1">Трансформатор 1</option>
        <option value="2">Трансформатор 2</option>
        <option value="3">Трансформатор 3</option>
        <option value="4">Трансформатор 4</option>
      </select>
      <div class="datetime_input">
        <div class="input_box">
          <label for="time-date">Дата:</label>
          <input
            class="input_input"
            type="date"
            name="dateInput"
            id="time-date"
            v-model="date_value"
            required
          />
        </div>

        <div class="input_box">
          <label for="time-input_1">От:</label>
          <input
            class="input_input"
            type="time"
            id="time-input_1"
            name="time"
            step="1"
            v-model="time_1_value"
          />
        </div>

        <div class="input_box">
          <label for="time-input_2">До:</label>
          <input
            class="input_input"
            type="time"
            id="time-input_2"
            name="time"
            step="1"
            v-model="time_2_value"
          />
        </div>
      </div>
      <div class="left_header">
        <input class="search" type="text" @input="onChangeSearchInput" v-model="search_text" />
        <div class="update" @click="getLog">Обновить</div>
        <select class="input_input" id="mySelect" v-model="format">
          <option value="">--Отчет--</option>
          <option value="xlsx">xlsx</option>
          <option value="csv">csv</option>
          <option value="docx">docx</option>
        </select>
      </div>
    </div>

    <div class="list_name">
      <div class="box">
        <div class="info headers">
          <div class="device h">Устройство</div>
          <div class="info_action h">Сообщение</div>
          <div class="date_of_collection h">Дата/время</div>
        </div>
      </div>
    </div>

    <div class="list">
      <div class="box" v-for="value in main_log" :key="value.id">
        <div class="info">
          <div class="device">
            <p>{{ value['device_id.name'] }}</p>
          </div>
          <div class="info_action">
            <p>{{ value.info }}</p>
          </div>
          <div class="date_of_collection">
            <p>{{ value.date_of_origin }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.select_device {
  margin-right: 10px;
}
.h {
  height: 30px;
  display: flex;
  align-items: center;
}
.left_header {
  display: flex;
  justify-content: space-between;
  width: 40%;
}
.button_box {
  display: flex;
  justify-content: space-around;
  width: 100%;
  margin-top: 20px;
}
.update {
  border-radius: 8px;
  background: #009485;
  padding: 2px 10px 2px 10px;
  font-size: 17px;
  transition: 0.2s;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  margin-left: 10px;
}

.update:hover {
  background: #04786c;
  transition: 0.2s;
  transition: 0.2s;
}

.title_search {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}
.title {
  margin-bottom: 10px;
  font-size: 20px;
}

.search {
  width: 320px;
  border: 2px solid black;
  border-radius: 5px;
  padding: 4px 10px;
  color: #000000;
  margin-left: 40px;
}

.search:hover {
  border: 2px solid #009485;
}

.search:focus {
  outline: #009485;
  border-color: #009485;
}

.list_main {
  width: 70%;
  margin-left: 25px;
  color: white;
  margin-top: 30px;
  margin: 0 auto;
  margin-top: 30px;
}

.list {
  overflow: scroll;
  overflow-x: hidden;
  height: 75vh;
}
.list_name {
  margin-bottom: 20px;
}

.box {
  border: 1px solid white;
  width: 98%;
}
.info {
  display: flex;
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

.device {
  width: 20%;
  border-right: 1px solid white;
  padding-left: 10px;
  padding-right: 10px;
}
.info_action {
  width: 55%;
  padding-left: 10px;
  padding-right: 10px;
  border-right: 1px solid white;
}

.date_of_collection {
  padding-left: 10px;
  padding-right: 10px;
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

.input_input {
  background: transparent;
  color: white;
  border: 2px solid #009485;
  border-radius: 15px;
  padding: 2px;
}

option {
  background: #989897;
  background: #009485;
}
label {
  color: white;
  margin-right: 10px;
}

.datetime_input {
  display: flex;
  width: 40%;
  justify-content: space-around;
}
input[type='time']::-webkit-calendar-picker-indicator {
  filter: invert(1); /* Инвертировать цвета */
}
input[type='date']::-webkit-calendar-picker-indicator {
  filter: invert(1); /* Инвертировать цвета */
}
</style>

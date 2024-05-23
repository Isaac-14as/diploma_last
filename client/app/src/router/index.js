import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import UserAdmin from '../views/UserAdmin.vue'
import Devices from '../views/Devices.vue'
import DeviceValue from '../views/DeviceValue.vue'
import ManagementLog from '../views/ManagementLog.vue'
import AccidentLog from '../views/AccidentLog.vue'
import Mnemo from '../views/Mnemo.vue'
import Graph from '../views/Graph.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Login
    },
    {
      path: '/user_admin',
      name: 'userAdmin',
      component: UserAdmin
    },
    {
      path: '/devices',
      name: 'devices',
      component: Devices
    },
    {
      path: '/device_value/:id',
      name: 'DeviceValue',
      component: DeviceValue
    },
    {
      path: '/management_log',
      name: 'ManagementLog',
      component: ManagementLog
    },
    {
      path: '/accident_log',
      name: 'AccidentLog',
      component: AccidentLog
    },
    {
      path: '/mnemo',
      name: 'Mnemo',
      component: Mnemo
    },
    {
      path: '/graph',
      name: 'Graph',
      component: Graph
    }
  ]
})

export default router

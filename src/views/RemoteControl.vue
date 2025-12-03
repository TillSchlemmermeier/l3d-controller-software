<template>
  <div class="h-full flex gap-6 justify-between mb-4 bg-zinc-900 rounded p-96">
    <div class="text-center">
      <p class="mb-2 text-zinc-400 text-xl">1. Connect Wi-Fi</p>
      <div class="bg-white p-2 rounded">
        <QrcodeVue :value="wifiQRString" :size="540" level="M" />
      </div>
      <p class="mt-1 text-xs text-zinc-500">{{ networkInfo.ssid }}</p>
    </div>

    <div class="text-center">
      <p class="mb-2 text-zinc-400 text-xl">2. Open App</p>
      <div class="bg-white p-2 rounded">
        <QrcodeVue :value="mobileAppString" :size="540" level="M" />
      </div>
      <p class="mt-1 text-xs text-zinc-500">{{ networkInfo.ip }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useUiStateStore } from '../stores/uiState'
import QrcodeVue from 'qrcode.vue'


const uiState = useUiStateStore()
const wifiQRString = ref('')
const mobileAppString = ref('')
const networkInfo = ref({ ip: 'localhost', port: 8000, ssid: '', password: '' })

onMounted(async () => {
  networkInfo.value = await uiState.getNetwork()
  const { ssid, password, ip, port } = networkInfo.value
  
  wifiQRString.value = `WIFI:T:WPA;S:${ssid};P:${password};;`
  mobileAppString.value = `http://${ip}:${port}/mobile`
})
</script>
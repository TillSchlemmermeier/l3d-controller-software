<template>
  <div class="h-full flex gap-6 justify-between mb-4 bg-zinc-900 rounded p-96">
    <div class="text-center">
      <p class="mb-2 text-zinc-400 text-xl">1. Connect Wi-Fi</p>
      <div class="bg-white p-2 rounded">
        <QrcodeVue :value="wifiQRString" :size="540" level="M" />
      </div>
      <p class="mt-1 text-xs text-zinc-500">{{ ssid }}</p>
    </div>

    <div class="text-center">
      <p class="mb-2 text-zinc-400 text-xl">2. Open App</p>
      <div class="bg-white p-2 rounded">
        <QrcodeVue :value="mobileAppString" :size="540" level="M" />
      </div>
      <p class="mt-1 text-xs text-zinc-500">{{ ip }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import QrcodeVue from 'qrcode.vue'

const ssid = import.meta.env.VITE_WIFI_SSID
const wifiQRString = `WIFI:T:WPA;S:${ssid};P:${import.meta.env.VITE_WIFI_PW};;`

const ip = ref('localhost')
const mobileAppString = ref('')

onMounted(async () => {
  ip.value = await window.ipcRenderer.getNetworkIp()
  mobileAppString.value = `http://${ip.value}:${import.meta.env.VITE_BACKEND_PORT}/mobile`
})
</script>
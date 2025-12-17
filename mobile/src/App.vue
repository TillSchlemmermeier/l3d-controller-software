<template>
  <main 
    @touchstart="handleTouchStart"
    class="w-screen h-dvh bg-zinc-950 text-white flex flex-col overflow-hidden font-sans select-none"
  >
    <div class="h-[35vh] w-full relative bg-black shrink-0">
      <CubePreview 
        ref="cubePreviewRef"
        :channel="store.selectedChannel" 
        :is-connected="isConnected"
        @cube-select="(e: CustomEvent) => store.selectChannel(e.detail)"
      />

      <!-- Channel Label and websocket connection status indicator-->
      <div 
        class="absolute top-4 left-4 bg-black/50 backdrop-blur px-3 py-1 rounded-full border border-white/10 text-xs font-bold tracking-wider pointer-events-none"
      >
        {{ 
          store.selectedChannel === 0 ?
          'GLOBAL VIEW' :
          `CHANNEL ${store.selectedChannel}`
      }}
      </div>
      <div
        class="absolute top-3 right-14 w-2 h-2 rounded-full transition-colors duration-300 z-50"
        :class="isConnected ? 'bg-green-500' : 'bg-red-500 animate-ping'"
      ></div>

      <FullscreenButton 
        :isFullscreen="isFullscreen"
        @toggleFullscreen="toggleFullscreen"
        class="absolute top-4 right-4"
      />
    </div>

    <div 
      class="flex-1 flex flex-col gap-3 p-3 min-h-0 bg-zinc-900 -mt-4 z-10 relative"
    >
      <ChannelSelector />
      <div 
        class="flex gap-3 items-center shrink-0 bg-zinc-950/30 p-3 rounded-2xl border border-white/5"
      >
        <div class="flex-1 flex flex-col gap-3">
          <MobileSlider
            @startSliding="store.isSlidingBrightness = true"
            @stopSliding="store.isSlidingBrightness = false"
            label="Brightness"
            v-model="currentBrightness"
          />
          <MobileSlider
            @startSliding="store.isSlidingFade = true"
            @stopSliding="store.isSlidingFade = false"
            label="Fade"
            v-model="currentFade"
          />
        </div>
        <ToggleChannelButton />
      </div>
      <GridControls />
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import CubePreview from './components/CubePreview.vue'
import MobileSlider from './components/MobileSlider.vue'
import FullscreenButton from './components/FullscreenButton.vue'
import ChannelSelector from './components/ChannelSelector.vue'
import GridControls from './components/GridControls.vue'
import ToggleChannelButton from './components/ToggleChannelButton.vue'
import { useMobileStore } from './stores/mobileState'

const store = useMobileStore()
const isFullscreen = ref(false)
const isConnected = ref(false)

const cubePreviewRef = ref<InstanceType<typeof CubePreview> | null>(null)
let socket: WebSocket | null = null

const currentBrightness = computed({
  get: () => store.currentBrightness,
  set: (val: number) => store.setCurrentBrightness(val)
})

const currentFade = computed({
  get: () => store.currentFade,
  set: (val: number) => store.setCurrentFade(val)
})


// --- WebSocket Logic ---
function connectWebSocket() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  const host = window.location.hostname
  const port = '8000'
  const wsUrl = `${protocol}//${host}:${port}/ws?skip=2`
  const getStateUrl = `${window.location.protocol}//${host}:${port}/api/get-state`

  socket = new WebSocket(wsUrl)
  socket.binaryType = 'arraybuffer'

  socket.onopen = () => { 
    isConnected.value = true 
    console.log('WebSocket connected')
    // Request full state on connect
    fetch(getStateUrl)
  }
  
  socket.onclose = () => { 
    isConnected.value = false
    setTimeout(connectWebSocket, 2000) 
  }

  socket.onmessage = (event) => {
    if (event.data instanceof ArrayBuffer) {
      if (cubePreviewRef.value) {
        cubePreviewRef.value.updateGeometry(new Float32Array(event.data))
      }
    } else {
      try {
        const msg = JSON.parse(event.data)
        handleServerMessage(msg)
      } catch (e) {
        console.error('Error parsing WS message', e)
      }
    }
  }
}

function handleServerMessage(msg: any) { // eslint-disable-line
  if (msg.type === 'state') {
    console.log('Full state update received via WS')
    store.setFullState(msg.data)
  } else if (msg.type === 'state_key') {
    const { key, value, channel } = msg.data
    store.updateKey(key, value, channel)
  } else if (msg.type === 'state_section') {
    store.updateSection(msg.data)
  }
}


// --- Lifecycle ---
onMounted(() => {
  connectWebSocket()
  document.addEventListener('fullscreenchange', () => {
    isFullscreen.value = !!document.fullscreenElement
  })
})

onUnmounted(() => {
  if (socket) socket.close()
})


// --- Actions ---
function toggleFullscreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen().catch(e => console.log(e))
    isFullscreen.value = true
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen()
      isFullscreen.value = false
    }
  }
}

function handleTouchStart(e: TouchEvent) {
  if (e.touches.length === 2) {
    e.preventDefault()
    store.strobeOneshot()
    vibrate([10, 10, 10])
  }
  if (e.touches.length === 3) {
    e.preventDefault()
    store.triggerRandom()
  }
}

function vibrate(pattern: number | number[]) {
  if (navigator.vibrate) navigator.vibrate(pattern)
}
</script>

<style>
.no-scrollbar::-webkit-scrollbar { display: none; }
.no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>
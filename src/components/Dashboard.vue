<template>
  <div 
    class="bg-black p-6 h-full flex flex-row gap-4 border-2"
    :class="{ 'border-red-600': isSelected, 'border-transparent': !isSelected }"
    @click="selectDashboard"
    >
    <div class="flex flex-col gap-4">

      <div class="flex flex-row gap-4"> 
        <div
          class="rounded-xl aspect-square p-3 flex flex-col items-center justify-center w-24"
          :class="gradientBackground(presentState.autopilot)"
          @click.stop="presentState.toggleAutopilot"
        >
          <span class="text-zinc-900 text-md font-bold text-center" >
            AUTO PILOT
          </span>
          <span class="font-semibold">
            {{ presentState.autopilot_time }} s
          </span>
        </div>
  
        <div class="rounded-xl aspect-square p-3 flex flex-col items-center justify-center w-24" :class="gradientBackground(presentState.crossfade_active)"
        >
          <span class="text-zinc-900 text-md font-bold text-center" >
            CROSS FADE
          </span>
        </div>
      </div>

      <div class="flex flex-row gap-4"> 
        <div
          class="rounded-xl aspect-square p-3 flex flex-col items-center justify-center w-24 bg-zinc-400"
          @click.stop="presentState.autopilotMode"
        >
          <span class="text-zinc-900 text-md font-bold text-center" >
            MODE:
          </span>
          <span class="font-semibold capitalize text-center">
            {{ presentState.random.replace(/_/g, ' ') }} 
          </span>
        </div>
      </div>


    </div>

    <div class="flex flex-col gap-4 flex-1">
      <div class="flex flex-row justify-between"> 
        <div class="rounded-xl aspect-square p-3 flex flex-col items-center justify-center w-24 bg-zinc-400">
          <span class="text-zinc-900 text-md font-bold text-center" >
            ONE SHOTS
          </span>
        </div>
    
        <div
          class="rounded-xl aspect-square p-3 flex flex-col items-center justify-center w-24 bg-zinc-400"
          @click.stop="presentState.rebootCore"
        >
          <span class="text-zinc-900 text-md font-bold text-center" >
            REBOOT CORE
          </span>
        </div>
      </div>
      <div class="flex flex-row gap-4">
        <div class="grid grid-cols-3 gap-1 w-36 mr-6 mb-5 border-1 border-white p-3 rounded-xl">
          <button 
            v-for="(icon, index) in icons" 
            :key="index"
            class="aspect-square rounded-md overflow-hidden"
            :class="{ 'invert': activeOneshot !== index + 1 }"
            @click="handleGridClick(index + 1)"
          >
            <img 
              :src="icon as string"
              :alt="`Oneshot ${index + 1}`"
              class="w-full h-full object-cover"
            />
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { usePresentStateStore } from '../stores/presentState'

const iconOrder = [
  'sides',
  'fade',
  'dark',
  'growing_sphere',
  'roll',
  'strobo',
  'cubes',
  'dark_sphere',
  'threesixty',
  'trigger',
]
const oneshotIcons = import.meta.glob('../assets/oneshots/*.{png,jpg,svg}', {
  eager: true,
  import: 'default'
})

const icons = iconOrder.map(name => oneshotIcons[`../assets/oneshots/${name}.svg`])

const presentState = usePresentStateStore()
const activeOneshot = ref(0)

const isSelected = computed(() => {
  const [section, index] = presentState.context
  return section === 10 && index === 1
})

function selectDashboard() {
  presentState.select(10, 1)
}

const gradientBackground = (param: boolean) => {
  return param
    ? 'bg-gradient-to-br from-emerald-600 to-green-400'
    : 'bg-gradient-to-br from-rose-500 to-red-400'
}

function handleGridClick(position: number) {
  console.log(`Grid position ${position} clicked`)
}

watch(() => presentState.oneshot, (newValue) => {
  if (newValue > 0) {
    console.log(`Oneshot ${newValue} activated`)
    activeOneshot.value = newValue
    setTimeout(() => {
      activeOneshot.value = 0
    }, 150)
  }
})
</script>

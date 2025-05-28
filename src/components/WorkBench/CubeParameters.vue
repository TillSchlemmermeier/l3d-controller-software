<template>
  <div class="p-3 rounded-lg transition-all duration-200 flex relative overflow-hidden" 
       :class="textColor">
    <div class="absolute inset-0 opacity-90"
      :class="gradientBackground">
    </div>

    <div class="flex flex-col justify-between w-full z-10">
      <div class="text-6xl font-bold text-center mb-3">
        L3D
      </div>
      <div class="flex flex-row justify-between">
        <div class="flex flex-col items-center">
          <div class="relative w-8 h-8">
            <img :src="brightnessEmptyIcon" class="absolute inset-0 opacity-90" />
            <div class="absolute inset-0 flex items-center justify-center">
              <div 
                class="w-3 h-3 rounded-full transition-all duration-200"
                :style="{
                  background: `conic-gradient(
                    rgb(39 39 42) ${presentState.brightness * 360}deg,
                    transparent ${presentState.brightness * 360}deg
                  )`
                }"
              ></div>
            </div>
          </div>
          <div class="text-lg font-medium w-12 text-right">
            {{ (presentState.brightness * 100).toFixed(0) }}%
          </div>
        </div>
        <div class="flex flex-col items-center">
          <img :src="fadeIcon" class="w-8 h-8 opacity-90" />
          <div class="text-lg font-medium w-12 text-right">
            {{ (presentState.fade * 100).toFixed(0) }}%
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { usePresentStateStore } from '../../stores/presentState'
import brightnessEmptyIcon from '../../assets/icons/brightness_empty.svg'
import fadeIcon from '../../assets/icons/fade.svg'

const presentState = usePresentStateStore()

const textColor = computed(() => {
  return presentState.IO 
    ? 'text-zinc-900' 
    : 'text-zinc-800'
})

const gradientBackground = computed(() => {
  return presentState.IO
    ? 'bg-gradient-to-br from-emerald-500 to-green-400'
    : 'bg-gradient-to-br from-rose-500 to-red-400'
})
</script>
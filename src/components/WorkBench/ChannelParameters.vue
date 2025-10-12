<template>
  <div class="p-3 rounded-lg transition-all duration-200 flex relative overflow-hidden shadow-md shadow-zinc-900"
       :class="[textColor]">
    <div class="absolute inset-0 opacity-90"
      :class="gradientBackground">
    </div>
    <div class="flex justify-between w-full z-10">
      <div class="text-6xl font-bold">
        {{ channel + 1 }}
      </div>
      <div class="flex flex-col gap-2">
        <div class="flex items-center">
          <div class="relative w-8 h-8">
            <img :src="brightnessEmptyIcon" class="absolute inset-0 opacity-90" />
            <div class="absolute inset-0 flex items-center justify-center">
              <div 
                class="w-3 h-3 rounded-full transition-all duration-200"
                :style="{
                  background: `conic-gradient(
                    rgb(39 39 42) ${channelParameters.brightness * 360}deg,
                    transparent ${channelParameters.brightness * 360}deg
                  )`
                }"
              ></div>
            </div>
          </div>
          <div class="text-lg font-medium w-12 text-right">
            {{ (channelParameters.brightness * 100).toFixed(0) }}%
          </div>
        </div>
        <div class="flex items-center">
          <img :src="fadeIcon" class="w-8 h-8 mr-2 opacity-90" />
          <div class="text-lg font-medium w-9 text-right">
            {{ (channelParameters.fade * 100).toFixed(0) }}%
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useCoreStateStore } from '../../stores/coreState'
import brightnessEmptyIcon from '../../assets/icons/brightness_empty.svg'
import fadeIcon from '../../assets/icons/fade.svg'

const props = defineProps({
  channel: {
    type: Number,
    default: 0,
  },
})

const coreState = useCoreStateStore()

const channelParameters = computed(() => {
  return coreState.getChannelParameters(props.channel)
})

const textColor = computed(() => {
  return coreState.channels[props.channel].IO
    ? 'text-zinc-900' 
    : 'text-zinc-800'
})

const gradientBackground = computed(() => {
  return coreState.channels[props.channel].IO
    ? 'bg-gradient-to-br from-emerald-600 to-green-400'
    : 'bg-gradient-to-br from-rose-500 to-red-400'
})

</script>
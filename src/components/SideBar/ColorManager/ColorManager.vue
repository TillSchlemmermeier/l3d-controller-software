<template>
  <div class="h-[1395px] bg-zinc-700 text-white font-medium flex flex-col">
    <div class="p-6">
      <!-- Gradient Slider -->
      <GradientSlider
        :mode="mode"
        :gradientStops="gradientStops"
        :gradientCss="gradientCss"
        :selectedStopIndex="selectedStopIndex"
        :selectedRegion="selectedRegion"
        @addStop="handleAddGradientStop"
        @selectStop="selectStop"
        @updateStopPosition="handleUpdateStopPosition"
        @updateRegion="selectedRegion = $event"
        @interactionEnd="sendColorUpdate"
      />

      <!-- Mode Toggle -->
      <TogglePill
        class="mt-2"
        :options="[
          { value: 'edit', label: 'Edit Stops' },
          { value: 'select', label: 'Select Region' }
        ]"
        v-model="mode"
        @update:model-value="sendColorUpdate"
      />
    </div>
    
    <!-- Color Picker -->
    <ColorPicker
      :selectedColor="selectedStop?.[1]"
      @colorChange="handleColorChange"
    />
    
    <!-- Delete Stop Button (Edit Mode Only) -->
    <div v-if="mode === 'edit'">
      <button
        v-if="canDeleteStop(selectedStop)"
        @click="deleteSelectedStop"
        class="mx-auto my-2 py-3 px-6 bg-zinc-800 text-white font-medium rounded-md flex items-center justify-center gap-2"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
        </svg>
        Delete Selected Stop
      </button>
      <div v-else class="py-8" />
    </div>
    <div v-else class="py-8" />

    <div class="px-6 pb-4">
      <!-- Speed Slider -->
      <RangeSlider 
        label="Speed"
        class="mb-10"
        v-model="speed"
        @change="sendColorUpdate"
      />

      <!-- Gradient Type Toggle -->
      <TogglePill
        :options="[
          { value: 'linear', label: 'Linear' },
          { value: 'radial', label: 'Radial' }
        ]"
        v-model="gradientType"
        @update:model-value="sendColorUpdate"
      >
        <template #default="{ option }">
          <span class="flex items-center gap-2">
            <svg v-if="option.value === 'linear'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 12h16m0 0l-4-4m4 4l-4 4" />
            </svg>
            <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {{ option.label }}
          </span>
        </template>
      </TogglePill>

      <!-- Rotation Speed Sliders -->
      <div v-if="gradientType === 'linear'" class="mt-10 flex flex-row gap-10 w-full">
        <RangeSlider 
          label="Rotate Speed Y"
          v-model="rotateSpeedY"
          :min=-100
          @change="sendColorUpdate"
        />
        
        <RangeSlider 
          label="Rotate Speed Z"
          v-model="rotateSpeedZ"
          :min=-100
          @change="sendColorUpdate"
        />
      </div>
      <div v-else class="mt-6 h-24" />

      <SoundOptions
        v-model="soundToLightOptions"
        @update:model-value="sendColorUpdate"
      />


      <!-- Copy From Other Channels -->
      <OtherChannels
        @copied-from-channel="channelCopied"
      />
    </div>
    <ActionButtons
      @clear="clearGradient"
      @save="saveGradient"
      @reset="resetSettings"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useCoreStateStore } from '../../../stores/coreState'
import { useUiStateStore } from '../../../stores/uiState'
import GradientSlider from './GradientSlider.vue'
import TogglePill from './TogglePill.vue'
import ColorPicker from './ColorPicker.vue'
import RangeSlider from './RangeSlider.vue'
import SoundOptions from './SoundOptions.vue'
import OtherChannels from './OtherChannels.vue'
import ActionButtons from './ActionButtons.vue'
import { colorStringToHSV, hsvToColorString } from '../../../utils/colorConversion'
import type { SelectedRegion } from '../../../types/types'

const currentHue = ref(0)
const saturation = ref(100)
const lightness = ref(50)
const mode = ref<'edit' | 'select'>('edit')
const gradientStops = ref<Array<[number, string]>>([
  [0, '#FF0000'],
  [100, '#0000FF']
])
const selectedStopIndex = ref(0)
const selectedRegion = ref<SelectedRegion>({ start: 0, end: 100 })
const speed = ref(0)
const gradientType = ref<'linear' | 'radial'>('linear')
const rotateSpeedY = ref(0)
const rotateSpeedZ = ref(0)
const soundToLightOptions = ref<string[]>([])

const coreState = useCoreStateStore()
const uiState = useUiStateStore()

const selectedStop = computed(() => {
  return gradientStops.value[selectedStopIndex.value]
})

const gradientCss = computed(() => {
  const stops = gradientStops.value
    .map(([position, color]) => `${color} ${position}%`)
    .join(', ')
  
  if (gradientType.value === 'radial') {
    return `radial-gradient(circle, ${stops})`
  } else {
    return `linear-gradient(to right, ${stops})`
  }
})

function loadColorData() {
  const channelIndex = uiState.channelIndex
  const channel = coreState.channels[channelIndex]

  if (!channel || !channel.color) return

  gradientStops.value = channel.color.gradient
  gradientType.value = channel.color.gradientType
  speed.value = channel.color.speed
  selectedRegion.value.start = channel.color.sectionStart
  selectedRegion.value.end = channel.color.sectionStart + channel.color.sectionWidth
  rotateSpeedY.value = channel.color.rotateSpeedY
  rotateSpeedZ.value = channel.color.rotateSpeedZ
  soundToLightOptions.value = channel.color.soundToLightOptions
}

function selectStop(index: number) {
  selectedStopIndex.value = index
  updateHSVFromColor(selectedStop.value[1])
}

function handleAddGradientStop(position: number) {
  const newStop: [number, string] = [
    position,
    hsvToColorString(currentHue.value, saturation.value, lightness.value)
  ]
  
  gradientStops.value.push(newStop)
  gradientStops.value.sort(([a], [b]) => a - b)  // Sort by position
  
  selectedStopIndex.value = gradientStops.value.findIndex(([pos]) => pos === position)
  
  sendColorUpdate()
}

function handleUpdateStopPosition(index: number, position: number) {
  gradientStops.value[index][0] = position
}

function deleteSelectedStop() {
  gradientStops.value.splice(selectedStopIndex.value, 1)
  selectedStopIndex.value -= 1

  sendColorUpdate()
}

function canDeleteStop(stop: [number, string]): boolean {
  return stop[0] !== 0 && stop[0] !== 100
}

function handleColorChange(color: string) {
  selectedStop.value[1] = color
  sendColorUpdate()
}

function channelCopied() {
  selectedStopIndex.value = 0
  updateHSVFromColor(gradientStops.value[0][1])
  loadColorData()
  sendColorUpdate()
}

function sendColorUpdate() {
  const channelIndex = uiState.channelIndex
  const colorData = {
    gradient: gradientStops.value,
    gradientType: gradientType.value,
    sectionWidth: selectedRegion.value.end - selectedRegion.value.start,
    sectionStart: selectedRegion.value.start,
    speed: speed.value,
    rotateSpeedY: rotateSpeedY.value,
    rotateSpeedZ: rotateSpeedZ.value,
    soundToLightOptions: soundToLightOptions.value
  }
  coreState.updateColorManager(channelIndex, colorData)
}

const updateHSVFromColor = (colorString: string) => {
  const hsv = colorStringToHSV(colorString)

  currentHue.value = hsv.h
  saturation.value = hsv.s
  lightness.value = hsv.v
}

function resetSettings() {
  gradientType.value = 'linear'
  selectedRegion.value = { start: 0, end: 100 }
  speed.value = 0
  rotateSpeedY.value = 0
  rotateSpeedZ.value = 0
  soundToLightOptions.value = []
  sendColorUpdate()
}

function clearGradient() {
  const channelIndex = uiState.channelIndex
  uiState.clearGradient(channelIndex)
  // Alternative: instead of clearing, reset to default white gradient.
  // gradientStops.value = [
  //   [0, '#FFFFFF'],
  //   [100, '#FFFFFF']
  // ]
  // selectedStopIndex.value = 0
  // updateHSVFromColor('#FFFFFF')
  // sendColorUpdate()
}

function saveGradient(subtype: string) {
  uiState.saveGradientPreset(
    gradientStops.value,
    subtype
  )
}

// watch for channel changes or changes in the current channel's color data
watch(
  [
    () => uiState.channelIndex,
    () => coreState.channels[uiState.channelIndex]?.color
  ],
  () => {
    loadColorData()
  },
  { immediate: true, deep: true }
)

onMounted(() => {
  selectedStopIndex.value = 0
  updateHSVFromColor(selectedStop.value[1])
  loadColorData()
})

</script>
<style scoped>
</style>
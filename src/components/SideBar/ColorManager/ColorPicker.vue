<template>
  <div>
    <!-- Color Picker Section -->
    <div class="">
      <div class="flex items-center justify-between mb-2 text-xs text-zinc-400 uppercase font-bold tracking-wider">
        <div>Picker</div>
        <div>RGB({{ rgbValues.r }}, {{ rgbValues.g }}, {{ rgbValues.b }})</div>
      </div>
      <div 
        class="relative aspect-video w-full rounded-sm border border-zinc-500 cursor-crosshair touch-none"
        :style="pickerBackground"
        @pointerdown="startPickerDrag"
        ref="colorPicker"
      >
        <!-- Color picker handle -->
        <div 
          class="absolute size-4 -translate-x-1/2 -translate-y-1/2 rounded-full border-2 border-white ring-2 ring-black cursor-grab"
          :style="handleStyle"
        ></div>
      </div>
    </div>

    <!-- Hue Slider -->
    <div class="mt-6">
      <div 
        class="relative h-6 w-full rounded-md cursor-pointer hue-slider" 
        @click="updateHue"
        @pointerdown="startHueDrag"
        ref="hueSlider"
      >
        <div 
          class="absolute h-8 w-3 -translate-x-1/2 -translate-y-1/2 top-1/2 rounded-full border-2 border-white ring-2 ring-black"
          :style="{ left: `${(currentHue / 360) * 100}%` }"
        ></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { hsvToRgb, colorStringToHSV, hsvToColorString } from '../../../utils/colorConversion'

interface Props {
  selectedColor?: string
}

const props = withDefaults(defineProps<Props>(), {
  selectedColor: '#FFFFFF',
})

interface Emits {
  (e: 'colorChange', color: string): void
}

const emit = defineEmits<Emits>()

const currentHue = ref(0)
const saturation = ref(100)
const lightness = ref(50)
const colorPicker = ref<HTMLElement>()
const hueSlider = ref<HTMLElement>()

const pickerBackground = computed(() => {
  return {
    background: `linear-gradient(to bottom, transparent 0%, rgb(0, 0, 0) 100%), linear-gradient(to right, rgb(255, 255, 255) 0%, transparent 100%), hsl(${currentHue.value}, 100%, 50%)`
  }
})

const handleStyle = computed(() => {
  return {
    background: hsvToColorString(currentHue.value, saturation.value, lightness.value),
    left: `${saturation.value}%`,
    top: `${100 - lightness.value}%`
  }
})

const rgbValues = computed(() => {
  return hsvToRgb(
    currentHue.value / 360,
    saturation.value / 100,
    lightness.value / 100
  )
})

function startPickerDrag(event: PointerEvent) {
  document.addEventListener('pointermove', updateColorFromPicker)
  document.addEventListener('pointerup', endPickerDrag)
  document.addEventListener('pointercancel', endPickerDrag)
  updateColorFromPicker(event)
}

function endPickerDrag() {
  document.removeEventListener('pointermove', updateColorFromPicker)
  document.removeEventListener('pointerup', endPickerDrag)
  document.removeEventListener('pointercancel', endPickerDrag)
  sendColorUpdate()
}

function updateColorFromPicker(event: MouseEvent) {
  if (!colorPicker.value) return
  
  const rect = colorPicker.value.getBoundingClientRect()
  const x = (event.clientX - rect.left) / rect.width
  const y = (event.clientY - rect.top) / rect.height
  
  saturation.value = Math.max(0, Math.min(100, x * 100))
  lightness.value = Math.max(0, Math.min(100, (1 - y) * 100))
}

function startHueDrag(event: PointerEvent) {
  document.addEventListener('pointermove', updateHue)
  document.addEventListener('pointerup', endHueDrag)
  document.addEventListener('pointercancel', endHueDrag)
  updateHue(event)
}

function endHueDrag() {
  document.removeEventListener('pointermove', updateHue)
  document.removeEventListener('pointerup', endHueDrag)
  document.removeEventListener('pointercancel', endHueDrag)
  sendColorUpdate()
}

function updateHue(event: MouseEvent) {
  if (!hueSlider.value) return
  
  const rect = hueSlider.value.getBoundingClientRect()
  const newHue = ((event.clientX - rect.left) / rect.width) * 360
  currentHue.value = Math.max(0, Math.min(360, newHue))
}

function sendColorUpdate() {
  const color = hsvToColorString(currentHue.value, saturation.value, lightness.value)
  emit('colorChange', color)
}

watch(() => props.selectedColor, (newColor) => {
  if (newColor) {
    const hsv = colorStringToHSV(newColor)
    if (hsv.s > 0 && hsv.v > 0) {
      currentHue.value = hsv.h
    }
    saturation.value = hsv.s
    lightness.value = hsv.v
  }
}, { immediate: true })
</script>

<style scoped>
.hue-slider {
  background: linear-gradient(to right, 
    hsl(0, 100%, 50%), 
    hsl(60, 100%, 50%), 
    hsl(120, 100%, 50%), 
    hsl(180, 100%, 50%), 
    hsl(240, 100%, 50%), 
    hsl(300, 100%, 50%), 
    hsl(360, 100%, 50%)
  );
}
</style>
<template>
  <div class="mb-6 flex-1">
    <div class="flex items-center justify-between mb-2 text-xs text-zinc-400 uppercase font-bold tracking-wider">
      <div>{{ label }}</div>
      <div>{{ Math.round(modelValue) }}</div>
    </div>
    <div class="flex gap-2 items-center">
      <div 
        class="relative flex-1 h-8 bg-zinc-800 rounded-md cursor-pointer touch-none"
        @pointerdown="startDrag"
        ref="sliderElement"
      >
        <!-- Slider track -->
        <div 
          class="absolute left-0 top-0 h-full bg-gradient-to-r from-blue-600 to-blue-400 rounded-md transition-none"
          :style="trackStyle"
        ></div>
        
        <!-- Slider handle -->
        <div 
          class="absolute top-1/2 -translate-y-1/2 w-10 h-10 bg-white rounded-full border-2 border-blue-500 shadow-lg cursor-grab active:cursor-grabbing"
          :style="{ left: `calc(${((value - min) / (100 - min)) * 100}% - 20px)` }"
        ></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

interface Props {
  modelValue: number
  label: string
  min?: number
}

interface Emits {
  (e: 'update:modelValue', value: number): void
  (e: 'change', value: number): void
}

const props = withDefaults(defineProps<Props>(), {
  min: 0
})

const emit = defineEmits<Emits>()

const value = computed({
  get: () => props.modelValue,
  set: (val: number) => emit('update:modelValue', val)
})

const trackStyle = computed(() => {
  const zeroPos = (0 - props.min) / (100 - props.min) * 100
  const handlePos = (value.value - props.min) / (100 - props.min) * 100
  
  if (value.value >= 0) {
    return { left: `${zeroPos}%`, width: `${handlePos - zeroPos}%` }
  } else {
    return { left: `${handlePos}%`, width: `${zeroPos - handlePos}%` }
  }
})

const sliderElement = ref<HTMLElement>()
const isDragging = ref(false)

function startDrag(event: PointerEvent) {
  document.addEventListener('pointermove', handleDragMove)
  document.addEventListener('pointerup', stopDrag)
  document.addEventListener('pointercancel', stopDrag)
  isDragging.value = true
  updateValueFromSlider(event)
}

function handleDragMove(event: PointerEvent) {
  updateValueFromSlider(event)
}

function stopDrag(event: PointerEvent) {
  isDragging.value = false
  const el = event.target as HTMLElement
  el.releasePointerCapture(event.pointerId)
  document.removeEventListener('pointermove', handleDragMove)
  document.removeEventListener('pointerup', stopDrag)
  document.removeEventListener('pointercancel', stopDrag)
  emit('change', value.value)
}

function updateValueFromSlider(event: PointerEvent) {
  if (!sliderElement.value) return

  const rect = sliderElement.value.getBoundingClientRect()
  // Clamp pointer position to slider bounds
  let x = event.clientX
  if (x < rect.left) x = rect.left
  if (x > rect.right) x = rect.right

  const percentage = (x - rect.left) / rect.width
  let newValue = props.min + percentage * (100 - props.min)

  // Snap to 0 if within -5 to 5 range
  if (newValue >= -5 && newValue <= 5) {
    newValue = 0
  }

  value.value = Math.round(Math.max(props.min, Math.min(100, newValue)))
}
</script>
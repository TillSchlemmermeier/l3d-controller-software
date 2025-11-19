<template>
  <!-- Preset Gallery -->
  <div 
    ref="presetGallery"
    class="w-full overflow-x-auto pb-2 mb-3 select-none
    scrollbar-thin scrollbar-track-transparent 
    scrollbar-thumb-zinc-500/50 hover:scrollbar-thumb-zinc-500/70 
    scrollbar-thumb-rounded-full scrollbar-track-rounded-full"
    @mousedown.prevent="startDragging"
    @mousemove="handleDrag"
    @mouseup="stopDragging"
    @mouseleave="stopDragging"
    >
    <div class="flex flex-nowrap gap-2 min-w-min"> 
      <button
        v-for="preset in sortedPresets"
        :key="preset.name"
        :data-preset="preset.name"
        class="relative flex-none w-28 rounded-lg overflow-hidden bg-zinc-300"
      >
      <div class="aspect-square relative">
        <img 
          :src="`src/assets/previews/${uiState.selectedElement}_p_${preset.name}.gif`" 
          class="w-full h-full object-cover"
          draggable="false"
          v-show="!gifLoadingErrors.get(preset.name)"
          @error="gifLoadingErrors.set(preset.name, true)"
          ref="imgRef"
        />
          <div 
            v-show="gifLoadingErrors.get(preset.name)"
            class="w-full h-full bg-black flex items-center justify-center p-2"
          >
            <p class="w-full text-zinc-200 text-lg text-center font-medium break-words">
              {{ formatName(preset.name) }}
            </p>
          </div>
          <!-- Small label below the GIF -->
          <div 
            class="absolute bottom-0 inset-x-0"
            :class="gifLoadingErrors.get(preset.name) ? 'hidden' : 'bg-black/60 py-1 px-2'"
          >
            <p class="text-[10px] leading-tight text-zinc-100 text-center font-medium truncate">
              {{ formatName(preset.name) }}
            </p>
          </div>
        </div>
      </button>
    </div>
  </div>
</template>


<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUiStateStore } from '../../stores/uiState'
import { Preset } from '../../types/types'

const emit = defineEmits<{
  (e: 'select', value: string): void
}>()

const uiState = useUiStateStore()
const gifLoadingErrors = ref(new Map<string, boolean>())
const presetGallery = ref<HTMLElement | null>(null)
const isDragging = ref(false)
const mouseDownX = ref(0)
const startX = ref(0)
const movedDistance = ref(0)


function formatName(name: string): string {
  return name.replace(/^[gae]_/, '').replace(/_/g, ' ')
}

const sortedPresets = computed(() => {
  gifLoadingErrors.value.clear()
  const presets = [...uiState.overlayPresets] as Preset[]
  console.log(presets)
  
  // Remove 'basic' preset before sorting
  const basicIndex = presets.findIndex(p => p.name === 'basic')
  const basicPreset = basicIndex !== -1 ? presets.splice(basicIndex, 1)[0] : null
  
  // Sort remaining presets based on selected method
  switch (uiState.sortBy) {
    case 'alpha':
      presets.sort((a, b) => a.name.localeCompare(b.name))
      break
    case 'date':
      presets.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
      break
    case 'usage':
      presets.sort((a, b) => b.request_count - a.request_count)
      break
  }
  
  // Add 'basic' preset back at the start if it exists
  if (basicPreset) {
    presets.unshift(basicPreset)
  }
  
  return presets
});

function startDragging(e: MouseEvent) {
  isDragging.value = true
  mouseDownX.value = e.clientX
  startX.value = e.clientX
  movedDistance.value = 0
}

function handleDrag(e: MouseEvent) {
  if (!isDragging.value || !presetGallery.value) return
  
  const dx = mouseDownX.value - e.clientX
  mouseDownX.value = e.clientX
  
  movedDistance.value += Math.abs(dx)
  presetGallery.value.scrollBy({
    left: dx,
    behavior: 'auto'
  })
}

function stopDragging(e: MouseEvent) {
  if (isDragging.value && movedDistance.value < 5) {
    // Handle as click if moved less than 5px
    const target = e.target as HTMLElement
    const button = target.closest('button')
    if (button) {
      const preset = button.getAttribute('data-preset')
      if (preset) {
        emit('select', preset)
      }
    }
  }
  isDragging.value = false
}

onMounted(async () => {
  console.log('Mounted Preset Gallery')
})

</script>
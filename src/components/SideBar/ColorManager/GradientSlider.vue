<template>
  <div class="relative h-12 cursor-copy ring-2 ring-white ring-offset-2 ring-offset-zinc-700 rounded-md touch-none">
    <!-- Clickable area for adding stops (Edit mode only) -->
    <div 
      v-if="mode === 'edit'"
      class="absolute inset-0 z-10"
      @click="handleAddStop"
    ></div>
    
    <!-- Gradient background -->
    <div 
      class="absolute inset-0 rounded-md"
      :style="{ background: gradientCss }"
    ></div>

    <!-- Edit mode: Gradient stops/markers -->
    <div
      v-if="mode === 'edit'"
      v-for="(stop, index) in gradientStops"
      :key="index"
      class="absolute top-1/2 -translate-y-1/2 z-20 flex flex-col items-center"
      :style="{ left: `calc(${stop[0]}% - 6px)` }"
    >
      <!-- Marker handle -->
      <div 
        class="w-4 rounded-full cursor-move border-2 border-white transition-all"
        :style="{ background: stop[1] }"
        @click.stop="emit('selectStop', index)"
        @pointerdown="startDrag(index, $event)"
        :class="[
          'transition-all duration-200',
          selectedStopIndex === index
            ? 'ring-3 ring-black h-18'
            : 'ring-2 ring-zinc-700 h-16'
        ]"
      ></div>
      <span class="absolute text-sm -bottom-7 text-white outline-none">{{ stop[0] }}</span>
    </div>

    <!-- Select mode: Region selection overlay -->
    <div v-if="mode === 'select'" class="absolute inset-0 z-10">
      <!-- Grey overlay for non-selected areas -->
      <div 
        class="absolute top-0 bottom-0 bg-black/40 rounded-l-md"
        :style="{ left: '0%', width: `${selectedRegion.start}%` }"
      ></div>
      
      <div 
        class="absolute top-0 bottom-0 bg-black/40 rounded-r-md"
        :style="{ left: `${selectedRegion.end}%`, width: `${100 - selectedRegion.end}%` }"
      ></div>
      
      <!-- Left resize handle -->
      <div 
        class="absolute top-0 bottom-0 w-4 bg-white/20 cursor-w-resize hover:bg-white/40 transition-colors z-20"
        :style="{ left: `calc(${selectedRegion.start}% - 4px)` }"
        @pointerdown="handleResizeStart('start', $event)"
      >
        <div class="w-full h-full flex items-center justify-center">
          <div class="w-0.5 h-4 bg-white rounded-full"></div>
        </div>
      </div>
      
      <!-- Right resize handle -->
      <div 
        class="absolute top-0 bottom-0 w-4 bg-white/20 cursor-e-resize hover:bg-white/40 transition-colors z-20"
        :style="{ left: `calc(${selectedRegion.end}% - 12px)` }"
        @pointerdown="handleResizeStart('end', $event)"
      >
        <div class="w-full h-full flex items-center justify-center">
          <div class="w-0.5 h-4 bg-white rounded-full"></div>
        </div>
      </div>
      
      <!-- Drag handle for moving the region -->
      <div 
        class="absolute top-0 bottom-0 cursor-move hover:bg-white/10 transition-colors z-15"
        :style="{ 
          left: `${selectedRegion.start}%`, 
          width: `${selectedRegion.end - selectedRegion.start}%` 
        }"
        @pointerdown="handleRegionDragStart($event)"
      >
        <div class="w-full h-full flex items-center justify-center">
          <div class="flex gap-1">
            <div class="w-0.5 h-3 bg-white/60 rounded-full"></div>
            <div class="w-0.5 h-3 bg-white/60 rounded-full"></div>
            <div class="w-0.5 h-3 bg-white/60 rounded-full"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { SelectedRegion } from '../../../types/types'

interface Props {
  mode: 'edit' | 'select'
  gradientStops: [number, string][]
  gradientCss: string
  selectedStopIndex: number
  selectedRegion: SelectedRegion
}

const props = defineProps<Props>()

interface Emits {
  (e: 'addStop', position: number): void
  (e: 'selectStop', index: number): void
  (e: 'updateStopPosition', index: number, position: number): void
  (e: 'updateRegion', region: SelectedRegion): void
  (e: 'interactionEnd'): void
}

const emit = defineEmits<Emits>()

const isDraggingMarker = ref(false)
const isDraggingRegion = ref(false)
const isResizingRegion = ref<'start' | 'end' | null>(null)
const draggedMarkerIndex = ref(-1)
const dragStart = ref({ x: 0, position: 0, regionStart: 0, regionEnd: 0 })

function handleAddStop(event: MouseEvent | PointerEvent) {
  const rect = (event.currentTarget as HTMLElement).getBoundingClientRect()
  const position = ((event.clientX - rect.left) / rect.width) * 100
  
  // Check if too close to existing stops
  const tooClose = props.gradientStops.some(stop => 
    Math.abs(stop[0] - position) < 5
  )
  
  if (!tooClose) {
    emit('addStop', Math.round(position))
  }
}

function addDragListeners() {
  document.addEventListener('pointermove', dragMove)
  document.addEventListener('pointerup', endDrag)
  document.addEventListener('pointercancel', endDrag)
}

function startDrag(index: number, event: PointerEvent) {
  addDragListeners()
  emit('selectStop', index)
  // Don't start dragging markers at position 0 or 100
  if (props.gradientStops[index][0] === 0 || props.gradientStops[index][0] === 100) {
    return
  }
  
  isDraggingMarker.value = true
  draggedMarkerIndex.value = index
  dragStart.value.x = event.clientX
  dragStart.value.position = props.gradientStops[index][0]
  
  event.preventDefault()
  event.stopPropagation()
}

function handleResizeStart(side: 'start' | 'end', event: PointerEvent) {
  addDragListeners()
  isResizingRegion.value = side
  dragStart.value.x = event.clientX
  dragStart.value.regionStart = props.selectedRegion.start
  dragStart.value.regionEnd = props.selectedRegion.end
  event.preventDefault()
}

function handleRegionDragStart(event: PointerEvent) {
  addDragListeners()
  isDraggingRegion.value = true
  dragStart.value.x = event.clientX
  dragStart.value.regionStart = props.selectedRegion.start
  dragStart.value.regionEnd = props.selectedRegion.end
  event.preventDefault()
}

function dragMove(event: PointerEvent) {
  const sliderWidth = 372 // Approximate gradient width
  const deltaX = event.clientX - dragStart.value.x
  const deltaPercent = (deltaX / sliderWidth) * 100
  
  if (isDraggingMarker.value && draggedMarkerIndex.value !== -1) {
    let newPosition = dragStart.value.position + deltaPercent
    
    // Constrain position between neighboring stops
    const stops = props.gradientStops
    const currentIndex = draggedMarkerIndex.value
    
    let minPosition = 1 // Can't go to 0
    let maxPosition = 99 // Can't go to 100
    
    // Check left neighbor
    for (let i = 0; i < currentIndex; i++) {
      if (stops[i][0] > minPosition) {
        minPosition = stops[i][0] + 1
      }
    }
    
    // Check right neighbor
    for (let i = currentIndex + 1; i < stops.length; i++) {
      if (stops[i][0] < maxPosition) {
        maxPosition = stops[i][0] - 1
      }
    }
    
    // Apply constraints
    newPosition = Math.max(minPosition, Math.min(maxPosition, newPosition))
    newPosition = Math.round(newPosition)
    
    emit('updateStopPosition', draggedMarkerIndex.value, newPosition)
    
  } else if (isDraggingRegion.value) {
    const regionWidth = dragStart.value.regionEnd - dragStart.value.regionStart
    let newStart = dragStart.value.regionStart + deltaPercent
    let newEnd = dragStart.value.regionEnd + deltaPercent

    // Keep within bounds
    if (newStart < 0) {
      newStart = 0
      newEnd = regionWidth
    }
    if (newEnd > 100) {
      newEnd = 100
      newStart = 100 - regionWidth
    }

    emit('updateRegion', {
      start: Math.round(Math.max(0, newStart)),
      end: Math.round(Math.min(100, newEnd))
    })
    
  } else if (isResizingRegion.value) {
    if (isResizingRegion.value === 'start') {
      const newStart = Math.round(Math.max(0, Math.min(dragStart.value.regionEnd - 1, dragStart.value.regionStart + deltaPercent)))
      emit('updateRegion', {
        start: newStart,
        end: props.selectedRegion.end
      })
    } else if (isResizingRegion.value === 'end') {
      const newEnd = Math.round(Math.min(100, Math.max(dragStart.value.regionStart + 1, dragStart.value.regionEnd + deltaPercent)))
      emit('updateRegion', {
        start: props.selectedRegion.start,
        end: newEnd
      })
    }
  }
}

function endDrag() {
  document.removeEventListener('pointermove', dragMove)
  document.removeEventListener('pointerup', endDrag)
  document.removeEventListener('pointercancel', endDrag)
  if (isDraggingMarker.value || isDraggingRegion.value || isResizingRegion.value) {
    emit('interactionEnd')
  }
  
  isDraggingMarker.value = false
  isDraggingRegion.value = false
  isResizingRegion.value = null
  draggedMarkerIndex.value = -1
}
</script>
<template v-if="coreState.channels.length < 8">
  <div class="w-full flex justify-center">
    <div class="relative w-34 h-36">
      <!-- Trash icon background -->
      <div 
        :style="{ 
          backgroundImage: backgroundImage,
          backgroundSize: '80%',
          backgroundPosition: 'center',
          backgroundRepeat: 'no-repeat',
        }"
        class="absolute inset-0 bg-slate-100 border-2 rounded-2xl transition-all duration-300 shadow-lg shadow-black"
        :class="{
          'opacity-10': !uiState.isDragging,
          'opacity-20 scale-110': uiState.isDragging,
          'ring-red-700 ring-6 ring-offset-3 ring-offset-zinc-700 animate-bounce opacity-100': uiState.deleteActive
        }"
      />
      
      <!-- Draggable area with independent opacity -->
      <draggable
        :v-model="trashZone"
        item-key="trash"
        class="absolute inset-0 opacity-40"
        :group="{ name: 'effects', put: true, pull: false }"
        @add="removeItem"
        :data-name="'trashZone'"
      >
        <template #item="{ element }">
          <div class="p-2 rounded-lg shadow-md bg-white/90">
            {{ element }}
          </div>
        </template>
      </draggable>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, nextTick } from 'vue'
import draggable from 'vuedraggable'
import { useCoreStateStore } from '../../stores/coreState'
import { useUiStateStore } from '../../stores/uiState'
import trashIcon from '../../assets/icons/trash.png'

const coreState = useCoreStateStore()
const uiState = useUiStateStore()
const trashZone = ref(['trash'])
const trashIconUrl = ref(trashIcon)
const backgroundImage = computed(() => `url(${trashIconUrl.value})`)


function removeItem(event: { item: HTMLElement; oldIndex: number }) {
  // uiState.isSelected = [-1, -1]
  event.item.remove()
  trashZone.value.pop()
  
  if (uiState.lastTypeDragged === 'channel') {
    coreState.removeChannel(event.oldIndex)
    // Force re-render of channel components
    nextTick(() => {
      // Temporarily remove and reattach channels to force Vue to re-evaluate templates
      const tempChannels = [...coreState.channels]
      coreState.channels = []
      nextTick(() => {
        coreState.channels = tempChannels
      })
    })
  } else if (uiState.lastTypeDragged === 'effect') {
    if (uiState.draggedChannelIndex === 9) {
      // Handle global effects
      coreState.removeEffect(9, event.oldIndex)
      nextTick(() => {
        const tempGlobalEffects = [...coreState.globalEffects]
        coreState.globalEffects = []
        nextTick(() => {
          coreState.globalEffects = tempGlobalEffects
        })
      })
    } else {
      // Handle channel effects
      coreState.removeEffect(uiState.draggedChannelIndex, event.oldIndex)
      nextTick(() => {
        const tempEffects = [...coreState.channels[uiState.draggedChannelIndex].effects]
        coreState.channels[uiState.draggedChannelIndex].effects = []
        nextTick(() => {
          coreState.channels[uiState.draggedChannelIndex].effects = tempEffects
        })
      })
    }
  }

  // delete animation
  const trashElement = document.querySelector('[data-name="trashZone"]')
  const trashRect = trashElement?.getBoundingClientRect()
  
  if (!trashRect) return
  
  // Calculate trash icon center
  const trashCenterX = trashRect.left + (trashRect.width / 2)
  const trashCenterY = trashRect.top + (trashRect.height / 2)
  
  // Create a clone of the dragged element for animation
  const clone = event.item.cloneNode(true) as HTMLElement
  
  // Position the clone at trash icon center
  const container = document.createElement('div')
  container.className = 'trash-animation-container'
  container.style.left = `${trashCenterX}px`
  container.style.top = `${trashCenterY}px`
  container.style.width = `${event.item.offsetWidth}px`
  container.style.height = `${event.item.offsetHeight}px`
  container.style.transform = 'translate(-50%, -50%)' // Center the container
  
  container.appendChild(clone)
  document.body.appendChild(container)


    // Start animation and cleanup container after it ends
  requestAnimationFrame(() => {
    clone.classList.add('being-trashed')
    setTimeout(() => {
      container.remove()
    }, 500) // Match this with animation duration
  }) // Match this with animation duration
}
</script>

<style>
  @keyframes suck-in {
    0% {
      transform: translate(-50%, -50%) scale(1);
      opacity: 1;
      transform-origin: center center;
    }
    50% {
      transform: translate(-50%, -50%) scale(0.9) scaleY(0.6);
      opacity: 0.8;
    }
    100% {
      transform: translate(-50%, -50%) scale(0) scaleY(0.2);
      opacity: 0;
    }
  }

  .trash-animation-container {
    position: fixed;
    pointer-events: none;
    z-index: 9999;
  }

  .being-trashed {
    animation: suck-in 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
  }
</style>

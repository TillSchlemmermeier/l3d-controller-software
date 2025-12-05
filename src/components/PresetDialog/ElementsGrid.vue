<template>
  <div 
    class="flex flex-row flex-wrap gap-3 mx-auto"
  >
    <template 
      v-if="uiState.elementType == 'generator' ||
            uiState.elementType == 'effect'"
    >
      <template v-for="element in sortedItems" :key="element">
        <button
          @click="$emit('select', element.name)"
          class="group w-28 aspect-square rounded-lg shadow-sm ring-1 ring-zinc-500/50"
          :class="[
            element.name === uiState.selectedElement
              ? 'bg-gradient-to-br from-zinc-500 to-zinc-400' 
              : 'bg-gradient-to-br from-zinc-400 to-zinc-300'
          ]"
        >
          <div class="flex h-full flex-col items-center justify-center p-3">
            <span class="text-m text-center font-semibold text-zinc-900 break-words w-full capitalize">
              {{ formatName(element.name) }}
            </span>
          </div>
        </button>
      </template>
    </template>
    <!-- For channel and global presets show cards with preview -->
    <template v-else>
      <template v-for="element in sortedPresets" :key="element">
        <button
          :data-preset="element"
          @click="() => {
            uiState.selectedElement = element.name;
            $emit('load', element.name)
          }"
          class="relative flex-none w-28 rounded-lg overflow-hidden bg-zinc-300"
        >
          <div class="aspect-square">
            <img 
              :src="`src/assets/previews/${uiState.elementType}_p_${element.name}.gif`"
              class="w-full h-full object-cover"
              draggable="false"
            />
          </div>
          <!-- Small label below the GIF -->
          <div class="absolute bottom-0 inset-x-0 bg-black/60 py-1 px-2">
            <p class="text-[10px] leading-tight text-zinc-100 text-center font-medium truncate">
              {{ formatName(element.name) }}
            </p>
          </div>
        </button>
      </template>
    </template>

    <!-- Toggle between generator and channel presets if we are creating a new channel-->
    <div v-if="newChannel">
      <button
        v-if="uiState.elementType === 'generator'"
        @click="$emit('changeType')"
        class="w-28 aspect-square rounded-lg bg-gradient-to-br from-zinc-500 to-zinc-400 shadow-sm ring-1 ring-zinc-800/50"
      >
        <span class="text-m text-center font-semibold text-zinc-900 break-words w-full capitalize">
          Switch to Channel Presets
        </span>
      </button>
      <button
        v-else="uiState.elementType === 'channel'"
        @click="$emit('changeType')"
        class="w-28 aspect-square rounded-lg bg-gradient-to-br from-zinc-500 to-zinc-400 shadow-sm ring-1 ring-zinc-800/50"
      >
        <span class="text-m text-center font-semibold text-zinc-900 break-words w-full capitalize">
          Switch to Generators
        </span>
      </button>
    </div>

    <!-- Save Preset Button -->
    <button
      v-if="!newChannel && uiState.admin == true"
      @click="$emit('toggleKeyboard')"
      class="group w-28 aspect-square rounded-lg bg-gradient-to-br from-zinc-700 to-zinc-500 shadow-sm ring-1 ring-zinc-800/50"
    >
      <div class="flex h-full flex-col items-center justify-center p-3">
        <span class="text-m text-center font-semibold text-zinc-300 break-words w-full capitalize">
          Save {{ uiState.elementType }} Preset
        </span>
      </div>
    </button>

  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useUiStateStore } from '../../stores/uiState'

defineProps<{
  newChannel: boolean
}>()

defineEmits<{
  (e: 'select', value: string): void
  (e: 'load', value: string): void
  (e: 'changeType'): void
  (e: 'toggleKeyboard'): void
}>()

const uiState = useUiStateStore()

function formatName(name: string): string {
  return name.replace(/^[gae]_/, '').replace(/_/g, ' ')
}

interface ElementItem {
  name: string
  created_at: string
  request_count: number
}

function sortElements(items: ElementItem[]): ElementItem[] {
  switch (uiState.sortBy) {
    case 'alpha':
      return items.sort((a, b) => a.name.localeCompare(b.name))
    case 'date':
      return items.sort((a, b) => {
        const dateA = new Date(a.created_at)
        const dateB = new Date(b.created_at)
        return dateB.getTime() - dateA.getTime() // newest first
      })
    case 'usage':
      return items.sort((a, b) => b.request_count - a.request_count) // most used first
    default:
      return items
  }
}

const sortedItems = computed(() => sortElements([...uiState.overlayItems] as ElementItem[]))

const sortedPresets = computed(() => sortElements([...uiState.overlayPresets] as ElementItem[]))
</script>
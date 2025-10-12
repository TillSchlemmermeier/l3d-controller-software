<template>
  <div class="h-screen w-full bg-zinc-700 text-white flex flex-col">
    <!-- Gallery Header -->
    <div class="p-3 border-b border-zinc-600 shrink-0">
      <!-- Gradient Type Filter -->
      <div class="flex mb-4">
          <button
            v-for="type in availableTypes"
            :key="type"
            class="w-16 aspect-square flex items-center justify-center relative transition-all duration-200 ease-in-out rounded mx-1 active:scale-95"
            :class="selectedType === type ? 'bg-zinc-500 shadow-lg scale-105' : 'bg-zinc-600'"
            @click="selectedType = type"
          >
            <div
              class="absolute top-0 left-0 h-1 w-full rounded-t transition-all duration-200"
              :class="selectedType === type ? 'bg-blue-500' : 'bg-transparent'"
            />
            <span class="truncate text-xs font-medium text-center">
              {{ getDisplayType(type) }}<br />({{ getTypeCount(type) }})
            </span>
          </button>
      </div>

      <!-- Sort Options -->
      <SortButtons />
    </div>

    <!-- Gallery Grid -->
    <div class="flex-1 px-4 mt-2 mb-20 overflow-y-auto scrollbar-thin scrollbar-track-transparent scrollbar-thumb-zinc-500/50 hover:scrollbar-thumb-zinc-500/70 scrollbar-thumb-rounded-full scrollbar-track-rounded-full">
      <div 
        v-for="group in groupedGradients"
        :key="group.subtype"
        class="mb-3"
      >
        <!-- Subtype Divider -->
        <div 
          v-if="group.subtype && uiState.sortGradientsBy === 'subtype'"
          class="flex items-center mb-4 pt-4"
        >
          <div class="flex-1 border-t border-zinc-500"></div>
          <h3 class="px-4 text-sm text-zinc-300 font-semibold">{{ group.subtype }}</h3>
          <div class="flex-1 border-t border-zinc-500"></div>
        </div>

        <!-- Gradients Grid -->
        <div class="grid grid-cols-6 gap-2">
          <div
            v-for="gradient in group.gradients"
            :key="gradient.id"
            class="group cursor-pointer transition-transform hover:scale-105"
            @click="selectGradient(gradient)"
          >
            <div 
              class="w-14 h-14 rounded-md shadow-sm"
              :style="{ background: generateGradientCSS(gradient.data) }"
            />
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div 
        v-if="isLoading"
        class="text-center text-zinc-400 mt-8"
      >
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-white mx-auto mb-4"></div>
        <div class="text-lg">Loading gradients...</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUiStateStore } from '../../../stores/uiState'
import { useCoreStateStore } from '../../../stores/coreState'
import type { GradientPreset, SortOption } from '../../../types/types'
import { ColorSorter } from '../../../utils/colorSorter'
import SortButtons from './SortButtons.vue'

const uiState = useUiStateStore()
const coreState = useCoreStateStore()

const selectedType = ref<string>('all')
const isLoading = ref(true)

const TYPE_DISPLAY_NAMES: Record<string, string> = {
  'all': 'All',
  'matplotlib': 'mpl',
  'webgradients': 'Web',
  'single_colors': 'Single',
  'two_colors': 'Two',
  'custom': 'Custom',
}

const gradientPresets = computed((): GradientPreset[] => 
  uiState.gradientPresets as GradientPreset[]
)

const availableTypes = computed(() => 
  ['all', ...new Set(gradientPresets.value.map(g => g.type))].sort()
)

const groupedGradients = computed(() => {
  const filteredGradients = selectedType.value === 'all' 
    ? gradientPresets.value 
    : gradientPresets.value.filter(g => g.type === selectedType.value)

  return ColorSorter.sortAndGroup(filteredGradients, uiState.sortGradientsBy as SortOption)
})

function getDisplayType(type: string): string {
  return TYPE_DISPLAY_NAMES[type] || type
}

function getTypeCount(type: string): number {
  if (type === 'all') return gradientPresets.value.length
  return gradientPresets.value.filter(g => g.type === type).length
}

function selectGradient(gradient: GradientPreset) {
  if (uiState.deleteActive) {
    handleDeleteGradient(gradient)
  } else {
    coreState.loadGradient(gradient.id)
  }
}

function handleDeleteGradient(gradient: GradientPreset) {
  if (!uiState.admin) {
    console.warn('Delete action attempted without admin privileges.')
    uiState.deleteActive = false
    return
  }

  const confirmed = window.confirm(
    `Are you sure you want to delete gradient ID "${gradient.id}" from the ${gradient.type} collection?`
  )
  
  if (confirmed) {
    uiState.deleteGradientPreset(gradient.id)
    uiState.fetchGradientPresets()
  }
  
  uiState.deleteActive = false
}

function generateGradientCSS(gradientData: Array<[number, string]>): string {
  const stopStrings = gradientData.map(([position, color]) => `${color} ${position}%`)
  return `linear-gradient(to right, ${stopStrings.join(', ')})`
}

onMounted(async () => {
  await uiState.fetchGradientPresets()
  isLoading.value = false
})
</script>
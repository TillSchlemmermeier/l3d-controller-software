<template>
   <!-- Separation Line -->
  <hr class="border-t border-zinc-600 my-4">

  <div class="grid grid-cols-12 gap-2 justify-center">
    <div class="col-span-3 gap-4 flex flex-col">
      <DashboardButton
        label="TRIGGER RANDOM"
        :onClick="() => coreState.triggerRandomizer(uiState.randomMode)"
      /> 
      <DashboardButton
        label="RANDOM COLOR"
        :onClick="coreState.randomizeColor"
      />
    </div>
    <div class="col-span-6">
      <div class="flex flex-row gap-2 justify-center flex-wrap">
        <button 
          v-for="(randomMode, index) in randomModes" 
          :key="index"
          class="aspect-square w-16 h-16 rounded-md overflow-hidden transition-all duration-100 flex items-center justify-center"
          :class="uiState.randomMode === randomMode.key
            ? 'bg-white text-black shadow-[0_0_10px_rgba(255,255,255,0.3)]' 
            : 'bg-zinc-500 text-zinc-900 '"
          @click.stop="uiState.randomMode = randomMode.key"
          :title="randomMode.key"
        >
          <!-- Wrapper to ensure SVG size -->
          <span class="w-10 h-10 flex items-center justify-center" v-html="randomMode.icon"></span>
        </button>
      </div>

    </div>
    <div class="col-span-3 gap-4 flex flex-col">
      <DashboardButton
        label="AUTO PILOT"
        :subLabel="`${coreState.autopilot_time} s`"
        :active="coreState.autopilot"
        :onClick="coreState.toggleAutopilot"
      />
      <DashboardButton
        label="MODE:"
        :subLabel="coreState.random.replace(/_/g, ' ')"
        :onClick="coreState.autopilotMode"
        />
    </div>

  </div>
</template>

<script setup lang="ts">
import { useCoreStateStore } from '../../stores/coreState'
import { useUiStateStore } from '../../stores/uiState'
import DashboardButton from './DashboardButton.vue'
import type { AutopilotMode } from '../../types/types'

const coreState = useCoreStateStore()
const uiState = useUiStateStore()

const randomModes: Array<{ key: AutopilotMode; icon: string }> = [
  {
    // Sketch: A simple square outline
    key: 'global',
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect x="2" y="2" width="20" height="20" rx="2" />
</svg>`
  },
  {
    // Sketch: Four vertical bars
    key: 'all_channels',
    icon: `<svg viewBox="0 0 24 24" fill="currentColor" stroke="none">
  <rect x="3" y="4" width="3" height="16" rx="1" />
  <rect x="8" y="4" width="3" height="16" rx="1" />
  <rect x="13" y="4" width="3" height="16" rx="1" />
  <rect x="18" y="4" width="3" height="16" rx="1" />
</svg>`
  },
  {
    // Sketch: 3x3 Grid of squares
    key: 'all_elements',
    icon: `<svg viewBox="0 0 24 24" fill="currentColor" stroke="none">
  <rect x="4" y="4" width="4" height="4" rx="0.5" />
  <rect x="10" y="4" width="4" height="4" rx="0.5" />
  <rect x="16" y="4" width="4" height="4" rx="0.5" />
  
  <rect x="4" y="10" width="4" height="4" rx="0.5" />
  <rect x="10" y="10" width="4" height="4" rx="0.5" />
  <rect x="16" y="10" width="4" height="4" rx="0.5" />
  
  <rect x="4" y="16" width="4" height="4" rx="0.5" />
  <rect x="10" y="16" width="4" height="4" rx="0.5" />
  <rect x="16" y="16" width="4" height="4" rx="0.5" />
</svg>`
  },
  {
    // Sketch: Vertical bar (left) + Question mark (right)
    key: 'random_channel',
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <!-- Bar -->
  <rect x="5" y="4" width="4" height="16" rx="1" fill="currentColor" stroke="none" />
  <!-- Question Mark -->
  <path d="M17 16v.01" />
  <path d="M17 13a2 2 0 0 0 .914-3.782 1.98 1.98 0 0 0-2.414.483" />
</svg>`
  },
  {
    // Sketch: Stack of 3 squares (left) + Question mark (right)
    key: 'random_channel_elements',
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <!-- Stack -->
  <rect x="5" y="4" width="4" height="4" rx="0.5" fill="currentColor" stroke="none" />
  <rect x="5" y="10" width="4" height="4" rx="0.5" fill="currentColor" stroke="none" />
  <rect x="5" y="16" width="4" height="4" rx="0.5" fill="currentColor" stroke="none" />
  <!-- Question Mark -->
  <path d="M17 16v.01" />
  <path d="M17 13a2 2 0 0 0 .914-3.782 1.98 1.98 0 0 0-2.414.483" />
</svg>`
  },
  {
    // Sketch: Single square (left) + Question mark (right)
    key: 'random_element',
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <!-- Square -->
  <rect x="5" y="10" width="4" height="4" rx="0.5" fill="currentColor" stroke="none" />
  <!-- Question Mark -->
  <path d="M17 16v.01" />
  <path d="M17 13a2 2 0 0 0 .914-3.782 1.98 1.98 0 0 0-2.414.483" />
</svg>`
  },
  {
    // Sketch: Center bar with selection brackets
    key: 'selected_channel',
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <!-- Center Bar -->
  <rect x="10" y="5" width="4" height="14" rx="1" fill="currentColor" stroke="none" />
  <!-- Brackets -->
  <path d="M8 3l-2 0l0 2" />
  <path d="M16 3l2 0l0 2" />
  <path d="M8 21l-2 0l0 -2" />
  <path d="M16 21l2 0l0 -2" />
</svg>`
  },
  {
    // Sketch: Center stack with selection brackets
    key: 'selected_channel_elements',
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <!-- Center Stack -->
  <rect x="10" y="5" width="4" height="4" rx="0.5" fill="currentColor" stroke="none" />
  <rect x="10" y="10" width="4" height="4" rx="0.5" fill="currentColor" stroke="none" />
  <rect x="10" y="15" width="4" height="4" rx="0.5" fill="currentColor" stroke="none" />
  <!-- Brackets -->
  <path d="M8 3l-2 0l0 2" />
  <path d="M16 3l2 0l0 2" />
  <path d="M8 21l-2 0l0 -2" />
  <path d="M16 21l2 0l0 -2" />
</svg>`
  },
  {
    // Sketch: Center square with selection brackets
    key: 'selected_element',
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <!-- Center Square -->
  <rect x="10" y="10" width="4" height="4" rx="0.5" fill="currentColor" stroke="none" />
  <!-- Brackets -->
  <path d="M8 7l-2 0l0 2" />
  <path d="M16 7l2 0l0 2" />
  <path d="M8 17l-2 0l0 -2" />
  <path d="M16 17l2 0l0 -2" />
</svg>`
  }
]
</script>

<style scoped>
/* Force SVGs injected via v-html to fill the wrapper */
:deep(svg) {
  width: 100%;
  height: 100%;
}
</style>
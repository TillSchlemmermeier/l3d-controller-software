<template>
  <div class="fixed bottom-6 left-26 z-50">
    <button
      @click="toggleShift"
      class="relative transition-all duration-300 ease-out w-20 h-20 rounded-2xl flex items-center justify-center backdrop-blur-lg shadow-2xl border"
      :class="uiState.shiftActivated
        ? 'bg-amber-500/90 border-amber-300/50 scale-110 ring-2 ring-white/30'
        : 'bg-zinc-800/50 border-zinc-700/40 opacity-40 hover:opacity-80'"
    >
      <img
        :src="shiftIcon"
        class="w-10 h-10 invert transition-opacity duration-300"
        :class="uiState.shiftActivated ? 'opacity-100' : 'opacity-60'"
      />

      <div
        v-if="uiState.shiftActivated"
        class="absolute -top-1 -right-1 w-3 h-3 bg-white rounded-full shadow-md"
      />
    </button>
  </div>
</template>

<script setup lang="ts">
import { useUiStateStore } from '../../stores/uiState'
import shiftIcon from '../../assets/icons/io.svg'

const uiState = useUiStateStore()

const toggleShift = () => {
  uiState.shiftActivated = !uiState.shiftActivated
}
</script>

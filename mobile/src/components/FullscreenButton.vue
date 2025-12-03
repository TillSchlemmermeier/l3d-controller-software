<template>
  <button 
    @click="$emit('toggleFullscreen')"
    class="absolute top-4 right-4 w-8 h-8 bg-black/50 backdrop-blur rounded-full border border-white/10 flex items-center justify-center text-white active:scale-90 transition-transform z-50"
  >
    <svg 
      v-if="!isFullscreen"
      class="w-4 h-4"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
    >
      <path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/>
    </svg>
    <svg 
      v-else
      class="w-4 h-4"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
    >
      <path d="M8 3v3a2 2 0 0 1-2 2H3m18 0h-3a2 2 0 0 1-2-2V3m0 18v-3a2 2 0 0 1 2-2h3M3 16h3a2 2 0 0 1 2 2v3"/>
    </svg>
  </button>
</template>

<script lang="ts" setup>
interface Props {
  isFullscreen: boolean
}

interface Emits {
  (e: 'toggleFullscreen'): void 
}

defineProps<Props>()
defineEmits<Emits>()
</script>
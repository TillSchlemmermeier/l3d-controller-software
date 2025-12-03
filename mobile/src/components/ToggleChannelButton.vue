<template>
  <button 
    v-if="store.selectedChannel > 0"
    @click="store.toggleChannelPower"
    class="w-16 h-full rounded-xl flex flex-col items-center justify-center gap-1 transition-all border-2"
    :class="store.getCurrentChannelObj?.IO 
      ? 'bg-green-500/20 border-green-500 text-green-500' 
      : 'bg-red-500/10 border-red-900/50 text-red-700'"
  >
    <svg
      class="w-6 h-6"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
    >
      <path d="M18.36 6.64a9 9 0 1 1-12.73 0"></path>
      <line x1="12" y1="2" x2="12" y2="12"></line>
    </svg>
    <span class="text-[10px] font-bold uppercase">
      {{ store.getCurrentChannelObj?.IO ? 'ON' : 'OFF' }}
    </span>
  </button>
</template>        


<script setup lang="ts">
import { useMobileStore } from '../stores/mobileState'

const store = useMobileStore()

</script>
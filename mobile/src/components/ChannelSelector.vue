<template>
<div class="flex gap-2 overflow-x-auto no-scrollbar shrink-0 pb-1 pt-1">
  <button 
    @click="store.selectChannel(0)"
    class="h-10 px-4 rounded-full text-sm font-bold transition-all whitespace-nowrap flex items-center gap-2 border"
    :class="store.selectedChannel === 0 
      ? 'bg-white text-black border-white shadow-lg' 
      : 'bg-zinc-800 text-zinc-400 border-zinc-700'"
  >
    ALL
  </button>
  
  <button 
    v-for="ch in store.channels" 
    :key="ch.id"
    @click="store.selectChannel(ch.id)"
    class="h-9 w-9 rounded-full text-sm font-bold transition-all flex items-center justify-center border relative shrink-0"
    :class="[
      store.selectedChannel === ch.id 
        ? 'bg-indigo-500 text-white border-indigo-400 shadow-lg scale-105' 
        : 'bg-zinc-800 text-zinc-400 border-zinc-700',
      !ch.IO && store.selectedChannel !== ch.id ? 'opacity-50' : ''
    ]"
  >
    {{ ch.id }}
    <div 
      class="absolute top-0 -right-1 w-3 h-3 rounded-full border-2 border-zinc-900"
      :class="ch.IO ? 'bg-green-500' : 'bg-red-500'"
    ></div>
  </button>
</div>

</template>
<script setup lang="ts">
import { useMobileStore } from '../stores/mobileState'

const store = useMobileStore()
</script>
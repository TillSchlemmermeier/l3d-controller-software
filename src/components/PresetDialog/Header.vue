<template>
  <div class="flex items-center px-6 py-3 border-b border-zinc-700">
    <!-- Sort icons (left) -->
    <div class="flex gap-4">
      <button 
        class="rounded-lg px-2 py-1 transition-all duration-150 active:scale-70"
        :class="{ 'bg-zinc-500/30': uiState.sortBy === 'alpha' }"
        @click="uiState.sortBy = 'alpha'"
        title="Sort alphabetically"
      >
        <img :src="sortAscendingLetters" class="w-7 h-7 invert"/>
      </button>
      <button 
        class="rounded-lg px-2 py-1 transition-all duration-150 active:scale-70"
        :class="{ 'bg-zinc-500/30': uiState.sortBy === 'usage' }"
        @click="uiState.sortBy = 'usage'"
        title="Sort by usage"
      >
        <img :src="sortAscendingNumbers" class="w-7 h-7 invert"/>
      </button>
      <button 
        class="rounded-lg px-2 py-1 transition-all duration-150 active:scale-70"
        :class="{ 'bg-zinc-500/30': uiState.sortBy === 'date' }"
        @click="uiState.sortBy = 'date'"
        title="Sort by date"
      >
        <img :src="calendarWeek" class="w-7 h-7 invert"/>
      </button>
    </div>

    <!-- Centered title -->
    <h2 class="flex-1 text-2xl text-zinc-100 text-center uppercase tracking-wider font-bold">
      {{ uiState.elementType }}
    </h2>

    <!-- Close button (right) -->
    <button 
      @click="$emit('close')"
      class="rounded-full p-1.5 hover:bg-zinc-500 transition-colors w-8"
    >
      <div class="relative w-5 h-5 flex items-center justify-center">
        <div class="absolute w-4 h-0.5 bg-zinc-300 rotate-45"></div>
        <div class="absolute w-4 h-0.5 bg-zinc-300 -rotate-45"></div>
      </div>
    </button>


  </div>
</template>


<script setup lang="ts">
import { useUiStateStore } from '../../stores/uiState';
import calendarWeek from '../../assets/icons/calendar-week.svg'
import sortAscendingLetters from '../../assets/icons/sort-a-z.svg'
import sortAscendingNumbers from '../../assets/icons/sort-0-9.svg'

const uiState = useUiStateStore();

defineEmits<{
  (e: 'close'): void
}>()
</script>
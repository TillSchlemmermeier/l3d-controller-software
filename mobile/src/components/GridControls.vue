<template>
  <div class="flex-1 min-h-0 grid grid-cols-12 gap-2">
    <div class="col-span-3 flex flex-col gap-2">
      <button
        @click="store.toggleAutopilot()"
        class="flex-1 rounded-xl flex flex-col items-center justify-center gap-1 border transition-all active:scale-95"
        :class="store.autopilot ? 'bg-emerald-600 border-emerald-400 text-white' : 'bg-zinc-800 border-zinc-700 text-zinc-500'"
      >
        <svg 
          height="36px"
          viewBox="0 -960 960 960"
          width="36px"
          fill="currentColor"
        >
          <path d="M560-160v-80h104L537-367l57-57 126 126v-102h80v240H560Zm-344 0-56-56 504-504H560v-80h240v240h-80v-104L216-160Zm151-377L160-744l56-56 207 207-56 56Z"/>
        </svg>
      </button>
      <button 
        @click="store.setAutopilotMode()"
        class="flex-1 rounded-xl bg-zinc-800 border border-zinc-700 flex flex-col items-center justify-center gap-1 active:bg-zinc-700 active:scale-95"
      >
        <span class="font-bold text-xs text-zinc-300">Autopilot Mode: {{ store.randomMode }}</span>
      </button>
    </div>

    <div class="col-span-6 grid grid-cols-3 gap-1.5 content-center">
      <button 
        v-for="mode in randomModes" 
        :key="mode.key"
        @click="store.triggerMode = mode.key"
        class="aspect-square rounded-lg flex items-center justify-center transition-all active:scale-90 border"
        :class="store.triggerMode === mode.key
          ? 'bg-white text-black border-white shadow-[0_0_10px_rgba(255,255,255,0.4)]' 
          : 'bg-zinc-800 text-zinc-600 border-zinc-700'"
      >
        <div class="w-8 h-8" v-html="mode.icon"></div>
      </button>
    </div>

    <div class="col-span-3 flex flex-col gap-2">
      <button 
        @click="store.undoRandom()" 
        class="flex-1 rounded-xl bg-zinc-800 border border-zinc-700 flex flex-col items-center justify-center gap-1 active:bg-zinc-700 active:scale-95">
          <svg 
            class="w-10 h-10 text-orange-400"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M3 7v6h6"></path>
            <path d="M21 17a9 9 0 0 0-9-9 9 9 0 0 0-6 2.3L3 13"></path>
          </svg>
      </button>
      <button
        @click="store.triggerRandom()"
        class="flex-1 rounded-xl bg-zinc-800 border border-zinc-700 flex flex-col items-center justify-center gap-1 active:bg-zinc-700 active:scale-95"
      >
        <span class="text-4xl">🎲</span>
      </button>
    </div>
  </div>

  <!-- Bottom Actions -->
  <div class="h-16 shrink-0 grid grid-cols-3 gap-3 mt-1">
    <button 
      @click="store.normalizeS2L()"
      class="rounded-xl bg-zinc-800 border border-zinc-700 font-bold text-xs text-zinc-300 active:bg-zinc-700 active:scale-95"
    >
      NORM S2L
    </button>
    <button
      @click="store.triggerOneshot()"
      class="rounded-xl bg-zinc-200 border-b-4 border-zinc-400 font-bold text-xs text-black active:border-b-0 active:translate-y-1 active:bg-white"
    >
      TRIGGER
    </button>
    <button
      @click="store.strobeOneshot()"
      class="rounded-xl bg-rose-600 border-b-4 border-rose-800 font-bold text-4xl text-white active:border-b-0 active:translate-y-1 active:bg-rose-500 shadow-lg shadow-rose-900/20"
    >⚡︎</button>
  </div>
</template>

<script setup lang="ts">
import { useMobileStore } from '../stores/mobileState'

const store = useMobileStore()

const randomModes: Array<{ key: string; icon: string }> = [
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
    // Sketch: coloured dot
    key: 'color',
    icon: `<div class="w-5 h-5 rounded-full bg-linear-to-tr from-blue-500 via-purple-500 to-red-500"></div>`
  }
]
</script>
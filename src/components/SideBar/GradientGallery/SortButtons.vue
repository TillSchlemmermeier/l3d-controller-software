<template>
  <div class="space-y-2 mb-2">
    <div class="mb-2 text-xs text-zinc-400 uppercase font-bold tracking-wider">
      Sort by
    </div>
    <div class="flex gap-3">
      <button
        v-for="option in sortOptions"
        :key="option.key"
        class="w-10 h-10 flex items-center justify-center rounded-lg transition-all duration-200 border-2"
        :class="uiState.sortGradientsBy === option.key
          ? 'bg-blue-600 border-blue-400 text-white shadow-lg scale-105'
          : 'bg-zinc-600 border-transparent text-zinc-300 hover:bg-zinc-500 hover:text-white'"
        :title="option.title"
        @click="uiState.sortGradientsBy = uiState.sortGradientsBy === option.key ? 'none' : option.key"
      >
        <span v-html="option.icon"></span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { SortOption } from '../../../types/types'
import { useUiStateStore } from '../../../stores/uiState'

const uiState = useUiStateStore()

const sortOptions: Array<{ key: SortOption; title: string; icon: string }> = [
  {
    key: 'subtype',
    title: 'Group by subtype',
    icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none">
      <rect x="3" y="3" width="18" height="4" rx="2" fill="currentColor"/>
      <rect x="3" y="10" width="12" height="4" rx="2" fill="currentColor"/>
      <rect x="3" y="17" width="15" height="4" rx="2" fill="currentColor"/>
    </svg>`
  },
  {
    key: 'mean',
    title: 'Sort by mean color',
    icon: `<svg width="28" height="28" viewBox="0 0 24 24" fill="none">
      <line x1="7" y1="7" x2="17" y2="7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      <path d="M9 11 L15 17 M15 11 L9 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>`
  },
  {
    key: 'first',
    title: 'Sort by first color',
    icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none">
      <path d="M16 6 L8 12 L16 18" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>`
  },
  {
    key: 'last',
    title: 'Sort by last color',
    icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none">
      <path d="M8 6 L16 12 L8 18" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>`
  },
  {
    key: 'usage',
    title: 'Sort by usage',
    icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
      <path d="M4 15l3 3l3 -3" />
      <path d="M7 6v12" />
      <path d="M17 3a2 2 0 0 1 2 2v3a2 2 0 1 1 -4 0v-3a2 2 0 0 1 2 -2z" />
      <path d="M17 16m-2 0a2 2 0 1 0 4 0a2 2 0 1 0 -4 0" />
      <path d="M19 16v3a2 2 0 0 1 -2 2h-1.5" />
    </svg>`
  },
  {
    key: 'date',
    title: 'Sort by date',
    icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
      <path d="M4 7a2 2 0 0 1 2 -2h12a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2v-12z" />
      <path d="M16 3v4" />
      <path d="M8 3v4" />
      <path d="M4 11h16" />
      <path d="M7 14h.013" />
      <path d="M10.01 14h.005" />
      <path d="M13.01 14h.005" />
      <path d="M16.015 14h.005" />
      <path d="M13.015 17h.005" />
      <path d="M7.01 17h.005" />
      <path d="M10.01 17h.005" />
    </svg>`
  },
  {
    key: 'random',
    title: 'Sort randomly',
    icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M3 7h14M7 3l4 4-4 4M17 17H3M13 21l-4-4 4-4" />
    </svg>`
  }
]
</script>
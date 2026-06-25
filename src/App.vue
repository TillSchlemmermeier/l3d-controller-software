<template>
  <div class="h-screen w-screen overflow-hidden flex bg-zinc-900">
    <nav>
      <PageNavigation />
    </nav>
    <main class="flex-1 w-full">
      <RouterView />
    </main>

    <!-- Blocking overlay until the very first successful connection -->
    <div v-if="!uiState.everConnected"
         class="fixed inset-0 flex items-center justify-center bg-zinc-800 z-50">
      <div class="text-center">
        <div class="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-green-500 mb-4 mx-auto"></div>
        <h2 class="text-xl text-white font-semibold">
          {{ uiState.connectionStatus === 'error'
            ? `Can't reach backend — retrying…`
            : 'Connecting to L3D Core…' }}
        </h2>
        <p v-if="uiState.connectionStatus === 'error' && uiState.connectionError"
           class="text-sm text-zinc-400 mt-2">{{ uiState.connectionError }}</p>
      </div>
    </div>

    <!-- Non-blocking banner: backend dropped after having been connected -->
    <div v-else-if="uiState.connectionStatus !== 'connected'"
         class="fixed top-0 inset-x-0 z-50 flex items-center justify-center gap-2 px-4 py-2 text-sm font-semibold text-white bg-red-600/90 shadow-lg">
      <span class="inline-block w-2 h-2 rounded-full bg-white animate-pulse"></span>
      <span v-if="uiState.connectionStatus === 'error'">Backend error: {{ uiState.connectionError }} — reconnecting…</span>
      <span v-else>Backend disconnected — reconnecting…</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import PageNavigation from './components/PageNavigation.vue'
import { useUiStateStore } from './stores/uiState'

const uiState = useUiStateStore()
</script>

<style scoped></style>

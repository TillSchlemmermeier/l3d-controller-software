<template>
  <div class="h-screen w-screen overflow-hidden flex bg-zinc-700">
    <!-- Loading Screen -->
    <div v-if="isLoading" 
         class="fixed inset-0 flex items-center justify-center bg-zinc-800 z-50">
      <div class="text-center">
        <div class="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-green-500 mb-4"></div>
        <h2 class="text-xl text-white font-semibold">{{ loadingStatus }}</h2>
      </div>
    </div>

    <!-- Main Content -->
    <template v-else>
      <nav class="bg-zinc-500">
        <PageNavigation />
      </nav>
      <main class="flex-1 w-full">
        <RouterView class="" />
      </main>
    </template>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { RouterView } from 'vue-router'
import PageNavigation from './components/PageNavigation.vue'

const isLoading = ref(false)
const loadingStatus = ref('Loading L3D...')

onMounted(async () => {
  console.log('App mounted')
  isLoading.value = false
})
</script>

<style scoped></style>
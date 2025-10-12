<template>
  <div class="fixed bottom-6 left-1/2 transform -translate-x-1/2 z-50">
    <div class="bg-zinc-800/90 backdrop-blur-lg rounded-2xl p-3 shadow-2xl border border-zinc-700/50">
      <div class="flex gap-8">
        <button
          v-for="(context, index) in contexts"
          :key="index"
          @click="selectContext(index)"
          class="relative group transition-all duration-300 ease-out"
          :class="[
            'w-20 h-20 rounded-xl flex items-center justify-center font-bold text-sm',
            isActive(index) 
              ? `${context.bg} ${context.text} shadow-lg scale-110 ring-2 ring-white/30` 
              : `${context.bgInactive} ${context.textInactive} hover:scale-105 hover:${context.bg}`
          ]"
        >
          <!-- Context Number -->
          <span class="relative z-10">{{ index + 1 }}</span>
          
          <!-- Active indicator -->
          <div 
            v-if="isActive(index)"
            class="absolute -top-1 -right-1 w-3 h-3 bg-white rounded-full shadow-md"
          />
          
          <!-- Ripple effect on click -->
          <div 
            v-if="isActive(index)"
            class="absolute inset-0 rounded-xl animate-ping opacity-20"
            :class="context.bg"
          />
        </button>
      </div>
      
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useUiStateStore } from '../../stores/uiState'
import { getAllContextColors } from '../../utils/colorSchemes'


const uiState = useUiStateStore()

const contexts = computed(() => getAllContextColors())

const isActive = (index: number) => uiState.contextIndex === index

const selectContext = (index: number) => {
  uiState.contextIndex = index
}
</script>
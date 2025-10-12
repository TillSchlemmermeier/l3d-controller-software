<template>
 <div class="h-screen w-[436px] bg-black">
    <div class="flex justify-around bg-zinc-800 pt-1">
      <button 
        @click="uiState.sidebarOption = 'console'"
        class="w-16 aspect-square flex items-center justify-center relative transition-all duration-200 ease-in-out rounded mx-1 active:scale-95"
        :class="[
          uiState.sidebarOption === 'console' 
            ? 'bg-zinc-500 shadow-lg scale-105'
            : 'bg-zinc-600'
        ]"
      >
        <div
          class="absolute top-0 h-1 w-full transition-all duration-200 rounded-l"
          :class="[
            uiState.sidebarOption === 'console'
              ? 'bg-amber-500'
              : 'bg-transparent'
          ]"
        ></div>
        <img
          :src="terminal"
          class="w-8 h-8 transition-transform duration-200"
          :class="[
            uiState.sidebarOption === 'console'
              ? 'opacity-100 scale-110 invert'
              : 'opacity-100'
          ]"
        />
      </button>
      
      <button 
        @click="uiState.sidebarOption = 'palette'"
        class="w-16 aspect-square flex items-center justify-center relative transition-all duration-200 ease-in-out rounded mx-1 active:scale-95"
        :class="[
          uiState.sidebarOption === 'palette' 
            ? 'bg-zinc-500 shadow-lg scale-105'
            : 'bg-zinc-600'
        ]"
      >
        <div
          class="absolute top-0 h-1 w-full transition-all duration-200 rounded-l"
          :class="[
            uiState.sidebarOption === 'palette'
              ? 'bg-amber-500'
              : 'bg-transparent'
          ]"
        ></div>
        <img
          :src="palette"
          class="w-8 h-8 transition-transform duration-200"
          :class="[
            uiState.sidebarOption === 'palette'
              ? 'opacity-100 scale-110 invert'
              : 'opacity-100'
          ]"
        />
      </button>

      <button 
        @click="uiState.sidebarOption = 'colors'"
        class="w-16 aspect-square flex items-center justify-center relative transition-all duration-200 ease-in-out rounded mx-1 active:scale-95"
        :class="[
          uiState.sidebarOption === 'colors' 
            ? 'bg-zinc-500 shadow-lg scale-105'
            : 'bg-zinc-600'
        ]"
      >
        <div
          class="absolute top-0 h-1 w-full transition-all duration-200 rounded-l"
          :class="[
            uiState.sidebarOption === 'colors'
              ? 'bg-amber-500'
              : 'bg-transparent'
          ]"
        ></div>
        <img
          :src="grid_view"
          class="w-8 h-8 transition-transform duration-200"
          :class="[
            uiState.sidebarOption === 'colors'
              ? 'opacity-100 scale-110 invert'
              : 'opacity-100'
          ]"
        />
      </button>
    </div>
    <div v-show="uiState.admin && uiState.sidebarOption === 'console'">
      <ConsoleOutput />
    </div>
    <div v-show="uiState.sidebarOption === 'palette'">
      <ColorManager />
    </div>
    <div v-show="uiState.sidebarOption === 'colors'">
      <ColorGallery />
    </div>
  </div>
</template>

<script setup lang="ts">
import ConsoleOutput from './ConsoleOutput.vue'
import ColorManager from './ColorManager/ColorManager.vue'
import ColorGallery from './GradientGallery/GradientGallery.vue'
import palette from '../../assets/icons/palette.svg'
import terminal from '../../assets/icons/terminal.svg'
import grid_view from '../../assets/icons/grid_view.svg'
import { useUiStateStore } from '../../stores/uiState'

const uiState = useUiStateStore()

</script>

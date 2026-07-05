<template>
  <div class="h-full flex flex-col py-4 w-16 bg-zinc-800">
    <button 
      v-for="(item, index) in menuItems" 
      :key="index"
      @click="handleClick(item)"
      class="w-full aspect-square flex items-center justify-center text-sm font-medium relative transition-all duration-200 ease-in-out rounded mx-1 mt-0.5 mb-20 active:scale-95"
      :class="[
        selectedItem === item.label 
          ? 'bg-zinc-500 shadow-lg scale-105'
          : 'bg-zinc-600'
      ]"
    >
      <div
        class="absolute left-0 w-1 h-full transition-all duration-200 rounded-l"
        :class="[
          selectedItem === item.label
            ? 'bg-amber-500'
            : 'bg-transparent'
        ]"
      ></div>
      <img
        :src="item.icon"
        class="w-10 h-10 transition-transform duration-200"
        :class="[
          selectedItem === item.label
            ? 'opacity-100 scale-110 invert'
            : 'opacity-100'
        ]"
      />
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { RouteNames } from '../router/RouteNames'
import { useUiStateStore } from '../stores/uiState'
import admin from '../assets/icons/admin.svg'
import home from '../assets/icons/home.svg'
import devices from '../assets/icons/devices.svg'

const uiState = useUiStateStore()
const router = useRouter()
const selectedItem = ref<string>('Home')

function handleClick(item: { label: string; action: () => void }) {
  selectedItem.value = item.label
  item.action()
}
const menuItems = computed(() => [
  { icon: home, label: 'Home', action: () => goTo(RouteNames.MAIN_PAGE) },
  ...(uiState.admin
    ? [{ icon: admin, label: 'Admin', action: () => goTo(RouteNames.ADMIN_VIEW) }]
    : []
  ),
  ...(uiState.admin
  ? [{ icon: devices, label: 'Remote', action: () => goTo(RouteNames.REMOTE_CONTROL) }]
  : []
),

])

function goTo(routeName: string) {
  router.push({ name: routeName })
}

</script>
<template>
  <div class="h-full flex flex-col py-4 w-16 justify-between bg-zinc-800">
    <button 
      v-for="(item, index) in menuItems" 
      :key="index"
      @click="handleClick(item)"
      class="w-full aspect-square flex items-center justify-center text-sm font-medium relative transition-all duration-200 ease-in-out rounded mx-1 my-0.5 active:scale-95"
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
import { useCoreStateStore } from '../stores/coreState'
import admin from '../assets/icons/admin.svg'
import io from '../assets/icons/io.svg'
import edit from '../assets/icons/edit.svg'
import home from '../assets/icons/home.svg'
import blank from '../assets/icons/blank.svg'
import midi_edit from '../assets/icons/midi_edit.svg'
import devices from '../assets/icons/devices.svg'
// import plumbing from '../assets/icons/plumbing.svg'

const uiState = useUiStateStore()
const coreState = useCoreStateStore()
const router = useRouter()
const selectedItem = ref<string>('Home')

function handleClick(item: { label: string; action: () => void }) {
  selectedItem.value = item.label
  item.action()
}
const menuItems = computed(() => [
  { icon: home, label: 'Home', action: () => goTo(RouteNames.MAIN_PAGE) },
  // { icon: coreState.shift_activated ? io : midi_edit, label: 'Select', action: () => goTo(RouteNames.MAIN_PAGE) },
  { icon: coreState.shift_activated ? io : midi_edit, label: 'Select', action: () => uiState.clickBehavior = 'select' },
  { icon: edit, label: 'Edit', action: () => uiState.clickBehavior = 'edit' },
  { icon: io, label: 'IO', action: () => uiState.clickBehavior = 'IO' },
  ...(uiState.admin
    ? [{ icon: admin, label: 'Admin', action: () => goTo(RouteNames.ADMIN_VIEW) }]
    : [{ icon: blank, label: 'Dummy', action: () => console.log('DUMMY CLICKED') }]
  ),
  ...(uiState.admin
  ? [{ icon: devices, label: 'Remote', action: () => goTo(RouteNames.REMOTE_CONTROL) }]
  : [{ icon: blank, label: 'Dummy', action: () => console.log('DUMMY CLICKED') }]
),
  { icon: blank, label: '2nd', action: () => goTo(RouteNames.SECOND_PAGE) },
  { icon: blank, label: 'Dummy2', action: () => console.log('DUMMY CLICKED') },
  { icon: blank, label: 'Dummy3', action: () => console.log('DUMMY CLICKED') },
  { icon: blank, label: 'Dummy4', action: () => console.log('DUMMY CLICKED') },
])

function goTo(routeName: string) {
  router.push({ name: routeName })
}

</script>
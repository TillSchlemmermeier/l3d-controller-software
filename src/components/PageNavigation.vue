<template>
  <div class="h-full flex flex-col py-4 w-14 justify-between">
    <button 
      v-for="(item, index) in menuItems" 
      :key="index"
      @click="handleClick(item)"
      class="w-full aspect-square flex items-center justify-center text-sm font-medium"
      :class="[
        selectedItem === item.label 
          ? 'bg-emerald-600 text-white' 
          : 'bg-zinc-500 '
      ]"
    >
      <img :src="item.icon" class="w-12 h-12"/>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { RouteNames } from '../router/RouteNames'
import { useSharedVariablesStore } from '../stores/sharedVariables'
import admin from '../assets/icons/admin.svg'
import io from '../assets/icons/io.svg'
import edit from '../assets/icons/edit.svg'
import home from '../assets/icons/home.svg'
import blank from '../assets/icons/blank.svg'
import midi_edit from '../assets/icons/midi_edit.svg'

const sharedVariables = useSharedVariablesStore()
const router = useRouter()
const selectedItem = ref<string>('Home')

function handleClick(item: { label: string; action: () => void }) {
  selectedItem.value = item.label
  item.action()
}
const menuItems = [
  { icon: home, label: 'Home', action: () => goTo(RouteNames.MAIN_PAGE) },
  { icon: midi_edit, label: 'Select', action: () => sharedVariables.clickBehavior = 'select' },
  { icon: edit, label: 'Edit', action: () => sharedVariables.clickBehavior = 'edit' },
  { icon: io, label: 'IO', action: () => sharedVariables.clickBehavior = 'IO' },
  { icon: admin, label: 'Admin', action: () => goTo(RouteNames.ADMIN_VIEW) },
  { icon: blank, label: '2nd', action: () => goTo(RouteNames.SECOND_PAGE) },
  { icon: blank, label: 'Dummy', action: () => console.log('DUMMY CLICKED') },
  { icon: blank, label: 'Dummy', action: () => console.log('DUMMY CLICKED') },
  { icon: blank, label: 'Dummy', action: () => console.log('DUMMY CLICKED') },
  { icon: blank, label: 'Dummy', action: () => console.log('DUMMY CLICKED') },
]

function goTo(routeName: string) {
  router.push({ name: routeName })
}

</script>

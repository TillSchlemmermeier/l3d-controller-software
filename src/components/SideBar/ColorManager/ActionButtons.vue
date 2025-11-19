<template>
  <div class="absolute bottom-2 right-4 flex flex-row gap-4">
    <button
      v-if="uiState.admin"
      @click="showSubtypePicker = !showSubtypePicker"
      class="py-4 px-6 w-24 bg-zinc-800 text-white font-medium rounded-md flex items-center justify-center gap-2"
    >
      Save
    </button>
    <button
      @click="emit('reset')"
      class="py-4 px-6 w-24 bg-zinc-800 text-white font-medium rounded-md flex items-center justify-center gap-2"
    >
      Reset Settings
    </button>
    <button
      @click="emit('clear')"
      class="py-4 px-6 w-24 bg-zinc-800 text-white font-medium rounded-md flex items-center justify-center gap-2"
    >
      Clear Gradient
    </button>
  </div>

  <!-- Subtype Picker -->
  <div 
    v-if="showSubtypePicker"
    class="absolute bottom-17 right-4 bg-zinc-800 rounded-md shadow-lg p-4 z-50 w-80 subtype-picker"
  >
    <div class="mb-2 text-sm font-bold text-zinc-300">Select a Subtype:</div>

    <!-- Subtype Input -->
    <div class="mb-3 flex gap-2">
      <input
        v-model="newSubtype"
        @keyup.enter="addSubtype"
        placeholder="Add new subtype"
        class="flex-1 px-3 py-2 bg-zinc-700 text-zinc-200 rounded border border-zinc-600 focus:border-blue-500 focus:outline-none"
      />
      <button
        @click="addSubtype"
        class="px-3 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
      >
        Add
      </button>
    </div>

    <ul>
      <li
        v-for="subtype in subtypes"
        :key="subtype"
        @click="handlePresetSave(subtype)"
        class="cursor-pointer px-3 py-2 rounded hover:bg-blue-500 hover:text-white transition-all mb-1"
      >
        {{ subtype }}
      </li>
    </ul>
  </div>

</template>

<script setup lang="ts">
import { computed, ref, watch, onUnmounted } from 'vue'
import { useUiStateStore } from '../../../stores/uiState'
import { GradientPreset } from '../../../types/types'

const uiState = useUiStateStore()

const emit = defineEmits<{
  (e: 'clear'): void
  (e: 'reset'): void
  (e: 'save', collection: string): void
}>()

const showSubtypePicker = ref(false)
const newSubtype = ref('')

const computedSubtypes = computed(() => {
  const customGradients = (uiState.gradientPresets as GradientPreset[]).filter(g => g.type === 'custom')
  return [...new Set(customGradients.map(g => g.subtype || 'No Subtype'))].sort()
})

const subtypes = ref<string[]>([])

// Sync subtypes with computedSubtypes
watch(computedSubtypes, (newVal) => {
  subtypes.value = [...newVal]
}, { immediate: true })

// Close picker when clicking outside
function handleOutsideClick(event: MouseEvent) {
  const picker = document.querySelector('.subtype-picker')
  if (picker && !picker.contains(event.target as Node)) {
    showSubtypePicker.value = false
  }
}
watch(showSubtypePicker, (visible) => {
  if (visible) {
    document.addEventListener('mousedown', handleOutsideClick)
  } else {
    document.removeEventListener('mousedown', handleOutsideClick)
  }
})
onUnmounted(() => {
  document.removeEventListener('mousedown', handleOutsideClick)
})

function addSubtype() {
  if (newSubtype.value.trim() && !subtypes.value.includes(newSubtype.value.trim())) {
    subtypes.value.push(newSubtype.value.trim())
    newSubtype.value = ''
  }
}

function handlePresetSave(subtype: string) {
  emit('save', subtype)
  showSubtypePicker.value = false
}
</script>
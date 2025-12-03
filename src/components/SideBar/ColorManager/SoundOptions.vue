<template>
  <div class="mt-6">
    <div class="text-xs text-zinc-400 uppercase font-bold tracking-wider mb-3">
      Sound to Light
    </div>
    <div class="grid grid-cols-5 gap-2">
      <button
        v-for="option in availableOptions"
        :key="option.value"
        @click="toggleOption(option.value)"
        class="px-2 py-3 rounded text-xs font-bold uppercase tracking-wider active:scale-95 transition"
        :class="selectedOptions.includes(option.value)
          ? 'bg-zinc-800 text-zinc-200 ring-2 ring-zinc-500'
          : 'bg-zinc-800 text-zinc-400'"
      >
        {{ option.label }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

interface SoundOption {
  value: string
  label: string
}

const availableOptions: SoundOption[] = [
  { value: 'startVal', label: 'Start Value' },
  { value: 'endVal', label: 'End Value' },
  { value: 'startSat', label: 'Start Sat' },
  { value: 'endSat', label: 'End Sat' },
  { value: 'regionWidth', label: 'Region Width' },
  { value: 'regionStart', label: 'Region Start' },
  { value: 'speed', label: 'Speed' },
  { value: 'rotateY', label: 'Rotate Y' },
  { value: 'rotateZ', label: 'Rotate Z' },
]

interface Props {
  modelValue: string[]
}

interface Emits {
  (e: 'update:modelValue', value: string[]): void 
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const selectedOptions = ref<string[]>(Array.isArray(props.modelValue) ? [...props.modelValue] : [])

watch(() => props.modelValue, (newValue) => {
  selectedOptions.value = Array.isArray(newValue) ? [...newValue] : []
}, { deep: true })

function toggleOption(value: string) {
  const index = selectedOptions.value.indexOf(value)
  if (index > -1) {
    selectedOptions.value.splice(index, 1)
  } else {
    selectedOptions.value.push(value)
  }
  emit('update:modelValue', selectedOptions.value)
}
</script>
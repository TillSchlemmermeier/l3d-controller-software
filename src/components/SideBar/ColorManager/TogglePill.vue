<template>
  <div class="relative flex bg-zinc-800 rounded-md p-1 w-full max-w-md mx-auto">
    <!-- Animated pill background -->
    <div
      class="absolute top-1 h-[calc(100%-0.5rem)] bg-white rounded transition-all duration-300"
      :style="{
        width: `calc(${100 / options.length}% - 0.5rem)`,
        left: `calc(${selectedIndex * (100 / options.length)}% + 0.25rem`
      }"
    ></div>
    <!-- Buttons -->
    <button
      v-for="option in options"
      :key="option.value"
      class="flex-1 py-4 px-3 text-sm font-medium rounded transition-all relative z-10 flex items-center justify-center gap-2"
      :class="modelValue === option.value ? 'text-zinc-900' : 'text-zinc-400 hover:text-white'"
      @click="$emit('update:modelValue', option.value)"
    >
      <slot :option="option" :selected="modelValue === option.value">{{ option.label }}</slot>
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Option<T> {
  value: T
  label: string
}

const props = defineProps<{
  options: Option<any>[]
  modelValue: any
}>()

defineEmits<{ (e: 'update:modelValue', value: any): void }>()

const selectedIndex = computed(() =>
  props.options.findIndex(opt => opt.value === props.modelValue)
)
</script>
<template>
  <div class="flex flex-col gap-2 w-full">
    <div class="flex justify-between text-zinc-400 text-sm font-medium uppercase tracking-wider">
      <span>{{ label }}</span>
      <span>{{ Math.round(modelValue * 100) }}%</span>
    </div>
    <input 
      type="range" 
      min="0" 
      max="1" 
      step="0.01"
      :value="modelValue"
      @input="updateValue"
      @mousedown="$emit('startSliding')"
      @touchstart="$emit('startSliding')"
      @mouseup="$emit('stopSliding')"
      @touchend="$emit('stopSliding')"
       class="w-full h-12 appearance-none bg-transparent cursor-pointer touch-none
[&::-webkit-slider-runnable-track]:h-2 [&::-webkit-slider-runnable-track]:rounded-full [&::-webkit-slider-runnable-track]:bg-zinc-800
[&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:h-7 [&::-webkit-slider-thumb]:w-7 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-white [&::-webkit-slider-thumb]:-mt-2.5 [&::-webkit-slider-thumb]:shadow-[0_2px_6px_rgba(0,0,0,0.3)]
[&::-moz-range-track]:h-2 [&::-moz-range-track]:rounded-full [&::-moz-range-track]:bg-zinc-800
[&::-moz-range-thumb]:h-7 [&::-moz-range-thumb]:w-7 [&::-moz-range-thumb]:rounded-full [&::-moz-range-thumb]:bg-white [&::-moz-range-thumb]:border-none [&::-moz-range-thumb]:shadow-[0_2px_6px_rgba(0,0,0,0.3)]"
    />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  label: string
  modelValue: number
}>()

const emit = defineEmits(['update:modelValue', 'startSliding', 'stopSliding'])

function updateValue(e: Event) {
  const val = parseFloat((e.target as HTMLInputElement).value)
  emit('update:modelValue', val)
  if (navigator.vibrate) navigator.vibrate(5) // Tiny tick feedback
}
</script>

<style scoped>
</style>
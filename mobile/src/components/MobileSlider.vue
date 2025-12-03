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
      class="w-full h-12 appearance-none bg-transparent cursor-pointer touch-none"
    />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  label: string
  modelValue: number
}>()

const emit = defineEmits(['update:modelValue'])

function updateValue(e: Event) {
  const val = parseFloat((e.target as HTMLInputElement).value)
  emit('update:modelValue', val)
  if (navigator.vibrate) navigator.vibrate(5) // Tiny tick feedback
}
</script>

<style scoped>
input[type=range]::-webkit-slider-runnable-track {
  background: #27272a; /* zinc-800 */
  height: 8px;
  border-radius: 999px;
}

input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none;
  height: 28px;
  width: 28px;
  border-radius: 50%;
  background: white;
  margin-top: -10px; /* center on track */
  box-shadow: 0 2px 6px rgba(0,0,0,0.3);
}
</style>
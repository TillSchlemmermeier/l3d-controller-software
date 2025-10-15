<template>
  <Transition
    enter-active-class="transition-opacity duration-300"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="transition-opacity duration-300"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div 
      v-if="show"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
      @click="$emit('close')"
    >
      <div class="bg-zinc-800 p-6 rounded-lg shadow-xl max-w-md">
        <p class="text-lg text-zinc-200">
          {{ message }}
        </p>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
defineProps<{
  show: boolean
  message: string
}>()

defineEmits<{
  close: []
}>()
</script>
<template>
  <div 
    class="w-3/4 mx-auto"
  >
    <div class="flex flex-col items-center gap-4">
      <input
        v-model="presetName"
        @keydown.enter.prevent="$emit('save', presetName)"
        class="9672 px-3 py-2 text-3xl text-center rounded-lg bg-zinc-700 border border-zinc-600 text-zinc-200"
      />
      <SimpleKeyboard
        :input="presetName"
        @onChange="updateSaveName"
        @save="$emit('save', presetName)"
      />
      <button 
        @click="$emit('cancel')"
        class="absolute w-28 bottom-10 right-10 bg-zinc-700 aspect-square rounded-lg hover:bg-zinc-600"
      >
        <span class="text-m text-center font-semibold text-zinc-200 break-words w-full ">
          Cancel
        </span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import SimpleKeyboard from './SimpleKeyboard.vue'

defineEmits<{
  (e: 'cancel'): void
  (e: 'save', value: string): void
}>()

const presetName = ref('TYPE NAME')

function updateSaveName(input: string) {
  presetName.value = input
}
</script>
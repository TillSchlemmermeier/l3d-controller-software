<template>
  <div 
    v-if="show" 
    class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
    @click="$emit('close')"
  >
    <div 
      @click.stop
      class="bg-zinc-800 p-6 rounded-lg w-96 space-y-4"
    >
      <h3 class="text-lg font-bold">Add New {{ elementType }}</h3>
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="block text-sm text-zinc-400 mb-1">Name</label>
          <input
            v-model="elementName"
            type="text"
            class="w-full bg-zinc-700 px-3 py-2 rounded-lg text-white"
            :placeholder="`${elementType.toLowerCase()}_name`"
            ref="inputRef"
            @keyup.esc="$emit('close')"
          />
        </div>
        <div class="flex justify-end gap-6">
          <button
            type="button"
            class="px-6 py-4 rounded-lg bg-zinc-700 hover:bg-zinc-600"
            @click="$emit('close')"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="px-6 py-4 rounded-lg bg-emerald-600 hover:bg-emerald-500"
          >
            Add
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'

const props = defineProps<{
  show: boolean
  elementType: string
}>()

const emit = defineEmits<{
  close: []
  add: [name: string]
}>()

const elementName = ref('')
const inputRef = ref<HTMLInputElement | null>(null)

function handleSubmit() {
  if (elementName.value.trim()) {
    emit('add', elementName.value.trim())
    elementName.value = ''
  }
}

watch(() => props.show, async (newValue) => {
  if (newValue) {
    await nextTick()
    inputRef.value?.focus()
  } else {
    elementName.value = ''
  }
})
</script>
<template>
  <div class="flex flex-col h-full">
    <!-- Top Section: Image and Info (fixed, no scroll) -->
    <div class="flex-shrink-0 space-y-3">
      <div class="w-52 h-48 mt-2 rounded-lg overflow-hidden mx-auto">
        <img 
          :src="`src/assets/previews/${displayName}_p_${presetInfo.name}.gif`"
          :key="`${displayName}-${presetInfo.name}`"
          class="w-full h-full object-cover"
          @error="handleImageError"
          loading="lazy"
        />
      </div>
      <div>
        <span class="text-zinc-400">Name:</span>
        <span class="font-medium ml-2">{{ presetInfo.name }}</span>
      </div>
      <div>
        <span class="text-zinc-400">Element:</span>
        <span class="font-medium ml-2">{{ presetInfo.elementName }}</span>
      </div>
      <div>
        <span class="text-zinc-400">Created:</span>
        <span class="font-medium ml-2">{{ formattedDate }}</span>
      </div>
      <div>
        <span class="text-zinc-400">Usage Count:</span>
        <span class="font-medium ml-2">{{ presetInfo.usageCount || 0 }}</span>
      </div>
    </div>

    <!-- Data Section: Grows to fill space, scrollable -->
    <div class="flex flex-col flex-grow border-t border-zinc-700 pt-3 mt-3 overflow-hidden">
      <h4 class="flex-shrink-0 text-zinc-400 font-medium mb-2">Data</h4>
      <pre class="flex-grow font-medium text-wrap bg-zinc-900 p-2 rounded text-xs overflow-y-auto max-w-full scrollbar-thin scrollbar-track-transparent scrollbar-thumb-zinc-500/50 hover:scrollbar-thumb-zinc-500/70 scrollbar-thumb-rounded-full scrollbar-track-rounded-full">{{ formatValue(presetInfo.data) }}</pre>
    </div>

    <!-- Actions: Fixed at bottom -->
    <div v-if="presetInfo.name !== 'basic'" class="flex-shrink-0 space-y-2 pt-2 border-t border-zinc-700">
      <button class="w-full text-left">
        <span class="text-zinc-400">Delete Preset</span>
        <span 
          class="font-medium ml-2 text-red-500 hover:text-red-400 transition-colors cursor-pointer"
          @click="$emit('delete')"
        >
          DELETE
        </span>
      </button>
      <button class="w-full text-left">
        <span class="text-zinc-400">Rename Preset</span>
        <span 
          class="font-medium ml-2 text-emerald-500 hover:text-emerald-400 transition-colors cursor-pointer"
          @click="showRename = true"
        >
          RENAME
        </span>
      </button>
      <input 
        v-if="showRename" 
        type="text" 
        v-model="newName"
        class="w-full bg-zinc-700 px-3 py-2 rounded-lg text-white"
        placeholder="New Preset Name"
        @keyup.enter="handleRename"
        @keyup.esc="showRename = false"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
// Script remains unchanged
import { ref, computed } from 'vue'
import { useUiStateStore } from '../../stores/uiState'

const uiState = useUiStateStore()

const presetInfo = computed(() => uiState.presetInfo)
const elementName = computed(() => uiState.selectedElement)
const elementType = computed(() => uiState.elementType)

const displayName = computed(() => {
  return ['generator', 'effect'].includes(elementType.value) ? elementName.value : elementType.value
})

const emit = defineEmits<{
  delete: []
  rename: [name: string]
}>()

const imageError = ref(false)
const showRename = ref(false)
const newName = ref('')

const formattedDate = computed(() => 
  new Date(presetInfo.value.created).toLocaleDateString()
)

function formatValue(obj: any): string {
  function formatRecursive(value: any, indent: string = ''): string {
    if (Array.isArray(value)) {
      // Custom formatting for arrays: no breaks after each comma, but newline after every 4th item
      if (value.length === 0) return '[]'
      let formatted = '['
      value.forEach((item, index) => {
        if (index > 0) {
          formatted += ', '
          if (index % 4 === 0) {
            formatted += '\n' + indent + '  '  // Indent after every 4th item
          }
        }
        formatted += formatRecursive(item, indent + '  ')
      })
      formatted += ']'
      return formatted
    } else if (typeof value === 'object' && value !== null) {
      // Pretty-print objects
      const entries = Object.entries(value)
      if (entries.length === 0) return '{}'
      let formatted = '{\n'
      entries.forEach(([key, val], index) => {
        formatted += indent + '  "' + key + '": ' + formatRecursive(val, indent + '  ')
        if (index < entries.length - 1) formatted += ','
        formatted += '\n'
      })
      formatted += indent + '}'
      return formatted
    } else {
      // Primitives
      return JSON.stringify(value)
    }
  }
  return formatRecursive(obj)
}

function handleImageError() {
  imageError.value = true
}

function handleRename() {
  if (newName.value.trim()) {
    emit('rename', newName.value.trim())
    newName.value = ''
    showRename.value = false
  }
}
</script>
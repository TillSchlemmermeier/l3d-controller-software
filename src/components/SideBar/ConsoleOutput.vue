<template>
  <div class="h-full console-widget bg-zinc-900 text-zinc-400 font-mono text-xs p-4 rounded-lg flex flex-col">
    <div class="flex justify-between mb-2">
      <h3 class="text-zinc-400">Console Output</h3>
      <button @click="clearOutput" class="text-zinc-500 hover:text-zinc-300">Clear</button>
    </div>
    <div ref="consoleContainer" class="flex-1 flex flex-col overflow-y-auto no-scrollbar">
      <div v-for="(line, index) in consoleLines"
           :key="index"
           :class="{'text-red-400': line.type === 'stderr'}"
           class="break-all shrink-0"
      >
        {{ line.data }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { useUiStateStore } from '../../stores/uiState'

const MAX_LINES = 300

const uiState = useUiStateStore()
const consoleLines = ref<Array<{type: string, data: string}>>([])

// An error while the console is out of sight flags the tab in the sidebar
const visible = computed(() => uiState.admin && uiState.sidebarOption === 'console')
watch(visible, (shown) => { if (shown) uiState.consoleError = false })
const consoleContainer = ref<HTMLElement | null>(null)

// The lines scroll so keeping the newest one in view is a scroll to the bottom.
async function handleConsoleOutput(_: any, data: {type: string, data: string}) {
  consoleLines.value.push(data)
  if (data.type === 'stderr' && !visible.value) uiState.consoleError = true
  if (consoleLines.value.length > MAX_LINES) {
    consoleLines.value = consoleLines.value.slice(-MAX_LINES)
  }

  await nextTick()

  const container = consoleContainer.value
  if (container) container.scrollTop = container.scrollHeight
}

function clearOutput() {
  consoleLines.value = []
}

let disposePythonOutput: (() => void) | null = null

onMounted(() => {
  disposePythonOutput = window.ipcRenderer.onPythonOutput(handleConsoleOutput)
})

onUnmounted(() => {
  disposePythonOutput?.()
})
</script>

<style scoped>
.no-scrollbar {
  scrollbar-width: none;
}
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
</style>

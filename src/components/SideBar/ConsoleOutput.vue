<template>
  <div class="h-[1395px] console-widget bg-zinc-900 text-zinc-400 font-mono text-xs p-4 rounded-lg flex flex-col">
    <div class="flex justify-between mb-2">
      <h3 class="text-zinc-400">Console Output</h3>
      <button @click="clearOutput" class="text-zinc-500 hover:text-zinc-300">Clear</button>
    </div>
    <div ref="consoleContainer" class="flex-1 flex flex-col overflow-hidden">
      <div v-for="(line, index) in visibleLines" 
           :key="index" 
           :class="{'text-red-400': line.type === 'stderr'}"
           class="break-all"
           ref="lineRefs"
      >
        {{ line.data }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'

const consoleLines = ref<Array<{type: string, data: string}>>([])
const consoleContainer = ref<HTMLElement | null>(null)
const lineRefs = ref<HTMLElement[]>([])
const visibleLines = ref<Array<{type: string, data: string}>>([])

async function handleConsoleOutput(_: any, data: {type: string, data: string}) {
  consoleLines.value.push(data)
  visibleLines.value = [...consoleLines.value]
  
  await nextTick()
  
  if (!consoleContainer.value) return
  
  const containerHeight = consoleContainer.value.clientHeight
  let totalHeight = 0
  
  // Calculate height from newest to oldest
  for (let i = lineRefs.value.length - 1; i >= 0; i--) {
    totalHeight += lineRefs.value[i].offsetHeight
    
    // If content exceeds container, remove older lines
    if (totalHeight > containerHeight) {
      consoleLines.value = consoleLines.value.slice(i + 1)
      visibleLines.value = [...consoleLines.value]
      break
    }
  }
}

function clearOutput() {
  consoleLines.value = []
  visibleLines.value = []
}

let disposePythonOutput: (() => void) | null = null

onMounted(() => {
  disposePythonOutput = window.ipcRenderer.onPythonOutput(handleConsoleOutput)
})

onUnmounted(() => {
  disposePythonOutput?.()
})
</script>
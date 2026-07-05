<template>
  <div class="p-4 bg-zinc-800 rounded-lg">
    <div class="flex flex-wrap gap-2 justify-center mt-3">
      <div 
        v-for="(frame, index) in frames" 
        :key="index"
        class="relative w-22 h-22 cursor-pointer"
        @click="selectFrame(index)"
      >
        <img 
          :src="frame" 
          class="w-full h-full object-cover rounded"
          :class="{
            'border-2 border-blue-500': index === selectedStart,
            'border-2 border-green-500': index === selectedEnd,
            'opacity-50': index < selectedStart || index > selectedEnd
          }"
        />
        <span class="absolute bottom-0 right-0 text-xs bg-black/50 text-white px-1 rounded">
          {{ index }}
        </span>
      </div>
    </div>
    
    <!-- Show recording status -->
    <div v-if="isRecording" class="text-zinc-200 text-lg text-center mt-2">
      Recording frames: {{ frames.length }} / 120
    </div>


    <div class="mt-6 flex justify-around">
      <div class="flex gap-4">
        <div>
          <label class="ml-12 text-center font-semibold text-zinc-200 break-words w-full mr-2">Start Frame:</label>
          <input 
            type="number" 
            v-model="selectedStart" 
            :max="selectedEnd"
            min="0"
            class="mt-6 w-16 px-2 py-1 bg-zinc-700 rounded text-zinc-200 font-semibold"
          />
        </div>
        <div>
          <label class="text-center font-semibold text-zinc-200 break-words w-full mr-2">End Frame:</label>
          <input 
            type="number" 
            v-model="selectedEnd"
            :min="selectedStart"
            :max="frames.length - 1"
            class="mt-6 w-16 px-2 py-1 bg-zinc-700 rounded text-zinc-200 font-semibold"
          />
        </div>
      </div>
      <div class="flex items-end mr-10 gap-4">
        <button 
          v-if="isRecording"
          @click="$emit('stopCapture')"
          class="w-24 aspect-square bg-red-600 rounded hover:bg-red-500 text-white font-medium"
        >
          Stop Recording
        </button>
        <button 
          @click="$emit('cancel')"
          class="w-24 px-4 py-2 bg-zinc-700 aspect-square rounded hover:bg-zinc-600"
        >
          <span class="text-center font-semibold text-zinc-200 break-words w-full ">
            Cancel
          </span>
        </button>
        <button 
          @click="$emit('create', selectedStart, selectedEnd, false)"
          :disabled="isSaveDisabled"
          class="w-24 px-4 py-2 bg-zinc-700 aspect-square rounded hover:bg-zinc-600"
        >
          <span class="text-center font-semibold text-zinc-200 break-words w-full ">
            Save without GIF
          </span>
        </button>
        <button 
          @click="$emit('create', selectedStart, selectedEnd)"
          class="w-24 px-4 py-2 bg-blue-600 aspect-square rounded hover:bg-blue-500"
        >
          <span class="text-center font-semibold text-zinc-200 break-words w-full">
            Save Preset
          </span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'

const props = defineProps<{
  frames: string[]
  isRecording?: boolean
}>()

const selectedStart = ref(0)
const selectedEnd = ref(props.frames.length - 1)
const isSelectingStart = ref(true)
const isSaveDisabled = ref(true)

watch(
  () => props.frames.length,
  (newLength) => {
    if (props.isRecording) {
      selectedEnd.value = newLength - 1
    }
  }
)

function selectFrame(index: number) {
  if (isSelectingStart.value) {
    // First click - set start frame
    selectedStart.value = index
    isSelectingStart.value = false
  } else {
    // Second click - set end frame
    if (index >= selectedStart.value) {
      selectedEnd.value = index
    } else {
      // If clicked before start frame, swap start and end
      selectedEnd.value = selectedStart.value
      selectedStart.value = index
    }
    isSelectingStart.value = true
  }
}

onMounted(() => {
  // Enable the save button after a short delay to prevent accidental clicks
  setTimeout(() => {
    isSaveDisabled.value = false
  }, 500)  // 500ms delay
})

defineEmits<{
  (e: 'create', startFrame: number, endFrame: number, gif?: boolean): void
  (e: 'cancel'): void
  (e: 'stopCapture'): void
}>()
</script>
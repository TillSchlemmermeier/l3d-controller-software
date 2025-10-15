<template>
  <div 
    class="fixed inset-0 z-50"
    @click.self="close"
    >
    <Transition 
      name="slide"
      appear
      enter-active-class="transition ease-out duration-300"
      enter-from-class="translate-y-full"
      enter-to-class="translate-y-0"
      leave-active-class="transition ease-in duration-300"
      leave-from-class="translate-y-0"
      leave-to-class="translate-y-full"
    >
      <div 
        v-if="showDialog"
        class="fixed bottom-0 left-0 right-0"
      >
        <div class="bg-zinc-400 shadow-up w-full rounded-t-xl">

          <DialogHeader
            @close="close"
          />

          <!-- Save confirmation lightbox -->
          <div v-if="isSuccess" 
            class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
            <div class="bg-zinc-800 border-emerald-700 border-3 text-emerald-600 text-2xl px-6 py-4 rounded-lg shadow-xl">
              Preset saved successfully!
            </div>
          </div>
          
          <div class="p-6">
            <FrameSelector
              v-if="showFrameSelector"
              :frames="capturedFrames"
              :is-recording="isRecording"
              @create="savePreset"
              @cancel="cancelGifCreation"
              @stopCapture="stopRecording"
              @toggleKeyboard="toggleKeyboard"
            />

            <PresetGallery
              v-if="showPresets"
              @select="loadPreset($event)"
            />

            <ElementsGrid
              v-if="showElements"
              :new-channel="newChannel"
              @select="fetchPresets"
              @load="loadPreset"
              @changeType="newChannelTypeSwitch"
              @toggleKeyboard="toggleKeyboard"
            />
            
            <Keyboard
              v-if="showKeyboard"
              @save="handleKeyboardSave"
              @cancel="cancelPresetSaving"
            />
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useCoreStateStore } from '../../stores/coreState'
import { useUiStateStore } from '../../stores/uiState'
import DialogHeader from './Header.vue'
import PresetGallery from './PresetGallery.vue'
import ElementsGrid from './ElementsGrid.vue'
import Keyboard from './Keyboard.vue'
import FrameSelector from './FrameSelector.vue'
import { createGIF } from 'gifshot'

const props = defineProps({
  channelPreviewRef: {
    type: Object,
    required: false,
    default: null
  }
})
const coreState = useCoreStateStore()
const uiState = useUiStateStore()

const showDialog = ref(true)
const showElements = ref(true)
const showPresets = ref(false)
const showKeyboard = ref(false)
const showFrameSelector = ref(false)

const presetName = ref('')
const newChannel = ref(false)
const isRecording = ref(false)
const capturedFrames = ref<string[]>([])
const isSuccess = ref(false)

const emit = defineEmits(['close'])

const close = () => {
  uiState.selectedElement = ''
  showDialog.value = false
  setTimeout(() => emit('close'), 300) // Wait for animation to complete
}

function toggleKeyboard () {
  showElements.value = false
  showPresets.value = false
  showKeyboard.value = !showKeyboard.value
}

function cancelPresetSaving() {
  showKeyboard.value = false
  showElements.value = true
}

function cancelGifCreation() {
  showFrameSelector.value = false
  showElements.value = true
}

function handleKeyboardSave(name: string) {
  presetName.value = name
  recordGif()
}

async function loadPreset(preset_name: string) {
  if (preset_name) {
    await coreState.load(preset_name)
    if (uiState.elementType === 'effect') {
      await coreState.select(0, uiState.channelIndex, uiState.effectIndex)
    } else if (uiState.elementType === 'generator' || uiState.elementType === 'channel') {
      await coreState.select(0, uiState.channelIndex, 9)
    } else if (uiState.elementType === 'global') {
      await coreState.select(0, 0, 9)
    }
    setTimeout(() => close(), 50)
  }
}

async function recordGif() {
  console.log('channelPreviewRef:', props.channelPreviewRef) // Add this line
  showKeyboard.value = false
  isRecording.value = true
  showFrameSelector.value = true
  capturedFrames.value = []

  if (uiState.elementType === 'global') {
    capturedFrames.value = await props.channelPreviewRef.captureCombinedView(
      (frame: string) => {
        capturedFrames.value.push(frame)
      }
    )
  } else {
    const channelIndex = uiState.channelIndex
    console.log('Channel index:', channelIndex)
    
    try {
      // Pass callback to handle new frames
      capturedFrames.value = await props.channelPreviewRef.captureFrames(
        channelIndex,
        (frame: string) => {
          capturedFrames.value.push(frame)
        }
      )
    } catch (error) {
      console.error('Failed to capture frames:', error)
    }
  }
  isRecording.value = false
}

function stopRecording() {
  if (props.channelPreviewRef) {
    props.channelPreviewRef.stopCapture()
  }
}

async function savePreset(startFrame: number, endFrame: number, gif: boolean = true) {
  try {
    // event?.preventDefault()
    console.log('Creating GIF from frames:', startFrame, endFrame)
    let gifData: string = ''

    if (gif) {
      // Select frames and create GIF
      const selectedFrames = capturedFrames.value.slice(startFrame, endFrame + 1)
      gifData = await new Promise<string>((resolve, reject) => {
        createGIF({
          images: selectedFrames,
          gifWidth: 170,
          gifHeight: 170,
          interval: 0.06,
          sampleInterval: 10,
          repeat: 0
        }, (obj: any) => {
          if (!obj.error) {
            resolve(obj.image)
          } else {
            reject(obj.error)
          }
        })
      })
    }

    // Save the Preset
    const response = await coreState.save(presetName.value, gifData)
    console.log(response)
    if (response.status == 200) { 
      console.log('Save successful:', response.message)
      showFrameSelector.value = false
      isSuccess.value = true
      // Auto-hide success message after 1 second
      setTimeout(() => {
        isSuccess.value = false
        close()
      }, 1000)
    } else if (response.status === 409) { // Conflict status
      // Show confirmation dialog
      const confirmOverwrite = await window.confirm(
        `A preset named "${presetName.value}" already exists. Do you want to overwrite it?`
      )
      
      if (confirmOverwrite) {
        // Try saving again with force flag
        const overwriteResponse = await coreState.save(presetName.value, gifData, true)
        if (overwriteResponse.status === 200) {
          showFrameSelector.value = false
          isSuccess.value = true
          setTimeout(() => {
            isSuccess.value = false
            close()
          }, 1000)
        }
      } else {
        console.error('Save failed:', response.message)
      }
    }
  } catch (error) {
    console.error('Failed to create GIF:', error)
  }
}

async function fetchPresets(element: string) {
  if (element === uiState.selectedElement) {
    loadPreset('basic')
    close()
  } else {
    uiState.selectedElement = element
    await uiState.fetchPresets()
    showPresets.value = true
  }
}

function newChannelTypeSwitch() {
  if (uiState.elementType === 'generator') {
    uiState.elementType = 'channel'
    showPresets.value = false
  } else if (uiState.elementType === 'channel') {
    uiState.elementType = 'generator'
  }
  populateOverlayElements()
}

async function populateOverlayElements() {
  if (uiState.elementType === 'newChannel') {
    uiState.elementType = 'generator'
    newChannel.value = true
  }
  if (uiState.elementType === 'generator' || uiState.elementType === 'effect') {
    await uiState.fetchActiveElements()
  } else {
    uiState.selectedElement = 'presets'
    await uiState.fetchPresets()
  }
}

onMounted(async () => {
  populateOverlayElements()
})

</script>

<style scoped>
</style>

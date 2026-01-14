<template>
  <!-- <div class="p-4 bg-zinc-800 rounded-lg border border-zinc-700 text-white">
    <div class="flex flex-col gap-2 text-sm">
      <div class="flex items-center gap-2">
        <div :class="['w-3 h-3 rounded-full', isConnected ? 'bg-green-500' : 'bg-red-500']"></div>
        <span>{{ statusMessage }}</span>
        <span v-if="isConnected" class="text-xs text-zinc-400">({{ uiState.launchPadMode }})</span>
      </div>
      <div v-if="lastMessage" class="font-mono bg-zinc-900 p-2 rounded text-xs">
        Last Input: {{ lastMessage }}
      </div>
    </div>
  </div> -->
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import { useCoreStateStore } from '../../stores/coreState'
import { useUiStateStore } from '../../stores/uiState'
import { launchpadModes, SYSEX_HEADER, SYSEX_END, LaunchpadContext, COLORS } from '../../utils/launchpad'

const coreState = useCoreStateStore()
const uiState = useUiStateStore()

const isConnected = ref(false)
const statusMessage = ref('Initializing MIDI...')
const lastMessage = ref('')
const gridState = ref<number[][]>(Array(8).fill(0).map(() => Array(8).fill(0)))

let midiAccess: MIDIAccess | null = null
let inputPort: MIDIInput | null = null
let outputPort: MIDIOutput | null = null

const DEVICE_NAME_SUBSTRING = 'Launchpad Mini MK3'
const CMD_SET_MODE = 0x0E
const SELECT_LAYOUT_CMD = 0x00
// const MODE_PROGRAMMER = 0x7F
const MODE_PROGRAMMER = 0x01

// Current mode handler
const currentMode = computed(() => launchpadModes[uiState.launchPadMode] || launchpadModes.dashboard)

// Context for mode handlers
const ctx = computed<LaunchpadContext>(() => ({
  outputPort,
  coreState,
  uiState,
  gridState,
  setPadColorSysEx,
  clearAllLeds,
}))

// Watch for mode changes
watch(() => uiState.launchPadMode, () => {
  if (isConnected.value) {
    clearAllLeds()
    currentMode.value.onEnter(ctx.value)
    updateModeButtons()
  }
})

// Watch for workbench structure changes
const workbenchSignature = computed(() => 
  JSON.stringify(coreState.channels.map(c => (
    { 
      g: c.generator?.name,
      e: c.effects.map(e => e?.name),
      io: c.effects.map(e => e?.IO),
    })))
)

watch(workbenchSignature, () => {
  if (isConnected.value && uiState.launchPadMode === 'workbench') {
    currentMode.value.refresh(ctx.value)
  }
})

onMounted(async () => {
  try {
    if (!navigator.requestMIDIAccess) {
      statusMessage.value = 'Web MIDI API not supported.'
      return
    }
    midiAccess = await navigator.requestMIDIAccess({ sysex: true })
    midiAccess.onstatechange = () => findController()
    findController()
  } catch (err) {
    console.error('MIDI Access Failed:', err)
    statusMessage.value = 'Failed to access MIDI devices.'
  }
})

function findController() {
  if (!midiAccess) return

  const findDawPort = <T extends { name: string | null }>(ports: T[]): T | null => {
    return ports.find(p => p.name?.includes(DEVICE_NAME_SUBSTRING) && (p.name.includes('MIDI 1') || p.name.includes('DAW')))
        || ports.find(p => p.name?.includes(DEVICE_NAME_SUBSTRING) && !p.name.includes('MIDI 2'))
        || ports.find(p => p.name?.includes(DEVICE_NAME_SUBSTRING))
        || null
  }

  inputPort = findDawPort(Array.from(midiAccess.inputs.values()))
  outputPort = findDawPort(Array.from(midiAccess.outputs.values()))

  if (inputPort) inputPort.onmidimessage = handleMidiMessage
  
  if (inputPort && outputPort) {
    isConnected.value = true
    statusMessage.value = `Connected: ${inputPort.name}`
    setTimeout(enterProgrammerMode, 100)
  } else {
    isConnected.value = false
    statusMessage.value = 'Launchpad not found.'
  }
}

function enterProgrammerMode() {
  if (!outputPort) return
  outputPort.send(new Uint8Array([...SYSEX_HEADER, CMD_SET_MODE, MODE_PROGRAMMER, SYSEX_END]))
  // outputPort.send(new Uint8Array([...SYSEX_HEADER, SELECT_LAYOUT_CMD, MODE_PROGRAMMER, SYSEX_END]))
  setTimeout(() => {
    clearAllLeds()
    updateModeButtons()
  }, 50)
}

function handleMidiMessage(event: MIDIMessageEvent) {
  const data = event.data
  if (!data) return
  const [status, note, velocity] = data
  console.log('MIDI Message received:', { status, note, velocity, data })
  lastMessage.value = `[${data.join(', ')}]`

  // Mode switching (89: Workbench, 79: Dashboard)
  if (velocity > 0 && (note === 89 || note === 79)) {
    console.log('Mode switch button pressed:', note)
    if (note === 89) uiState.launchPadMode = 'workbench'
    if (note === 79) uiState.launchPadMode = 'dashboard'
    updateModeButtons()
    return
  }

  if ((status & 0xF0) === 0x90 && velocity > 0) {
    currentMode.value.onPadPress(ctx.value, note)
  }
}

function updateModeButtons() {
  if (!outputPort) return
  console.log('Updating mode buttons:', uiState.launchPadMode)
  const isWorkbench = uiState.launchPadMode === 'workbench'
  setPadColorSysEx(89, isWorkbench ? COLORS.GREEN : COLORS.GRAY)
  setPadColorSysEx(79, !isWorkbench ? COLORS.GREEN : COLORS.GRAY)
}

function setPadColorSysEx(note: number, color: number) {
  if (!outputPort) return
  outputPort.send(new Uint8Array([...SYSEX_HEADER, 0x03, 0x00, note, color, SYSEX_END]))
}

function clearAllLeds() {
  if (!outputPort) return
  for (let row = 1; row <= 9; row++) {
    for (let col = 1; col <= 9; col++) {
      const note = row * 10 + col
      if (note >= 11 && note <= 99) setPadColorSysEx(note, 0)
    }
  }
}

onUnmounted(() => {
  if (inputPort) inputPort.onmidimessage = null
  clearAllLeds()
})
</script>

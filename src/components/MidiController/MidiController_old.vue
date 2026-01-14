<template>
  <div class="p-4 bg-zinc-800 rounded-lg border border-zinc-700 text-white">
    <div class="flex flex-col gap-2 text-sm">
      <div class="flex items-center gap-2">
        <div :class="['w-3 h-3 rounded-full', isConnected ? 'bg-green-500' : 'bg-red-500']"></div>
        <span>{{ statusMessage }}</span>
      </div>
      <div v-if="lastMessage" class="font-mono bg-zinc-900 p-2 rounded text-xs">
        Last Input: {{ lastMessage }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import { useCoreStateStore } from '../../stores/coreState'
import { useUiStateStore } from '../../stores/uiState'
import { gradientSets } from '../../utils/colorSchemes'

const coreState = useCoreStateStore()
const uiState = useUiStateStore()

const isConnected = ref(false)
const statusMessage = ref('Initializing MIDI...')
const lastMessage = ref('')

let midiAccess: MIDIAccess | null = null
let inputPort: MIDIInput | null = null
let outputPort: MIDIOutput | null = null

// Launchpad Mini MK3 Constants
const DEVICE_NAME_SUBSTRING = 'Launchpad Mini MK3'
const SYSEX_HEADER = [0xF0, 0x00, 0x20, 0x29, 0x02, 0x0D]
const SYSEX_END = 0xF7

// Mode commands
const CMD_SET_MODE = 0x0E
const MODE_PROGRAMMER = 0x7F  // Programmer mode - full LED control

// Context Buttons
const contexts = [15, 16, 17, 18]

// Context colors on Launchpad
const CONTEXT_COLORS = [3, 33, 13, 57] // White, Cyan, Yellow, Pink

const GENERATOR_COLOR = 2
const COLOR_PALETTE: Record<string, number> = {
  // Grays
  'gray': 1, 'slate': 1, 'zinc': 1, 'white': 3,
  // Reds & Pinks
  'red': 5, 'rose': 5, 'pink': 57, 'fuchsia': 53,
  // Oranges & Yellows
  'orange': 9, 'amber': 9, 'yellow': 13, 'lime': 17,
  // Greens
  'green': 21, 'emerald': 25, 'teal': 29,
  // Blues & Cyans
  'cyan': 33, 'sky': 37, 'blue': 45,
  // Purples
  'indigo': 49, 'violet': 49, 'purple': 53,
}

const OFF_COLOR = 1 // Grey for disabled elements

// 8x8 Grid State [row][col] (row 0=bottom, row 7=top)
const gridState = ref<number[][]>(Array(8).fill(0).map(() => Array(8).fill(0)))

// Maps a Tailwind color class to a Novation palette color code
function tailwindToNovation(tailwindClass: string): number {
  const match = tailwindClass.match(/(?:from-|to-|bg-)(\w+)-\d+/)
  if (match) {
    const colorName = match[1]
    return COLOR_PALETTE[colorName] || 1
  }
  return 1
}

// Get Novation color for an element based on its name
function getElementColor(name: string | undefined): number {
  if (!name) return 0
  
  // Generate hash from name
  let hash = 0
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash)
  }
  
  const index = Math.abs(hash) % gradientSets.length
  const gradient = gradientSets[index]
  
  return tailwindToNovation(gradient.from)
}

// Convert grid position (row, col) to Launchpad note number
function gridToNote(row: number, col: number): number {
  return row * 10 + col
}

// Convert note number to grid position
function noteToGrid(note: number): { row: number, col: number } {
  return {
    row: Math.floor(note / 10),
    col: note % 10
  }
}

// Watch for specific workbench structure changes (channels, generators, effects)
const workbenchSignature = computed(() => {
  return JSON.stringify(coreState.channels.map(c => ({
    g: c.generator?.name,
    e: c.effects.map(e => e?.name)
  })))
})

watch(workbenchSignature, () => {
  if (isConnected.value) {
    clearAllLeds()
    refreshWorkbench()
    contexts.forEach((note, i) => {  
      setPadColorSysEx(note, CONTEXT_COLORS[i])
    })
  }
})

onMounted(async () => {
  try {
    if (!navigator.requestMIDIAccess) {
      statusMessage.value = 'Web MIDI API not supported in this environment.'
      return
    }

    midiAccess = await navigator.requestMIDIAccess({ sysex: true })
    
    midiAccess.onstatechange = (e) => {
      if (e.port) {
        console.log('MIDI State Change:', e.port.name, e.port.state)
      }
      findController()
    }

    findController()

  } catch (err) {
    console.error('MIDI Access Failed:', err)
    statusMessage.value = 'Failed to access MIDI devices.'
  }
})

function findController() {
  if (!midiAccess) return

  const inputs = Array.from(midiAccess.inputs.values())
  const outputs = Array.from(midiAccess.outputs.values())

  console.log('Available MIDI Inputs:', inputs.map(i => i.name))
  console.log('Available MIDI Outputs:', outputs.map(o => o.name))

  const findDawPort = <T extends { name: string | null }>(ports: T[]): T | null => {
    const dawPort = ports.find(p => p.name && 
      p.name.includes(DEVICE_NAME_SUBSTRING) && 
      (p.name.includes('MIDI 1') || p.name.includes('DAW'))
    )
    if (dawPort) return dawPort
    
    const basePort = ports.find(p => p.name && 
      p.name.includes(DEVICE_NAME_SUBSTRING) && 
      !p.name.includes('MIDI 2')
    )
    if (basePort) return basePort
    
    return ports.find(p => p.name && p.name.includes(DEVICE_NAME_SUBSTRING)) || null
  }

  inputPort = findDawPort(inputs)
  outputPort = findDawPort(outputs)

  if (inputPort) {
    inputPort.onmidimessage = handleMidiMessage
    console.log('Connected to Input:', inputPort.name)
  }

  if (outputPort) {
    console.log('Connected to Output:', outputPort.name)
  }

  if (inputPort && outputPort) {
    isConnected.value = true
    statusMessage.value = `Connected to ${inputPort.name}`
    setTimeout(() => enterProgrammerMode(), 100)
  } else {
    isConnected.value = false
    statusMessage.value = 'Launchpad not found. Please connect it.'
  }
}

function enterProgrammerMode() {
  if (!outputPort) return
  
  const msg = new Uint8Array([...SYSEX_HEADER, CMD_SET_MODE, MODE_PROGRAMMER, SYSEX_END])
  outputPort.send(msg)
  
  setTimeout(() => {
    clearAllLeds()
    refreshWorkbench()
    contexts.forEach((note, i) => {  
      setPadColorSysEx(note, CONTEXT_COLORS[i])
    })
  }, 50)
}

function handleMidiMessage(event: MIDIMessageEvent) {
  const data = event.data
  if (!data) return
  const [status, note, velocity] = data
  
  console.log(`MIDI Message: [${data.join(', ')}] | Status: ${status}, Note: ${note}, Vel: ${velocity}`)
  lastMessage.value = `[${data.join(', ')}]`

  // Handle Note On (pad press) - only on press, not release
  if ((status & 0xF0) === 0x90 && velocity > 0) {
    handlePadPress(note)
  }
}

function handlePadPress(note: number) {
  if (note >= 15 && note <= 18) {
    const index = contexts.indexOf(note)
    uiState.contextIndex = index
    return
  }
  const { row, col } = noteToGrid(note)
  const channelIndex = col - 1
  
  // Row 8 = generator (elementIndex 9), Row 7 = effect 0, Row 6 = effect 1, etc.
  // So: elementIndex = 9 for row 8, and (8 - row) for rows 1-7
  let elementIndex: number
  if (row === 8) {
    elementIndex = 9 // Generator
  } else {
    elementIndex = 7 - row // Effects: row 7 -> 0, row 6 -> 1, etc.
  }
  
  // Check if channel exists
  if (channelIndex >= coreState.channels.length) {
    console.log(`Channel ${channelIndex} does not exist`)
    return
  }
  
  // Check if effect exists
  const channel = coreState.channels[channelIndex]
  if (elementIndex != 9 && elementIndex >= channel.effects.length) {
    console.log(`Effect ${elementIndex} for channel ${channelIndex} does not exist`)
    return
  }

  coreState.select(uiState.contextIndex, channelIndex, elementIndex)
  
  flashPad(note)
}

//  Flash a pad briefly to indicate selection
function flashPad(note: number) {
  const { row, col } = noteToGrid(note)
  // Check bounds (1-8)
  if (row < 1 || row > 8 || col < 1 || col > 8) return

  // Get original color from our state
  // gridState is 0-indexed: row 0=bottom (Launchpad row 1), row 7=top (Launchpad row 8)
  // col 0=left (Launchpad col 1)
  const originalColor = gridState.value[row - 1][col - 1]
  
  setPadColorSysEx(note, 3) // White flash
  setTimeout(() => {
    setPadColorSysEx(note, originalColor)
  }, 100)
}

function refreshWorkbench() {
  if (!outputPort) return
  
  // Reset grid state
  for(let r=0; r<8; r++) for(let c=0; c<8; c++) gridState.value[r][c] = 0;

  const numChannels = Math.min(coreState.channels.length, 8)
  
  for (let ch = 0; ch < numChannels; ch++) {
    const channel = coreState.channels[ch]
    const colIdx = ch // 0-7
    
    // Generator at Row 8 (index 7 in our gridState)
    if (channel.generator) {
       gridState.value[7][colIdx] = GENERATOR_COLOR
    }

    // Effects at Rows 7..1 (indices 6..0 in our gridState)
    // effect 0 -> Row 7 (index 6)
    // effect 1 -> Row 6 (index 5)
    for (let i = 0; i < Math.min(channel.effects.length, 7); i++) {
       const effect = channel.effects[i]
       if (effect) {
         const rowIdx = 6 - i
         const color = effect.IO ? getElementColor(effect.name) : OFF_COLOR
         gridState.value[rowIdx][colIdx] = color
       }
    }
  }
  
  // Send SysEx updates based on gridState
  const updates: number[] = []
  for(let r=0; r<8; r++) {
    for(let c=0; c<8; c++) {
       const color = gridState.value[r][c]
       // Launchpad Note: Row 1-8, Col 1-8 -> Note = Row*10 + Col
       // Our r is 0-7 (1-8), c is 0-7 (1-8)
       const note = (r + 1) * 10 + (c + 1)
       updates.push(0x00, note, color)
    }
  }
  
  if (updates.length > 0) {
    // Send in one batch
    const msg = new Uint8Array([...SYSEX_HEADER, 0x03, ...updates, SYSEX_END])
    outputPort.send(msg)
  }
  
  console.log('Workbench display refreshed')
}

function setPadColorSysEx(note: number, colorCode: number) {
  if (!outputPort) return
  const msg = new Uint8Array([...SYSEX_HEADER, 0x03, 0x00, note, colorCode, SYSEX_END])
  outputPort.send(msg)
}

function clearAllLeds() {
  if (!outputPort) return
  
  for (let row = 1; row <= 9; row++) {
    for (let col = 1; col <= 9; col++) {
      const note = row * 10 + col
      if (note >= 11 && note <= 99) {
        setPadColorSysEx(note, 0)
      }
    }
  }
}

onUnmounted(() => {
  if (inputPort) {
    inputPort.onmidimessage = null
  }
  clearAllLeds()
})
</script>

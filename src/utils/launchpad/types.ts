import type { Ref } from 'vue'

export interface LaunchpadContext {
  outputPort: MIDIOutput | null
  coreState: any
  uiState: any
  gridState: Ref<number[][]>
  setPadColorSysEx: (note: number, color: number) => void
  clearAllLeds: () => void
}

export interface LaunchpadMode {
  name: string
  onEnter: (ctx: LaunchpadContext) => void
  onPadPress: (ctx: LaunchpadContext, note: number) => void
  refresh: (ctx: LaunchpadContext) => void
}

// Shared constants
export const SYSEX_HEADER = [0xF0, 0x00, 0x20, 0x29, 0x02, 0x0D]
export const SYSEX_END = 0xF7

// Color palette
export const COLORS = {
  OFF: 0,
  GRAY: 1,
  GENERATOR: 2,
  WHITE: 3,
  RED: 5,
  ORANGE: 9,
  YELLOW: 13,
  LIME: 17,
  GREEN: 21,
  EMERALD: 25,
  TEAL: 29,
  CYAN: 33,
  SKY: 37,
  BLUE: 45,
  INDIGO: 49,
  PURPLE: 53,
  PINK: 57,
}

// Context button notes and colors
export const CONTEXT_BUTTONS = [15, 16, 17, 18]
export const CONTEXT_COLORS = [COLORS.WHITE, COLORS.CYAN, COLORS.YELLOW, COLORS.PINK]

// Tailwind to Novation mapping
export const TAILWIND_TO_NOVATION: Record<string, number> = {
  'gray': 1, 'slate': 1, 'zinc': 1, 'white': 3,
  'red': 5, 'rose': 5, 'pink': 57, 'fuchsia': 53,
  'orange': 9, 'amber': 9, 'yellow': 13, 'lime': 17,
  'green': 21, 'emerald': 25, 'teal': 29,
  'cyan': 33, 'sky': 37, 'blue': 45,
  'indigo': 49, 'violet': 49, 'purple': 53,
}

// Helper: Convert note to grid position
export function noteToGrid(note: number) {
  return { row: Math.floor(note / 10), col: note % 10 }
}

// Helper: Convert grid position to note
export function gridToNote(row: number, col: number) {
  return row * 10 + col
}

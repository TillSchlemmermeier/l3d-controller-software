import { gradientSets } from '../colorSchemes'
import type { LaunchpadMode } from './types'
import { COLORS, CONTEXT_BUTTONS, CONTEXT_COLORS, TAILWIND_TO_NOVATION, noteToGrid, SYSEX_HEADER, SYSEX_END } from './types'

function getElementColor(name: string | undefined): number {
  if (!name) return COLORS.OFF
  let hash = 0
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash)
  }
  const index = Math.abs(hash) % gradientSets.length
  const match = gradientSets[index].from.match(/(?:from-)(\w+)-\d+/)
  return match ? (TAILWIND_TO_NOVATION[match[1]] || COLORS.GRAY) : COLORS.GRAY
}

export const workbenchMode: LaunchpadMode = {
  name: 'workbench',

  onEnter(ctx) {
    this.refresh(ctx)
  },

  onPadPress(ctx, note) {
    // Context button press
    if (note >= 15 && note <= 18) {
      ctx.uiState.contextIndex = CONTEXT_BUTTONS.indexOf(note)
      return
    }

    if (note === 11) {
      ctx.uiState.shiftActivated = !ctx.uiState.shiftActivated
      this.refresh(ctx)
      return
    }

    const { row, col } = noteToGrid(note)
    if (row < 1 || row > 8 || col < 1 || col > 8) return

    const channelIndex = col - 1
    const elementIndex = row === 8 ? 9 : 7 - row // Row 8 = generator, else effect

    if (channelIndex >= ctx.coreState.channels.length) return
    
    const channel = ctx.coreState.channels[channelIndex]
    if (elementIndex !== 9 && elementIndex >= channel.effects.length) return

    if (ctx.uiState.shiftActivated && elementIndex <= 7) {
      ctx.coreState.toggleEffect(channelIndex, elementIndex)
      this.refresh(ctx)
    } else {
      ctx.coreState.select(ctx.uiState.contextIndex, channelIndex, elementIndex)
    }

    // Flash pad
    const originalColor = ctx.gridState.value[row - 1][col - 1]
    ctx.setPadColorSysEx(note, COLORS.WHITE)
    setTimeout(() => ctx.setPadColorSysEx(note, originalColor), 100)
  },

  refresh(ctx) {
    if (!ctx.outputPort) return

    // Reset grid state
    for (let r = 0; r < 8; r++) for (let c = 0; c < 8; c++) ctx.gridState.value[r][c] = COLORS.OFF

    const numChannels = ctx.coreState.channels.length

    for (let ch = 0; ch < numChannels; ch++) {
      const channel = ctx.coreState.channels[ch]
      
      // Generator at row 8 (gridState index 7)
      ctx.gridState.value[7][ch] = COLORS.GENERATOR

      // Effects at rows 7..1 (gridState indices 6..0)
      for (let i = 0; i < channel.effects.length; i++) {
        const effect = channel.effects[i]
        ctx.gridState.value[6 - i][ch] = effect.IO ? getElementColor(effect.name) : COLORS.GRAY
      }
    }

    ctx.gridState.value[0][0] = ctx.uiState.shiftActivated ? COLORS.GREEN : COLORS.RED

    CONTEXT_BUTTONS.forEach((_, i) => {
      ctx.gridState.value[0][4 + i] = CONTEXT_COLORS[i]
    })

    // Send batch SysEx
    const updates: number[] = []
    for (let r = 0; r < 8; r++) {
      for (let c = 0; c < 8; c++) {
        updates.push(0x00, (r + 1) * 10 + (c + 1), ctx.gridState.value[r][c])
      }
    }

    if (updates.length > 0) {
      ctx.outputPort.send(new Uint8Array([...SYSEX_HEADER, 0x03, ...updates, SYSEX_END]))
    }
  }
}

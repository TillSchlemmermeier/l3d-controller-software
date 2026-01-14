import type { LaunchpadMode } from './types'
import { COLORS, noteToGrid, SYSEX_HEADER, SYSEX_END } from './types'
import type { AutopilotMode } from '../../types/types'

const RANDOM_MODES: AutopilotMode[] = [
  'global',
  'all_channels',
  'all_elements',
  'random_channel',
  'random_channel_elements',
  'random_element',
  'selected_channel',
  'selected_channel_elements',
  'selected_element',
]

export const dashboardMode: LaunchpadMode = {
  name: 'dashboard',

  onEnter(ctx) {
    this.refresh(ctx)
  },

  onPadPress(ctx, note) {
    const { row, col } = noteToGrid(note)
    if (row < 1 || row > 8 || col < 1 || col > 8) return

    // Row 8: Top Controls
    if (row === 8) {
      if (col === 1) ctx.coreState.normalize()
      if (col === 2) ctx.coreState.rebootCore()
      if (col === 3) ctx.coreState.undoRandom()
      if (col === 4) ctx.coreState.toggleCube()
      
      // Flash feedback for momentary buttons
      if (col <= 4) {
        ctx.setPadColorSysEx(note, COLORS.WHITE)
        setTimeout(() => this.refresh(ctx), 100)
      } else {
        // Toggle button update
        this.refresh(ctx)
      }
    }

    // Row 6: Random Triggers
    if (row === 6 && col === 1) {
      ctx.coreState.triggerRandomizer(ctx.uiState.randomMode)
      ctx.setPadColorSysEx(note, COLORS.WHITE)
      setTimeout(() => this.refresh(ctx), 100)
    }

    if (row === 6 && col === 8) {
      ctx.coreState.toggleAutopilot()
      this.refresh(ctx)
    }

    // Row 5: Random Mode Selection
    if (row === 6 && col >= 3 && col <= 6) {
      const modeIndex = col - 3
      ctx.uiState.randomMode = RANDOM_MODES[modeIndex]
      this.refresh(ctx)
    }

    // Row 4: Random Mode Selection (continued)
    if (row === 5 && col >= 3 && col <= 6) {
      const modeIndex = 4 + (col - 3)
      ctx.uiState.randomMode = RANDOM_MODES[modeIndex]
      this.refresh(ctx)
    }

    // Row 3: Random Mode Selection (last one)
    if (row === 4 && col === 3) {
      ctx.uiState.randomMode = RANDOM_MODES[8]
      this.refresh(ctx)
    }

    if (row === 4 && col === 1) {
      ctx.coreState.randomizeColor()
      ctx.setPadColorSysEx(note, COLORS.WHITE)
      setTimeout(() => this.refresh(ctx), 100)
    }


    // Row 4: Autopilot Controls
    if (row === 4 && col === 8) {
      ctx.coreState.autopilotMode()
      this.refresh(ctx)
    }

    // Row 2: OneShots 1-5
    if (row === 2 && col <= 5) {
      const oneshotIndex = col
      ctx.coreState.fireOneShot(oneshotIndex)
      
      // Flash feedback
      ctx.setPadColorSysEx(note, COLORS.WHITE)
      setTimeout(() => this.refresh(ctx), 100)
    }

    // Row 1: OneShots 6-10
    if (row === 1 && col <= 5) {
      const oneshotIndex = col + 5
      ctx.coreState.fireOneShot(oneshotIndex)
      
      // Flash feedback
      ctx.setPadColorSysEx(note, COLORS.WHITE)
      setTimeout(() => this.refresh(ctx), 100)
    }
  },

  refresh(ctx) {
    if (!ctx.outputPort) return

    // Reset grid state
    for (let r = 0; r < 8; r++) for (let c = 0; c < 8; c++) ctx.gridState.value[r][c] = COLORS.OFF

    // Row 8: Top Controls
    ctx.gridState.value[7][0] = COLORS.YELLOW // NORM S2L
    ctx.gridState.value[7][1] = COLORS.RED    // REBOOT CORE
    ctx.gridState.value[7][2] = COLORS.ORANGE // UNDO RANDOM
    ctx.gridState.value[7][3] = ctx.coreState.IO ? COLORS.GREEN : COLORS.RED // I/O CUBE

    // Row 6: Random Triggers
    ctx.gridState.value[5][0] = COLORS.PURPLE // TRIGGER RANDOM
    ctx.gridState.value[3][0] = COLORS.PINK   // RANDOM COLOR

    // Row 5: Random Modes
    RANDOM_MODES.forEach((mode, index) => {
      const isSelected = ctx.uiState.randomMode === mode
      const row = Math.floor(index / 4)
      ctx.gridState.value[5 - row][index % 4 + 2] = isSelected ? COLORS.WHITE : COLORS.GRAY
    })

    // Row 4: Autopilot
    ctx.gridState.value[5][7] = ctx.coreState.autopilot ? COLORS.GREEN : COLORS.RED // AUTO PILOT
    ctx.gridState.value[3][7] = COLORS.BLUE // AUTO PILOT MODE

    // Row 2: OneShots 1-5
    for (let i = 0; i < 5; i++) {
      ctx.gridState.value[1][i] = COLORS.CYAN
    }

    // Row 1: OneShots 6-10
    for (let i = 0; i < 5; i++) {
      ctx.gridState.value[0][i] = COLORS.CYAN
    }

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

import { defineStore } from 'pinia'

export interface ChannelState {
  id: number
  IO: boolean
  brightness: number
  fade: number
}
const API_BASE = '/api' 

export const useMobileStore = defineStore('mobile', {
  state: () => ({
    channels: Array.from({ length: 8 }, (_, i) => ({
      id: i + 1,
      IO: true,
      brightness: 1.0,
      fade: 0.0
    })),
    autopilot: false,
    brightness: 1.0,
    fade: 0,
    randomMode: 'all_elements',
    selectedChannel: 1
  }),

  getters: {
    getChannelParameters: (state) => (channelIndex: number) => {
      const channel = state.channels[channelIndex]
      if (channel) {
        return {
          IO: channel.IO,
          brightness: channel.brightness,
          fade: channel.fade,
        }
      }
    },
    getCurrentChannelObj: (state) => {
      return state.channels[state.selectedChannel - 1]
    },
    currentBrightness: (state) => {
      if (state.selectedChannel === 0) return state.brightness
      return state.channels[state.selectedChannel - 1]?.brightness ?? 1.0
    },
    currentFade: (state) => {
      if (state.selectedChannel === 0) return state.fade
      return state.channels[state.selectedChannel - 1]?.fade ?? 0.0
    },
  },
  
  actions: {
    toggleChannelPower() {
      const channel = this.getCurrentChannelObj
      if (channel) {
        // Optimistic update
        const newValue = !channel.IO
        this.updateKey('IO', newValue, channel.id - 1)
        this.vibrate(20)

        fetch(`${API_BASE}/toggle-channel-key/${channel.id - 1}/IO`)
      }
    },

    selectChannel(channel: number) {
      this.selectedChannel = channel
      fetch(`${API_BASE}/select/0/${channel - 1}/9`)
      this.vibrate(10)
    },

    toggleAutopilot() {
      fetch(`${API_BASE}/toggle-autopilot`)
      this.vibrate(20)
    },

    setAutopilotMode(mode: string) {
      this.randomMode = mode
      this.vibrate(10)
      fetch(`${API_BASE}/autopilot-mode/${mode}`)
    },

    triggerRandom() {
      if (this.randomMode === 'color') {
        fetch(`${API_BASE}/randomize-color/${this.selectedChannel - 1}`)
      } else {
        fetch(`${API_BASE}/trigger-randomizer`)
      }
      this.vibrate([30, 50, 30])
    },

    undoRandom() {
      fetch(`${API_BASE}/undo-random`)
      this.vibrate(30)
    },

    normalizeS2L() {
      fetch(`${API_BASE}/normalize-s2l`)
      this.vibrate(20)
    },

    triggerOneshot() {
      fetch(`${API_BASE}/oneshot/10`)
      this.vibrate(50)
    },

    strobeOneshot() {
      fetch(`${API_BASE}/oneshot/6`)
      this.vibrate([10, 10, 10, 10])
    },

    vibrate(pattern: number | number[]) {
      if (navigator.vibrate) navigator.vibrate(pattern)
    },

    setCurrentBrightness(value: number) {
      if (this.selectedChannel > 0) {
        // Update channel-specific brightness
        this.updateKey('brightness', value, this.selectedChannel - 1)
        fetch(`${API_BASE}/update-channel-key/${this.selectedChannel - 1}/brightness/${value}`)
      } else {
        // Update global brightness
        this.brightness = value
        fetch(`${API_BASE}/update-global-key/brightness/${value}`)
      }
    },

    setCurrentFade(value: number) {
      if (this.selectedChannel > 0) {
        // Update channel-specific fade
        this.updateKey('fade', value, this.selectedChannel - 1)
        fetch(`${API_BASE}/update-channel-key/${this.selectedChannel - 1}/fade/${value}`)
      } else {
        // Update global fade
        this.fade = value
        fetch(`${API_BASE}/update-global-key/fade/${value}`)
      }
    },

    setFullState(data: any) { // eslint-disable-line
      const { numberOfChannels } = data
      // Recreate channels array based on numberOfChannels
      this.channels = Array.from({ length: numberOfChannels }, (_, i) => {
        const channel = data[i] || {}  // Get channel data or empty object
        return {
          id: i + 1,
          IO: channel.IO ?? true,
          brightness: channel.brightness ?? 1.0,
          fade: channel.fade ?? 0.0,
        }
      })

      // Update global keys
      this.autopilot = data.autoppilot
      this.brightness = data.brightness
      this.fade = data.fade
    },

    updateKey(key: string, value: any, channelIndex: number | null) { // eslint-disable-line
    if (channelIndex !== null && channelIndex !== undefined) {
      // Channel specific update
      const ch = this.channels[channelIndex]
      if (ch) {
        if (key === 'IO') ch.IO = value
        if (key === 'brightness') ch.brightness = value
        if (key === 'fade') ch.fade = value
      }
    } else {
      // Global update
      if (key === 'autopilot') this.autopilot = value
      if (key === 'brightness') this.brightness = value
      if (key === 'fade') this.fade = value
    }
  },

    updateSection(data: any) { // eslint-disable-line
      Object.keys(data).forEach(key => {
        const index = Number(key)
        // If key is a number, it's a channel index
        if (!isNaN(index) && this.channels[index]) {
          const chData = data[key]
          const ch = this.channels[index]
          if (chData.IO !== undefined) ch.IO = chData.IO
          if (chData.brightness !== undefined) ch.brightness = chData.brightness
          if (chData.fade !== undefined) ch.fade = chData.fade
        }
      })
    }
  }

})
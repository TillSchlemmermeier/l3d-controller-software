import { defineStore } from 'pinia'
import { useUiStateStore } from './uiState'
import { coreState, AutopilotMode } from '../types/types'

const baseUrl = 'http://0.0.0.0:8000/api'
// shared secret for destructive endpoints
const adminToken = import.meta.env.VITE_ADMIN_TOKEN || ''

// IPC listeners registered by initializeIPC()
let ipcDisposers: Array<() => void> = []

// A color-manager section is only usable if it carries a non-empty gradient of
// [position, color] pairs. Anything else (cleared gradient, corrupted state)
// must be treated as "no color manager" rather than installed into the store.
function hasValidGradient(section: any): boolean {
  return !!section
    && Array.isArray(section.gradient)
    && section.gradient.length > 0
    && section.gradient.every((stop: any) => Array.isArray(stop) && stop.length >= 2)
}

export const useCoreStateStore = defineStore('coreState', {
  state: (): coreState => ({
    IO: false,
    brightness: 0,
    fade: 0,
    autopilot: false,
    autopilot_time: 0,
    random: '',
    s2l_values: [],
    s2l_thresholds: [],
    s2l_normalize: false,
    s2l_gain: 0,
    s2l_update: false,
    context: [[0,9]],
    oneshot: 0,
    numberOfChannels: 0,
    channels: [],
    globalEffects: [],
    globalColor: undefined
  }),

  getters: {
    getChannelParameters: (state: coreState) => (channelIndex: number) => {
      const channel = state.channels[channelIndex]
      return {
        IO: channel.IO,
        brightness: channel.brightness,
        fade: channel.fade,
      }
    },
  },
  actions: {
    async requestStateUpdate() {
      try {
        await fetch(`${baseUrl}/get-state`, {
          method: 'GET',
        })
      } catch (error) {
        console.error('error', error)
      }
    },
    async rebootCore() {
      await window.ipcRenderer.restartBackend()
    },

    async select(contextIndex: number, channelIndex: number, elementIndex: number) {
      const url = `${baseUrl}/select/${contextIndex}/${channelIndex}/${elementIndex}`
      await this.callBackend(url)
    },

    async toggleCube() {
      const url = `${baseUrl}/toggle-cube`
      await this.callBackend(url)
    },

    async normalize() {
      const url = `${baseUrl}/normalize-s2l`
      await this.callBackend(url)
    },

    async toggleAutopilot() {
      const url = `${baseUrl}/toggle-autopilot`
      await this.callBackend(url)
    },

    async autopilotMode(mode?: AutopilotMode) {
      const url_mode = mode ? mode : 'next'
      const url = `${baseUrl}/autopilot-mode/${url_mode}`
      await this.callBackend(url)
    },

    async triggerRandomizer(mode: AutopilotMode) {
      const url = `${baseUrl}/trigger-randomizer/${mode}`
      await this.callBackend(url)
    },

    async undoRandom() {
      const url = `${baseUrl}/undo-random`
      await this.callBackend(url)
    },

    async randomizeColor() {
      const uiState = useUiStateStore()
      const channelIndex = uiState.channelIndex
      const url = `${baseUrl}/randomize-color/${channelIndex}`
      await this.callBackend(url)
    },

    async fireOneShot(index: number) {
      const url = `${baseUrl}/oneshot/${index}`
      await this.callBackend(url)
    },

    // load a new channel, generator, effect or global effect
    async load(preset_name: string) {
      const uiState = useUiStateStore()
      const url = `${baseUrl}/load/${uiState.elementType}/${preset_name}/${uiState.channelIndex}/${uiState.effectIndex}/${uiState.selectedElement}`
      await this.callBackend(url)
    },

    async copyChannel(channelIndex: number) {
      const url = `${baseUrl}/copychannel/${channelIndex}`
      await this.callBackend(url)
    },

    async moveChannel(channelIndex: number, newIndex: number) {
      const url = `${baseUrl}/movechannel/${channelIndex}/${newIndex}`
      await this.callBackend(url)
    },

    async copyEffect(fromChannel: number, fromIndex: number, toChannel: number, toIndex: number) {
      const url = `${baseUrl}/copyeffect/${fromChannel}/${fromIndex}/${toChannel}/${toIndex}`
      await this.callBackend(url)
    },

    async moveEffect(channelIndex: number, oldIndex: number, newIndex: number) {
      const url = `${baseUrl}/moveeffect/${channelIndex}/${oldIndex}/${newIndex}`
      await this.callBackend(url)
    },

    async toggleEffect(channelIndex: number, effectIndex: number) {
      const url = `${baseUrl}/toggleeffect/${channelIndex}/${effectIndex}`
      await this.callBackend(url)
    },

    async removeEffect(channelIndex: number, effectIndex: number) {
      const url = `${baseUrl}/remove/effect/${channelIndex}/${effectIndex}`
      await this.callBackend(url, 'DELETE')
    },

    async removeChannel(channelIndex: number) {
      const url = `${baseUrl}/remove/channel/${channelIndex}/0`
      await this.callBackend(url, 'DELETE')
    },

    // save a generator, effect, channel or global preset
    async save(presetName: string, preview?: string, force: boolean = false) {
      const uiState = useUiStateStore()
      
      let formData = new FormData()
      formData.append('preset', presetName)
      formData.append('type', uiState.elementType)
      formData.append('channel', uiState.channelIndex.toString())
      formData.append('index', uiState.effectIndex.toString())
      formData.append('force', force.toString())
      
      if (preview) {
        const base64Data = preview.replace(/^data:image\/gif;base64,/, '')
        const blob = await fetch(`data:image/gif;base64,${base64Data}`).then(res => res.blob())
        formData.append('preview', new File([blob], `${presetName}.gif`, { type: 'image/gif' }))
      }
    
      const response = await fetch(`${baseUrl}/save/`, {
        method: 'POST',
        headers: { 'X-Admin-Token': adminToken },
        body: formData
      })
      const data = await response.json()
      return {
        status: response.status,
        message: data.message
      }
    },

    async updateColorManager(channel: number, colorData: {
      gradient: Array<[number, string]>,
      gradientType: 'linear' | 'radial',
      sectionWidth: number,
      sectionStart: number,
      speed: number,
      rotateSpeedY: number,
      rotateSpeedZ: number,
      soundToLightOptions: string[]
    }) {
      const url = `${baseUrl}/color-manager/${channel}`
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(colorData)
        })
        const data = await response.json()
        console.log('Color manager updated:', data.message)
      } catch (error) {
        console.error('Error updating color manager:', error)
      }
    },

    async loadGradient(gradientId: number) {
      const uiState = useUiStateStore()
      const url = `${baseUrl}/load-gradient/${gradientId}/${uiState.channelIndex}`
      await this.callBackend(url)
    },

    // make a state-mutating API call (POST by default, DELETE for removals)
    async callBackend(url: string, method: 'POST' | 'DELETE' = 'POST') {
      console.log('calling backend', method, url)
      try {
        const response = await fetch(url, { method, headers: { 'X-Admin-Token': adminToken } })
        const data = await response.json()
        console.log(data)
      } catch (error) {
        console.error('error', error)
      }
    },

    initializeIPC() {
      const uiState = useUiStateStore()
      ipcDisposers.forEach(dispose => dispose())
      ipcDisposers = [
        window.ipcRenderer.onWebSocketConnected(() => {
          console.log('WebSocket connected, requesting state update')
          uiState.setConnected()
          this.requestStateUpdate()
        }),
        window.ipcRenderer.onWebSocketDisconnected(() => {
          console.log('WebSocket disconnected')
          uiState.setDisconnected()
        }),
        window.ipcRenderer.onWebSocketError((error: string) => {
          console.error('WebSocket error:', error)
          uiState.setConnectionError(error)
        }),
        window.ipcRenderer.onReinitializeRenderers(() => {
          console.log('Backend restarted, re-syncing state')
          this.requestStateUpdate()
        }),
        window.ipcRenderer.onStateData((message: any) => {
          this.$state = this.parseState(message)
          uiState.clampChannelIndex(this.channels.length)
        }),
        window.ipcRenderer.onStateSectionData((message: any) => {
          this.updateSingleElement(message)
        }),
        window.ipcRenderer.onStateKeyData((message: any) => {
          console.log('update key', message)
          this.updateSingleKey(message)
        }),
      ]
    },

    updateSingleElement(data: any) {
      const channel = Number(Object.keys(data)[0])
      const value = data[channel]
      const index = Number(Object.keys(value)[0])
      const section = value[index]

      if (channel === 9) {
        if (index === 8) {
          this.globalColor = hasValidGradient(section) ? section : undefined
        } else {
          this.globalEffects[index] = section
        }
      } else {
        if (index === 9) {
          this.channels[channel].generator = section
        } else if (index === 8) {
          this.channels[channel].color = hasValidGradient(section) ? section : undefined
        } else {
          this.channels[channel].effects[index] = section
        }
      }
    },

    updateSingleKey(data: any) {
      if (data.channel != null) {
        this.channels[data.channel] = {
          ...this.channels[data.channel],
          [data.key]: data.value
        }
      } else {
        (this as any)[data.key] = data.value
      }
    },

     parseState(data: Record<string, any>): coreState {
      const { numberOfChannels, ...rest } = data
      const parsedState: Partial<coreState> = { ...rest }
    
      // Transform channels
      parsedState.channels = Array.from({ length: numberOfChannels }, (_, i) => {
        const channel = { ...data[i] }
        const { numberOfEffects } = channel
    
        // Transform effects into array
        const effects = Array.from({ length: numberOfEffects }, (_, j) => channel[j])
        
        // Create clean channel object
        return {
          IO: channel.IO,
          brightness: channel.brightness,
          fade: channel.fade,
          numberOfEffects: numberOfEffects,
          effects,
          generator: channel[9],
          color: hasValidGradient(channel[8]) ? channel[8] : undefined
        }
      })

      // Transform global effects
      parsedState.globalEffects = Array.from(
          { length: data[9].numberOfEffects },
          (_, i) => data[9][i]
        )

      parsedState.globalColor = hasValidGradient(data[9][8]) ? data[9][8] : undefined

      return parsedState as coreState
    }
  },
});


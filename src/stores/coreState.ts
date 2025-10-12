import { defineStore } from 'pinia'
import { useUiStateStore } from './uiState'
import { coreState } from '../types/types'

const baseUrl = 'http://0.0.0.0:8000/api'

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
    crossfade_active: false,
    numberOfChannels: 0,
    channels: [],
    globalEffects: []
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

    async autopilotMode() {
      const url = `${baseUrl}/autopilot-mode`
      await this.callBackend(url)
    },

    async triggerRandomizer() {
      const url = `${baseUrl}/trigger-randomizer`
      await this.callBackend(url)
    },

    // load a new channel, generator, effect or global effect
    async load(preset_name: string) {
      const uiState = useUiStateStore()
      const url = `${baseUrl}/load/${uiState.dialogType}/${preset_name}/${uiState.channelIndex}/${uiState.effectIndex}/${uiState.selectedElement}`
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
      await this.callBackend(url)
    },

    async removeChannel(channelIndex: number) {
      const url = `${baseUrl}/remove/channel/${channelIndex}/0`
      await this.callBackend(url)
    },
    
    // delete a generator, effect, channel or global preset
    async delete(preset: string, element?: string) {
      const uiState = useUiStateStore()
      const url = `${baseUrl}/delete/${uiState.dialogType}/${preset}/${element}`
      await this.callBackend(url)
    },

    // save a generator, effect, channel or global preset
    async save(presetName: string, preview?: string, force: boolean = false) {
      const uiState = useUiStateStore()
      
      let formData = new FormData()
      formData.append('preset', presetName)
      formData.append('type', uiState.dialogType)
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

    // make API call
    async callBackend(url: string) {
      console.log('fetching data from', url)
      try {
        const response = await fetch(url, {
          method: 'GET',
        })
        const data = await response.json()
        console.log(data)
      } catch (error) {
        console.error('error', error)
      }
    },

    initializeIPC() {
      window.ipcRenderer.onWebSocketConnected(() => {
        console.log('WebSocket connected, requesting state update')
        this.requestStateUpdate()
        console.log('Initial state loaded')
      })
      window.ipcRenderer.onStateData((message: any) => {
        this.$state = this.parseState(message)
      })
      window.ipcRenderer.onStateSectionData((message: any) => {
        this.updateSingleElement(message)
      })
      window.ipcRenderer.onStateKeyData((message: any) => {
        console.log('update key', message)
        this.updateSingleKey(message)
      })
    },

    updateSingleElement(data: any) {
      const channel = Number(Object.keys(data)[0])
      const value = data[channel]
      const index = Number(Object.keys(value)[0])
      const section = value[index]

      if (channel === 9) {
        this.globalEffects[index] = section
      } else {
        if (index === 9) {
          this.channels[channel].generator = section
        } else if (index === 8) {
          this.channels[channel].color = section
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
          color: channel[8]
        }
      })

      // Transform global effects
      parsedState.globalEffects = Array.from(
          { length: data[9].numberOfEffects },
          (_, i) => data[9][i]
        )
    
      return parsedState as coreState
    }
  },
});


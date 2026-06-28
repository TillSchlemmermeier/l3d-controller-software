import { defineStore } from 'pinia'
import {
  AdminElements,
  AdminPresets,
  AutopilotMode,
  ConnectionStatus,
  ElementInfo,
  GradientPreset,
  Preset,
  PresetInfo,
  SortOption
   } from '../types/types.ts'

const baseUrl = 'http://0.0.0.0:8000/api'

export const useUiStateStore = defineStore('uiState', {
  state: () => ({
    draggedChannelIndex: 0,
    lastTypeDragged: 'channel',
    dialogOpen: false,
    elementType: 'generator',
    channelIndex: 0,
    effectIndex: 0,
    overlayItems: [],
    overlayPresets: [] as Preset[],
    adminElements: [] as AdminElements[],
    adminPresets: [] as AdminPresets[],
    gradientPresets: [] as GradientPreset[],
    selectedElement: '',
    elementInfo: {} as ElementInfo,
    selectedPreset: '',
    presetInfo: {} as PresetInfo,
    newChannel: false,
    admin: true,
    sortBy: 'alpha', // alpha, date, usage
    sortGradientsBy: 'subtype' as SortOption,
    clickBehavior: 'select', // select, edit, IO
    isDragging: false,
    contextIndex: 0,
    deleteActive: false,
    sidebarOption: 'console', // console, colors, palette
    randomMode: 'global' as AutopilotMode,
    launchPadMode: 'workbench' as 'workbench' | 'dashboard',
    shiftActivated: false, // whether to IO effects or select them
    connectionStatus: 'connecting' as ConnectionStatus, // Electron-main <-> Python WS lifecycle
    connectionError: '',
    everConnected: false, // becomes true after the first successful connect
  }),
  actions: {
    // backend connection lifecycle
    setConnected() {
      this.connectionStatus = 'connected'
      this.connectionError = ''
      this.everConnected = true
    },
    setDisconnected() {
      if (this.connectionStatus !== 'error') {
        this.connectionStatus = 'disconnected'
      }
    },
    setConnectionError(message: string) {
      this.connectionStatus = 'error'
      this.connectionError = message || 'Unknown WebSocket error'
    },

    // fetch the names of active effects or generators
    async fetchActiveElements() {
      const url = `get-active-elements/${this.elementType}`
      this.overlayItems = await this.callBackend(url)
    },

    // fetch the names of all available effects or generators
    async fetchAllElements() {
      const url = `get-element-names/${this.elementType}`
      this.adminElements = await this.callBackend(url)
    },

    // fetch the names of element, channel and global presets containing the element
    async fetchAllPresets() {
      const url = `get-all-presets/${this.elementType}/${this.selectedElement}`
      this.adminPresets = await this.callBackend(url)
      console.log('fetched all presets', this.adminPresets)
    },

    // fetch the list of presets for an element
    async fetchPresets() {
      const url = `get-presets/${this.elementType}/${this.selectedElement}`
      this.overlayPresets = await this.callBackend(url)
    },

    // fetch all available info from the database for the selected element
    async fetchElementInfo() {
      const url = `get-element-info/${this.elementType}/${this.selectedElement}`
      this.elementInfo = await this.callBackend(url)
    },

    // fetch all available info from the database for the selected preset
    async fetchPresetInfo() {
      const url = `get-preset-info/${this.elementType}/${this.selectedElement}/${this.selectedPreset}`
      this.presetInfo = await this.callBackend(url)
    },

    // delete a preset
    async deletePreset() {
      const url = `delete-preset/${this.elementType}/${this.selectedElement}/${this.selectedPreset}`
      const response = await this.callBackend(url, 'DELETE')
      console.log('delete response', response)
    },

    // delete an element
    async deleteElement() {
      const url = `delete-element/${this.elementType}/${this.selectedElement}`
      const response = await this.callBackend(url, 'DELETE')
      console.log('delete response', response)
    },

    // add an element
    async addElement(type: string, name: string) {
      const url = `add-element/${type}/${name}`
      const response = await this.callBackend(url, 'POST')
      console.log('add response', response)
    },

    // toggle active status of generator or effect
    async toggleElementActive() {
      const url = `toggle-element-active/${this.elementType}/${this.selectedElement}`
      const response = await this.callBackend(url, 'POST')
      console.log('toggle response', response)
    },

    async renamePreset(newName: string) {
      const url = `rename-preset/${this.elementType}/${this.selectedElement}/${this.selectedPreset}/${newName}`
      const response = await this.callBackend(url, 'POST')
      console.log('rename response', response)
      this.selectedPreset = newName
    },

    async fetchGradientPresets() {
      const url = `get-gradient-presets`
      const gradients = await this.callBackend(url)
      this.gradientPresets = gradients.map((preset: any) => ({
        ...preset,
        data: JSON.parse(preset.data) as Array<[number, string]>
      }))
    },

    async saveGradientPreset(gradientArray: Array<[number, string]>, subtype: string) {
      const url = `save-gradient`
      const gradientString = JSON.stringify(gradientArray)
      await this.callBackend(url, 'POST', { subtype, gradientString })
      this.fetchGradientPresets()
    },

    async deleteGradientPreset(id: number) {
      const url = `delete-gradient/${id}`
      await this.callBackend(url, 'DELETE')
      this.fetchGradientPresets()
    },

    async checkPresetConsistency() {
      const url = `validate-presets`
      const response = await this.callBackend(url)
      console.log('Validation results:', response)
      return response
    },

    async clearGradient(channel: number) {
      const url = `clear-gradient/${channel}`
      await this.callBackend(url, 'POST')
    },

    // call the backend; GET by default, with an optional JSON body for POST
    async callBackend(url: string, method: 'GET' | 'POST' | 'DELETE' = 'GET', data?: any) {
      console.log(method, url)
      try {
        const options: RequestInit = { method }
        if (data !== undefined) {
          options.headers = { 'Content-Type': 'application/json' }
          options.body = JSON.stringify(data)
        }
        const response = await fetch(`${baseUrl}/${url}`, options)
        return await response.json()
      } catch (error) {
        console.error('error', error)
      }
    }
  },

})

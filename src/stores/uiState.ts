import { defineStore } from 'pinia'
import { ElementInfo, PresetInfo, AdminElements, Preset, GradientPreset, SortOption, AdminPresets, AutopilotMode } from '../types/types.ts'

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
    randomMode: 'global' as AutopilotMode

  }),
  actions: {
    // fetch the names of active effects or generators
    async fetchActiveElements() {
      const url = `get-active-elements/${this.elementType}`
      this.overlayItems = await this.fetchFromBackend(url)
    },

    // fetch the names of all available effects or generators
    async fetchAllElements() {
      const url = `get-element-names/${this.elementType}`
      this.adminElements = await this.fetchFromBackend(url)
    },

    // fetch the names of element, channel and global presets containing the element
    async fetchAllPresets() {
      const url = `get-all-presets/${this.elementType}/${this.selectedElement}`
      this.adminPresets = await this.fetchFromBackend(url)
      console.log('fetched all presets', this.adminPresets)
    },

    // fetch the list of presets for an element
    async fetchPresets() {
      const url = `get-presets/${this.elementType}/${this.selectedElement}`
      this.overlayPresets = await this.fetchFromBackend(url)
    },

    // fetch all available info from the database for the selected element
    async fetchElementInfo() {
      const url = `get-element-info/${this.elementType}/${this.selectedElement}`
      this.elementInfo = await this.fetchFromBackend(url)
    },

    // fetch all available info from the database for the selected preset
    async fetchPresetInfo() {
      const url = `get-preset-info/${this.elementType}/${this.selectedElement}/${this.selectedPreset}`
      this.presetInfo = await this.fetchFromBackend(url)
    },

    // delete a preset
    async deletePreset() {
      const url = `delete-preset/${this.elementType}/${this.selectedElement}/${this.selectedPreset}`
      const response = await this.fetchFromBackend(url)
      console.log('delete response', response)
    },

    // delete an element
    async deleteElement() {
      const url = `delete-element/${this.elementType}/${this.selectedElement}`
      const response = await this.fetchFromBackend(url)
      console.log('delete response', response)
    },

    // add an element
    async addElement(type: string, name: string) {
      const url = `add-element/${type}/${name}`
      const response = await this.fetchFromBackend(url)
      console.log('add response', response)
    },

    // toggle active status of generator or effect
    async toggleElementActive() {
      const url = `toggle-element-active/${this.elementType}/${this.selectedElement}`
      const response = await this.fetchFromBackend(url)
      console.log('toggle response', response)
    },

    async renamePreset(newName: string) {
      const url = `rename-preset/${this.elementType}/${this.selectedElement}/${this.selectedPreset}/${newName}`
      const response = await this.fetchFromBackend(url)
      console.log('rename response', response)
      this.selectedPreset = newName
    },

    async fetchGradientPresets() {
      const url = `get-gradient-presets`
      const gradients = await this.fetchFromBackend(url)
      this.gradientPresets = gradients.map((preset: any) => ({
        ...preset,
        data: JSON.parse(preset.data) as Array<[number, string]>
      }))
    },

    async saveGradientPreset(gradientArray: Array<[number, string]>, subtype: string) {
      const url = `save-gradient`
      const gradientString = JSON.stringify(gradientArray)
      await this.postToBackend(url, { subtype, gradientString })
      this.fetchGradientPresets()
    },

    async deleteGradientPreset(id: number) {
      const url = `delete-gradient/${id}`
      await this.fetchFromBackend(url)
      this.fetchGradientPresets()
    },

    async checkPresetConsistency() {
      const url = `validate-presets`
      const response = await this.fetchFromBackend(url)
      console.log('Validation results:', response)
      return response
    },

    async clearGradient(channel: number) {
      const url = `clear-gradient/${channel}`
      await this.fetchFromBackend(url)
    },

    async getNetwork() {
      const url = `network-info`
      const response = await this.fetchFromBackend(url)
      return response
    },

    // make GET call
    async fetchFromBackend(url: string) {
      console.log('fetching data from', url)
      try {
        const response = await fetch(`http://0.0.0.0:8000/api/${url}`, {
          method: 'GET',
        })
        const data = await response.json()
        return data
      } catch (error) {
        console.error('error', error)
      }
    },

    // make POST call
    async postToBackend(url: string, data: any) {
      console.log('posting data to', url)
      try {
        const response = await fetch(`http://0.0.0.0:8000/api/${url}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        })
        const result = await response.json()
        return result
      } catch (error) {
        console.error('error', error)
      }
    }
  },

})

<template>
  <div class="min-h-screen bg-zinc-900 text-white">
    <div class="flex items-center justify-between p-4 bg-zinc-800">
      <h1 class="text-2xl font-bold">Admin Panel</h1>
      <!-- Navigation Tabs -->
      <div class="w-full flex gap-4 p-4 bg-zinc-800">
        <button 
          v-for="tab in tabs" 
          :key="tab"
          @click="changeType(tab)"
          class="px-4 py-2 rounded-lg transition-all"
          :class="activeTab === tab ? 'bg-emerald-600' : 'bg-zinc-700 hover:bg-zinc-600'"
        >
          {{ tab }}
        </button>
      </div>
      <div class="flex gap-4">
        <button 
        @click="showAddElementDialog = true, saveType = 'generator'" 
        class="bg-zinc-700 hover:bg-zinc-600 text-zinc-200 px-4 py-2 rounded-lg"
        >
        Add Generator
      </button>
      <button 
      @click="showAddElementDialog = true, saveType = 'effect'" 
        class="bg-zinc-700 hover:bg-zinc-600 text-zinc-200 px-4 py-2 rounded-lg"
        >
        Add Effect
      </button>
      <button 
        @click="handlePresetConsistencyCheck" 
        class="bg-zinc-700 hover:bg-zinc-600 text-zinc-200 px-4 py-2 rounded-lg"
      >
        Check all Presets
      </button>
      </div>

    </div>
    <div 
      v-if="showValidationMessage"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
    >
      <div class="bg-zinc-800 p-6 rounded-lg shadow-xl">
        <p class="text-lg text-zinc-200">
          Check Terminal for preset validation results
        </p>
      </div>
    </div>

    <!-- Add Element Dialog -->
    <div v-if="showAddElementDialog" 
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-2"
      @click="showAddElementDialog = false"
    >
      <div 
        @click.stop
        class="bg-zinc-800 p-6 rounded-lg w-96 space-y-4"
      >
        <h3 class="text-lg font-bold">Add New {{ activeTab }}</h3>
        <form @submit.prevent="handleAddElement" class="space-y-4">
          <div>
            <label class="block text-sm text-zinc-400 mb-1">Name</label>
            <input
              v-model="newElementName"
              type="text"
              class="w-full bg-zinc-700 px-3 py-2 rounded-lg text-white"
              :placeholder="`${activeTab.toLowerCase()}_name`"
              ref="inputRef"
              @keyup.esc="showAddElementDialog = false"
            />
          </div>
          <div class="flex justify-end gap-2">
            <button
              type="button"
              class="px-4 py-2 rounded-lg bg-zinc-700 hover:bg-zinc-600"
              @click="showAddElementDialog = false"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500"
            >
              Add
            </button>
          </div>
        </form>
      </div>
    </div>

    <div 
      v-if="showAddMessage"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
    >
      <div class="bg-zinc-800 p-6 rounded-lg shadow-xl">
        <p class="text-lg text-zinc-200">
          Please restart the program for the new element to take effect
        </p>
      </div>
    </div>




    <div class="p-6">
      <!-- Left Content -->
      <div class="relative">
        <!-- Right Info Panel -->
        <div class="float-right w-80 ml-6">
          <div class="bg-zinc-800 rounded-lg p-4 sticky top-6">
            <div class="border-b border-zinc-700 pb-2 mb-3">
              <h3 class="text-lg font-bold">Info</h3>
            </div>

            <!-- Element Info -->
            <div v-if="selectedType === 'element' && uiState.elementInfo" class="space-y-2">
              <div class="w-48 h-48 rounded-lg overflow-hidden">
                <img 
                  :src="`src/assets/previews/${uiState.selectedElement}_p_basic.gif`"
                  class="w-full h-full object-cover"
                  @error="gifLoadingErrors.set(uiState.presetInfo.name, true)"
                  v-show="!gifLoadingErrors.get(uiState.presetInfo.name)"
                  loading="lazy"
                />
              </div>
              <div>
                <span class="text-zinc-400">Name:</span>
                <span class="font-medium ml-2">{{ uiState.elementInfo.name }}</span>
              </div>
              <div>
                <span class="text-zinc-400">Type:</span>
                <span class="font-medium ml-2">{{ uiState.elementInfo.type }}</span>
              </div>
              <div>
                <span class="text-zinc-400">Created:</span>
                <span class="font-medium ml-2">{{ new Date(uiState.elementInfo.created).toLocaleDateString() }}</span>
              </div>
              <div>
                <span class="text-zinc-400">Usage Count:</span>
                <span class="font-medium ml-2">{{ uiState.elementInfo.usageCount }}</span>
              </div>
              <div>
                <span class="text-zinc-400">Status:</span>
                <span 
                  class="ml-2 px-2 py-0.5 rounded-full text-md font-medium"
                  :class="uiState.elementInfo.isActive ? 'bg-emerald-500/20 text-emerald-300' : 'bg-red-500/20 text-red-300'"
                >
                  {{ uiState.elementInfo.isActive ? 'Active' : 'Inactive' }}
                </span>
              </div>
              <button>
                <span class="font-medium ml-2 text-red-500 hover:text-red-400 transition-colors cursor-pointer"
                  @click="handleToggleElement()"
                >
                  <span v-if="uiState.elementInfo.isActive" class="text-red-500 hover:text-red-400">
                    DEACTIVATE
                  </span>
                  <span v-else class="text-green-500 hover:text-green-400">
                    ACTIVATE
                  </span> 
                </span>
              </button>
              <button>
                <span class="font-medium ml-2 text-red-500 hover:text-red-400 transition-colors cursor-pointer"
                  @click="handleDeleteElement()"
                >
                  DELETE
                </span>
              </button>
            </div>

            <!-- Preset Info -->
            <div v-else-if="selectedType === 'preset' && uiState.presetInfo" class="space-y-3">
              <div class="w-52 h-48 rounded-lg overflow-hidden">
                <img 
                  :src="`src/assets/previews/${uiState.selectedElement}_p_${uiState.presetInfo.name}.gif`"
                  class="w-full h-full object-cover"
                  @error="gifLoadingErrors.set(uiState.presetInfo.name, true)"
                  v-show="!gifLoadingErrors.get(uiState.presetInfo.name)"
                  loading="lazy"
                />
              </div>
              <div>
                <span class="text-zinc-400">Name:</span>
                <span class="font-medium ml-2">{{ uiState.presetInfo.name }}</span>
              </div>
              <div>
                <span class="text-zinc-400">Element:</span>
                <span class="font-medium ml-2">{{ uiState.presetInfo.elementName }}</span>
              </div>
              <div>
                <span class="text-zinc-400">Created:</span>
                <span class="font-medium ml-2">{{ new Date(uiState.presetInfo.created).toLocaleDateString() }}</span>
              </div>
              <div>
                <span class="text-zinc-400">Usage Count:</span>
                <span class="font-medium ml-2">{{ uiState.presetInfo.usageCount || 0 }}</span>
              </div>
              <div class="border-t border-zinc-700 pt-3 mt-3">
                <h4 class="text-zinc-400 font-medium mb-2">Parameters</h4>
                <div class="space-y-2">
                  <div v-for="(value, key) in uiState.presetInfo.data" :key="key" class="flex justify-between">
                    <span class="text-zinc-400">{{ key }}:</span>
                    <span class="font-medium">{{ typeof value === 'number' ? value.toFixed(2) : value }}</span>
                  </div>
                </div>
              </div>
              <button v-if="uiState.presetInfo.name !== 'basic'">
                <span class="text-zinc-400">Delete Preset</span>
                <span class="font-medium ml-2 text-red-500 hover:text-red-400 transition-colors cursor-pointer"
                  @click="deletePreset(uiState.presetInfo.name)"
                >
                  DELETE
                </span>
              </button>
              <button v-if="uiState.presetInfo.name !== 'basic'">
                <span class="text-zinc-400">Rename Preset</span>
                <span class="font-medium ml-2 text-red-500 hover:text-red-400 transition-colors cursor-pointer"
                  @click="showRenamePreset = true"
                >
                  RENAME
                </span>
              </button>
              <input 
                v-if="showRenamePreset" 
                type="text" 
                v-model="newPresetName"
                class="w-full bg-zinc-700 px-3 py-2 rounded-lg text-white"
                placeholder="New Preset Name"
                @keyup.enter="handleNewPresetName"
                @keyup.esc="showRenamePreset = false"
              />
            </div>

            <!-- Empty State -->
            <div v-else class="text-zinc-500 text-center">
              Select an element or preset to view details
            </div>
          </div>  
        </div>

        <div class="flex-1">
          <!-- Element Selector -->
          <div v-if="['Generator', 'Effect'].includes(activeTab)" class="mb-6">
            <div class="flex flex-wrap gap-4">
              <button
                v-for="element in uiState.adminElements"
                :key="element.name"
                @click="handleElementClick(element)"
                class="p-6 rounded-lg transition-all text-center"
                :class="[
                  uiState.selectedElement === element.name ? 'bg-emerald-600' : 'bg-zinc-700 hover:bg-zinc-600',
                  element.active ? 'opacity-100' : 'opacity-50']"
              >
                {{ element.name }}
              </button>
            </div>
          </div>

          <!-- Preset Grid -->
          <div v-if="showPresets" class="mt-6">
            <h2 class="text-xl mb-4">Presets for {{ uiState.selectedElement }}</h2>
            <div class="flex flex-row flex-wrap gap-4">
              <div
                v-for="preset in uiState.overlayPresets"
                :key="preset.name"
                @click="handlePresetClick(preset.name)"
                class="bg-zinc-800 p-1 rounded-lg relative group w-24 h-24"
              >
                <img 
                  :src="`src/assets/previews/${uiState.selectedElement}_p_${preset.name}.gif`"
                  class="object-cover"
                  draggable="false"
                  v-show="!gifLoadingErrors.get(preset.name)"
                  @error="gifLoadingErrors.set(preset.name, true)"
                  ref="imgRef"
                />
                <span class="text-center">
                  {{ preset.name }}
                </span>
              </div>
            </div>
          </div>

          <!-- Channel Settings -->
          <div v-if="activeTab === 'Channel'" class="grid grid-cols-3 gap-4">
            <!-- Channel settings interface -->
          </div>

          <!-- Global Settings -->
          <div v-if="activeTab === 'Global'" class="grid grid-cols-2 gap-4">
            <!-- Global settings interface -->
          </div>
        </div>
        
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onUnmounted, watch, nextTick } from 'vue'
import { useUiStateStore } from '../stores/uiState'

const tabs = ['Generator', 'Effect', 'Channel', 'Global']
const activeTab = ref('Generator')
const showPresets = ref(false)
const gifLoadingErrors = ref(new Map<string, boolean>())
const selectedType = ref<'element' | 'preset' | null>(null)
const uiState = useUiStateStore()
const showAddElementDialog = ref(false)
const newElementName = ref('')
const inputRef = ref<HTMLInputElement | null>(null)
const saveType = ref('')
const showValidationMessage = ref(false)
const showAddMessage = ref(false)
const showRenamePreset = ref(false)
const newPresetName = ref('')

async function changeType(type: string) {
  activeTab.value = type
  selectedType.value = null
  showPresets.value = false
  uiState.dialogType = type.toLowerCase()
  uiState.fetchAllElements()
}

async function handleElementClick(element: any) {
  uiState.selectedElement = element.name
  selectedType.value = 'element'
  uiState.fetchElementInfo()
  uiState.fetchPresets()
  showPresets.value = true
  gifLoadingErrors.value.clear() // Clear previous error states
}

async function handlePresetClick(preset: string) {
  uiState.selectedPreset = preset
  selectedType.value = 'preset'
  uiState.fetchPresetInfo()
}


async function deletePreset(presetName: string) {
  // Don't allow deletion of basic presets
  if (presetName === 'basic') {
    alert("Cannot delete basic preset. It will be deleted automatically when deleting the element.")
    return
  }
  
  if (!confirm(`Are you sure you want to delete preset "${presetName}"?`)) return
  uiState.deletePreset()
  uiState.fetchPresets()
}


async function handleAddElement() {
  if (newElementName.value) {
    await uiState.addElement(saveType.value, newElementName.value)
    showAddElementDialog.value = false
    newElementName.value = ''
    uiState.fetchAllElements()
    // Show message for 2 seconds
    showAddMessage.value = true
    setTimeout(() => {
      showAddMessage.value = false
    }, 2000)
  }
}

async function handleNewPresetName() {
  if (newPresetName.value) {
    await uiState.renamePreset(newPresetName.value)
    showRenamePreset.value = false
    newPresetName.value = ''
    uiState.fetchPresets()
  }
}

async function handleDeleteElement() {
  if (!confirm(`Are you sure you want to delete "${uiState.selectedElement}"? This will also delete all associated presets.`)) {
    return
  }
  uiState.deleteElement()
  uiState.fetchAllElements()
}

async function handleToggleElement() {
  uiState.toggleElementActive()
  uiState.fetchAllElements()
  uiState.fetchElementInfo()
}


async function handlePresetConsistencyCheck() {
  if (confirm('Are you sure you want to check all presets?')) {
    const results = await uiState.checkPresetConsistency()
    console.log(results)
    // Show message for 2 seconds
    showValidationMessage.value = true
    setTimeout(() => {
      showValidationMessage.value = false
    }, 2000)
  }
}

// Focus input when dialog opens
watch(showAddElementDialog, async (newValue) => {
  if (newValue) {
    await nextTick()
    inputRef.value?.focus()
  } else {
    newElementName.value = ''
  }
})


onUnmounted(() => {
  gifLoadingErrors.value.clear()
})

</script>
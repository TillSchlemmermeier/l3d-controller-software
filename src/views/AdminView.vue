<template>
  <div class="h-screen bg-zinc-900 text-white">
    <!-- Header -->
    <div class="flex items-center justify-between p-4 bg-zinc-800">
      <h1 class="text-2xl font-bold">Admin Panel</h1>

      <!-- Navigation Tabs -->
      <div class="w-full flex gap-4 p-4 bg-zinc-800">
        <button 
          v-for="tab in tabs" 
          :key="tab"
          @click="changeType(tab)"
          class="px-6 py-4 rounded-lg transition-all"
          :class="activeTab === tab ? 'bg-emerald-600' : 'bg-zinc-700 hover:bg-zinc-600'"
        >
          {{ tab }}
        </button>
      </div>

      <!-- Action Buttons -->
      <div class="flex gap-4">
        <button 
          @click="openAddDialog('generator')"
          class="bg-zinc-700 hover:bg-zinc-600 text-zinc-200 px-4 py-2 rounded-lg"
        >
          Add Generator
        </button>
        <button
          @click="openAddDialog('effect')"
          class="bg-zinc-700 hover:bg-zinc-600 text-zinc-200 px-4 py-2 rounded-lg"
        >
          Add Effect
        </button>
      </div>
    </div>

    <!-- Status Messages -->
    <StatusMessage
      :show="showAddMessage"
      message="Please restart the program for the new element to take effect"
      @close="showAddMessage = false"
    />

    <!-- Add Element Dialog -->
    <AddElementDialog
      :show="showAddElementDialog"
      :element-type="addElementType"
      @close="showAddElementDialog = false"
      @add="handleAddElement"
    />

    <!-- Main Content -->
    <div class="p-6">
      <div class="relative">
        <!-- Right Info Panel -->
        <div class="float-right w-1/6 ml-6">
          <div class="bg-zinc-800 rounded-lg p-4 pb-12 h-[1250px] overflow-hidden">
            <div class="border-b border-zinc-700">
              <h3 class="text-lg font-bold">Info</h3>
            </div>

            <!-- Element Info -->
            <ElementInfoPanel
              v-if="selectedType === 'element' && uiState.elementInfo"
              @toggle="handleToggleElement"
              @delete="handleDeleteElement"
            />

            <!-- Preset Info -->
            <PresetInfoPanel
              v-else-if="selectedType === 'preset' && uiState.presetInfo"
              @delete="deletePreset"
              @rename="handleRenamePreset"
            />

            <!-- Empty State -->
            <div v-else class="text-zinc-500 text-center">
              Select an element or preset to view details
            </div>
          </div>  
        </div>

        <!-- Left Content -->
        <div class="flex-1">
          <!-- Element Grid -->
          <div class="mb-6">
            <div class="flex flex-wrap gap-4">
              <button
                v-if="activeTab !== 'Channel' && activeTab !== 'Global'"
                v-for="element in uiState.adminElements"
                :key="element.name"
                @click="handleElementClick(element)"
                class="flex flex-col items-center justify-center px-4 h-18 rounded-lg transition-all min-w-[120px]"
                :class="[
                  activeElement === element.name ? 'bg-emerald-600' : 'bg-zinc-700 hover:bg-zinc-600',
                  element.active ? 'opacity-100' : 'opacity-50'
                ]"
              >
                <div class="font-medium">{{ element.name }}</div>
                <div v-if="!element.active" class="text-xs text-zinc-400">
                  (Inactive)
                </div>
              </button>
            </div>
          </div>

          <!-- Preset Grid -->
          <PresetGrid
            v-if="showPresets"
            :element-type="activeElementType"
            :element-name="activeElement"
            @select="handlePresetClick"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useUiStateStore } from '../stores/uiState'
import { dialog } from '../components/ConfirmDialog.vue'
import AddElementDialog from '../components/AdminSection/AddElementDialog.vue'
import StatusMessage from '../components/AdminSection/StatusMessage.vue'
import ElementInfoPanel from '../components/AdminSection/ElementInfoPanel.vue'
import PresetInfoPanel from '../components/AdminSection/PresetInfoPanel.vue'
import PresetGrid from '../components/AdminSection/PresetGrid.vue'

const tabs = ['Generator', 'Effect', 'Channel', 'Global']
const activeTab = ref('Generator')
const activeElement = ref('g_cube')
const activeElementType = ref('generator')
const showPresets = ref(false)
const selectedType = ref<'element' | 'preset' | null>(null)
const uiState = useUiStateStore()

// Dialog states
const showAddElementDialog = ref(false)
const addElementType = ref('')
const showAddMessage = ref(false)

async function changeType(type: string) {
  activeElementType.value = type.toLowerCase()
  activeTab.value = type
  selectedType.value = null
  showPresets.value = false
  uiState.elementType = type.toLowerCase()
  await uiState.fetchAllElements()
  if (type === 'Channel' || type === 'Global') {
    handleElementClick({name: 'presets'})
  }
}

async function handleElementClick(element: any) {
  uiState.selectedElement = element.name
  activeElement.value = element.name
  selectedType.value = 'element'
  await uiState.fetchElementInfo()
  // await uiState.fetchPresets()
  await uiState.fetchAllPresets()
  showPresets.value = true
}

async function handlePresetClick(presetName: string, presetType: string) {
  uiState.selectedPreset = presetName

  if (presetType === 'channel') {
    uiState.elementType = 'channel'
    uiState.selectedElement = 'presets'
  } else if (presetType === 'global') {
    uiState.elementType = 'global'
    uiState.selectedElement = 'presets'
  } else {
    uiState.elementType = activeElementType.value
    uiState.selectedElement = activeElement.value
  }
  selectedType.value = 'preset'
  uiState.fetchPresetInfo()
}

function openAddDialog(type: string) {
  addElementType.value = type
  showAddElementDialog.value = true
}

async function handleAddElement(name: string) {
  await uiState.addElement(addElementType.value, name)
  showAddElementDialog.value = false
  await uiState.fetchAllElements()

  showAddMessage.value = true
  setTimeout(() => {
    showAddMessage.value = false
  }, 2000)
}

async function deletePreset() {
  if (uiState.selectedPreset === 'basic') {
    await dialog.alert({
      title: 'Cannot delete',
      message: "Cannot delete the basic preset. It is removed automatically when the element is deleted.",
    })
    return
  }

  if (!await dialog.confirm({
    title: 'Delete preset',
    message: `Delete preset "${uiState.selectedPreset}"?`,
    confirmText: 'Delete',
    danger: true,
  })) return

  uiState.deletePreset()
  uiState.fetchPresets()
}

async function handleRenamePreset(newName: string) {
  await uiState.renamePreset(newName)
  uiState.fetchPresets()
}

async function handleDeleteElement() {
  if (!await dialog.confirm({
    title: 'Delete element',
    message: `Delete "${uiState.selectedElement}"? This will also delete all associated presets.`,
    confirmText: 'Delete',
    danger: true,
  })) return

  await uiState.deleteElement()
  await uiState.fetchAllElements()
}

async function handleToggleElement() {
  await uiState.toggleElementActive()
  await uiState.fetchAllElements()
  await uiState.fetchElementInfo()
}
</script>
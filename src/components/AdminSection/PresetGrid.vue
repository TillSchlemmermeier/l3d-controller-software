<template>
  <div class="mt-6 space-y-8 overflow-y-auto">
    <!-- Element Presets -->
    <div v-if="['generator', 'effect'].includes(props.elementType) && elementPresets.length > 0">
      <h2 @click="isElementCollapsed = !isElementCollapsed" class="text-xl mb-4 cursor-pointer flex items-center">
        Element Presets for {{ displayName }}
        <span class="ml-2 text-zinc-400">{{ isElementCollapsed ? '▶' : '▼' }}</span>
      </h2>
      <div v-show="!isElementCollapsed" class="space-y-4">
        <div class="flex flex-row flex-wrap gap-4">
          <div
            v-for="preset in paginatedElementPresets"
            :key="`element-${preset.name}`"
            @click="$emit('select', preset.name, props.elementType)"
            class="bg-zinc-800 p-2 rounded-lg relative group cursor-pointer hover:bg-zinc-700 transition-colors"
            :class="selectedPreset === preset.name ? 'ring-2 ring-emerald-500' : ''"
          >
            <div class="w-24 h-24 rounded overflow-hidden mb-2">
              <img
                :src="`src/assets/previews/${props.elementName}_p_${preset.name}.gif`"
                :key="`element-${preset.name}`"
                class="w-full h-full object-cover"
                draggable="false"
                v-show="!imageErrors.has(preset.name)"
                @error="handleImageError(preset.name)"
                loading="lazy"
              />
              <div
                v-if="imageErrors.has(preset.name)"
                class="w-full h-full bg-zinc-700 flex items-center justify-center"
              >
                <span class="text-zinc-500 text-xs">No preview</span>
              </div>
            </div>
            <span class="text-center text-sm block truncate">
              {{ preset.name }}
            </span>
          </div>
        </div>
        <!-- Pagination for Element Presets -->
        <div v-if="elementPresets.length > 50" class="flex justify-center mt-4">
          <button
            @click="elementPage = Math.max(1, elementPage - 1)"
            :disabled="elementPage === 1"
            class="px-3 py-1 bg-zinc-700 hover:bg-zinc-600 disabled:bg-zinc-800 disabled:cursor-not-allowed rounded mr-2"
          >
            Prev
          </button>
          <span class="px-3 py-1 text-zinc-300">
            {{ elementPage }} / {{ Math.ceil(elementPresets.length / 50) }}
          </span>
          <button
            @click="elementPage = Math.min(Math.ceil(elementPresets.length / 50),elementPage + 1)" 
            :disabled="elementPage === Math.ceil(elementPresets.length / 50)"
            class="px-3 py-1 bg-zinc-700 hover:bg-zinc-600 disabled:bg-zinc-800 disabled:cursor-not-allowed rounded ml-2"
          >
            Next
          </button>
        </div>
      </div>
    </div>

    <!-- Channel Presets -->
    <div v-if="channelPresets.length > 0">
      <h2 @click="isChannelCollapsed = !isChannelCollapsed" class="text-xl mb-4 cursor-pointer flex items-center">
        Channel Presets using {{ displayName }}
        <span class="text-sm text-zinc-400 ml-2">({{ channelPresets.length }})</span>
        <span class="ml-2 text-zinc-400">{{ isChannelCollapsed ? '▶' : '▼' }}</span>
      </h2>
      <div v-show="!isChannelCollapsed" class="space-y-4">
        <div class="flex flex-row flex-wrap gap-4">
          <div
            v-for="preset in paginatedChannelPresets"
            :key="`channel-${preset.name}`"
            @click="$emit('select', preset.name, 'channel')"
            class="bg-zinc-800 p-2 rounded-lg relative group cursor-pointer hover:bg-zinc-700 transition-colors border border-blue-500/30"
            :class="selectedPreset === preset.name ? 'ring-2 ring-emerald-500' : ''"
          >
            <div class="w-24 h-24 rounded overflow-hidden mb-2">
              <img
                :src="`src/assets/previews/channel_p_${preset.name}.gif`"
                :key="`channel-${preset.name}`"
                class="w-full h-full object-cover"
                draggable="false"
                v-show="!imageErrors.has(preset.name)"
                @error="handleImageError(preset.name)"
                loading="lazy"
              />
              <div
                v-if="imageErrors.has(preset.name)"
                class="w-full h-full bg-zinc-700 flex items-center justify-center"
              >
                <span class="text-zinc-500 text-xs">No preview</span>
              </div>
            </div>
            <span class="text-center text-sm block truncate">
              {{ preset.name }}
            </span>
          </div>
        </div>
        <!-- Pagination for Channel Presets -->
        <div v-if="channelPresets.length > 50" class="flex justify-center mt-4">
          <button
            @click="channelPage = Math.max(1, channelPage - 1)"
            :disabled="channelPage === 1"
            class="px-3 py-1 bg-zinc-700 hover:bg-zinc-600 disabled:bg-zinc-800 disabled:cursor-not-allowed rounded mr-2"
          >
            Prev
          </button>
          <span class="px-3 py-1 text-zinc-300">
            {{ channelPage }} / {{ Math.ceil(channelPresets.length / 50) }}
          </span>
          <button
            @click="channelPage = Math.min(Math.ceil(channelPresets.length / 50),channelPage + 1)" 
            :disabled="channelPage === Math.ceil(channelPresets.length / 50)"
            class="px-3 py-1 bg-zinc-700 hover:bg-zinc-600 disabled:bg-zinc-800 disabled:cursor-not-allowed rounded ml-2"
          >
            Next
          </button>
        </div>
      </div>
    </div>

    <!-- Global Presets -->
    <div v-if="globalPresets.length > 0">
      <h2 @click="isGlobalCollapsed = !isGlobalCollapsed" class="text-xl mb-4 cursor-pointer flex items-center">
        Global Presets using {{ displayName }}
        <span class="text-sm text-zinc-400 ml-2">({{ globalPresets.length }})</span>
        <span class="ml-2 text-zinc-400">{{ isGlobalCollapsed ? '▶' : '▼' }}</span>
      </h2>
      <div v-show="!isGlobalCollapsed" class="space-y-4">
        <div class="flex flex-row flex-wrap gap-4">
          <div
            v-for="preset in paginatedGlobalPresets"
            :key="`global-${preset.name}`"
            @click="$emit('select', preset.name, 'global')"
            class="bg-zinc-800 p-2 rounded-lg relative group cursor-pointer hover:bg-zinc-700 transition-colors border border-purple-500/30"
            :class="selectedPreset === preset.name ? 'ring-2 ring-emerald-500' : ''"
          >
           <div class="w-24 h-24 rounded overflow-hidden mb-2">
              <img
                :src="`src/assets/previews/global_p_${preset.name}.gif`"
                :key="`global-${preset.name}`"
                class="w-full h-full object-cover"
                draggable="false"
                v-show="!imageErrors.has(preset.name)"
                @error="handleImageError(preset.name)"
                loading="lazy"
              />
              <div
                v-if="imageErrors.has(preset.name)"
                class="w-full h-full bg-zinc-700 flex items-center justify-center"
              >
                <span class="text-zinc-500 text-xs">No preview</span>
              </div>
            </div>
            <span class="text-center text-sm block truncate">
              {{ preset.name }}
            </span>
          </div>
        </div>
        <!-- Pagination for Global Presets -->
        <div v-if="globalPresets.length > 50" class="flex justify-center mt-4">
          <button
            @click="globalPage = Math.max(1, globalPage - 1)"
            :disabled="globalPage === 1"
            class="px-3 py-1 bg-zinc-700 hover:bg-zinc-600 disabled:bg-zinc-800 disabled:cursor-not-allowed rounded mr-2"
          >
            Prev
          </button>
          <span class="px-3 py-1 text-zinc-300">
            {{ globalPage }} / {{ Math.ceil(globalPresets.length / 50) }}
          </span>
          <button
            @click="globalPage = Math.min(Math.ceil(globalPresets.length / 50), globalPage + 1)"
            :disabled="globalPage === Math.ceil(globalPresets.length / 50)"
            class="px-3 py-1 bg-zinc-700 hover:bg-zinc-600 disabled:bg-zinc-800 disabled:cursor-not-allowed rounded ml-2"
          >
            Next
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="elementPresets.length === 0 && channelPresets.length === 0 && globalPresets.length === 0" 
         class="text-center text-zinc-500 py-8">
      No presets found for {{ displayName }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useUiStateStore } from '../../stores/uiState'

const uiState = useUiStateStore()

const props = defineProps<{
  elementType: string
  elementName: string
}>()

const selectedPreset = computed(() => uiState.selectedPreset)

// Use props for display name (fixed for the grid)
const displayName = computed(() => {
  return ['generator', 'effect'].includes(props.elementType) ? props.elementName : props.elementType
})

// Filter element presets based on props (original element type)
const elementPresets = computed(() => 
  uiState.adminPresets.filter(p => p.type === props.elementType)
)

const channelPresets = computed(() => 
  uiState.adminPresets.filter(p => p.type === 'channel')
)

const globalPresets = computed(() => 
  uiState.adminPresets.filter(p => p.type === 'global')
)

// Pagination state
const elementPage = ref(1)
const channelPage = ref(1)
const globalPage = ref(1)

// Collapse state
const isElementCollapsed = ref(false)
const isChannelCollapsed = ref(false)
const isGlobalCollapsed = ref(false)

// Paginated computed properties
const paginatedElementPresets = computed(() => {
  const start = (elementPage.value - 1) * 50
  const end = start + 50
  return elementPresets.value.slice(start, end)
})

const paginatedChannelPresets = computed(() => {
  const start = (channelPage.value - 1) * 50
  const end = start + 50
  return channelPresets.value.slice(start, end)
})

const paginatedGlobalPresets = computed(() => {
  const start = (globalPage.value - 1) * 50
  const end = start + 50
  return globalPresets.value.slice(start, end)
})

defineEmits<{
  select: [presetName: string, presetType: string]
}>()

const imageErrors = ref(new Set<string>())

function handleImageError(presetName: string) {
  imageErrors.value.add(presetName)
}
</script>
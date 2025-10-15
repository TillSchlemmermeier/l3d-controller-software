<template>
  <div class="mt-6 space-y-8 overflow-y-auto">
    <!-- Element Presets -->
    <div v-if="['generator', 'effect'].includes(props.elementType) && elementPresets.length > 0">
      <h2 class="text-xl mb-4">Element Presets for {{ displayName }}</h2>
      <div class="flex flex-row flex-wrap gap-4">
        <div
          v-for="preset in elementPresets"
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
    </div>

    <!-- Channel Presets -->
    <div v-if="channelPresets.length > 0">
      <h2 class="text-xl mb-4">
        Channel Presets using {{ displayName }}
        <span class="text-sm text-zinc-400 ml-2">({{ channelPresets.length }})</span>
      </h2>
      <div class="flex flex-row flex-wrap gap-4">
        <div
          v-for="preset in channelPresets"
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
    </div>

    <!-- Global Presets -->
    <div v-if="globalPresets.length > 0">
      <h2 class="text-xl mb-4">
        Global Presets using {{ displayName }}
        <span class="text-sm text-zinc-400 ml-2">({{ globalPresets.length }})</span>
      </h2>
      <div class="flex flex-row flex-wrap gap-4">
        <div
          v-for="preset in globalPresets"
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

defineEmits<{
  select: [presetName: string, presetType: string]
}>()

const imageErrors = ref(new Set<string>())

function handleImageError(presetName: string) {
  imageErrors.value.add(presetName)
}
</script>
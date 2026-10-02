<template>
  <div class="mt-6 space-y-8 overflow-y-auto">
    <template v-for="section in sections" :key="section.key">
      <div v-if="section.visible && section.presets.length > 0">
        <h2 @click="collapsed[section.key] = !collapsed[section.key]" class="text-xl mb-4 cursor-pointer flex items-center">
          {{ section.title }} {{ displayName }}
          <span v-if="section.showCount" class="text-sm text-zinc-400 ml-2">({{ section.presets.length }})</span>
          <span class="ml-2 text-zinc-400">{{ collapsed[section.key] ? '▶' : '▼' }}</span>
        </h2>
        <div v-show="!collapsed[section.key]" class="space-y-4">
          <div class="flex flex-row flex-wrap gap-4">
            <div
              v-for="preset in section.presets.slice((page[section.key] - 1) * 50, page[section.key] * 50)"
              :key="`${section.key}-${preset.name}`"
              @click="$emit('select', preset.name, section.type)"
              class="bg-zinc-800 p-2 rounded-lg relative group cursor-pointer hover:bg-zinc-700 transition-colors"
              :class="[section.border, selectedPreset === preset.name ? 'ring-2 ring-emerald-500' : '']"
            >
              <div class="w-24 h-24 rounded overflow-hidden mb-2">
                <img
                  :src="`src/assets/previews/${section.imagePrefix}_p_${preset.name}.gif`"
                  :key="`${section.key}-${preset.name}`"
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
          <div v-if="section.presets.length > 50" class="flex justify-center mt-4">
            <button
              @click="page[section.key] = Math.max(1, page[section.key] - 1)"
              :disabled="page[section.key] === 1"
              class="px-3 py-1 bg-zinc-700 hover:bg-zinc-600 disabled:bg-zinc-800 disabled:cursor-not-allowed rounded mr-2"
            >
              Prev
            </button>
            <span class="px-3 py-1 text-zinc-300">
              {{ page[section.key] }} / {{ Math.ceil(section.presets.length / 50) }}
            </span>
            <button
              @click="page[section.key] = Math.min(Math.ceil(section.presets.length / 50), page[section.key] + 1)"
              :disabled="page[section.key] === Math.ceil(section.presets.length / 50)"
              class="px-3 py-1 bg-zinc-700 hover:bg-zinc-600 disabled:bg-zinc-800 disabled:cursor-not-allowed rounded ml-2"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </template>

    <!-- Empty State -->
    <div v-if="elementPresets.length === 0 && channelPresets.length === 0 && globalPresets.length === 0" 
         class="text-center text-zinc-500 py-8">
      No presets found for {{ displayName }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive } from 'vue'
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

type SectionKey = 'element' | 'channel' | 'global'

// The three sections differ only in these fields; everything else in the template is shared.
const sections = computed(() => [
  {
    key: 'element' as SectionKey,
    title: 'Element Presets for',
    visible: ['generator', 'effect'].includes(props.elementType),
    showCount: false,
    presets: elementPresets.value,
    type: props.elementType,
    imagePrefix: props.elementName,
    border: '',
  },
  {
    key: 'channel' as SectionKey,
    title: 'Channel Presets using',
    visible: true,
    showCount: true,
    presets: channelPresets.value,
    type: 'channel',
    imagePrefix: 'channel',
    border: 'border border-blue-500/30',
  },
  {
    key: 'global' as SectionKey,
    title: 'Global Presets using',
    visible: true,
    showCount: true,
    presets: globalPresets.value,
    type: 'global',
    imagePrefix: 'global',
    border: 'border border-purple-500/30',
  },
])

// Pagination (50 per page) and collapse state per section
const page = reactive<Record<SectionKey, number>>({ element: 1, channel: 1, global: 1 })
const collapsed = reactive<Record<SectionKey, boolean>>({ element: false, channel: false, global: false })

defineEmits<{
  select: [presetName: string, presetType: string]
}>()

const imageErrors = ref(new Set<string>())

function handleImageError(presetName: string) {
  imageErrors.value.add(presetName)
}
</script>
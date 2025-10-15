<!-- filepath: /home/yannig/dev/l3d-controller-software/src/components/PresetUpdater.vue -->
<template>
  <div class="bg-zinc-800 rounded-lg p-6 space-y-6">
    <div class="border-b border-zinc-700 pb-4">
      <h3 class="text-xl font-bold">Update Presets for {{ elementName }}</h3>
      <p class="text-zinc-400 text-sm mt-1">
        Modify parameters and update all associated presets
      </p>
    </div>

    <!-- Update Type Selector -->
    <div class="space-y-2">
      <label class="block text-sm font-medium text-zinc-300">Update Type</label>
      <select 
        v-model="updateType"
        class="w-full bg-zinc-700 px-4 py-2 rounded-lg text-white border border-zinc-600 focus:border-emerald-500 focus:outline-none"
      >
        <option value="">Select update type...</option>
        <optgroup label="Category Changes">
          <option value="category_added">Category Added</option>
          <option value="category_removed">Category Removed</option>
          <option value="category_renamed">Category Renamed</option>
        </optgroup>
        <optgroup label="Range Changes">
          <option value="range_extended">Range Extended</option>
          <option value="range_shrinked">Range Shrinked</option>
        </optgroup>
        <optgroup label="Parameter Changes">
          <option value="param_added">Parameter Added</option>
          <option value="param_removed">Parameter Removed</option>
          <option value="param_renamed">Parameter Renamed</option>
        </optgroup>
      </select>
    </div>

    <!-- Parameter Selector -->
    <div v-if="updateType" class="space-y-2">
      <label class="block text-sm font-medium text-zinc-300">Parameter</label>
      <select 
        v-model="paramIndex"
        class="w-full bg-zinc-700 px-4 py-2 rounded-lg text-white border border-zinc-600 focus:border-emerald-500 focus:outline-none"
      >
        <option :value="null">Select parameter...</option>
        <option v-for="(param, index) in parameters" :key="index" :value="index">
          {{ param.label }} ({{ param.name }})
        </option>
      </select>
    </div>

    <!-- Category Added/Removed/Renamed Forms -->
    <div v-if="updateType.startsWith('category_') && paramIndex !== null" class="space-y-4">
      <div class="space-y-2">
        <label class="block text-sm font-medium text-zinc-300">Old Categories</label>
        <div class="space-y-2">
          <div v-for="(_, index) in oldCategories" :key="index" class="flex gap-2">
            <input 
              v-model="oldCategories[index]"
              type="text"
              class="flex-1 bg-zinc-700 px-3 py-2 rounded-lg text-white border border-zinc-600"
              placeholder="Category name"
            />
            <button 
              @click="oldCategories.splice(index, 1)"
              class="px-3 py-2 bg-red-600 hover:bg-red-500 rounded-lg"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
          <button 
            @click="oldCategories.push('')"
            class="w-full px-3 py-2 bg-zinc-700 hover:bg-zinc-600 rounded-lg border border-zinc-600 border-dashed"
          >
            + Add Category
          </button>
        </div>
      </div>

      <div class="space-y-2">
        <label class="block text-sm font-medium text-zinc-300">New Categories</label>
        <div class="space-y-2">
          <div v-for="(_, index) in newCategories" :key="index" class="flex gap-2">
            <input 
              v-model="newCategories[index]"
              type="text"
              class="flex-1 bg-zinc-700 px-3 py-2 rounded-lg text-white border border-zinc-600"
              placeholder="Category name"
            />
            <button 
              @click="newCategories.splice(index, 1)"
              class="px-3 py-2 bg-red-600 hover:bg-red-500 rounded-lg"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
          <button 
            @click="newCategories.push('')"
            class="w-full px-3 py-2 bg-zinc-700 hover:bg-zinc-600 rounded-lg border border-zinc-600 border-dashed"
          >
            + Add Category
          </button>
        </div>
      </div>

      <div v-if="updateType === 'category_removed'" class="space-y-2">
        <label class="block text-sm font-medium text-zinc-300">Fallback Category (optional)</label>
        <select 
          v-model="fallbackCategory"
          class="w-full bg-zinc-700 px-4 py-2 rounded-lg text-white border border-zinc-600"
        >
          <option :value="null">Delete presets using removed category</option>
          <option v-for="cat in newCategories" :key="cat" :value="cat">{{ cat }}</option>
        </select>
      </div>
    </div>

    <!-- Range Extended/Shrinked Forms -->
    <div v-if="updateType.startsWith('range_') && paramIndex !== null" class="space-y-4">
      <div class="grid grid-cols-2 gap-4">
        <div class="space-y-2">
          <label class="block text-sm font-medium text-zinc-300">Old Min</label>
          <input 
            v-model.number="oldMin"
            type="number"
            step="any"
            class="w-full bg-zinc-700 px-3 py-2 rounded-lg text-white border border-zinc-600"
          />
        </div>
        <div class="space-y-2">
          <label class="block text-sm font-medium text-zinc-300">Old Max</label>
          <input 
            v-model.number="oldMax"
            type="number"
            step="any"
            class="w-full bg-zinc-700 px-3 py-2 rounded-lg text-white border border-zinc-600"
          />
        </div>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div class="space-y-2">
          <label class="block text-sm font-medium text-zinc-300">New Min</label>
          <input 
            v-model.number="newMin"
            type="number"
            step="any"
            class="w-full bg-zinc-700 px-3 py-2 rounded-lg text-white border border-zinc-600"
          />
        </div>
        <div class="space-y-2">
          <label class="block text-sm font-medium text-zinc-300">New Max</label>
          <input 
            v-model.number="newMax"
            type="number"
            step="any"
            class="w-full bg-zinc-700 px-3 py-2 rounded-lg text-white border border-zinc-600"
          />
        </div>
      </div>

      <div class="flex items-center gap-2">
        <input 
          v-model="keepAbsolute"
          type="checkbox"
          id="keepAbsolute"
          class="w-4 h-4 bg-zinc-700 border-zinc-600 rounded"
        />
        <label for="keepAbsolute" class="text-sm text-zinc-300">
          Keep absolute values (recalculate MIDI)
        </label>
      </div>
      <p class="text-xs text-zinc-500">
        If unchecked, MIDI values stay the same (proportional scaling)
      </p>
    </div>

    <!-- Parameter Added Form -->
    <div v-if="updateType === 'param_added'" class="space-y-4">
      <div class="space-y-2">
        <label class="block text-sm font-medium text-zinc-300">Parameter Name</label>
        <input 
          v-model="newParamName"
          type="text"
          class="w-full bg-zinc-700 px-3 py-2 rounded-lg text-white border border-zinc-600"
          placeholder="param_name"
        />
      </div>

      <div class="space-y-2">
        <label class="block text-sm font-medium text-zinc-300">Parameter Label</label>
        <input 
          v-model="newParamLabel"
          type="text"
          class="w-full bg-zinc-700 px-3 py-2 rounded-lg text-white border border-zinc-600"
          placeholder="Parameter Label"
        />
      </div>

      <div class="space-y-2">
        <label class="block text-sm font-medium text-zinc-300">Default MIDI Value</label>
        <input 
          v-model.number="defaultMidi"
          type="number"
          min="0"
          max="1"
          step="0.01"
          class="w-full bg-zinc-700 px-3 py-2 rounded-lg text-white border border-zinc-600"
        />
      </div>

      <div class="space-y-2">
        <label class="block text-sm font-medium text-zinc-300">Insert Position</label>
        <select 
          v-model.number="insertPosition"
          class="w-full bg-zinc-700 px-4 py-2 rounded-lg text-white border border-zinc-600"
        >
          <option v-for="i in parameters.length + 1" :key="i" :value="i - 1">
            Position {{ i }} {{ i === 1 ? '(beginning)' : i === parameters.length + 1 ? '(end)' : '' }}
          </option>
        </select>
      </div>
    </div>

    <!-- Parameter Removed Form -->
    <div v-if="updateType === 'param_removed' && paramIndex !== null" class="space-y-4">
      <div class="flex items-center gap-2">
        <input 
          v-model="deletePresets"
          type="checkbox"
          id="deletePresets"
          class="w-4 h-4 bg-zinc-700 border-zinc-600 rounded"
        />
        <label for="deletePresets" class="text-sm text-zinc-300">
          Delete presets instead of removing parameter
        </label>
      </div>
      <p class="text-xs text-zinc-500">
        If checked, all presets using this element will be deleted
      </p>
    </div>

    <!-- Parameter Renamed Form -->
    <div v-if="updateType === 'param_renamed' && paramIndex !== null" class="space-y-4">
      <div class="space-y-2">
        <label class="block text-sm font-medium text-zinc-300">New Parameter Name</label>
        <input 
          v-model="newParamName"
          type="text"
          class="w-full bg-zinc-700 px-3 py-2 rounded-lg text-white border border-zinc-600"
          placeholder="new_param_name"
        />
      </div>

      <div class="space-y-2">
        <label class="block text-sm font-medium text-zinc-300">New Parameter Label</label>
        <input 
          v-model="newParamLabel"
          type="text"
          class="w-full bg-zinc-700 px-3 py-2 rounded-lg text-white border border-zinc-600"
          placeholder="New Parameter Label"
        />
      </div>
    </div>

    <!-- Preview Section -->
    <div v-if="updateType && canPreview" class="bg-zinc-900 rounded-lg p-4 space-y-2">
      <h4 class="text-sm font-medium text-zinc-300">Preview</h4>
      <div class="text-sm text-zinc-400 space-y-1">
        <p>Affected presets will be updated automatically</p>
        <p class="text-yellow-500" v-if="willDeletePresets">
          ⚠️ Some presets may be deleted based on your settings
        </p>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="flex gap-3 pt-4 border-t border-zinc-700">
      <button 
        @click="handlePreview"
        :disabled="!canSubmit"
        class="flex-1 px-4 py-2 bg-zinc-700 hover:bg-zinc-600 disabled:bg-zinc-800 disabled:text-zinc-600 rounded-lg transition-colors"
      >
        Preview Changes
      </button>
      <button 
        @click="handleUpdate"
        :disabled="!canSubmit"
        class="flex-1 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 disabled:bg-zinc-800 disabled:text-zinc-600 rounded-lg transition-colors font-medium"
      >
        Update All Presets
      </button>
    </div>

    <!-- Results Dialog -->
    <div v-if="showResults" 
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
      @click="showResults = false"
    >
      <div 
        @click.stop
        class="bg-zinc-800 p-6 rounded-lg w-[500px] max-h-[80vh] overflow-y-auto space-y-4"
      >
        <h3 class="text-lg font-bold">Update Results</h3>
        
        <div class="space-y-2">
          <div class="flex justify-between text-sm">
            <span class="text-zinc-400">Total Presets:</span>
            <span class="font-medium">{{ results.total }}</span>
          </div>
          <div class="flex justify-between text-sm">
            <span class="text-zinc-400">Updated:</span>
            <span class="font-medium text-emerald-400">{{ results.updated }}</span>
          </div>
          <div class="flex justify-between text-sm">
            <span class="text-zinc-400">Deleted:</span>
            <span class="font-medium text-red-400">{{ results.deleted }}</span>
          </div>
          <div v-if="results.errors.length > 0" class="flex justify-between text-sm">
            <span class="text-zinc-400">Errors:</span>
            <span class="font-medium text-yellow-400">{{ results.errors.length }}</span>
          </div>
        </div>

        <div v-if="results.errors.length > 0" class="mt-4">
          <h4 class="text-sm font-medium text-zinc-300 mb-2">Errors</h4>
          <div class="space-y-2 max-h-40 overflow-y-auto">
            <div v-for="(error, index) in results.errors" :key="index" 
              class="text-sm bg-zinc-900 p-2 rounded"
            >
              <div class="font-medium text-yellow-400">{{ error.preset }}</div>
              <div class="text-zinc-400 text-xs">{{ error.error }}</div>
            </div>
          </div>
        </div>

        <button 
          @click="showResults = false"
          class="w-full px-4 py-2 bg-emerald-600 hover:bg-emerald-500 rounded-lg"
        >
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

interface Parameter {
  name: string
  label: string
  index: number
}

const props = defineProps<{
  elementName: string
  elementType: string
  parameters: Parameter[]
}>()

const emit = defineEmits<{
  update: [config: any]
  preview: [config: any]
}>()

// Form state
const updateType = ref('')
const paramIndex = ref<number | null>(null)

// Category fields
const oldCategories = ref<string[]>([''])
const newCategories = ref<string[]>([''])
const fallbackCategory = ref<string | null>(null)

// Range fields
const oldMin = ref(0)
const oldMax = ref(1)
const newMin = ref(0)
const newMax = ref(1)
const keepAbsolute = ref(true)

// Parameter fields
const newParamName = ref('')
const newParamLabel = ref('')
const defaultMidi = ref(0.5)
const deletePresets = ref(false)
const insertPosition = ref(0)

// Results
const showResults = ref(false)
const results = ref({
  total: 0,
  updated: 0,
  deleted: 0,
  errors: []
})

const canSubmit = computed(() => {
  if (!updateType.value || paramIndex.value === null) return false

  if (updateType.value.startsWith('category_')) {
    return oldCategories.value.some(c => c.trim()) && 
           newCategories.value.some(c => c.trim())
  }

  if (updateType.value.startsWith('range_')) {
    return oldMin.value < oldMax.value && newMin.value < newMax.value
  }

  if (updateType.value === 'param_added') {
    return newParamName.value.trim() && newParamLabel.value.trim()
  }

  if (updateType.value === 'param_renamed') {
    return newParamName.value.trim() && newParamLabel.value.trim()
  }

  return true
})

const canPreview = computed(() => canSubmit.value)

const willDeletePresets = computed(() => {
  return (updateType.value === 'category_removed' && !fallbackCategory.value) ||
         (updateType.value === 'param_removed' && deletePresets.value)
})

function buildConfig() {
  const config: any = {
    element_name: props.elementName,
    element_type: props.elementType,
    update_type: updateType.value,
    param_index: paramIndex.value
  }

  if (updateType.value.startsWith('category_')) {
    config.old_categories = oldCategories.value.filter(c => c.trim())
    config.new_categories = newCategories.value.filter(c => c.trim())
    if (updateType.value === 'category_removed') {
      config.fallback_category = fallbackCategory.value
    }
  } else if (updateType.value.startsWith('range_')) {
    config.old_min = oldMin.value
    config.old_max = oldMax.value
    config.new_min = newMin.value
    config.new_max = newMax.value
    config.keep_absolute = keepAbsolute.value
  } else if (updateType.value === 'param_added') {
    config.param_name = newParamName.value
    config.param_label = newParamLabel.value
    config.default_midi = defaultMidi.value
    config.param_index = insertPosition.value
  } else if (updateType.value === 'param_removed') {
    config.delete_preset = deletePresets.value
  } else if (updateType.value === 'param_renamed') {
    config.new_name = newParamName.value
    config.new_label = newParamLabel.value
  }

  return config
}

function handlePreview() {
  emit('preview', buildConfig())
}

function handleUpdate() {
  if (confirm(`This will update all presets for ${props.elementName}. Continue?`)) {
    emit('update', buildConfig())
  }
}

function showUpdateResults(data: any) {
  results.value = data
  showResults.value = true
}

// Reset form when update type changes
watch(updateType, () => {
  paramIndex.value = null
  oldCategories.value = ['']
  newCategories.value = ['']
  fallbackCategory.value = null
  newParamName.value = ''
  newParamLabel.value = ''
  deletePresets.value = false
})

// Expose method to parent
defineExpose({
  showUpdateResults
})
</script>
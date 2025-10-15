<template>
  <div class="space-y-2">
    <div class="w-48 h-48 rounded-lg overflow-hidden">
      <img 
        :src="`src/assets/previews/${elementInfo.name}_p_basic.gif`"
        class="w-full h-full object-cover"
        @error="handleImageError"
        v-show="!imageError"
        loading="lazy"
      />
    </div>
    <div>
      <span class="text-zinc-400">Name:</span>
      <span class="font-medium ml-2">{{ elementInfo.name }}</span>
    </div>
    <div>
      <span class="text-zinc-400">Type:</span>
      <span class="font-medium ml-2">{{ elementInfo.type }}</span>
    </div>
    <div>
      <span class="text-zinc-400">Created:</span>
      <span class="font-medium ml-2">{{ formattedDate }}</span>
    </div>
    <div>
      <span class="text-zinc-400">Usage Count:</span>
      <span class="font-medium ml-2">{{ elementInfo.usageCount }}</span>
    </div>
    <div>
      <span class="text-zinc-400">Status:</span>
      <span 
        class="ml-2 px-2 py-0.5 rounded-full text-md font-medium"
        :class="elementInfo.isActive ? 'bg-emerald-500/20 text-emerald-300' : 'bg-red-500/20 text-red-300'"
      >
        {{ elementInfo.isActive ? 'Active' : 'Inactive' }}
      </span>
    </div>
    <button class="w-full">
      <span 
        class="font-medium ml-2 transition-colors cursor-pointer"
        :class="elementInfo.isActive ? 'text-red-500 hover:text-red-400' : 'text-green-500 hover:text-green-400'"
        @click="$emit('toggle')"
      >
        {{ elementInfo.isActive ? 'DEACTIVATE' : 'ACTIVATE' }}
      </span>
    </button>
    <button class="w-full">
      <span 
        class="font-medium ml-2 text-red-500 hover:text-red-400 transition-colors cursor-pointer"
        @click="$emit('delete')"
      >
        DELETE
      </span>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useUiStateStore } from '../../stores/uiState'

const uiState = useUiStateStore()

const elementInfo = computed(() => uiState.elementInfo)

const imageError = ref(false)

const formattedDate = computed(() => 
new Date(elementInfo.value?.created || '').toLocaleDateString()
)

function handleImageError() {
  imageError.value = true
}

defineEmits<{
  toggle: []
  delete: []
}>()
</script>
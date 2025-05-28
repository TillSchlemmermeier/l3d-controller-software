<template>
  <template v-if="loading">
    <div>Loading Generator...</div>
  </template>
  <template v-else>
    <div 
      @click="$emit('click')" 
      @dblclick="$emit('dblclick')"
      class="relative"
      :class="{ 'z-10 opacity-100': isSelected, 'z-0 opacity-90': !isSelected }"
    >
      <div 
        class="relative p-4 rounded-xl overflow-hidden backdrop-blur-sm shadow-lg transition-all duration-200"
        :class="[
          `shadow-${colors.text}/10`,
          { 'scale-120 ring-2': isSelected },
          { [colors.border]: isSelected }
        ]"
      >
        <!-- Gradient Background -->
        <div 
          class="absolute inset-0 opacity-90"
          :class="colors.gradient"
        ></div>
        
        <!-- Glass effect overlay -->
        <div class="absolute inset-0 bg-white opacity-10"></div>
        
        <!-- Content -->
        <div class="relative z-10">
          <!-- Generator Name Header -->
          <div 
            class="border-b pb-2 mb-3"
            :class="colors.border + '/50'"
          >
            <div 
              class="text-xl text-center font-extrabold tracking-wide capitalize drop-shadow-sm"
              :class="colors.text"
            >
              {{ thisGenerator.name.replace(/^g_/, '').replace(/_/g, ' ') }}
            </div>
          </div>
    
          <!-- Parameters Grid -->
          <div class="grid grid-cols-2">
            <template
              v-for="index in Array.from({ length: thisGenerator.params.length / 4 }, (_, i) => i)"
              :key="index"
            >
              <div 
                class="text-sm font-medium capitalize text-nowrap"
                :class="colors.text"
              >
                {{ thisGenerator.params[4 * index] }}
              </div>
              <div 
                class="text-right text-sm font-bold text-zinc-900"
              >
                {{ thisGenerator.params[4 * index + 2] }}
              </div>
            </template>
          </div>
        </div>
      </div>
    </div>
  </template>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { usePresentStateStore } from '../../stores/presentState'
import { getGeneratorColors } from '../../utils/colors'

const props = defineProps({
  channel: {
    type: Number,
    required: true,
  },
  isSelected: {
    type: Boolean,
    required: false,
    default: false,
  },
})

const presentState = usePresentStateStore()
const thisGenerator = ref()
const loading = ref(true)
const colors = getGeneratorColors()

onMounted(async () => {
  thisGenerator.value = presentState.channels[props.channel]?.generator
  if (thisGenerator.value) {
    loading.value = false
  }
})

watch(
  () => presentState.channels[props.channel].generator,
  (newVal) => {
    thisGenerator.value = newVal
  },
  { deep: true },
)
</script>

<style scoped>
</style>

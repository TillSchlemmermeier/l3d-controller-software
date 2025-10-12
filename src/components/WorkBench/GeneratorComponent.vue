<template>
  <template v-if="loading">
    <div>Loading Generator...</div>
  </template>
  <template v-else>
    <div 
      class="relative mt-2 group z-10"
    >
      <!-- Ring overlay (only for context generators) -->
      <div
        v-if="hasContext"
        class="absolute ring-3 ring-offset-3 ring-offset-zinc-700 inset-0 rounded-xl pointer-events-none animate-pulse"
        :class="getRingClasses"
      ></div>

      <div class="relative p-4 rounded-xl shadow-lg shadow-zinc-900 transition-all duration-200">
        <!-- Gradient Background -->
        <div 
          class="absolute inset-0 rounded-xl"
          :class="colors.gradient"
        ></div>

        <!-- Context number overlay -->
        <div 
          v-if="hasContext"
          class="absolute inset-0 flex items-center justify-center pointer-events-none select-none overflow-hidden"
        >
          <div 
            class="text-[120px] font-black leading-none opacity-15 mix-blend-multiply"
            :class="contextNumberClasses"
          >
            {{ props.context + 1 }}
          </div>
        </div>

        <!-- Glass effect overlay -->
        <div class="absolute inset-0 bg-white opacity-10 rounded-xl"></div>
        
        <div class="relative z-10">
          <!-- Generator Name Header -->
          <div 
            class="border-b pb-2 mb-3"
            :class="colors.border"
          >
            <div 
              class="text-xl text-center font-extrabold tracking-wide capitalize drop-shadow-sm"
              :class="getHeaderTextStyle()"
            >
              {{ thisGenerator.name.replace(/^g_/, '').replace(/_/g, ' ') }}
            </div>
          </div>
    
          <!-- Parameters Grid -->
          <div class="grid grid-cols-2">
            <template
              v-for="_, index in (thisGenerator.params.length / 4)"
              :key="index"
            >
              <div 
                class="text-sm font-medium capitalize text-nowrap"
                :class="colors.text"
              >
                {{ thisGenerator.params[4 * index] }}
              </div>
              <div class="flex items-center justify-end gap-2">
                <div 
                  class="text-right text-sm font-bold" 
                  :class="colors.text"
                >
                  {{ thisGenerator.params[4 * index + 2] }}
                </div>
                <!-- Circular Progress -->
                <div 
                  v-if="hasContext"
                  class="relative w-3 h-3 flex-shrink-0" 
                >
                  <svg 
                    class="w-full h-full -rotate-90 origin-center" 
                    viewBox="0 0 32 32"
                  >
                    <!-- Background circle -->
                    <circle
                      cx="16"
                      cy="16"
                      r="14"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="4"
                      stroke-opacity="0.2"
                    />
                    <!-- Progress circle -->
                    <circle
                      cx="16"
                      cy="16"
                      r="14"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="4"
                      :style="{
                        strokeDasharray: `${loadProgressCircles ? 0 : Number(thisGenerator.params[4 * index + 3]) * 88}, 88`,
                        strokeDashoffset: 0
                      }"
                      :class="[
                        'transition-[stroke-dasharray]',
                        initialFill ? 'duration-500' : 'duration-0',
                        'ease-out'
                      ]"
                    />
                  </svg>
                </div>
              </div>
            </template>
          </div>
        </div>
      </div>
    </div>
  </template>
</template>

<script setup lang="ts">
import { onMounted, ref, watch, nextTick, computed } from 'vue'
import { useCoreStateStore } from '../../stores/coreState'
import { getGeneratorColors, getContextColorSet } from '../../utils/colorSchemes'

const props = defineProps({
  channel: {
    type: Number,
    required: true,
  },
  context: {
    type: Number,
    required: false,
    default: 4
  }
})

const coreState = useCoreStateStore()
const thisGenerator = ref()
const loading = ref(true)
const colors = getGeneratorColors()
const loadProgressCircles = ref(true)
const initialFill = ref(true)

onMounted(async () => {
  thisGenerator.value = coreState.channels[props.channel]?.generator
  if (thisGenerator.value) {
    loading.value = false
  }
  if (props.context < 4) {
    loadProgressCircles.value = true
    nextTick(() => {
      loadProgressCircles.value = false
    })
  }
})

watch(
  () => coreState.channels[props.channel]?.generator,
  (newVal) => {
    thisGenerator.value = newVal
    if (newVal) {
      loading.value = false
    }
  },
  { deep: true }
)

watch(() => props.context, (newVal, oldVal) => {
  if (oldVal === 4 && newVal < 4) {
    loadProgressCircles.value = true
    initialFill.value = true
    nextTick(() => {
      loadProgressCircles.value = false
    })
    setTimeout(() => {
      initialFill.value = false
    }, 500)
  }
})

const hasContext = computed(() => {
  return props.context !== 4
})

const getRingClasses = computed(() => {
  if (props.context === 4) return ''
  
  const contextColorSet = getContextColorSet(props.context)
  return contextColorSet?.ring || ''
})

const getHeaderTextStyle = (): string => {
  if (props.context === 4) return colors.text
  
  const contextColorSet = getContextColorSet(props.context)
  return contextColorSet?.text || colors.text
}

const contextNumberClasses = computed(() => {
  const baseTextColor = colors.text
  return `${baseTextColor.replace('text-', 'text-')}/20`
})
</script>

<style scoped>
</style>
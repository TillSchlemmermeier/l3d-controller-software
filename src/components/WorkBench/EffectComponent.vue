<template>
  <template v-if="loading">
    <div>Loading Effect...</div>
  </template>
  <template v-else>
    <div 
      class="relative mt-2 group"
      :class="{ 
        'z-10 opacity-100': hasContext && thisEffect.IO,
        'z-0 opacity-90': !hasContext && thisEffect.IO,
        'z-0 opacity-50': !thisEffect.IO 
      }"
    >
      <!-- Ring overlay (only for context effects) -->
      <div
        v-if="hasContext"
        class="absolute ring-3 ring-offset-3 ring-offset-zinc-700 inset-0 rounded-xl pointer-events-none animate-pulse"
        :class="getRingClasses"
      ></div>

      <div
        class="relative p-3 rounded-xl shadow-md shadow-zinc-900 transition-all duration-200"
        :class="[
          { 'grayscale': !thisEffect.IO }
        ]"
      >
        <!-- Gradient Background -->
        <div 
          class="absolute inset-0 rounded-xl"
          :class="[
            getColors.gradient,
            { 'backdrop-blur-sm': !thisEffect.IO }
          ]"
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
        
        <div class="relative z-10">
          <!-- Effect Name Header -->
          <div class="border-b pb-1 mb-2"
                :class="[
                  getColors.border,
                  { 'border-opacity-50': !thisEffect.IO }
                ]">
            <div class="text-lg font-bold text-center tracking-wide capitalize"
              :class="[getHeaderTextStyle(), { 'blur-[0.7px]': !thisEffect.IO }]">
              {{ thisEffect.name.replace(/^e_/, '').replace(/_/g, ' ') }}
            </div>
          </div>
    
          <!-- Parameters Grid -->
          <div class="grid grid-cols-2">
            <template
              v-for="_, index in (thisEffect.params.length / 4)"
              :key="index"
            >
              <div class="text-sm font-medium text-nowrap capitalize" 
                   :class="[getColors.text, { 'blur-[0.7px]': !thisEffect.IO }]">
                {{ thisEffect.params[4 * index] }}
              </div>
              <div class="flex items-center justify-end gap-2">

                <div class="text-right text-sm font-semibold"
                  :class="[getColors.text, { 'blur-[0.7px]': !thisEffect.IO }]">
                  {{ thisEffect.params[4 * index + 2] }}
                </div>
  
                <div 
                  v-if="hasContext"
                  class="relative w-3 h-3" 
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
                        strokeDasharray: `${loadProgressCircles ? 0 : Number(thisEffect.params[4 * index + 3]) * 88}, 88`,
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
import { computed, ref, watch, nextTick } from 'vue'
import { useCoreStateStore } from '../../stores/coreState'
import { getColorsByName, getContextColorSet } from '../../utils/colorSchemes'

const props = defineProps({
  channel: {
    type: Number,
    required: true,
  },
  effectNumber: {
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
const loadProgressCircles = ref(false)
const initialFill = ref(true)

const thisEffect = computed(() => {
  if (props.channel === 9) {
    return coreState.globalEffects[props.effectNumber]
  }
  return coreState.channels[props.channel].effects[props.effectNumber]
})

const loading = computed(() => !thisEffect.value)

const getColors = computed(() => {
  return getColorsByName(thisEffect.value?.name || '')
})

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
  if (props.context === 4) return getColors.value.text

  const contextColorSet = getContextColorSet(props.context)
  return contextColorSet?.text || getColors.value.text
}

const contextNumberClasses = computed(() => {
  const baseTextColor = getColors.value.text
  return `${baseTextColor.replace('text-', 'text-')}/20`
})
</script>
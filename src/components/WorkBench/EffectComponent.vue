<template>
  <template v-if="loading">
    <div>Loading Effect...</div>
  </template>
  <template v-else>
    <div 
      class="relative mt-2 group"
      @click="$emit('click')"
      @dblclick="$emit('dblclick')"
      :class="{ 
        'z-10 opacity-100': isSelected && thisEffect.IO, 
        'z-0 opacity-90': !isSelected && thisEffect.IO,
        'z-0 opacity-50': !thisEffect.IO 
      }"
    >
      <div
        class="relative p-3 rounded-xl shadow-md shadow-zinc-900 transition-all duration-200 overflow-hidden"
        :class="[
          { 'shadow-lg scale-120 ring-2': isSelected },
          { 'grayscale': !thisEffect.IO },
          { 'border-3 border-red-500': context == 0 },
          { 'border-3 border-green-500': context == 1 },
          { 'border-3 border-orange-500': context == 2 },
          { 'border-3 border-blue-500': context == 3 }
        ]"
      >
        <!-- Gradient Background -->
        <div 
          class="absolute inset-0"
          :class="[
            getColors.gradient,
            { 'backdrop-blur-sm': !thisEffect.IO }
          ]"
        ></div>
        
        <div class="relative z-10">
          <!-- Effect Name Header -->
          <div class="border-b pb-1 mb-2"
                :class="[
                  getColors.border,
                  { 'border-opacity-50': !thisEffect.IO }
                ]">
            <div class="text-lg font-bold text-center tracking-wide capitalize"
              :class="[getColors.text, { 'blur-[0.7px]': !thisEffect.IO }]">
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
                  v-if="isSelected"
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
import { usePresentStateStore } from '../../stores/presentState'
import { getColorsByName } from '../../utils/colors'

const props = defineProps({
  channel: {
    type: Number,
    required: true,
  },
  effectNumber: {
    type: Number,
    required: true,
  },
  isSelected: {
    type: Boolean,
    required: false,
    default: false,
  },
  context: {
    type: Number,
    required: false,
    default: 4
  }
})

const presentState = usePresentStateStore()
const loadProgressCircles = ref(true)
const initialFill = ref(true)

const thisEffect = computed(() => {
  if (props.channel === 9) {
    console.log(presentState.globalEffects[props.effectNumber])
    return presentState.globalEffects[props.effectNumber]
  }
  return presentState.channels[props.channel].effects[props.effectNumber]
})

const loading = computed(() => !thisEffect.value)

const getColors = computed(() => {
  return getColorsByName(thisEffect.value?.name || '')
})

watch(() => props.isSelected, (newVal) => {
  if (newVal) {
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
</script>

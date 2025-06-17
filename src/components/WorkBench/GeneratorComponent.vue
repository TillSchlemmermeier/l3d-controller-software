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
        class="relative p-4 rounded-xl overflow-hidden backdrop-blur-sm shadow-lg shadow-zinc-900 transition-all duration-200"
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
                  class="text-right text-sm font-bold text-zinc-900" 
                >
                  {{ thisGenerator.params[4 * index + 2] }}
                </div>
                <!-- Circular Progress -->
                <div 
                  v-if="isSelected"
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
                        strokeDasharray: `${loadProgressCircles ? 0 : thisGenerator.params[4 * index + 3] * 88}, 88`,
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
import { onMounted, ref, watch, nextTick } from 'vue'
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
const loadProgressCircles = ref(true)
const initialFill = ref(true)

onMounted(async () => {
  thisGenerator.value = presentState.channels[props.channel]?.generator
  console.log(thisGenerator.value)
  if (thisGenerator.value) {
    console.log('Generator loaded:', thisGenerator.value)
    loading.value = false
  }
  if (props.isSelected) {
    loadProgressCircles.value = true
    nextTick(() => {
      loadProgressCircles.value = false
    })
  }
})

watch(
  () => presentState.channels[props.channel]?.generator,
  (newVal) => {
    thisGenerator.value = newVal
    if (newVal) {
      loading.value = false
    }
  },
  { deep: true }
)

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

<style scoped>
</style>
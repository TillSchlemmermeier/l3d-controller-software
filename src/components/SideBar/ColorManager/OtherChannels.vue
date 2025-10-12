<template>
  <div class="mt-8">
    <div class="text-xs text-zinc-400 uppercase font-bold tracking-wider mb-3">
      Copy From Other Channel
    </div>
      <div class="grid grid-cols-4 gap-2">
        <div
          v-for="(channel, index) in coreState.channels"
          :key="index"
          class="group cursor-pointer"
          @click="loadGradientFromChannel(index)"
        >
          <div 
            class="mb-2 w-20 h-16 rounded border border-zinc-500 flex items-center justify-center"
            :class="[{ 'ring-4 ring-blue-500 opacity-30': index === uiState.channelIndex }]"
            :style="{ background: generateChannelGradientCSS(channel.color) }"
          >
            <span class="text-4xl font-bold text-white drop-shadow-lg">
              {{ index + 1 }}
            </span>
          </div>
        </div>
      </div>
  </div>
</template>

<script setup lang="ts">
import { useCoreStateStore } from '../../../stores/coreState'
import { useUiStateStore } from '../../../stores/uiState'

interface Emits {
  (e: 'copiedFromChannel'): void
}
const emit = defineEmits<Emits>()

const coreState = useCoreStateStore()
const uiState = useUiStateStore()

function loadGradientFromChannel(channelIndex: number) {
  const sourceChannel = coreState.channels[channelIndex]

  if (!sourceChannel?.color) return

  coreState.channels[uiState.channelIndex].color = { ...sourceChannel.color }
  emit('copiedFromChannel')
}

function generateChannelGradientCSS(colorData: any): string {
  if (!colorData?.gradient) {
    return 'linear-gradient(to right, #666666, #666666)'
  }

  const stopStrings = colorData.gradient.map(([position, color]: [number, string]) => `${color} ${position}%`)

  return colorData.gradientType === 'radial'
    ? `radial-gradient(circle, ${stopStrings.join(', ')})`
    : `linear-gradient(to right, ${stopStrings.join(', ')})`
}
</script>
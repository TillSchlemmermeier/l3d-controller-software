<template>
  <div
    v-if="uiState.admin || !adminOnly"
    class="rounded-xl w-24 h-24 p-3 flex flex-col items-center justify-center select-none transition-all duration-150 cursor-pointer active:scale-95 active:opacity-80"
    :class="backgroundClass"
    @click.stop="handleClick"
    v-longpress="handleLongPress"
  >
    <span class="text-zinc-900 text-sm font-bold text-center leading-tight drop-shadow-sm">
      {{ label }}
    </span>
    <span v-if="subLabel" class="text-zinc-800 text-sm font-semibold text-center mt-0.5 drop-shadow-sm capitalize">
      {{ subLabel }}
    </span>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useUiStateStore } from '../../stores/uiState'
import { vLongpress } from '../../directives/longpress'

interface Props {
  label: string
  subLabel?: string
  active?: boolean | undefined
  adminOnly?: boolean
  onClick?: () => void
  onLongPress?: () => void
}

const props = withDefaults(defineProps<Props>(), {
  active: undefined,
  adminOnly: false
})

const uiState = useUiStateStore()

const backgroundClass = computed(() => {
  if (props.active === undefined) {
    return 'bg-gradient-to-br from-zinc-400 via-zinc-300 to-zinc-500'
  } else if (props.active === true) {
    return 'bg-gradient-to-br from-emerald-500 via-green-400 to-emerald-600'
  } else {
    return 'bg-gradient-to-br from-rose-400 via-red-400 to-rose-600'
  }
})

// a long press is followed by a click, which would run the short action too
const longPressed = ref(false)

const handleLongPress = () => {
  if (!props.onLongPress) return
  longPressed.value = true
  props.onLongPress()
}

const handleClick = () => {
  if (longPressed.value) {
    longPressed.value = false
    return
  }
  if (props.onClick) {
    props.onClick()
  }
}
</script>
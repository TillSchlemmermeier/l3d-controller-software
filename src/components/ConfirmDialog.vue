<template>
  <Transition name="dialog">
    <div
      v-if="state.open"
      class="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm select-none"
      @click.self="respond(state.isAlert)"
    >
      <div class="w-[90%] max-w-md rounded-2xl bg-zinc-800 border border-zinc-700 shadow-2xl p-6">
        <h2 v-if="state.options.title" class="text-lg font-semibold text-white mb-2">
          {{ state.options.title }}
        </h2>
        <p class="text-zinc-300 text-base leading-relaxed">
          {{ state.options.message }}
        </p>
        <div class="flex justify-end gap-3 mt-6">
          <button
            v-if="!state.isAlert"
            @click="respond(false)"
            class="px-6 py-3 rounded-xl text-base font-medium bg-zinc-700 text-zinc-200 active:scale-95 transition"
          >
            {{ state.options.cancelText || 'Cancel' }}
          </button>
          <button
            @click="respond(true)"
            class="px-6 py-3 rounded-xl text-base font-semibold text-white active:scale-95 transition"
            :class="state.options.danger ? 'bg-rose-600' : 'bg-amber-500'"
          >
            {{ state.options.confirmText || 'OK' }}
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script lang="ts">
import { reactive, defineComponent } from 'vue'

export interface ConfirmOptions {
  title?: string
  message: string
  confirmText?: string
  cancelText?: string
  danger?: boolean   // style the confirm button as destructive (rose)
}

// One dialog shared across the whole app
const state = reactive({
  open: false,
  isAlert: false,
  options: { message: '' } as ConfirmOptions,
})
let resolver: ((value: boolean) => void) | null = null

function show(options: ConfirmOptions, isAlert: boolean): Promise<boolean> {
  if (resolver) resolver(false)   // cancel any dialog already open
  state.options = options
  state.isAlert = isAlert
  state.open = true
  return new Promise((res) => { resolver = res })
}

function respond(value: boolean) {
  state.open = false
  const r = resolver
  resolver = null
  if (r) r(value)
}

export const dialog = {
  confirm: (options: ConfirmOptions) => show(options, false),
  alert: (options: ConfirmOptions) => show(options, true),
}

export default defineComponent({
  setup: () => ({ state, respond }),
})
</script>

<style scoped>
.dialog-enter-active,
.dialog-leave-active {
  transition: opacity 0.15s ease;
}
.dialog-enter-from,
.dialog-leave-to {
  opacity: 0;
}
</style>

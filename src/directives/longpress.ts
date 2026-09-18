// Long-press as a touch-friendly alternative to double-tap.
// Fires after 750ms of holding still; movement > 10px cancels it so drag/scroll win.
export const vLongpress = {
  mounted(el: HTMLElement, binding: { value: (e: PointerEvent) => void }) {
    const ac = new AbortController(), o = { signal: ac.signal }
    let timer: ReturnType<typeof setTimeout>, x = 0, y = 0
    const cancel = () => clearTimeout(timer)
    el.addEventListener('pointerdown', (e: PointerEvent) => {
      x = e.clientX; y = e.clientY
      timer = setTimeout(() => binding.value(e), 750)
    }, o)
    el.addEventListener('pointermove', (e: PointerEvent) => {
      if (Math.hypot(e.clientX - x, e.clientY - y) > 10) cancel()
    }, o)
    el.addEventListener('pointerup', cancel, o)
    el.addEventListener('pointercancel', cancel, o)
    ;(el as any)._lp = ac
  },
  unmounted: (el: any) => el._lp?.abort(),
}

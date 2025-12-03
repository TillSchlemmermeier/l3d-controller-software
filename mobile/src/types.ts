export interface Effect {
  name: string
  IO: number
  update: boolean
  params: Array<string | number | boolean>
}

export interface Generator {
  name: string
  update: boolean
  params: Array<string | number | boolean>
}

export interface Color {
  gradient: Array<[number, string]>,
  gradientType: 'linear' | 'radial',
  sectionWidth: number,
  sectionStart: number,
  speed: number,
  rotateSpeedY: number,
  rotateSpeedZ: number,
  soundToLightOptions: string[],
  update: boolean
}

export interface Channel {
  IO: number
  brightness: number
  fade: number
  numberOfEffects: number
  generator: Generator
  effects: Effect[]
  color?: Color
}

export interface coreState {
  IO: boolean
  brightness: number
  fade: number
  autopilot: boolean
  autopilot_time: number
  random: string
  s2l_values: number[]
  s2l_thresholds: number[]
  s2l_normalize: boolean
  s2l_gain: number
  s2l_update: boolean
  context: number[][]
  oneshot: number
  crossfade_active: boolean
  numberOfChannels: number
  channels: Channel[]
  globalEffects: Effect[]
}
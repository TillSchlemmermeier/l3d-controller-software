export interface SelectedRegion {
  start: number // 0-100
  end: number // 0-100
}

export interface GradientPreset {
  id: number
  type: string
  subtype?: string
  data: Array<[number, string]>
  request_count: number
  created_at: string
}

export type SortOption = 'first' | 'last' | 'none' | 'subtype' | 'mean' | 'random' | 'date' | 'usage'

export type AutopilotMode = 'global' | 'all_channels' | 'all_elements' | 'random_channel' | 'random_channel_elements' | 'random_element' | 'selected_channel' | 'selected_channel_elements' | 'selected_element' | 'colors'

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
  globalColor?: Color
}

export interface ElementInfo {
  name: string
  type: string
  created: string
  usageCount: number
  isActive: boolean
}

export interface Preset {
  name: string
  created_at: string
  request_count: number
}

export interface PresetData {
  name: string
  update: number
  params: number[]
  IO?: number  // Optional, only present for effects
}

export interface PresetInfo {
  name: string
  elementName: string
  data: PresetData
  usageCount: number
  created: string
}

export interface AdminElements {
  name: string
  active: boolean
}
export interface AdminPresets {
  type: string
  name: string
}
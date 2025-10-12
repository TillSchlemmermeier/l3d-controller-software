interface GradientSet {
  from: string
  to: string
  text: string
  border: string
  bg?: string
}

interface ComponentColors {
  gradient: string
  text: string
  border: string
  bg: string
}

export interface ContextColorSet {
  bg: string
  text: string
  bgInactive: string
  textInactive: string
  border: string
  ring: string
}

export const gradientSets: GradientSet[] = [
  // Generator colors
  {
    from: 'from-amber-500',
    to: 'to-orange-300',
    text: 'text-amber-900',
    border: 'border-amber-200',
    bg: 'bg-amber-50'
  },
  // Effect colors
  // Blues & Cyans
  { from: 'from-blue-500', to: 'to-cyan-300', text: 'text-blue-900', border: 'border-blue-300' },
  { from: 'from-sky-500', to: 'to-blue-300', text: 'text-sky-900', border: 'border-sky-300' },
  { from: 'from-cyan-500', to: 'to-sky-300', text: 'text-cyan-900', border: 'border-cyan-300' },
  
  // Purples & Pinks
  { from: 'from-purple-500', to: 'to-pink-300', text: 'text-purple-900', border: 'border-purple-300' },
  { from: 'from-fuchsia-500', to: 'to-purple-300', text: 'text-fuchsia-900', border: 'border-fuchsia-300' },
  { from: 'from-violet-500', to: 'to-purple-300', text: 'text-violet-900', border: 'border-violet-300' },
  
  // Reds & Oranges
  { from: 'from-rose-500', to: 'to-orange-300', text: 'text-rose-900', border: 'border-rose-300' },
  { from: 'from-red-500', to: 'to-rose-300', text: 'text-red-900', border: 'border-red-300' },
  { from: 'from-orange-500', to: 'to-amber-300', text: 'text-orange-900', border: 'border-orange-300' },
  
  // Yellows & Ambers
  { from: 'from-amber-500', to: 'to-yellow-300', text: 'text-amber-900', border: 'border-amber-300' },
  { from: 'from-yellow-500', to: 'to-lime-300', text: 'text-yellow-900', border: 'border-yellow-300' },
  
  // Greens
  { from: 'from-teal-500', to: 'to-emerald-300', text: 'text-teal-900', border: 'border-teal-300' },
  { from: 'from-emerald-500', to: 'to-green-300', text: 'text-emerald-900', border: 'border-emerald-300' },
  { from: 'from-green-500', to: 'to-lime-300', text: 'text-green-900', border: 'border-green-300' },
  
  // Cool Mixed Tones
  { from: 'from-indigo-500', to: 'to-blue-300', text: 'text-indigo-900', border: 'border-indigo-300' },
  { from: 'from-violet-500', to: 'to-indigo-300', text: 'text-violet-900', border: 'border-violet-300' },
  { from: 'from-purple-500', to: 'to-indigo-300', text: 'text-purple-900', border: 'border-purple-300' },
  
  // Warm Mixed Tones
  { from: 'from-rose-500', to: 'to-pink-300', text: 'text-rose-900', border: 'border-rose-300' },
  { from: 'from-orange-500', to: 'to-rose-300', text: 'text-orange-900', border: 'border-orange-300' },
  { from: 'from-amber-500', to: 'to-orange-300', text: 'text-amber-900', border: 'border-amber-300' },
  
  // Earth Tones
  { from: 'from-amber-600', to: 'to-yellow-400', text: 'text-amber-900', border: 'border-amber-400' },
  { from: 'from-lime-600', to: 'to-emerald-400', text: 'text-lime-900', border: 'border-lime-400' },
  { from: 'from-teal-600', to: 'to-cyan-400', text: 'text-teal-900', border: 'border-teal-400' },

  // Soft Pastels
  { from: 'from-pink-400', to: 'to-rose-200', text: 'text-pink-800', border: 'border-pink-300' },
  { from: 'from-sky-400', to: 'to-indigo-200', text: 'text-sky-800', border: 'border-sky-300' },

  // Nature Inspired
  { from: 'from-amber-500', to: 'to-orange-200', text: 'text-amber-800', border: 'border-amber-300' },

  // Ocean Tones
  { from: 'from-cyan-500', to: 'to-blue-200', text: 'text-cyan-800', border: 'border-cyan-300' },
  { from: 'from-blue-400', to: 'to-slate-200', text: 'text-blue-800', border: 'border-blue-300' },
  { from: 'from-teal-400', to: 'to-sky-200', text: 'text-teal-800', border: 'border-teal-300' },

  // Vibrant Combinations
  { from: 'from-violet-500', to: 'to-rose-300', text: 'text-violet-800', border: 'border-violet-300' },
  { from: 'from-cyan-600', to: 'to-teal-400', text: 'text-cyan-900', border: 'border-cyan-400' }
]

export function getColorsByName(name: string): ComponentColors {
  if (!name) return {
    gradient: 'bg-gradient-to-br from-gray-500 to-gray-300',
    text: 'text-gray-900',
    border: 'border-gray-300',
    bg: 'bg-white'
  }

  // Generate hash from name
  let hash = 0
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash)
  }

  const index = Math.abs(hash) % gradientSets.length
  const gradient = gradientSets[index]
  
  return {
    gradient: `bg-gradient-to-br ${gradient.from} ${gradient.to}`,
    text: gradient.text,
    border: gradient.border,
    bg: gradient.bg || 'bg-white'
  }
}

export function getGeneratorColors(): ComponentColors {
  return {
    gradient: 'bg-gradient-to-br from-slate-500 to-zinc-200 grayscale',
    text: 'text-slate-900',
    border: 'border-slate-200',
    bg: 'bg-slate-50'
  }
}

export function getEffectColors(): ComponentColors {
  return {
    gradient: 'bg-gradient-to-br from-slate-400 to-blue-200',
    text: 'text-slate-900',
    border: 'border-slate-300',
    bg: 'bg-slate-50'
  }
}

export const contextColors: Record<number, ContextColorSet> = {
  0: { // White context
    bg: 'bg-white',
    text: 'text-zinc-950 font-extrabold',
    bgInactive: 'bg-white/80',
    textInactive: 'text-zinc-900',
    border: 'border-white',
    ring: 'ring-white'
  },
  1: { // Cyan context
    bg: 'bg-cyan-400',
    text: 'text-zinc-950 font-extrabold',
    bgInactive: 'bg-cyan-600',
    textInactive: 'text-zinc-900',
    border: 'border-zinc-300',
    ring: 'ring-cyan-400'
  },
  2: { // Yellow context
    bg: 'bg-yellow-400',
    text: 'text-zinc-950 font-extrabold',
    bgInactive: 'bg-yellow-600',
    textInactive: 'text-white',
    border: 'border-zinc-500',
    ring: 'ring-yellow-400'
  },
  3: { // Pink context
    bg: 'bg-pink-400',
    text: 'text-zinc-950 font-extrabold',
    bgInactive: 'bg-pink-600',
    textInactive: 'text-white',
    border: 'border-zinc-900',
    ring: 'ring-pink-400'
  },
}

export function getContextColors(contextIndex: number): { bg: string, text: string } {
  const context = contextColors[contextIndex]
  if (!context) return { bg: '', text: '' }

  return {
    bg: context.bg,
    text: context.text
  }
}

export function getContextColorSet(contextIndex: number): ContextColorSet | null {
  return contextColors[contextIndex] || null
}

export function getAllContextColors(): ContextColorSet[] {
  return Object.values(contextColors)
}

export function hsvToRgb(h: number, s: number, v: number) {
  let r: number, g: number, b: number
  
  const i = Math.floor(h * 6)
  const f = h * 6 - i
  const p = v * (1 - s)
  const q = v * (1 - f * s)
  const t = v * (1 - (1 - f) * s)
  
  switch (i % 6) {
    case 0: r = v; g = t; b = p; break
    case 1: r = q; g = v; b = p; break
    case 2: r = p; g = v; b = t; break
    case 3: r = p; g = q; b = v; break
    case 4: r = t; g = p; b = v; break
    case 5: r = v; g = p; b = q; break
    default: r = 0; g = 0; b = 0
  }
  
  return {
    r: Math.round(r * 255),
    g: Math.round(g * 255),
    b: Math.round(b * 255)
  }
}

export function colorStringToHSV(colorString: string): { h: number, s: number, v: number } {
  const hex = colorString.replace('#', '')
  
  const r = parseInt(hex.substr(0, 2), 16) / 255
  const g = parseInt(hex.substr(2, 2), 16) / 255
  const b = parseInt(hex.substr(4, 2), 16) / 255
  
  const max = Math.max(r, g, b)
  const min = Math.min(r, g, b)
  const diff = max - min
  
  let h = 0
  const s = max === 0 ? 0 : diff / max
  const v = max
  
  if (diff !== 0) {
    if (max === r) h = ((g - b) / diff) % 6
    else if (max === g) h = (b - r) / diff + 2
    else h = (r - g) / diff + 4
  }
  
  h = Math.round(h * 60)
  if (h < 0) h += 360
  
  return {
    h: h,
    s: Math.round(s * 100),
    v: Math.round(v * 100)
  }
}

export function hsvToColorString(h: number, s: number, v: number): string {
  const rgb = hsvToRgb(h / 360, s / 100, v / 100)
  return (
    '#' +
    rgb.r.toString(16).padStart(2, '0') +
    rgb.g.toString(16).padStart(2, '0') +
    rgb.b.toString(16).padStart(2, '0')
  ).toUpperCase()
}

export function hexToRgb(hex: string): { r: number; g: number; b: number } | null {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : null
}

export function hexToHue(hex: string): number {
  const rgb = hexToRgb(hex)
  if (!rgb) return 0
  return rgbToHue(rgb.r, rgb.g, rgb.b)
}

export function rgbToHue(r: number, g: number, b: number): number {
  r /= 255; g /= 255; b /= 255
  const max = Math.max(r, g, b)
  const min = Math.min(r, g, b)
  let h = 0
  
  if (max !== min) {
    if (max === r) h = (g - b) / (max - min)
    else if (max === g) h = 2 + (b - r) / (max - min)
    else h = 4 + (r - g) / (max - min)
    h *= 60
    if (h < 0) h += 360
  }
  
  return h
}

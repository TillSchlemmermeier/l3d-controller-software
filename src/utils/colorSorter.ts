import type { GradientPreset, SortOption } from '../types/types'
import { hexToRgb, hexToHue, rgbToHue } from './colorConversion'

export class ColorSorter {
  static sortAndGroup(gradients: GradientPreset[], sortBy: SortOption) {
    if (sortBy === 'subtype') {
      return this.groupBySubtype(gradients)
    } else if (sortBy === 'random') {
      return [{ subtype: '', gradients: this.shuffleArray(gradients) }]
    } else if (sortBy === 'date' || sortBy === 'usage') {
      const sortedGradients = this.sortByField(gradients, sortBy)
      return [{ subtype: '', gradients: sortedGradients }]
    }
    
    const sortedGradients = sortBy === 'none' 
      ? gradients 
      : this.sortByColor(gradients, sortBy)
    
    return [{ subtype: '', gradients: sortedGradients }]
  }

  private static groupBySubtype(gradients: GradientPreset[]) {
    const groups: Record<string, GradientPreset[]> = {}
    
    gradients.forEach(g => {
      const key = g.subtype || 'No Subtype'
      if (!groups[key]) groups[key] = []
      groups[key].push(g)
    })
    
    return Object.entries(groups)
      .map(([subtype, grads]) => ({
        subtype,
        gradients: this.sortByColor(grads, 'first')
      }))
      .sort((a, b) => a.subtype.localeCompare(b.subtype))
  }

  private static sortByColor(gradients: GradientPreset[], sortBy: SortOption) {
    return [...gradients].sort((a, b) => {
      const hueA = this.getHueForSorting(a.data, sortBy)
      const hueB = this.getHueForSorting(b.data, sortBy)
      if (hueA === null || hueB === null) return 0
      return hueA - hueB
    })
  }

  private static sortByField(gradients: GradientPreset[], sortBy: 'date' | 'usage') {
    return [...gradients].sort((a, b) => {
      if (sortBy === 'date') {
        // Assuming created_at is a string in 'YYYY-MM-DD HH:MM:SS' format
        return new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
      } else if (sortBy === 'usage') {
        // Sort by request_count descending (most used first)
        return b.request_count - a.request_count
      }
      return 0
    })
  }

  private static shuffleArray(gradients: GradientPreset[]) {
    const shuffled = [...gradients]
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1))
      ;[shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
    }
    return shuffled
  }

  private static getHueForSorting(gradientData: Array<[number, string]>, sortBy: SortOption): number | null {
    switch (sortBy) {
      case 'first':
        return this.getColorHue(gradientData, 'first')
      case 'last':
        return this.getColorHue(gradientData, 'last')
      case 'mean':
        return this.getMeanColorHue(gradientData)
      default:
        return null
    }
  }

  private static getColorHue(gradientData: Array<[number, string]>, type: 'first' | 'last'): number | null {
    const stops = gradientData.map(([position, color]) => ({ position, color }))
    if (stops.length === 0) return null
    
    stops.sort((a, b) => a.position - b.position)
    const color = type === 'first' ? stops[0].color : stops[stops.length - 1].color
    return hexToHue(color)
  }

  private static getMeanColorHue(gradientData: Array<[number, string]>): number | null {
    const stops = gradientData.map(([position, color]) => ({ position, color }))
    
    let totalR = 0, totalG = 0, totalB = 0
    stops.forEach(stop => {
      const rgb = hexToRgb(stop.color)
      if (rgb) {
        totalR += rgb.r
        totalG += rgb.g
        totalB += rgb.b
      }
    })
    
    const avgR = totalR / stops.length
    const avgG = totalG / stops.length
    const avgB = totalB / stops.length
    
    return rgbToHue(avgR, avgG, avgB)
  }
}
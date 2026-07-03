export * from './types'
export { workbenchMode } from './workbenchMode'
export { dashboardMode } from './dashboardMode'

import { LaunchpadMode } from './types'
import { workbenchMode } from './workbenchMode'
import { dashboardMode } from './dashboardMode'

export const launchpadModes: Record<string, LaunchpadMode> = {
  dashboard: dashboardMode,
  workbench: workbenchMode,
}

from db_manager import DatabaseManager
import json
from typing import List, Dict, Optional, Any
from enum import Enum

class UpdateType(Enum):
    CATEGORY_ADDED = "category_added"
    CATEGORY_REMOVED = "category_removed"
    CATEGORY_RENAMED = "category_renamed"
    RANGE_EXTENDED = "range_extended"
    RANGE_SHRINKED = "range_shrinked"
    PARAM_ADDED = "param_added"
    PARAM_REMOVED = "param_removed"
    PARAM_RENAMED = "param_renamed"

class PresetUpdater:
    def __init__(self):
        self.db = DatabaseManager()

    def get_all_presets_for_element(self, element_name: str, element_type: str) -> List[Dict]:
        """Get all presets (direct, channel, and global) containing a specific element"""
        all_presets = []
        
        # Get direct element presets
        direct_presets = self.db.get_preset_names(element_type, element_name)
        for preset_dict in direct_presets:
            preset_name = preset_dict['name']
            data = self.db.get_preset(element_type, element_name, preset_name, False)
            all_presets.append({
                'type': element_type,
                'category': element_name,
                'name': preset_name,
                'preset': preset_name,  # Add for compatibility
                'element': element_name,  # Add for compatibility
                'data': data,
                'path': []  # Direct presets have empty path
            })

        # Get channel presets containing this element
        channel_presets = self.db.get_preset_names('channel', 'presets')
        for preset_dict in channel_presets:
            preset_name = preset_dict['name']
            data = self.db.get_preset('channel', 'presets', preset_name, False)

            # Check if this element is in the channel and find its path
            if element_type == 'generator' and data.get(9, {}).get('name') == element_name:
                all_presets.append({
                    'type': 'channel',
                    'category': 'presets',
                    'name': preset_name,
                    'preset': preset_name,
                    'element': element_name,
                    'data': data,
                    'path': [9]  # Generator is at index 9
                })
            elif element_type == 'effect':
                for i in range(data.get('numberOfEffects', 0)):
                    if data.get(i, {}).get('name') == element_name:
                        all_presets.append({
                            'type': 'channel',
                            'category': 'presets',
                            'name': preset_name,
                            'preset': preset_name,
                            'element': element_name,
                            'data': data,
                            'path': [i]  # Effect is at index i
                        })
                        break  # Only add once per channel preset

        # Get global presets containing this element
        global_presets = self.db.get_preset_names('global', 'presets')
        for preset_dict in global_presets:
            preset_name = preset_dict['name']
            data = self.db.get_preset('global', 'presets', preset_name, False)

            # Track all instances found (can be multiple per global preset)
            instances_found = []
            
            # Check all channels in the global preset
            for channel_idx in range(data.get('numberOfChannels', 0)):
                channel = data.get(channel_idx, {})
                if element_type == 'generator' and channel.get(9, {}).get('name') == element_name:
                    instances_found.append([channel_idx, 9])
                elif element_type == 'effect':
                    for effect_idx in range(channel.get('numberOfEffects', 0)):
                        if channel.get(effect_idx, {}).get('name') == element_name:
                            instances_found.append([channel_idx, effect_idx])

            # Also check global effects (channel 9)
            if element_type == 'effect' and 9 in data:
                for effect_idx in range(data[9].get('numberOfEffects', 0)):
                    if data[9].get(effect_idx, {}).get('name') == element_name:
                        instances_found.append([9, effect_idx])

            # Add a preset entry for each instance found
            # Note: This means one global preset may be updated multiple times
            # if it contains the same element in multiple places
            for path in instances_found:
                all_presets.append({
                    'type': 'global',
                    'category': 'presets',
                    'name': preset_name,
                    'preset': preset_name,
                    'element': element_name,
                    'data': data,
                    'path': path  # Path to element within global preset
                })

        return all_presets

    def get_params_from_preset(self, preset: Dict) -> List:
        """Extract params array from preset based on its type and path"""
        data = preset['data']
        path = preset['path']

        if preset['type'] in ['generator', 'effect']:
            # Direct preset
            return data.get('params', [])

        # Navigate to the element using path
        current = data
        for key in path:
            current = current[key]

        return current.get('params', [])

    def set_params_in_preset(self, preset: Dict, new_params: List):
        """Set params array in preset based on its type and path"""
        data = preset['data']
        path = preset['path']
        
        if preset['type'] in ['generator', 'effect']:
            # Direct preset
            data['params'] = new_params
            return

        # Navigate to the element using path
        current = data
        for key in path[:-1]:
            current = current[key]

        # Set params on the final element
        current[path[-1]]['params'] = new_params

    def update_category_added(self, params: List, param_index: int,
                             old_categories: List[str], new_categories: List[str]) -> List:
        """Handle case where a category is added to a parameter"""
        # Find the parameter at param_index
        param_start = param_index * 4
        if param_start + 3 >= len(params):
            return params

        old_midi_value = params[param_start + 3]

        # Calculate new MIDI value to maintain same category
        old_category_count = len(old_categories)
        new_category_count = len(new_categories)

        # Convert old MIDI to category index
        old_category_index = int(old_midi_value * old_category_count)
        old_category_index = min(old_category_index, old_category_count - 1)

        # Find the old category in new categories list
        old_category = old_categories[old_category_index]
        try:
            new_category_index = new_categories.index(old_category)
            # Convert back to MIDI value
            new_midi_value = (new_category_index + 0.5) / new_category_count
            params[param_start + 3] = new_midi_value
        except ValueError:
            # Category no longer exists, keep closest
            pass

        return params

    def update_category_removed(self, params: List, param_index: int,
                               old_categories: List[str], new_categories: List[str],
                               fallback_category: Optional[str] = None) -> Optional[List]:
        """Handle case where a category is removed. Returns None if preset should be deleted"""
        param_start = param_index * 4
        if param_start + 3 >= len(params):
            return params

        old_midi_value = params[param_start + 3]

        # Calculate which category was selected
        old_category_count = len(old_categories)
        old_category_index = int(old_midi_value * old_category_count)
        old_category_index = min(old_category_index, old_category_count - 1)
        old_category = old_categories[old_category_index]

        # Check if the selected category still exists
        if old_category not in new_categories:
            if fallback_category is None:
                # Delete this preset
                return None
            else:
                # Use fallback category
                try:
                    new_category_index = new_categories.index(fallback_category)
                    new_category_count = len(new_categories)
                    new_midi_value = (new_category_index + 0.5) / new_category_count
                    params[param_start + 3] = new_midi_value
                except ValueError:
                    return None
        else:
            # Recalculate MIDI value for existing category
            new_category_index = new_categories.index(old_category)
            new_category_count = len(new_categories)
            new_midi_value = (new_category_index + 0.5) / new_category_count
            params[param_start + 3] = new_midi_value

        return params

    def update_category_renamed(self, params: List, param_index: int,
                               old_categories: List[str], new_categories: List[str]) -> List:
        """Handle case where categories are renamed"""
        # Categories are renamed but order stays the same, just update if needed
        # The MIDI values should map to the same position
        return params

    def update_range_extended(self, params: List, param_index: int,
                             old_min: float, old_max: float,
                             new_min: float, new_max: float,
                             keep_absolute: bool = True) -> List:
        """Handle case where numeric range is extended"""
        param_start = param_index * 4
        if param_start + 3 >= len(params):
            return params

        midi_value = params[param_start + 3]

        if keep_absolute:
            # Keep the absolute value the same
            # midi_value maps to old_min + (old_max - old_min) * midi_value
            # We need new_midi that maps to the same absolute value
            old_value = old_min + (old_max - old_min) * midi_value
            new_midi_value = (old_value - new_min) / (new_max - new_min)
            new_midi_value = max(0.0, min(1.0, new_midi_value))
            params[param_start + 3] = new_midi_value
        # else: keep the same MIDI value (proportional)

        return params

    def update_range_shrinked(self, params: List, param_index: int,
                             old_min: float, old_max: float,
                             new_min: float, new_max: float,
                             keep_absolute: bool = True) -> Optional[List]:
        """Handle case where numeric range is shrinked. Returns None if preset should be deleted"""
        param_start = param_index * 4
        if param_start + 3 >= len(params):
            return params

        midi_value = params[param_start + 3]
        old_value = old_min + (old_max - old_min) * midi_value

        # Check if old value is outside new range
        if old_value < new_min or old_value > new_max:
            if keep_absolute:
                # Clamp to new range
                clamped_value = max(new_min, min(new_max, old_value))
                new_midi_value = (clamped_value - new_min) / (new_max - new_min)
                params[param_start + 3] = new_midi_value
            # else: keep the same MIDI value (proportional)
        elif keep_absolute:
            # Recalculate MIDI value for new range
            new_midi_value = (old_value - new_min) / (new_max - new_min)
            params[param_start + 3] = new_midi_value

        return params

    def update_param_added(self, params: List, param_index: int,
                        param_name: str, param_label: str,
                        default_midi: float = 0.0) -> List:
        """Handle case where a parameter is added"""
        # Insert new parameter at the specified index
        insert_pos = param_index * 4
        new_param = [param_name, param_label, param_index, default_midi]

        # Update indices of following parameters
        for i in range(insert_pos, len(params), 4):
            if i + 2 < len(params):
                # Ensure the index is an integer before incrementing
                current_index = params[i + 2]
                if isinstance(current_index, str):
                    try:
                        params[i + 2] = int(current_index) + 1
                    except (ValueError, TypeError):
                        # If conversion fails, keep it as is or set to calculated index
                        params[i + 2] = (i // 4) + 1
                else:
                    params[i + 2] = int(current_index) + 1

        # Insert new parameter
        params[insert_pos:insert_pos] = new_param

        return params

    def update_param_removed(self, params: List, param_index: int,
                        delete_preset: bool = False) -> Optional[List]:
        """Handle case where a parameter is removed. Returns None if preset should be deleted"""
        if delete_preset:
            return None

        # Remove parameter at the specified index
        remove_pos = param_index * 4
        if remove_pos + 4 <= len(params):
            del params[remove_pos:remove_pos + 4]

        # Update indices of following parameters
        for i in range(remove_pos, len(params), 4):
            if i + 2 < len(params):
                # Ensure the index is an integer before decrementing
                current_index = params[i + 2]
                if isinstance(current_index, str):
                    try:
                        params[i + 2] = int(current_index) - 1
                    except (ValueError, TypeError):
                        # If conversion fails, set to calculated index
                        params[i + 2] = i // 4
                else:
                    params[i + 2] = int(current_index) - 1

        return params

    def update_param_renamed(self, params: List, param_index: int,
                           new_name: str, new_label: str) -> List:
        """Handle case where a parameter is renamed"""
        param_start = param_index * 4
        if param_start + 1 < len(params):
            params[param_start] = new_name
            params[param_start + 1] = new_label

        return params

    def apply_update(self, preset: Dict, update_type: UpdateType, **kwargs) -> Optional[Dict]:
        """Apply an update to a preset. Returns None if preset should be deleted"""
        params = self.get_params_from_preset(preset)

        if update_type == UpdateType.CATEGORY_ADDED:
            new_params = self.update_category_added(
                params, kwargs['param_index'],
                kwargs['old_categories'], kwargs['new_categories']
            )
        elif update_type == UpdateType.CATEGORY_REMOVED:
            new_params = self.update_category_removed(
                params, kwargs['param_index'],
                kwargs['old_categories'], kwargs['new_categories'],
                kwargs.get('fallback_category')
            )
        elif update_type == UpdateType.CATEGORY_RENAMED:
            new_params = self.update_category_renamed(
                params, kwargs['param_index'],
                kwargs['old_categories'], kwargs['new_categories']
            )
        elif update_type == UpdateType.RANGE_EXTENDED:
            new_params = self.update_range_extended(
                params, kwargs['param_index'],
                kwargs['old_min'], kwargs['old_max'],
                kwargs['new_min'], kwargs['new_max'],
                kwargs.get('keep_absolute', True)
            )
        elif update_type == UpdateType.RANGE_SHRINKED:
            new_params = self.update_range_shrinked(
                params, kwargs['param_index'],
                kwargs['old_min'], kwargs['old_max'],
                kwargs['new_min'], kwargs['new_max'],
                kwargs.get('keep_absolute', True)
            )
        elif update_type == UpdateType.PARAM_ADDED:
            new_params = self.update_param_added(
                params, kwargs['param_index'],
                kwargs['param_name'], kwargs['param_label'],
                kwargs.get('default_midi', 0.0)
            )
        elif update_type == UpdateType.PARAM_REMOVED:
            new_params = self.update_param_removed(
                params, kwargs['param_index'],
                kwargs.get('delete_preset', False)
            )
        elif update_type == UpdateType.PARAM_RENAMED:
            new_params = self.update_param_renamed(
                params, kwargs['param_index'],
                kwargs['new_name'], kwargs['new_label']
            )
        else:
            return preset
        
        if new_params is None:
            return None
        
        self.set_params_in_preset(preset, new_params)
        return preset

    def save_preset(self, preset: Dict):
        """Save updated preset back to database"""
        preset_type = preset['type']
        category = preset['category']
        preset_name = preset['name']
        data = preset['data']

        # Use the appropriate save method based on type
        if preset_type in ['generator', 'effect']:
            self.db.save_preset(preset_type, category, preset_name, data)
        elif preset_type == 'channel':
            self.db.save_preset('channel', 'presets', preset_name, data)
        elif preset_type == 'global':
            self.db.save_preset('global', 'presets', preset_name, data)

    def delete_preset(self, preset: Dict):
        """Delete a preset from the database"""
        preset_type = preset['type']
        category = preset['category']
        preset_name = preset['name']

        with self.db.get_db_connection() as conn:
            cursor = conn.cursor()

            # Get element_id based on type and category
            if preset_type in ['generator', 'effect']:
                cursor.execute('''
                    SELECT id FROM elements WHERE name = ? AND type = ?
                ''', (category, preset_type))
            elif preset_type == 'channel':
                cursor.execute('''
                    SELECT id FROM elements WHERE name = ? AND type = ?
                ''', ('presets', 'channel'))
            elif preset_type == 'global':
                cursor.execute('''
                    SELECT id FROM elements WHERE name = ? AND type = ?
                ''', ('presets', 'global'))

            result = cursor.fetchone()
            if not result:
                return

            element_id = result[0]

            cursor.execute('''
                DELETE FROM presets
                WHERE name = ? AND element_id = ?
            ''', (preset_name, element_id))
            conn.commit()

    def update_all_presets(self, element_name: str, element_type: str,
                          update_type: UpdateType, **kwargs) -> Dict[str, Any]:
        """Update all presets for an element. Returns summary of changes"""
        presets = self.get_all_presets_for_element(element_name, element_type)

        summary = {
            'total': len(presets),
            'updated': 0,
            'deleted': 0,
            'errors': []
        }

        for preset in presets:
            try:
                updated_preset = self.apply_update(preset, update_type, **kwargs)

                if updated_preset is None:
                    self.delete_preset(preset)
                    summary['deleted'] += 1
                else:
                    self.save_preset(updated_preset)
                    summary['updated'] += 1
            except Exception as e:
                summary['errors'].append({
                    'preset': preset['preset'],
                    'error': str(e)
                })

        return summary
rom db_manager import DatabaseManager
import json
from typing import Callable, List, Dict

class PresetUpdater:
    def __init__(self):
        self.db = DatabaseManager()

    def get_all_presets_for_element(self, element_name: str, element_type: str) -> List[Dict]:
        """Get all presets that contain this element from all preset types"""
        presets = []
        
        # Get direct presets
        element_presets = self.db.get_preset_names(element_type, element_name)
        for preset in element_presets:
            data = self.db.get_preset(element_type, element_name, preset, False)
            presets.append({
                'type': element_type,
                'element': element_name,
                'preset': preset,
                'data': data
            })

        # Get channel presets containing this element
        channel_presets = self.db.get_preset_names('channel', 'presets')
        for preset in channel_presets:
            data = self.db.get_preset('channel', 'presets', preset, False)
            if element_type == 'generator' and data[9]['name'] == element_name:
                presets.append({
                    'type': 'channel',
                    'element': 'presets',
                    'preset': preset,
                    'data': data
                })
            elif element_type == 'effect':
                for i in range(data['numberOfEffects']):
                    if data[i]['name'] == element_name:
                        presets.append({
                            'type': 'channel',
                            'element': 'presets',
                            'preset': preset,
                            'data': data
                        })

        # Get global presets containing this element
        global_presets = self.db.get_preset_names('global', 'presets')
        for preset in global_presets:
            data = self.db.get_preset('global', 'presets', preset, False)
            # Check regular channels
            for i in range(data['numberOfChannels']):
                if i in data:
                    channel = data[i]
                    if element_type == 'generator' and channel[9]['name'] == element_name:
                        presets.append({
                            'type': 'global',
                            'element': 'presets',
                            'preset': preset,
                            'data': data
                        })
                    elif element_type == 'effect':
                        for j in range(channel['numberOfEffects']):
                            if channel[j]['name'] == element_name:
                                presets.append({
                                    'type': 'global',
                                    'element': 'presets',
                                    'preset': preset,
                                    'data': data
                                })
            
            # Check global effects channel for effects
            if element_type == 'effect' and 9 in data:
                channel = data[9]
                for i in range(channel['numberOfEffects']):
                    if channel[i]['name'] == element_name:
                        presets.append({
                            'type': 'global',
                            'element': 'presets',
                            'preset': preset,
                            'data': data
                        })

        return presets

    def update_params_in_preset(self, preset: Dict, element_name: str, 
                              element_type: str, update_func: Callable[[List], List]) -> Dict:
        """Update params array for given element in a preset"""
        data = preset['data']
        
        if preset['type'] == element_type:
            # Direct preset
            data['params'] = update_func(data['params'])
        
        elif preset['type'] == 'channel':
            # Channel preset
            if element_type == 'generator' and data[9]['name'] == element_name:
                data[9]['params'] = update_func(data[9]['params'])
            elif element_type == 'effect':
                for i in range(data['numberOfEffects']):
                    if data[i]['name'] == element_name:
                        data[i]['params'] = update_func(data[i]['params'])
        
        elif preset['type'] == 'global':
            # Global preset
            for i in range(data['numberOfChannels']):
                if i in data:
                    channel = data[i]
                    if element_type == 'generator' and channel[9]['name'] == element_name:
                        channel[9]['params'] = update_func(channel[9]['params'])
                    elif element_type == 'effect':
                        for j in range(channel['numberOfEffects']):
                            if channel[j]['name'] == element_name:
                                channel[j]['params'] = update_func(channel[j]['params'])
            
            # Check global effects channel
            if element_type == 'effect' and 9 in data:
                channel = data[9]
                for i in range(channel['numberOfEffects']):
                    if channel[i]['name'] == element_name:
                        channel[i]['params'] = update_func(channel[i]['params'])
        
        return preset

    def save_preset(self, preset: Dict):
        """Save updated preset back to database"""
        with self.db.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE presets 
                SET data = ?
                WHERE name = ? AND element_id = (
                    SELECT id FROM elements WHERE name = ? AND type = ?
                )
            ''', (json.dumps(preset['data']), preset['preset'], 
                  preset['element'], preset['type']))
            conn.commit()

def update_presets(element_name: str, element_type: str, update_func: Callable[[List], List]):
    """Main function to update all presets for a given element"""
    updater = PresetUpdater()
    
    # Get all presets containing this element
    presets = updater.get_all_presets_for_element(element_name, element_type)
    print(f"Found {len(presets)} presets containing {element_type} {element_name}")
    
    # Update each preset
    for preset in presets:
        print(f"Updating {preset['type']} preset: {preset['preset']}")
        updated_preset = updater.update_params_in_preset(
            preset, element_name, element_type, update_func)
        updater.save_preset(updated_preset)
    
    print("Update complete!")



# Example update function
def update_params(params: List) -> List:
    # Modify params array here
    # Example: Double all numeric values at index 2
    for i in range(0, len(params), 4):
        if isinstance(params[i+2], (int, float)):
            params[i+2] *= 2
    return params

# Update all presets for a generator
update_presets('g_cube', 'generator', update_params)

# Update all presets for an effect
update_presets('e_rainbow', 'effect', update_params)
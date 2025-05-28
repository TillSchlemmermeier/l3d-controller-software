import json
import time
import numpy as np
from typing import Dict, List, Tuple
from db_manager import DatabaseManager

class PresetValidator:
    def __init__(self):
        self.db = DatabaseManager()
        self.validation_results = []
        self.start_time = 0
        self._initialize_elements()

    def _initialize_elements(self):
        """Initialize generators and effects from database"""
        self.generators = [gen['name'] for gen in self.db.get_active_elements('generator')]
        self.effects = [eff['name'] for eff in self.db.get_active_elements('effect')]
        # Create namespace for imports
        self.namespace = {}

        for generator in self.generators:
            exec(f'from generators.{generator} import *', self.namespace)
        for effect in self.effects:
            exec(f'from effects.{effect} import *', self.namespace)

    def validate_generator(self, generator_name: str, preset_data: Dict) -> Tuple[bool, str]:
        """Validate a single generator preset"""
        try:
            generator = self.namespace[generator_name]()
            
            midi_values = preset_data['params'][3::4]
            generator(midi_values)
            
            current_state = generator.return_state()
            for i, state_param in enumerate(current_state):
                stored_values = preset_data['params'][4*i:4*i+3]
                if stored_values != list(state_param[:3]):
                    return False, f"Parameter mismatch at index {i}"
                    
            return True, ""
        except Exception as e:
            return False, str(e)

    def validate_effect(self, effect_name: str, preset_data: Dict) -> Tuple[bool, str]:
        """Validate a single effect preset"""
        try:
            effect = self.namespace[effect_name]()
            
            world = np.zeros([3, 10, 10, 10])
            midi_values = preset_data['params'][3::4]
            effect(world, midi_values)
            
            current_state = effect.return_state()
            for i, state_param in enumerate(current_state):
                stored_values = preset_data['params'][4*i:4*i+3]
                if stored_values != list(state_param[:3]):
                    return False, f"Parameter mismatch at index {i}"
            
            return True, ""
        except Exception as e:
            return False, str(e)

    def validate_channel(self, channel_data: Dict, is_global: bool = False) -> List[Dict]:
        """Validate a channel with its generator and effects"""
        results = []
        
        if not is_global and 9 in channel_data:
            generator_data = channel_data[9]
            valid, message = self.validate_generator(generator_data['name'], generator_data)
            results.append({
                'type': 'generator',
                'name': generator_data['name'],
                'preset': 'channel',
                'valid': valid,
                'message': message
            })
        
        for i in range(channel_data['numberOfEffects']):
            effect_data = channel_data[i]
            valid, message = self.validate_effect(effect_data['name'], effect_data)
            results.append({
                'type': 'effect',
                'name': effect_data['name'],
                'preset': 'channel',
                'valid': valid,
                'message': message
            })
        
        return results

    def validate_global_preset(self, preset_data: Dict) -> List[Dict]:
        """Validate a global preset with all its channels"""
        results = []
        
        for i in range(preset_data['numberOfChannels']):
            if i in preset_data:
                channel_results = self.validate_channel(preset_data[i])
                results.extend(channel_results)
        
        if 9 in preset_data:
            channel_results = self.validate_channel(preset_data[9], is_global=True)
            results.extend(channel_results)
        
        return results

    def validate_all(self) -> Dict:
        """Validate all presets and return results as JSON"""
        self.start_time = time.time()
        self.validation_results = []
        
        print("Starting preset validation...")
        
        # Validate generator presets
        for generator in self.generators:
            presets = self.db.get_preset_names('generator', generator)
            for preset in presets:
                preset_data = self.db.get_preset('generator', generator, preset, False)
                valid, message = self.validate_generator(generator, preset_data)
                self.validation_results.append({
                    'type': 'generator',
                    'name': generator,
                    'preset': preset,
                    'valid': valid,
                    'message': message
                })
        
        # Validate effects, channels, and global presets
        # ... (rest of validation logic)
        
        # Generate summary
        elapsed_time = time.time() - self.start_time
        invalid_presets = [r for r in self.validation_results if not r['valid']]
        
        summary = {
            'total_presets': len(self.validation_results),
            'invalid_presets': len(invalid_presets),
            'time_taken': round(elapsed_time, 2),
            'average_time': round(elapsed_time/len(self.validation_results), 3),
            'all_valid': len(invalid_presets) == 0,
            'results': self.validation_results
        }
        
        # Print summary
        self._print_summary(summary)
        
        return summary
    
    def _print_summary(self, summary: Dict):
        """Print validation summary to console"""
        print("\nPreset Validation Summary:")
        print("-" * 50)
        print(f"Total presets checked: {summary['total_presets']}")
        print(f"Time taken: {summary['time_taken']} seconds")
        print(f"Average time per preset: {summary['average_time']} seconds")
        
        if not summary['all_valid']:
            print(f"\nInvalid presets found ({summary['invalid_presets']}/{summary['total_presets']}):")
            for result in summary['results']:
                if not result['valid']:
                    print(f"- {result['type']}: {result['name']} - {result['preset']}")
                    if result['message']:
                        print(f"  Error: {result['message']}")
        else:
            print("\nAll presets are valid!")

# Example usage:
if __name__ == "__main__":
    validator = PresetValidator()
    results = validator.validate_all()
    # Optionally save results to file
    with open('validation_results.json', 'w') as f:
        json.dump(results, f, indent=2)
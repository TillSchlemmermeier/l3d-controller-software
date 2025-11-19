import json
import time
import numpy as np
import traceback  # Add this import at the top
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
        self.generators = [gen['name'] for gen in self.db.get_element_names('generator')]
        self.effects = [eff['name'] for eff in self.db.get_element_names('effect')]
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
            mismatches = []  # Collect ALL mismatches

            for i, state_param in enumerate(current_state):
                stored_values = preset_data['params'][4*i:4*i+3]
                current_values = list(state_param[:3])

                if stored_values != current_values:
                    mismatches.append(
                        f"param[{i}]: {stored_values} != {current_values}"
                    )

            if mismatches:
                return False, "; ".join(mismatches)
            return True, ""

        except Exception as e:
            # Capture full exception details
            error_msg = f"{type(e).__name__}: {str(e)}"
            if not str(e):  # If str(e) is empty, use traceback
                error_msg = f"{type(e).__name__}: {traceback.format_exc().splitlines()[-1]}"
            return False, error_msg

    def validate_effect(self, effect_name: str, preset_data: Dict) -> Tuple[bool, str]:
        """Validate a single effect preset"""
        try:
            effect = self.namespace[effect_name]()

            world = np.zeros([3, 10, 10, 10])
            midi_values = preset_data['params'][3::4]
            effect(world, midi_values)

            current_state = effect.return_state()
            mismatches = []  # Collect ALL mismatches

            for i, state_param in enumerate(current_state):
                stored_values = preset_data['params'][4*i:4*i+3]
                current_values = list(state_param[:3])

                if stored_values != current_values:
                    mismatches.append(
                        f"param[{i}]: {stored_values} != {current_values}"
                    )

            if mismatches:
                return False, "; ".join(mismatches)
            return True, ""

        except Exception as e:
            # Capture full exception details
            error_msg = f"{type(e).__name__}: {str(e)}"
            if not str(e):  # If str(e) is empty, use traceback
                error_msg = f"{type(e).__name__}: {traceback.format_exc().splitlines()[-1]}"
            return False, error_msg

    def validate_channel(self, channel_data: Dict, preset_name: str = 'channel', is_global: bool = False) -> List[Dict]:
        """Validate a channel with its generator and effects"""
        results = []

        if not is_global and 9 in channel_data:
            generator_data = channel_data[9]
            valid, message = self.validate_generator(generator_data['name'], generator_data)
            results.append({
                'type': 'generator',
                'name': generator_data['name'],
                'preset': preset_name,
                'valid': valid,
                'message': message  # Now contains detailed mismatches
            })

        for i in range(channel_data['numberOfEffects']):
            effect_data = channel_data[i]
            valid, message = self.validate_effect(effect_data['name'], effect_data)
            results.append({
                'type': 'effect',
                'name': effect_data['name'],
                'preset': preset_name,
                'valid': valid,
                'message': message  # Now contains detailed mismatches
            })

        return results

    def validate_global_preset(self, preset_name: str, preset_data: Dict) -> List[Dict]:
        """Validate a global preset with all its channels"""
        results = []

        for i in range(preset_data['numberOfChannels']):
            if i in preset_data:
                channel_results = self.validate_channel(preset_data[i], preset_name)
                results.extend(channel_results)

        if 9 in preset_data:
            channel_results = self.validate_channel(preset_data[9], preset_name, is_global=True)
            results.extend(channel_results)

        return results

    def validate_all(self) -> Dict:
        """Validate all presets and return results as JSON"""
        self.start_time = time.time()
        self.validation_results = []

        print("Starting preset validation...")

        # Validate generator presets
        print("Validating generator presets...")
        for generator in self.generators:
            presets = self.db.get_preset_names('generator', generator)
            for preset in presets:
                preset_data = self.db.get_preset('generator', generator, preset['name'], False)
                valid, message = self.validate_generator(generator, preset_data)
                self.validation_results.append({
                    'type': 'generator',
                    'name': generator,
                    'preset': preset,
                    'valid': valid,
                    'message': message
                })

        # Validate effect presets
        print("Validating effect presets...")
        for effect in self.effects:
            presets = self.db.get_preset_names('effect', effect)
            for preset in presets:
                preset_data = self.db.get_preset('effect', effect, preset['name'], False)
                valid, message = self.validate_effect(effect, preset_data)
                self.validation_results.append({
                    'type': 'effect',
                    'name': effect,
                    'preset': preset,
                    'valid': valid,
                    'message': message
                })

        # Validate channel presets
        print("Validating channel presets...")
        channel_presets = self.db.get_preset_names('channel', 'presets')
        for preset in channel_presets:
            preset_data = self.db.get_preset('channel', 'presets', preset['name'], False)
            channel_results = self.validate_channel(preset_data, preset['name'])

            # Store individual results (don't aggregate - show all details)
            for result in channel_results:
                self.validation_results.append({
                    'type': 'channel',
                    'name': result['name'],  # Effect/generator name
                    'preset': preset,
                    'valid': result['valid'],
                    'message': result['message']  # Detailed error
                })

        # Validate global presets
        print("Validating global presets...")
        global_presets = self.db.get_preset_names('global', 'presets')
        for preset in global_presets:
            preset_data = self.db.get_preset('global', 'presets', preset['name'], False)
            global_results = self.validate_global_preset(preset['name'], preset_data)

            # Store individual results (don't aggregate - show all details)
            for result in global_results:
                self.validation_results.append({
                    'type': 'global',
                    'name': result['name'],  # Effect/generator name
                    'preset': preset,
                    'valid': result['valid'],
                    'message': result['message']  # Detailed error
                })

        # Generate summary
        elapsed_time = time.time() - self.start_time
        invalid_presets = [r for r in self.validation_results if not r['valid']]

        summary = {
            'total_presets': len(self.validation_results),
            'invalid_presets': len(invalid_presets),
            'time_taken': round(elapsed_time, 2),
            'average_time': round(elapsed_time/len(self.validation_results), 3) if self.validation_results else 0,
            'all_valid': len(invalid_presets) == 0,
            'results': self.validation_results
        }

        # Print summary
        self._print_summary(summary)

        return summary

    def _print_summary(self, summary: Dict):
        """Print validation summary to console"""
        print("\n" + "="*60)
        print("PRESET VALIDATION SUMMARY")
        print("="*60)
        print(f"Total presets checked: {summary['total_presets']}")
        print(f"Time taken: {summary['time_taken']} seconds")
        print(f"Average time per preset: {summary['average_time']} seconds")

        if not summary['all_valid']:
            print(f"\n⚠ Invalid presets found ({summary['invalid_presets']}/{summary['total_presets']}):")

            # Group by preset name for cleaner output
            by_preset = {}
            for result in summary['results']:
                if not result['valid']:
                    preset_key = (result['type'], result['preset']['name'])
                    if preset_key not in by_preset:
                        by_preset[preset_key] = []
                    by_preset[preset_key].append(result)

            for (preset_type, preset_name), results in by_preset.items():
                print(f"\n{preset_type}: {preset_name}")
                for result in results:
                    print(f"  - {result['name']}")
                    if result['message']:
                        # Indent the detailed error message
                        for line in result['message'].split('; '):
                            print(f"    {line}")
        else:
            print("\n✓ All presets are valid!")

# Example usage:
if __name__ == "__main__":
    validator = PresetValidator()
    results = validator.validate_all()
    # Optionally save results to file
    with open('validation_results.json', 'w') as f:
        json.dump(results, f, indent=2)
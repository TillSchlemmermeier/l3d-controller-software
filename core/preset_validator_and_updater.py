import json
import time
import numpy as np
from typing import Dict, List, Tuple, Optional, Callable, Any
from db_manager import DatabaseManager
from multiprocessing import shared_memory

class PresetValidator:
    def __init__(self, interactive: bool = True):
        self.db = DatabaseManager()
        self.validation_results = []
        self.start_time = 0
        self.interactive = interactive  # Whether to prompt user for fixes
        self.fixes_applied = 0
        self._initialize_elements()
        self.shm = self.create_mock_s2l_memory()

    def __del__(self):
        """Cleanup shared memory on destruction"""
        if hasattr(self, 'shm') and self.shm:
            self.cleanup_mock_s2l_memory(self.shm)

    def create_mock_s2l_memory(self):
        """Create temporary shared memory for initialization"""
        try:
            # Try to access existing shared memory
            shm = shared_memory.SharedMemory(name="global_s2l_memory")
        except FileNotFoundError:
            # Create mock data: 10 channels, 8 bytes each, initialized with '0.0'
            mock_data = bytearray()
            for _ in range(10):
                mock_data.extend("0.0".ljust(8).encode('utf-8'))
            
            shm = shared_memory.SharedMemory(
                name="global_s2l_memory",
                create=True,
                size=len(mock_data)
            )
            shm.buf[:] = mock_data
        return shm

    def cleanup_mock_s2l_memory(self, shm):
        """Clean up temporary shared memory"""
        try:
            shm.close()
            shm.unlink()
        except Exception:
            pass
    
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

    def _prompt_user_fix(self, element_type: str, element_name: str, preset_name: str, 
                         param_index: int, stored_values: List, current_values: List,
                         current_midi: float) -> tuple:
        """Prompt user whether to fix a mismatch"""
        if not self.interactive:
            return ('n', None)
        
        print(f"\n{'='*60}")
        print(f"MISMATCH DETECTED")
        print(f"{'='*60}")
        print(f"Type: {element_type}")
        print(f"Name: {element_name}")
        print(f"Preset: {preset_name}")
        print(f"Parameter index: {param_index}")
        print(f"\nCurrent MIDI value: {current_midi:.3f}")
        print(f"\nStored values:  {stored_values}")
        print(f"Current values: {current_values}")
        print(f"\nDifferences:")
        for i, (stored, current) in enumerate(zip(stored_values, current_values)):
            if stored != current:
                labels = ['UI Label', 'Variable Name', 'Display Value']
                print(f"  {labels[i]}: '{stored}' → '{current}'")
        
        while True:
            print("\nOptions:")
            print("  y - Update stored labels to match current behavior")
            print("  m - Change MIDI value to get desired behavior")
            print("  n - Skip this mismatch")
            print("  q - Quit validation")
            
            response = input("\nYour choice: ").lower()
            
            if response in ['y', 'n', 'q']:
                return (response, None)
            elif response == 'm':
                new_midi = self._prompt_midi_change(
                    element_type, element_name, preset_name,
                    param_index, stored_values, current_midi
                )
                if new_midi is not None:
                    return ('m', new_midi)
            else:
                print("Please enter 'y', 'm', 'n', or 'q'")

    def _prompt_midi_change(self, element_type: str, element_name: str, preset_name: str,
                        param_index: int, desired_values: List, current_midi: float) -> Optional[float]:
        """Prompt user to change MIDI value and preview result"""
        print(f"\n{'─'*60}")
        print("MIDI VALUE ADJUSTMENT")
        print(f"{'─'*60}")
        print(f"Current MIDI value: {current_midi:.3f}")
        print(f"Desired display value: {desired_values[2]}")
        
        suggested_midi = self._suggest_midi_value(
            element_type, element_name, param_index, desired_values[2], current_midi
        )
        
        if suggested_midi is not None:
            print(f"\n💡 Suggested MIDI value: {suggested_midi:.3f}")
            use_suggestion = input("Use suggestion? (y/n): ").lower()
            if use_suggestion == 'y':
                new_midi = suggested_midi
            else:
                new_midi = self._get_midi_input()
        else:
            print("\n⚠ Could not suggest value automatically")
            new_midi = self._get_midi_input()
        
        if new_midi is None:
            return None
        
        preview_result = self._preview_midi_change(
            element_type, element_name, param_index, new_midi
        )
        
        if preview_result is None:
            print("❌ Failed to preview new MIDI value")
            return None
        
        print(f"\n📋 Preview with MIDI = {new_midi:.3f}:")
        print(f"  UI Label: {preview_result[0]}")
        print(f"  Variable: {preview_result[1]}")
        print(f"  Display:  {preview_result[2]}")
        
        while True:
            confirm = input("\nAccept this value? (y/n/r to retry): ").lower()
            if confirm == 'y':
                return new_midi
            elif confirm == 'n':
                return None
            elif confirm == 'r':
                return self._prompt_midi_change(
                    element_type, element_name, preset_name,
                    param_index, desired_values, current_midi
                )
            else:
                print("Please enter 'y', 'n', or 'r'")

    def _get_midi_input(self) -> Optional[float]:
        """Get MIDI value input from user with validation"""
        while True:
            try:
                user_input = input("Enter new MIDI value (0.0-1.0, or 'c' to cancel): ").lower()
                if user_input == 'c':
                    return None
                
                new_midi = float(user_input)
                if 0.0 <= new_midi <= 1.0:
                    return new_midi
                else:
                    print("❌ Value must be between 0.0 and 1.0")
            except ValueError:
                print("❌ Invalid input. Enter a number or 'c' to cancel")

    def _suggest_midi_value(self, element_type: str, element_name: str, 
                       param_index: int, desired_display: any, current_midi: float) -> Optional[float]:
        """Try to find MIDI value that produces desired display value"""
        try:
            test_values = np.linspace(0, 1, 21)
            for midi_val in test_values:
                result = self._preview_midi_change(element_type, element_name, param_index, midi_val)
                if result and result[2] == desired_display:
                    return float(midi_val)
            return None
        except Exception as e:
            print(f"⚠ Error suggesting MIDI value: {e}")
            return None

    def _preview_midi_change(self, element_type: str, element_name: str, 
                        param_index: int, new_midi: float) -> Optional[List]:
        """Preview what return_state returns for a given MIDI value"""
        try:
            if element_type == 'generator':
                element = self.namespace[element_name]()
                current_state = element.return_state()
                num_params = len(current_state)
                dummy_args = [0] * num_params
                dummy_args[param_index] = new_midi
                element(dummy_args)
                new_state = element.return_state()
                return list(new_state[param_index][:3])
                
            elif element_type == 'effect':
                element = self.namespace[element_name]()
                world = np.zeros([3, 10, 10, 10])
                current_state = element.return_state()
                num_params = len(current_state)
                dummy_args = [0] * num_params
                dummy_args[param_index] = new_midi
                element(world, dummy_args)
                new_state = element.return_state()
                return list(new_state[param_index][:3])
            return None
        except Exception as e:
            print(f"⚠ Error previewing MIDI change: {e}")
            return None

    def _save_preset(self, element_type: str, element_name: str, preset_name: str,
                     preset_data: Dict, parent_preset_type: str = None, 
                     parent_preset_name: str = None, parent_preset_data: Dict = None) -> bool:
        """Save the preset to the database"""
        try:
            if parent_preset_type and parent_preset_data:
                self.db.save_preset(parent_preset_type, parent_preset_name, preset_name, parent_preset_data)
            else:
                self.db.save_preset(element_type, element_name, preset_name, preset_data)
            return True
        except Exception as e:
            print(f"  Error saving preset: {e}")
            return False

    def _handle_added_parameter(self, element_type: str, element_name: str, preset_name: str,
                                param_index: int, current_param_state: List,
                                element_instance: Any, midi_values: List) -> Optional[List]:
        """Handle a new parameter detected in the code but missing in preset"""
        if not self.interactive:
            return None

        print(f"\n{'='*60}")
        print(f"NEW PARAMETER DETECTED")
        print(f"{'='*60}")
        print(f"Type: {element_type}")
        print(f"Name: {element_name}")
        print(f"Preset: {preset_name}")
        print(f"Index: {param_index}")
        print(f"Parameter: {current_param_state[0]} ({current_param_state[1]})")

        while True:
            response = input("\nAdd this parameter to preset? (y/n/q): ").lower()
            if response == 'q':
                return 'q'
            elif response == 'n':
                return None
            elif response == 'y':
                print(f"Enter MIDI value for '{current_param_state[0]}'")
                new_midi = self._get_midi_input()
                if new_midi is None:
                    return None # Cancelled

                # Update midi values and re-run element to get correct display value
                # Note: midi_values is already padded to the correct length
                midi_values[param_index] = new_midi

                if element_type == 'generator':
                    element_instance(midi_values)
                elif element_type == 'effect':
                    world = np.zeros([3, 10, 10, 10])
                    element_instance(world, midi_values)

                new_state = element_instance.return_state()

                # Construct new parameter data [label, var, display, midi]
                new_param_data = list(new_state[param_index][:3]) + [new_midi]
                return new_param_data
            else:
                print("Please enter 'y', 'n', or 'q'")

    def _handle_removed_parameters(self, element_type: str, element_name: str, preset_name: str,
                                   removed_params: List[List]) -> str:
        """Handle extra parameters in preset that are missing in code"""
        if not self.interactive:
            return 'n'

        print(f"\n{'='*60}")
        print(f"REMOVED PARAMETERS DETECTED")
        print(f"{'='*60}")
        print(f"Type: {element_type}")
        print(f"Name: {element_name}")
        print(f"Preset: {preset_name}")
        print(f"Extra parameters found starting at index {len(removed_params)}") # This index logic was slightly off in print, fixed below
        print(f"Count: {len(removed_params)}")
        print("Parameters to remove:")
        for i, param in enumerate(removed_params):
            print(f"  - {param[0]} ({param[1]}) [Value: {param[2]}, MIDI: {param[3]}]")

        while True:
            response = input("\nRemove these parameters from preset? (y/n/q): ").lower()
            if response in ['y', 'n', 'q']:
                return response
            print("Please enter 'y', 'n', or 'q'")

    def _validate_element_generic(self, element_type: str, element_name: str,preset_name: str, 
                                  preset_data: Dict, element_instance: Any,
                                  parent_preset_type: str = None, parent_preset_name: str = None,
                                  parent_preset_data: Dict = None) -> Tuple[bool, str, Optional[Dict]]:
        """Generic validation logic for both generators and effects"""
        try:
            # Extract stored parameters into a list of lists [label, var, display, midi]
            raw_params = preset_data['params']
            stored_params_list = [raw_params[i:i+4] for i in range(0, len(raw_params), 4)]

            # Extract MIDI values from stored params
            midi_values = [p[3] for p in stored_params_list]

            # 1. Get expected parameter count from the live instance
            # We call return_state() first to see what the code expects
            initial_state = element_instance.return_state()
            expected_params = len(initial_state)

            # 2. Pad MIDI values if code expects more than preset has
            # This prevents "list index out of range" when calling the element
            if len(midi_values) < expected_params:
                padding = [0.5] * (expected_params - len(midi_values))
                midi_values.extend(padding)

            # 3. Run element to get current state with these MIDI values
            if element_type == 'generator':
                element_instance(midi_values)
            elif element_type == 'effect':
                world = np.zeros([3, 10, 10, 10])
                element_instance(world, midi_values)

            current_state = element_instance.return_state()

            mismatches = []
            changes_made = False

            # Iterate through current parameters (handling matches and additions)
            i = 0
            while i < len(current_state):
                current_param = current_state[i]
                current_values = list(current_param[:3])

                if i < len(stored_params_list):
                    # MATCH: Parameter exists in both
                    stored_values = stored_params_list[i][:3]
                    current_midi = stored_params_list[i][3]

                    if stored_values != current_values:
                        action, new_midi = self._prompt_user_fix(
                            element_type, element_name, preset_name,
                            i, stored_values, current_values, current_midi
                        )

                        if action == 'q':
                            return False, "User quit validation", None
                        elif action == 'y':
                            # Update labels
                            stored_params_list[i][:3] = current_values
                            changes_made = True
                            print("  ✓ Updated labels")
                            self.fixes_applied += 1
                        elif action == 'm':
                            # Update MIDI and labels
                            midi_values[i] = new_midi

                            # Re-run to get updated display value
                            if element_type == 'generator':
                                element_instance(midi_values)
                            elif element_type == 'effect':
                                world = np.zeros([3, 10, 10, 10])
                                element_instance(world, midi_values)

                            new_state_run = element_instance.return_state()
                            new_values_run = list(new_state_run[i][:3])

                            stored_params_list[i] = new_values_run + [new_midi]
                            changes_made = True
                            print(f"  ✓ Updated MIDI to {new_midi:.3f} and labels")
                            self.fixes_applied += 1
                        else:
                            mismatches.append(f"Mismatch at {i}: {stored_values} != {current_values}")
                else:
                    # ADDITION: Parameter in code but not in preset
                    result = self._handle_added_parameter(
                        element_type, element_name, preset_name,
                        i, current_values, element_instance, midi_values
                    )

                    if result == 'q':
                        return False, "User quit validation", None
                    elif result:
                        # Add new parameter to stored list
                        stored_params_list.append(result)
                        changes_made = True
                        print(f"  ✓ Added parameter {i}")
                        self.fixes_applied += 1
                    else:
                        mismatches.append(f"Missing parameter at {i}: {current_values[0]}")

                i += 1

            # REMOVAL: Check for extra parameters in preset
            if len(stored_params_list) > len(current_state):
                extra_params = stored_params_list[len(current_state):]
                action = self._handle_removed_parameters(
                    element_type, element_name, preset_name,
                    extra_params
                )

                if action == 'q':
                    return False, "User quit validation", None
                elif action == 'y':
                    # Truncate list
                    stored_params_list = stored_params_list[:len(current_state)]
                    changes_made = True
                    print(f"  ✓ Removed {len(extra_params)} extra parameters")
                    self.fixes_applied += 1
                else:
                    mismatches.append(f"{len(extra_params)} extra parameters found")

            if changes_made:
                # Flatten list back to single array
                new_flat_params = [item for sublist in stored_params_list for item in sublist]
                preset_data['params'] = new_flat_params

                if self._save_preset(element_type, element_name, preset_name, preset_data,
                                     parent_preset_type, parent_preset_name, parent_preset_data):
                    print("  ✓ Preset saved successfully")
                else:
                    mismatches.append("Failed to save preset")

            if mismatches:
                return False, "; ".join(mismatches), preset_data
            return True, "", preset_data

        except Exception as e:
            # Print traceback for debugging if needed, but keep clean output for now
            import traceback
            traceback.print_exc()
            return False, str(e), None

    def validate_generator(self, generator_name: str, preset_name: str, preset_data: Dict,
                       parent_preset_type: str = None, parent_preset_name: str = None,
                       parent_preset_data: Dict = None) -> Tuple[bool, str, Optional[Dict]]:
        """Validate a single generator preset"""
        try:
            generator = self.namespace[generator_name]()
            return self._validate_element_generic(
                'generator', generator_name, preset_name, preset_data, generator,
                parent_preset_type, parent_preset_name, parent_preset_data
            )
        except Exception as e:
            return False, str(e), None

    def validate_effect(self, effect_name: str, preset_name: str, preset_data: Dict,
                    parent_preset_type: str = None, parent_preset_name: str = None,
                    parent_preset_data: Dict = None) -> Tuple[bool, str, Optional[Dict]]:
        """Validate a single effect preset"""
        try:
            effect = self.namespace[effect_name]()
            return self._validate_element_generic(
                'effect', effect_name, preset_name, preset_data, effect,
                parent_preset_type, parent_preset_name, parent_preset_data
            )
        except Exception as e:
            return False, str(e), None

    def validate_channel(self, channel_data: Dict, preset_name: str, is_global: bool = False,
                     parent_preset_type: str = None, parent_preset_data: Dict = None) -> List[Dict]:
        """Validate a channel with its generator and effects"""
        results = []
        
        if parent_preset_type is None:
            parent_preset_type = 'global' if is_global else 'channel'
        
        if not is_global and 9 in channel_data:
            generator_data = channel_data[9]
            valid, message, updated_data = self.validate_generator(
                generator_data['name'], preset_name, generator_data,
                parent_preset_type=parent_preset_type,
                parent_preset_name='presets',
                parent_preset_data=parent_preset_data
            )
            
            if message == "User quit validation":
                raise KeyboardInterrupt("User requested quit")
            
            results.append({
                'type': 'generator',
                'name': generator_data['name'],
                'preset': preset_name,
                'valid': valid,
                'message': message
            })
        
        for i in range(channel_data['numberOfEffects']):
            effect_data = channel_data[i]
            valid, message, updated_data = self.validate_effect(
                effect_data['name'], preset_name, effect_data,
                parent_preset_type=parent_preset_type,
                parent_preset_name='presets',
                parent_preset_data=parent_preset_data
            )
            
            if message == "User quit validation":
                raise KeyboardInterrupt("User requested quit")
            
            results.append({
                'type': 'effect',
                'name': effect_data['name'],
                'preset': preset_name,
                'valid': valid,
                'message': message
            })
        
        return results

    def validate_global_preset(self, preset_name: str, preset_data: Dict) -> List[Dict]:
        """Validate a global preset with all its channels"""
        results = []
        
        for i in range(preset_data['numberOfChannels']):
            if i in preset_data:
                channel_results = self.validate_channel(
                    preset_data[i], preset_name,
                    parent_preset_type='global',
                    parent_preset_data=preset_data
                )
                results.extend(channel_results)
        
        if 9 in preset_data:
            channel_results = self.validate_channel(
                preset_data[9], preset_name, is_global=True,
                parent_preset_type='global',
                parent_preset_data=preset_data
            )
            results.extend(channel_results)
        
        return results

    def validate_all(self) -> Dict:
        """Validate all presets and return results as JSON"""
        self.start_time = time.time()
        self.validation_results = []
        self.fixes_applied = 0
        
        print("Starting preset validation...")
        if self.interactive:
            print("Interactive mode: You will be prompted to fix mismatches")
        else:
            print("Non-interactive mode: Only reporting mismatches")
        
        try:
            # Validate generator presets
            print("\nValidating generator presets...")
            for generator in self.generators:
                presets = self.db.get_preset_names('generator', generator)
                for preset in presets:
                    preset_data = self.db.get_preset('generator', generator, preset['name'], False)
                    valid, message, updated_data = self.validate_generator(
                        generator, preset['name'], preset_data
                    )
                    
                    if message == "User quit validation":
                        raise KeyboardInterrupt("User requested quit")
                    
                    self.validation_results.append({
                        'type': 'generator',
                        'name': generator,
                        'preset': preset,
                        'valid': valid,
                        'message': message
                    })
            
            # Validate effect presets
            print("\nValidating effect presets...")
            for effect in self.effects:
                presets = self.db.get_preset_names('effect', effect)
                for preset in presets:
                    preset_data = self.db.get_preset('effect', effect, preset['name'], False)
                    valid, message, updated_data = self.validate_effect(
                        effect, preset['name'], preset_data
                    )
                    
                    if message == "User quit validation":
                        raise KeyboardInterrupt("User requested quit")
                    
                    self.validation_results.append({
                        'type': 'effect',
                        'name': effect,
                        'preset': preset,
                        'valid': valid,
                        'message': message
                    })
            
            # Validate channel presets
            print("\nValidating channel presets...")
            channel_presets = self.db.get_preset_names('channel', 'presets')
            for preset in channel_presets:
                preset_data = self.db.get_preset('channel', 'presets', preset['name'], False)
                channel_results = self.validate_channel(
                    preset_data, preset['name'],
                    parent_preset_data=preset_data
                )
                
                all_valid = all(r['valid'] for r in channel_results)
                messages = [r['message'] for r in channel_results if not r['valid']]
                
                self.validation_results.append({
                    'type': 'channel',
                    'name': 'presets',
                    'preset': preset,
                    'valid': all_valid,
                    'message': '; '.join(messages) if messages else ''
                })
            
            # Validate global presets
            print("\nValidating global presets...")
            global_presets = self.db.get_preset_names('global', 'presets')
            for preset in global_presets:
                preset_data = self.db.get_preset('global', 'presets', preset['name'], False)
                global_results = self.validate_global_preset(preset['name'], preset_data)
                
                all_valid = all(r['valid'] for r in global_results)
                messages = [r['message'] for r in global_results if not r['valid']]
                
                self.validation_results.append({
                    'type': 'global',
                    'name': 'presets',
                    'preset': preset,
                    'valid': all_valid,
                    'message': '; '.join(messages) if messages else ''
                })
        
        except KeyboardInterrupt:
            print("\n\nValidation interrupted by user")
        
        elapsed_time = time.time() - self.start_time
        invalid_presets = [r for r in self.validation_results if not r['valid']]
        
        summary = {
            'total_presets': len(self.validation_results),
            'invalid_presets': len(invalid_presets),
            'fixes_applied': self.fixes_applied,
            'time_taken': round(elapsed_time, 2),
            'average_time': round(elapsed_time/len(self.validation_results), 3) if self.validation_results else 0,
            'all_valid': len(invalid_presets) == 0,
            'results': self.validation_results
        }
        
        self._print_summary(summary)
        return summary
    
    def _print_summary(self, summary: Dict):
        """Print validation summary to console"""
        print("\n" + "="*60)
        print("PRESET VALIDATION SUMMARY")
        print("="*60)
        print(f"Total presets checked: {summary['total_presets']}")
        print(f"Fixes applied: {summary['fixes_applied']}")
        print(f"Time taken: {summary['time_taken']} seconds")
        print(f"Average time per preset: {summary['average_time']} seconds")
        
        if not summary['all_valid']:
            print(f"\n⚠ Invalid presets remaining ({summary['invalid_presets']}/{summary['total_presets']}):")
            for result in summary['results']:
                if not result['valid']:
                    print(f"  - {result['type']}: {result['name']} - {result['preset']['name']}")
                    if result['message']:
                        print(f"    Error: {result['message']}")
        else:
            print("\n✓ All presets are valid!")

if __name__ == "__main__":
    import sys
    interactive = '--non-interactive' not in sys.argv
    validator = PresetValidator(interactive=interactive)
    results = validator.validate_all()
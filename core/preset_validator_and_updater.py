import json
import time
import numpy as np
from typing import Dict, List, Tuple, Optional
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
        shm = self.create_mock_s2l_memory()

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

    def cleanup_mock_s2l_memory(shm):
        """Clean up temporary shared memory"""
        shm.close()
        try:
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
        """Prompt user whether to fix a mismatch
        
        Returns:
            tuple: (action, new_midi_value)
            action: 'y' (update labels), 'n' (skip), 'q' (quit), 'm' (change MIDI)
            new_midi_value: float if action=='m', else None
        """
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
                # If user cancels MIDI change, loop back to main prompt
            else:
                print("Please enter 'y', 'm', 'n', or 'q'")

    def _prompt_midi_change(self, element_type: str, element_name: str, preset_name: str,
                        param_index: int, desired_values: List, current_midi: float) -> Optional[float]:
        """Prompt user to change MIDI value and preview result
        
        Returns:
            float: New MIDI value if user confirms, None if cancelled
        """
        print(f"\n{'─'*60}")
        print("MIDI VALUE ADJUSTMENT")
        print(f"{'─'*60}")
        print(f"Current MIDI value: {current_midi:.3f}")
        print(f"Desired display value: {desired_values[2]}")  # Display value is index 2
        
        # Try to suggest a MIDI value (smart mode)
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
            return None  # User cancelled
        
        # Preview what return_state would return with new MIDI
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
                return None  # Cancel
            elif confirm == 'r':
                # Retry with new input
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
        """Try to find MIDI value that produces desired display value
    
        Uses binary search for numeric values, brute force for categories
        """
        try:
            # Test a range of MIDI values to find which produces desired display
            test_values = np.linspace(0, 1, 21)  # Test 21 points (0.0, 0.05, 0.1, ..., 1.0)
            
            for midi_val in test_values:
                result = self._preview_midi_change(element_type, element_name, param_index, midi_val)
                if result and result[2] == desired_display:
                    return float(midi_val)
            
            # If exact match not found, return None (user must input manually)
            return None
            
        except Exception as e:
            print(f"⚠ Error suggesting MIDI value: {e}")
            return None

    def _preview_midi_change(self, element_type: str, element_name: str, 
                        param_index: int, new_midi: float) -> Optional[List]:
        """Preview what return_state returns for a given MIDI value
    
        Returns:
            List: [ui_label, var_name, display_value] or None if error
        """
        try:
            if element_type == 'generator':
                element = self.namespace[element_name]()
                # Create dummy args with new MIDI at param_index
                # We need to know how many params this element has
                current_state = element.return_state()
                num_params = len(current_state)
                dummy_args = [0.5] * num_params  # Default all to 0.5
                dummy_args[param_index] = new_midi
                
                element(dummy_args)
                new_state = element.return_state()
                return list(new_state[param_index][:3])
                
            elif element_type == 'effect':
                element = self.namespace[element_name]()
                world = np.zeros([3, 10, 10, 10])
                
                current_state = element.return_state()
                num_params = len(current_state)
                dummy_args = [0.5] * num_params
                dummy_args[param_index] = new_midi
                
                element(world, dummy_args)
                new_state = element.return_state()
                return list(new_state[param_index][:3])
        
            return None
            
        except Exception as e:
            print(f"⚠ Error previewing MIDI change: {e}")
            return None

    def _update_preset_parameter(self, element_type: str, element_name: str, preset_name: str,
                                  preset_data: Dict, param_index: int, new_values: List,
                                  parent_preset_type: str = None, parent_preset_name: str = None,
                                  parent_preset_data: Dict = None) -> bool:
        """Update a specific parameter in the preset
        
        Args:
            element_type: Type of element ('generator', 'effect', 'channel', 'global')
            element_name: Name of the element
            preset_name: Name of the preset being updated
            preset_data: The preset data containing the parameter
            param_index: Index of the parameter to update
            new_values: New values to set [ui_label, var_name, display_value]
            parent_preset_type: If this is nested in a channel/global preset, the parent type
            parent_preset_name: Name of the parent preset
            parent_preset_data: The full parent preset data
        """
        try:
            # Update the preset_data with new values (modifies in-place)
            preset_data['params'][4*param_index:4*param_index+3] = new_values
            
            # Save the appropriate preset
            if parent_preset_type and parent_preset_data:
                # This is a nested element in a channel/global preset
                # Save the entire parent preset (which now contains the updated nested data)
                self.db.save_preset(parent_preset_type, parent_preset_name, preset_name, parent_preset_data)
            else:
                # This is a standalone generator/effect preset
                self.db.save_preset(element_type, element_name, preset_name, preset_data)
            
            return True
        except Exception as e:
            print(f"  Error updating preset: {e}")
            return False

    def validate_generator(self, generator_name: str, preset_name: str, preset_data: Dict,
                       parent_preset_type: str = None, parent_preset_name: str = None,
                       parent_preset_data: Dict = None) -> Tuple[bool, str, Optional[Dict]]:
        """Validate a single generator preset
        
        Args:
            generator_name: Name of the generator
            preset_name: Name of the preset
            preset_data: Generator preset data
            parent_preset_type: If nested, the type ('channel' or 'global')
            parent_preset_name: If nested, the parent preset name (e.g., 'presets')
            parent_preset_data: If nested, the full parent preset data
        """
        try:
            generator = self.namespace[generator_name]()
            
            midi_values = preset_data['params'][3::4]
            generator(midi_values)
            
            current_state = generator.return_state()
            mismatches = []
            
            for i, state_param in enumerate(current_state):
                stored_values = preset_data['params'][4*i:4*i+3]
                current_values = list(state_param[:3])
                
                if stored_values != current_values:
                    current_midi = midi_values[i]
                    action, new_midi = self._prompt_user_fix(
                        'generator', generator_name, preset_name, 
                        i, stored_values, current_values, current_midi
                    )
                    
                    if action == 'q':
                        return False, "User quit validation", None
                    elif action == 'y':
                        # Update labels only
                        if self._update_preset_parameter(
                            'generator', generator_name, preset_name, 
                            preset_data, i, current_values,
                            parent_preset_type, parent_preset_name, parent_preset_data
                        ):
                            print("  ✓ Updated labels successfully")
                            self.fixes_applied += 1
                        else:
                            mismatches.append(f"Failed to update parameter {i}")
                    elif action == 'm':
                        # Update MIDI value
                        preset_data['params'][4*i + 3] = new_midi  # MIDI is at index 3
                        
                        # Get new return_state with updated MIDI
                        midi_values[i] = new_midi
                        generator(midi_values)
                        new_state = generator.return_state()
                        new_values = list(new_state[i][:3])
                        
                        # Update both MIDI and labels
                        preset_data['params'][4*i:4*i+3] = new_values
                        
                        if self._update_preset_parameter(
                            'generator', generator_name, preset_name, 
                            preset_data, i, new_values,
                            parent_preset_type, parent_preset_name, parent_preset_data
                        ):
                            print(f"  ✓ Updated MIDI to {new_midi:.3f} and labels successfully")
                            self.fixes_applied += 1
                        else:
                            mismatches.append(f"Failed to update parameter {i}")
                    else:  # 'n' - skip
                        mismatches.append(f"Parameter mismatch at index {i}: {stored_values} != {current_values}")
            
            if mismatches:
                return False, "; ".join(mismatches), preset_data
            return True, "", preset_data
            
        except Exception as e:
            return False, str(e), None

    def validate_effect(self, effect_name: str, preset_name: str, preset_data: Dict,
                    parent_preset_type: str = None, parent_preset_name: str = None,
                    parent_preset_data: Dict = None) -> Tuple[bool, str, Optional[Dict]]:
        """Validate a single effect preset
        
        Args:
            effect_name: Name of the effect
            preset_name: Name of the preset
            preset_data: Effect preset data
            parent_preset_type: If nested, the type ('channel' or 'global')
            parent_preset_name: If nested, the parent preset name (e.g., 'presets')
            parent_preset_data: If nested, the full parent preset data
        """
        try:
            effect = self.namespace[effect_name]()
            
            world = np.zeros([3, 10, 10, 10])
            midi_values = preset_data['params'][3::4]
            effect(world, midi_values)
            
            current_state = effect.return_state()
            mismatches = []
            
            for i, state_param in enumerate(current_state):
                stored_values = preset_data['params'][4*i:4*i+3]
                current_values = list(state_param[:3])
                
                if stored_values != current_values:
                    current_midi = midi_values[i]
                    action, new_midi = self._prompt_user_fix(
                        'effect', effect_name, preset_name, 
                        i, stored_values, current_values, current_midi
                    )
                    
                    if action == 'q':
                        return False, "User quit validation", None
                    elif action == 'y':
                        # Update labels only
                        if self._update_preset_parameter(
                            'effect', effect_name, preset_name, 
                            preset_data, i, current_values,
                            parent_preset_type, parent_preset_name, parent_preset_data
                        ):
                            print("  ✓ Updated labels successfully")
                            self.fixes_applied += 1
                        else:
                            mismatches.append(f"Failed to update parameter {i}")
                    elif action == 'm':
                        # Update MIDI value
                        preset_data['params'][4*i + 3] = new_midi
                        
                        # Get new return_state with updated MIDI
                        midi_values[i] = new_midi
                        world = np.zeros([3, 10, 10, 10])
                        effect(world, midi_values)
                        new_state = effect.return_state()
                        new_values = list(new_state[i][:3])
                        
                        # Update both MIDI and labels
                        preset_data['params'][4*i:4*i+3] = new_values
                        
                        if self._update_preset_parameter(
                            'effect', effect_name, preset_name, 
                            preset_data, i, new_values,
                            parent_preset_type, parent_preset_name, parent_preset_data
                        ):
                            print(f"  ✓ Updated MIDI to {new_midi:.3f} and labels successfully")
                            self.fixes_applied += 1
                        else:
                            mismatches.append(f"Failed to update parameter {i}")
                    else:  # 'n' - skip
                        mismatches.append(f"Parameter mismatch at index {i}: {stored_values} != {current_values}")
            
            if mismatches:
                return False, "; ".join(mismatches), preset_data
            return True, "", preset_data
            
        except Exception as e:
            return False, str(e), None

    def validate_channel(self, channel_data: Dict, preset_name: str, is_global: bool = False,
                     parent_preset_type: str = None, parent_preset_data: Dict = None) -> List[Dict]:
        """Validate a channel with its generator and effects

        Args:
            channel_data: The channel data
            preset_name: Name of the parent preset
            is_global: Whether this is from a global preset
            parent_preset_type: Type of parent preset ('channel' or 'global')
            parent_preset_data: The full parent preset data (channel or global)
        """
        results = []
        
        # Determine the actual parent type (if not explicitly passed)
        if parent_preset_type is None:
            parent_preset_type = 'global' if is_global else 'channel'
        
        if not is_global and 9 in channel_data:
            generator_data = channel_data[9]
            valid, message, updated_data = self.validate_generator(
                generator_data['name'], preset_name, generator_data,
                parent_preset_type=parent_preset_type,  # Use determined type
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
                parent_preset_type=parent_preset_type,  # Use determined type
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
                    parent_preset_type='global',  # Explicitly pass 'global'
                    parent_preset_data=preset_data
                )
                results.extend(channel_results)
        
        if 9 in preset_data:
            channel_results = self.validate_channel(
                preset_data[9], preset_name, is_global=True,
                parent_preset_type='global',  # Explicitly pass 'global'
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
                    parent_preset_data=preset_data  # Pass parent!
                )
                
                # Aggregate results for the channel preset
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
                
                # Aggregate results for the global preset
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
        
        # Generate summary
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
        
        # Print summary
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

# Example usage:
if __name__ == "__main__":
    import sys
    
    # Check if --non-interactive flag is passed
    interactive = '--non-interactive' not in sys.argv
    
    validator = PresetValidator(interactive=interactive)
    results = validator.validate_all()
    
    # Optionally save results to file
    # with open('validation_results.json', 'w') as f:
    #     json.dump(results, f, indent=2)
    
    # print(f"\n✓ Results saved to validation_results.json")
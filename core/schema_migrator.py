from core.preset_administration.schema_comparator import SchemaComparator, SchemaChange, ChangeType
from core.preset_administration.preset_updater import PresetUpdater, UpdateType
from typing import Dict, List
import json

class SchemaMigrator:
    """Automatically migrate presets based on schema changes"""
    
    def __init__(self):
        self.updater = PresetUpdater()
        self.migration_log = []
    
    def migrate_from_changes(self, changes: List[SchemaChange], dry_run: bool = False):
        """Apply migrations based on detected schema changes"""
        
        print("=" * 60)
        print("SCHEMA MIGRATION")
        print("=" * 60)
        
        if dry_run:
            print("DRY RUN MODE - No changes will be saved")
            print()
        
        # Group changes by element
        changes_by_element = {}
        for change in changes:
            key = f"{change.element_type}.{change.element_name}"
            if key not in changes_by_element:
                changes_by_element[key] = []
            changes_by_element[key].append(change)
        
        # Process each element's changes
        for element_key, element_changes in changes_by_element.items():
            element_type, element_name = element_key.split('.', 1)
            
            print(f"\n{element_key}:")
            print("-" * 60)
            
            # Sort changes to apply in correct order
            # 1. Parameter removals (from end to start)
            # 2. Parameter additions (from start to end)
            # 3. Other changes
            removals = [c for c in element_changes if c.change_type == ChangeType.PARAM_REMOVED]
            additions = [c for c in element_changes if c.change_type == ChangeType.PARAM_ADDED]
            others = [c for c in element_changes if c.change_type not in [ChangeType.PARAM_REMOVED, ChangeType.PARAM_ADDED]]
            
            # Sort removals by index descending (remove from end first)
            removals.sort(key=lambda c: c.details['param_index'], reverse=True)
            # Sort additions by index ascending (add from start first)
            additions.sort(key=lambda c: c.details['param_index'])
            
            sorted_changes = removals + additions + others
            
            for change in sorted_changes:
                self._apply_single_change(element_name, element_type, change, dry_run)
        
        print("\n" + "=" * 60)
        print("MIGRATION COMPLETE")
        print("=" * 60)
        
        return self.migration_log
    
    def _apply_single_change(self, element_name: str, element_type: str, 
                            change: SchemaChange, dry_run: bool):
        """Apply a single schema change to all presets"""
        
        details = change.details
        
        print(f"\n  {change.change_type.value}:")
        print(f"    Details: {details}")
        
        # Map SchemaChange to PresetUpdater UpdateType and kwargs
        if change.change_type == ChangeType.PARAM_ADDED:
            update_type = UpdateType.PARAM_ADDED
            kwargs = {
                'param_index': details['param_index'],
                'param_name': details['param_name'],
                'param_label': details['param_label'],
                'default_midi': 0.0  # Default to 0, could be smarter
            }
            
        elif change.change_type == ChangeType.PARAM_REMOVED:
            update_type = UpdateType.PARAM_REMOVED
            kwargs = {
                'param_index': details['param_index'],
                'delete_preset': False  # Don't delete presets by default
            }
            
        elif change.change_type == ChangeType.PARAM_RENAMED:
            update_type = UpdateType.PARAM_RENAMED
            kwargs = {
                'param_index': details['param_index'],
                'new_name': details['new_name'],
                'new_label': details['new_label']
            }
            
        elif change.change_type == ChangeType.RANGE_CHANGED:
            # Determine if range was extended or shrinked
            old_range = details['old_max'] - details['old_min']
            new_range = details['new_max'] - details['new_min']
            
            if new_range > old_range:
                update_type = UpdateType.RANGE_EXTENDED
            else:
                update_type = UpdateType.RANGE_SHRINKED
                
            kwargs = {
                'param_index': details['param_index'],
                'old_min': details['old_min'],
                'old_max': details['old_max'],
                'new_min': details['new_min'],
                'new_max': details['new_max'],
                'keep_absolute': True
            }
            
        elif change.change_type == ChangeType.CATEGORIES_CHANGED:
            old_cats = details['old_categories']
            new_cats = details['new_categories']
            
            # Determine if categories were added or removed
            if len(new_cats) > len(old_cats):
                update_type = UpdateType.CATEGORY_ADDED
            else:
                update_type = UpdateType.CATEGORY_REMOVED
                
            kwargs = {
                'param_index': details['param_index'],
                'old_categories': old_cats,
                'new_categories': new_cats,
                'fallback_category': new_cats[0] if new_cats else None
            }
        else:
            print(f"    ⚠ Unsupported change type: {change.change_type}")
            return
        
        # Apply the update
        if not dry_run:
            summary = self.updater.update_all_presets(
                element_name=element_name,
                element_type=element_type,
                update_type=update_type,
                **kwargs
            )
            
            print(f"    Updated: {summary['updated']}")
            print(f"    Deleted: {summary['deleted']}")
            if summary['errors']:
                print(f"    Errors: {len(summary['errors'])}")
                for error in summary['errors'][:3]:  # Show first 3 errors
                    print(f"      - {error['preset']}: {error['error']}")
                if len(summary['errors']) > 3:
                    print(f"      ... and {len(summary['errors']) - 3} more")
            
            self.migration_log.append({
                'element': f"{element_type}.{element_name}",
                'change': change.change_type.value,
                'summary': summary
            })
        else:
            print(f"    [DRY RUN] Would update presets with {update_type.value}")

def main():
    """Main migration workflow"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Migrate presets based on schema changes')
    parser.add_argument('--old-schema', default='element_schemas_old.json',
                       help='Path to old schema file')
    parser.add_argument('--new-schema', default='element_schemas.json',
                       help='Path to new schema file')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be changed without actually changing')
    parser.add_argument('--output-log', default='migration_log.json',
                       help='Path to save migration log')
    
    args = parser.parse_args()
    
    # Compare schemas
    print("Comparing schemas...")
    comparator = SchemaComparator(args.old_schema, args.new_schema)
    changes = comparator.compare_all()
    
    if not changes:
        print("No changes detected!")
        return
    
    print(f"\nDetected {len(changes)} changes:")
    for change in changes:
        print(f"  - {change}")
    
    # Migrate
    migrator = SchemaMigrator()
    log = migrator.migrate_from_changes(changes, dry_run=args.dry_run)
    
    # Save log
    if not args.dry_run:
        with open(args.output_log, 'w') as f:
            json.dump(log, f, indent=2)
        print(f"\nMigration log saved to {args.output_log}")

if __name__ == '__main__':
    main()
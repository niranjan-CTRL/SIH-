import sys
import traceback
sys.path.insert(0, '.')
try:
    print('Importing app.main...')
    sys.stdout.flush()
    import app.main
    print('SUCCESS! App imported')
    print(f'App: {app.main.app}')
except Exception as e:
    print(f'ERROR: {e}')
    traceback.print_exc()

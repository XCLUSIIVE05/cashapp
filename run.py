import os
import sys

# Print current directory
print(f"Current directory: {os.getcwd()}")
print(f"Python executable: {sys.executable}")
print(f"Python path: {sys.path}")

try:
    from app import create_app
    
    app = create_app()
    
    if __name__ == '__main__':
        app.run(debug=True)
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()
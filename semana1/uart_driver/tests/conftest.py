import sys
from pathlib import Path

# Permite que los tests en tests/ hagan "from config import UartConfig", etc.,
# sin importar desde donde se ejecute pytest.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

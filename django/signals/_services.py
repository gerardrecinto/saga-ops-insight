from typing import Optional

# DIP: populated by SignalsConfig.ready() — views import from here, never from adapters
ingestion: Optional[object] = None
risk: Optional[object] = None

from ambra_sdk.service.entrypoints.generated.audit import \
    AsyncAudit as GAsyncAudit
from ambra_sdk.service.entrypoints.generated.audit import Audit as GAudit


class Audit(GAudit):
    """Audit."""


class AsyncAudit(GAsyncAudit):
    """AsyncAudit."""

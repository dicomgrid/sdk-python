from ambra_sdk.service.entrypoints.generated.appointment import \
    Appointment as GAppointment
from ambra_sdk.service.entrypoints.generated.appointment import \
    AsyncAppointment as GAsyncAppointment


class Appointment(GAppointment):
    """Appointment."""


class AsyncAppointment(GAsyncAppointment):
    """AsyncAppointment."""

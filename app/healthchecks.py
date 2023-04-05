from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class HealthCheckStatus:
    name: str
    is_healthy: bool


@dataclass
class HealthSummary:
    health_checks: List[HealthCheckStatus]
    is_healthy: bool = True


class HealthCheck:
    def is_healthy(self) -> HealthCheckStatus:
        pass


class HealthCheckService:
    def __init__(self, health_checks: Iterable[HealthCheck]):
        assert isinstance(health_checks, object)
        self.health_checks = health_checks

    def get_health(self) -> HealthSummary:
        is_healthy = True
        health_checks = list()
        for health_check in self.health_checks:
            current_status = health_check.is_healthy()
            is_healthy = is_healthy and current_status.is_healthy
            health_checks.append(current_status)
        return HealthSummary(is_healthy=is_healthy, health_checks=health_checks)
        
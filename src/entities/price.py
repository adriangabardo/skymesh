from __future__ import annotations

import msgspec


class Price(msgspec.Struct, frozen=True):
    amount: float
    currency: str

    breakdown_base: float
    breakdown_distance: float
    breakdown_layover: float

    def __str__(self) -> str:
        return (
            f"{self.currency} {self.amount:,.2f} "
            f"(Base: {self.breakdown_base:.2f}, "
            f"Distance: {self.breakdown_distance:.2f}, "
            f"Layover: {self.breakdown_layover:.2f})"
        )

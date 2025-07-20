from dataclasses import field
from ninja import ModelSchema, Schema
from devices.models import Device, Location


class LocationSchema(ModelSchema):
    class Meta:
        model = Location
        fields = ("id", "name")


class DeviceSchema(ModelSchema):
    # Optional field for nested schema
    location: LocationSchema | None = None

    class Meta:
        model = Device
        fields = ("id", "name", "slug", "location")


class DeviceCreateSchema(Schema):
    name: str
    location_id: int | None = None


class ErrorSchema(Schema):
    message: str


class DeviceLocationPatch(Schema):
    """
    Schema for patching a device's location.
    """

    location_id: int | None = None

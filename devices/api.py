from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from devices.models import Device, Location
from devices.schemas import (
    DeviceLocationPatch,
    DeviceSchema,
    LocationSchema,
    DeviceCreateSchema,
    ErrorSchema,
)


app = NinjaAPI()


@app.get("devices/", response=list[DeviceSchema])
def get_devices(request):
    """
    Retrieve a list of all devices.
    """
    return Device.objects.all()


@app.get("devices/{slug}", response=DeviceSchema)
def get_device(request, slug: str):
    """
    Retrieve a single device by its slug.
    """
    device = get_object_or_404(Device, slug=slug)
    return device


@app.post("devices/", response={200: DeviceSchema, 404: ErrorSchema})
def create_device(request, device: DeviceCreateSchema):
    """
    Create a new device.
    """
    if device.location_id:
        # this returns a boolean indicating if the location exists
        location_exists = Location.objects.filter(id=device.location_id).exists()
        if not location_exists:
            return 404, {"message": "Location not found"}

    device_data = device.model_dump()
    device_model = Device.objects.create(**device_data)
    return device_model


@app.get("locations/", response=list[LocationSchema])
def get_locations(request):
    """
    Retrieve a list of all locations.
    """
    return Location.objects.all()


@app.post("devices/{device_slug}/set-location/", response=DeviceSchema)
def update_device_location(request, device_slug, location: DeviceLocationPatch):
    """
    Update the location of a device.
    """
    device = get_object_or_404(Device, slug=device_slug)

    if location.location_id:
        location = get_object_or_404(Location, id=location.location_id)
        device.location = location
    else:
        device.location = None

    device.save()

    return device

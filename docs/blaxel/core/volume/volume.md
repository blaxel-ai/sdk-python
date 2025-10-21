Module blaxel.core.volume.volume
================================

Classes
-------

`VolumeCreateConfiguration(name: str | None = None, display_name: str | None = None, size: int | None = None, region: str | None = None)`
:   Simplified configuration for creating volumes with default values.

    ### Static methods

    `from_dict(data: Dict[str, <built-in function any>]) ‑> blaxel.core.volume.volume.VolumeCreateConfiguration`
    :

`VolumeInstance(volume: blaxel.core.client.models.volume.Volume)`
:   

    ### Static methods

    `create(config: blaxel.core.volume.volume.VolumeCreateConfiguration | blaxel.core.client.models.volume.Volume | Dict[str, <built-in function any>]) ‑> blaxel.core.volume.volume.VolumeInstance`
    :

    `create_if_not_exists(config: blaxel.core.volume.volume.VolumeCreateConfiguration | blaxel.core.client.models.volume.Volume | Dict[str, <built-in function any>]) ‑> blaxel.core.volume.volume.VolumeInstance`
    :   Create a volume if it doesn't exist, otherwise return existing.

    `delete(volume_name: str) ‑> blaxel.core.client.models.volume.Volume`
    :

    `get(volume_name: str) ‑> blaxel.core.volume.volume.VolumeInstance`
    :

    `list() ‑> list[blaxel.core.volume.volume.VolumeInstance]`
    :

    ### Instance variables

    `display_name`
    :

    `metadata`
    :

    `name`
    :

    `region`
    :

    `size`
    :

    `spec`
    :

    `status`
    :
Module blaxel.core.sandbox.preview
==================================

Functions
---------

`to_utc_z(dt: datetime.datetime) ‑> str`
:   

Classes
-------

`SandboxPreview(preview: blaxel.core.client.models.preview.Preview)`
:   Represents a sandbox preview with its metadata and tokens.

    ### Instance variables

    `metadata: dict | None`
    :

    `name: str`
    :

    `spec: blaxel.core.client.models.preview_spec.PreviewSpec | None`
    :

`SandboxPreviewToken(preview_token: blaxel.core.client.models.preview_token.PreviewToken)`
:   Represents a preview token with its value and expiration.

    ### Instance variables

    `expires_at: datetime.datetime`
    :

    `preview_token: blaxel.core.client.models.preview_token.PreviewToken`
    :

    `value: str`
    :

`SandboxPreviewTokens(preview: blaxel.core.client.models.preview.Preview)`
:   Manages preview tokens for a sandbox preview.

    ### Instance variables

    `preview_name: str`
    :

    `resource_name: str`
    :

    ### Methods

    `create(self, expires_at: datetime.datetime) ‑> blaxel.core.sandbox.preview.SandboxPreviewToken`
    :   Create a new preview token.

    `delete(self, token_name: str) ‑> dict`
    :   Delete a preview token.

    `list(self) ‑> List[blaxel.core.sandbox.preview.SandboxPreviewToken]`
    :   List all preview tokens.

`SandboxPreviews(sandbox: blaxel.core.client.models.sandbox.Sandbox)`
:   Manages sandbox previews.

    ### Instance variables

    `sandbox_name: str`
    :

    ### Methods

    `create(self, preview: blaxel.core.client.models.preview.Preview) ‑> blaxel.core.sandbox.preview.SandboxPreview`
    :   Create a new preview.

    `delete(self, preview_name: str) ‑> dict`
    :   Delete a preview.

    `get(self, preview_name: str) ‑> blaxel.core.sandbox.preview.SandboxPreview`
    :   Get a specific preview by name.

    `list(self) ‑> List[blaxel.core.sandbox.preview.SandboxPreview]`
    :   List all previews for the sandbox.
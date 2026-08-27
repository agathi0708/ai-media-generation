from pydantic import BaseModel, Field, model_validator


class Scene(BaseModel):

    scene_id: int = Field(..., ge=1)

    narration: str = Field(
        ...,
        min_length=1,
    )

    visual_prompt: str | None = Field(
        default=None,
        min_length=1,
    )

    visual_prompts: list[str] | None = Field(
        default=None,
        min_length=1,
    )

    @model_validator(mode="after")
    def validate_visual_prompts(self):

        if not self.visual_prompt and not self.visual_prompts:
            raise ValueError(
                "Either visual_prompt or visual_prompts is required."
            )

        if self.visual_prompts:

            self.visual_prompts = [
                prompt.strip()
                for prompt in self.visual_prompts
                if prompt and prompt.strip()
            ]

            if not self.visual_prompts:
                raise ValueError(
                    "visual_prompts cannot be empty."
                )

        if self.visual_prompt:
            self.visual_prompt = self.visual_prompt.strip()

        return self


class SceneGenerateRequest(BaseModel):

    scene_id: int = Field(..., ge=1)

    narration: str = Field(
        ...,
        min_length=1,
    )

    visual_prompt: str | None = Field(
        default=None,
        min_length=1,
    )

    visual_prompts: list[str] | None = Field(
        default=None,
        min_length=1,
    )

    voice: str | None = None

    @model_validator(mode="after")
    def validate_visual_prompts(self):

        if not self.visual_prompt and not self.visual_prompts:
            raise ValueError(
                "Either visual_prompt or visual_prompts is required."
            )

        if self.visual_prompts:

            self.visual_prompts = [
                prompt.strip()
                for prompt in self.visual_prompts
                if prompt and prompt.strip()
            ]

            if not self.visual_prompts:
                raise ValueError(
                    "visual_prompts cannot be empty."
                )

        if self.visual_prompt:
            self.visual_prompt = self.visual_prompt.strip()

        return self


class SceneGenerateResponse(BaseModel):

    scene_id: int

    audio_path: str

    video_path: str | None

    audio_url: str

    video_url: str | None

    image_paths: list[str] = Field(
        default_factory=list
    )

    image_urls: list[str] = Field(
        default_factory=list
    )


class MultiSceneGenerateRequest(BaseModel):

    scenes: list[SceneGenerateRequest] = Field(
        ...,
        min_length=1,
    )


class MultiSceneGenerateResponse(BaseModel):

    scenes: list[SceneGenerateResponse]
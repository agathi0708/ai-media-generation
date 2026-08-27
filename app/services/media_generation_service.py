from app.providers.image.provider import ImageProvider
from app.providers.tts.provider import TTSProvider
from app.providers.video.provider import VideoProvider

from app.schemas.scene import Scene
from app.storage.local_storage import LocalMediaStorage


class MediaGenerationError(Exception):
    """Raised when media generation fails."""


class MediaGenerationService:

    def __init__(
        self,
        tts_provider: TTSProvider,
        image_provider: ImageProvider,
        video_provider: VideoProvider,
        storage: LocalMediaStorage,
    ):
        self.tts_provider = tts_provider
        self.image_provider = image_provider
        self.video_provider = video_provider
        self.storage = storage

    # -----------------------------------
    # Generate narration audio
    # -----------------------------------

    def generate_audio(
        self,
        project_id: str,
        scene: Scene,
        voice_id: str,
    ) -> str:

        try:

            audio = self.tts_provider.generate_speech(
                text=scene.narration,
                voice_id=voice_id,
            )

            audio_path = self.storage.save_audio(
                audio=audio,
                filename=(
                    f"{project_id}_scene_"
                    f"{scene.scene_id}.mp3"
                ),
            )

            return audio_path

        except Exception as exc:

            raise MediaGenerationError(
                f"Audio generation failed "
                f"for scene {scene.scene_id}."
            ) from exc

    # -----------------------------------
    # Generate one image
    # -----------------------------------

    def generate_single_image(
        self,
        project_id: str,
        scene: Scene,
        prompt: str,
        image_number: int = 1,
    ) -> str:

        try:

            if not prompt or not prompt.strip():

                raise ValueError(
                    "Image prompt cannot be empty."
                )

            image = self.image_provider.generate_image(
                prompt=prompt,
            )

            # -----------------------------------
            # File name
            # -----------------------------------

            if image_number == 1:

                filename = (
                    f"{project_id}_scene_"
                    f"{scene.scene_id}.png"
                )

            else:

                filename = (
                    f"{project_id}_scene_"
                    f"{scene.scene_id}_image_"
                    f"{image_number}.png"
                )

            # -----------------------------------
            # Save image
            # -----------------------------------

            image_path = self.storage.save_image(
                image=image,
                filename=filename,
            )

            return image_path

        except Exception as exc:

            raise MediaGenerationError(
                f"Image generation failed "
                f"for scene {scene.scene_id}, "
                f"image {image_number}."
            ) from exc

    # -----------------------------------
    # Generate all images
    # -----------------------------------

    def generate_images(
        self,
        project_id: str,
        scene: Scene,
    ) -> list[str]:

        try:

            # -----------------------------------
            # Multiple images
            # -----------------------------------

            if scene.visual_prompts:

                image_paths = []

                for index, prompt in enumerate(
                    scene.visual_prompts,
                    start=1,
                ):

                    image_path = (
                        self.generate_single_image(
                            project_id=project_id,
                            scene=scene,
                            prompt=prompt,
                            image_number=index,
                        )
                    )

                    image_paths.append(
                        image_path
                    )

                return image_paths

            # -----------------------------------
            # Single image
            # -----------------------------------

            if scene.visual_prompt:

                image_path = (
                    self.generate_single_image(
                        project_id=project_id,
                        scene=scene,
                        prompt=scene.visual_prompt,
                        image_number=1,
                    )
                )

                return [
                    image_path
                ]

            raise ValueError(
                "Either visual_prompt or "
                "visual_prompts is required."
            )

        except MediaGenerationError:
            raise

        except Exception as exc:

            raise MediaGenerationError(
                f"Image generation failed "
                f"for scene {scene.scene_id}."
            ) from exc

    # -----------------------------------
    # Generate video
    # -----------------------------------

    def generate_video(
        self,
        project_id: str,
        scene: Scene,
        image_paths: list[str],
        audio_path: str | None = None,
        duration: int = 5,
    ) -> str:

        try:

            # -----------------------------------
            # Validate images
            # -----------------------------------

            if not image_paths:

                raise ValueError(
                    "At least one image is required "
                    "to generate video."
                )

            # -----------------------------------
            # Select video prompt
            # -----------------------------------

            prompt = ""

            if scene.visual_prompt:

                prompt = scene.visual_prompt

            elif scene.visual_prompts:

                prompt = scene.visual_prompts[0]

            # -----------------------------------
            # Generate video
            # -----------------------------------

            video = self.video_provider.generate_video(

                prompt=prompt,

                # First image for backward compatibility
                image_url=image_paths[0],

                # All images
                image_paths=image_paths,

                # Narration audio
                audio_url=audio_path,

                duration=duration,
            )

            # -----------------------------------
            # Save video
            # -----------------------------------

            video_path = self.storage.save_video(
                video=video,
                filename=(
                    f"{project_id}_scene_"
                    f"{scene.scene_id}.mp4"
                ),
            )

            return video_path

        except Exception as exc:

            raise MediaGenerationError(
                f"Video generation failed "
                f"for scene {scene.scene_id}."
            ) from exc

    # -----------------------------------
    # Generate complete scene media
    # -----------------------------------

    def generate_scene_media(
        self,
        project_id: str,
        scene: Scene,
        voice_id: str,
        image_path: str | None = None,
        generate_video: bool = True,
        duration: int = 5,
    ) -> dict:

        try:

            # -----------------------------------
            # 1. Generate audio
            # -----------------------------------

            audio_path = self.generate_audio(
                project_id=project_id,
                scene=scene,
                voice_id=voice_id,
            )

            # -----------------------------------
            # 2. Generate images
            # -----------------------------------

            if image_path:

                # Existing/specified single image
                image_paths = [
                    image_path
                ]

            else:

                # Generate one or multiple images
                image_paths = (
                    self.generate_images(
                        project_id=project_id,
                        scene=scene,
                    )
                )

            # -----------------------------------
            # Validate images
            # -----------------------------------

            if not image_paths:

                raise MediaGenerationError(
                    f"No images generated "
                    f"for scene {scene.scene_id}."
                )

            # -----------------------------------
            # 3. Generate video
            # -----------------------------------

            video_path = None

            if generate_video:

                video_path = self.generate_video(
                    project_id=project_id,
                    scene=scene,

                    # IMPORTANT:
                    # Pass ALL images
                    image_paths=image_paths,

                    audio_path=audio_path,
                    duration=duration,
                )

            # -----------------------------------
            # 4. Return generated assets
            # -----------------------------------

            return {
                "scene_id": scene.scene_id,

                "audio_path": audio_path,

                "image_paths": image_paths,

                "video_path": video_path,
            }

        except MediaGenerationError:
            raise

        except Exception as exc:

            raise MediaGenerationError(
                f"Media generation failed "
                f"for scene {scene.scene_id}."
            ) from exc
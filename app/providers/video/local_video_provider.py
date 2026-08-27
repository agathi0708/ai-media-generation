import subprocess
import tempfile
from pathlib import Path

import imageio_ffmpeg

from app.providers.video.provider import VideoProvider


class LocalVideoProvider(VideoProvider):

    def __init__(self):
        self.ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    # -----------------------------------
    # Get audio duration
    # -----------------------------------

    def _get_audio_duration(
        self,
        audio_path: Path,
    ) -> float:

        command = [
            self.ffmpeg,
            "-i",
            str(audio_path),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        output = result.stderr

        for line in output.splitlines():

            if "Duration:" not in line:
                continue

            duration_text = (
                line.split("Duration:")[1]
                .split(",")[0]
                .strip()
            )

            hours, minutes, seconds = (
                duration_text.split(":")
            )

            return (
                int(hours) * 3600
                + int(minutes) * 60
                + float(seconds)
            )

        raise RuntimeError(
            "Could not determine audio duration."
        )

    # -----------------------------------
    # Generate video
    # -----------------------------------

    def generate_video(
        self,
        prompt: str,
        image_url: str | None = None,
        audio_url: str | None = None,
        duration: int = 5,
        image_paths: list[str] | None = None,
    ) -> bytes:

        # -----------------------------------
        # Build image list
        # -----------------------------------

        images = []

        # New multi-image support
        if image_paths:

            images = [
                Path(path)
                for path in image_paths
                if path
            ]

        # Backward compatibility
        elif image_url:

            images = [
                Path(image_url)
            ]

        else:

            raise ValueError(
                "At least one image path is required."
            )

        # -----------------------------------
        # Validate images
        # -----------------------------------

        if not images:

            raise ValueError(
                "At least one image path is required."
            )

        for image_path in images:

            if not image_path.exists():

                raise FileNotFoundError(
                    f"Image file not found: "
                    f"{image_path}"
                )

        # -----------------------------------
        # Check audio
        # -----------------------------------

        if audio_url:

            audio_path = Path(audio_url)

            if not audio_path.exists():

                raise FileNotFoundError(
                    f"Audio file not found: "
                    f"{audio_path}"
                )

            actual_duration = (
                self._get_audio_duration(
                    audio_path
                )
            )

            if actual_duration <= 0:

                raise RuntimeError(
                    "Audio duration is invalid."
                )

        else:

            audio_path = None
            actual_duration = float(duration)

        # -----------------------------------
        # Calculate duration per image
        # -----------------------------------

        image_count = len(images)

        duration_per_image = (
            actual_duration / image_count
        )

        # -----------------------------------
        # Temporary working directory
        # -----------------------------------

        with tempfile.TemporaryDirectory() as temp_dir:

            temp_directory = Path(temp_dir)

            output_path = (
                temp_directory
                / "generated_video.mp4"
            )

            # -----------------------------------
            # Build FFmpeg command
            # -----------------------------------

            command = [
                self.ffmpeg,
                "-y",
            ]

            # -----------------------------------
            # Add every image as an input
            # -----------------------------------

            for image_path in images:

                command.extend(
                    [
                        "-loop",
                        "1",
                        "-t",
                        str(duration_per_image),
                        "-i",
                        str(image_path),
                    ]
                )

            # -----------------------------------
            # Add audio
            # -----------------------------------

            if audio_path:

                command.extend(
                    [
                        "-i",
                        str(audio_path),
                    ]
                )

            # -----------------------------------
            # Build filter for every image
            # -----------------------------------

            filters = []

            for index in range(image_count):

                filter_part = (
                    f"[{index}:v]"
                    "scale=1920:1080:"
                    "force_original_aspect_ratio=decrease,"
                    "pad=1920:1080:"
                    "(ow-iw)/2:"
                    "(oh-ih)/2,"
                    "setsar=1,"
                    "fps=24,"
                    f"trim=duration={duration_per_image},"
                    "setpts=PTS-STARTPTS"
                    f"[v{index}]"
                )

                filters.append(
                    filter_part
                )

            # -----------------------------------
            # Concatenate images
            # -----------------------------------

            concat_inputs = "".join(
                f"[v{index}]"
                for index in range(image_count)
            )

            concat_filter = (
                concat_inputs
                + f"concat=n={image_count}:"
                "v=1:"
                "a=0,"
                "format=yuv420p"
                "[video]"
            )

            filters.append(
                concat_filter
            )

            filter_complex = ";".join(
                filters
            )

            command.extend(
                [
                    "-filter_complex",
                    filter_complex,

                    "-map",
                    "[video]",
                ]
            )

            # -----------------------------------
            # Map audio
            # -----------------------------------

            if audio_path:

                audio_input_index = image_count

                command.extend(
                    [
                        "-map",
                        f"{audio_input_index}:a:0",

                        "-c:a",
                        "aac",

                        "-b:a",
                        "128k",

                        "-ar",
                        "44100",

                        "-ac",
                        "2",

                        "-shortest",
                    ]
                )

            # -----------------------------------
            # Video settings
            # -----------------------------------

            command.extend(
                [
                    "-c:v",
                    "libx264",

                    "-preset",
                    "medium",

                    "-crf",
                    "23",

                    "-pix_fmt",
                    "yuv420p",

                    "-movflags",
                    "+faststart",
                ]
            )

            # -----------------------------------
            # Output
            # -----------------------------------

            command.append(
                str(output_path)
            )

            # -----------------------------------
            # Run FFmpeg
            # -----------------------------------

            try:

                result = subprocess.run(
                    command,
                    check=True,
                    capture_output=True,
                    text=True,
                )

            except subprocess.CalledProcessError as exc:

                raise RuntimeError(
                    "FFmpeg failed to generate "
                    "the local video:\n"
                    f"{exc.stderr}"
                ) from exc

            # -----------------------------------
            # Validate output
            # -----------------------------------

            if not output_path.exists():

                raise RuntimeError(
                    "FFmpeg completed but the "
                    "video file was not created."
                )

            video_bytes = (
                output_path.read_bytes()
            )

            if not video_bytes:

                raise RuntimeError(
                    "Generated video is empty."
                )

            return video_bytes
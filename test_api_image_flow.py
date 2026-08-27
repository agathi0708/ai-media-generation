from app.providers.image.huggingface_provider import HuggingFaceImageProvider
from app.schemas.scene import Scene


def main():
    scene = Scene(
        scene_id=1,
        narration="A modern electric car travels through a busy city.",
        visual_prompt=(
            "A realistic cinematic electric car driving through "
            "a modern city street during sunset, pedestrians and "
            "buildings in the background, natural lighting, "
            "professional documentary style."
        ),
    )

    print("Testing Hugging Face image generation...")
    print("Creating provider...")

    provider = HuggingFaceImageProvider()

    print("Generating image...")
    print("Please wait...")

    image = provider.generate_image(
        prompt=scene.visual_prompt
    )

    print("Image generated successfully.")
    print("Image size:", len(image), "bytes")


if __name__ == "__main__":
    main()

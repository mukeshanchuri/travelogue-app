import replicate
import os

# Initialize client (not strictly necessary unless you want to override defaults)
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
replicate.Client(api_token=REPLICATE_API_TOKEN)

def generate_image(prompt: str) -> str:
    output = replicate.run(
        "stability-ai/stable-diffusion:1d152d7b0e38a2c3f94be2ff98f902892f2059379a8a50a2c54c86eab94772b3",
        input={
            "prompt": prompt,
            "width": 512,
            "height": 512,
            "num_outputs": 1
        }
    )
    return output[0]  # This will be the image URL

import replicate
import os

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
replicate.Client(api_token=REPLICATE_API_TOKEN)

def generate_image(prompt: str) -> str:
    output = replicate.run(
        "stability-ai/stable-diffusion:db21e45b76aa1ec295e0d9cb8b1d69ea8cbdcf5757dd2f94cc178b962e172f1c",
        input={
            "prompt": prompt,
            "width": 512,
            "height": 512
        }
    )
    return output[0]

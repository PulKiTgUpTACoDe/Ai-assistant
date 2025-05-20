import requests
import os
from dotenv import load_dotenv

load_dotenv()

def generate_image(
    prompt: str,
    name: str,
    output_format: str = "jpeg",
    negative_prompt: str = None,
    aspect_ratio: str = None,
    mode: str = "text-to-image",
    seed: int = None,
    strength: float = None,
    image: str = None,
    **kwargs
) -> str:
    
    data = {
        "prompt": prompt,
        "output_format": output_format,
        "image-name": name,
        "mode": mode,
    }
    if negative_prompt:
        data["negative_prompt"] = negative_prompt
    if aspect_ratio:
        data["aspect_ratio"] = aspect_ratio
    if seed is not None:
        data["seed"] = seed
    if strength is not None:
        data["strength"] = strength
    if image:
        data["image"] = image
    data.update(kwargs)

    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/sd3",
        headers={
            "authorization": f"Bearer {os.getenv('STABILITY_API_KEY')}",
            "accept": "image/*"
        },
        files={"none": ''},
        data=data,
    )

    if response.status_code == 200:
        filename = f"./ai-agent/public/{name}.{output_format}"
        with open(filename, 'wb') as file:
            file.write(response.content)
        return filename
    else:
        raise Exception(str(response.json()))


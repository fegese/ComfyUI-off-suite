import torch
import re
import random

class GWNumFormatter:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_number": ("INT", {
                    "default": 0,
                    "min": 0,  # Minimum value
                    "max": 100000000,  # Maximum value
                }),
                "width": ("INT", {
                    "default": 3,
                    "min": 0,
                    "max": 10,
                })
            },
        }

    RETURN_TYPES = ("STRING",)
    # RETURN_NAMES = ("image_output_name",)

    FUNCTION = "format"

    CATEGORY = "GW"

    def format(self, input_number, width):
        return (f"%0{width}d" % (input_number),)

def tensorToNP(image):
    out = torch.clamp(255. * image.detach().cpu(), 0, 255).to(torch.uint8)
    out = out[..., [2, 1, 0]]
    out = out.numpy()

    return out

class QueryGenderAge:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("INSIGHTFACE",),
                "image": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("STRING", "NUMBER",)
    # RETURN_NAMES = ("image_output_name",)

    FUNCTION = "execute"

    CATEGORY = "OFF"

    def execute(self, model, image):
        faces = model.get(tensorToNP(image[0]))

        # Check if any face is detected
        if faces:
            print(faces[0].sex, faces[0].age)
            return (faces[0].sex, faces[0].age,)
        else:
            print("No face detected.")
            return ("Unknown", -1,)  # Return default values if no face is detected

class RandomSeedFromList:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "seed_string": ("STRING", {}),
            }
        }

    RETURN_TYPES = ("INT",)

    FUNCTION = "execute"

    CATEGORY = "OFF"

    def IS_CHANGED(s, *args, **kwargs):
        return torch.rand(1).item()

    def execute(self, seed_string):
        tokens = seed_string.split(',')
        seeds = [int(item) for item in tokens]

        seed = random.choice(seeds)

        return (seed,)

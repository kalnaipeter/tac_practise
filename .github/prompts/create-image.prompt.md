---
description: "Generate images via an image generation API. Example of a control flow prompt with STOP guards and loops."
---

# Create Image

Generates image(s) based on the provided prompt using an image generation API.

## Variables

IMAGE_GENERATION_PROMPT: $1
NUMBER_OF_IMAGES: $2 or 3 if not provided
IMAGE_OUTPUT_DIR: public/generated_images/<date_time>/

## Workflow

- First, check your available tools for image generation capabilities. If none available, STOP immediately and inform the user.
- Then check if `IMAGE_GENERATION_PROMPT` is provided. If not, STOP immediately and ask the user to provide it.
- Take note of `IMAGE_GENERATION_PROMPT` and `NUMBER_OF_IMAGES`.
- Create output directory: `IMAGE_OUTPUT_DIR`
- IMPORTANT: Then generate `NUMBER_OF_IMAGES` images using the `IMAGE_GENERATION_PROMPT` following the `image-loop` below.

<image-loop>
  - Call the image generation API with the prompt
  - Wait for completion
  - Save the prompt text to `IMAGE_OUTPUT_DIR/prompt_<concise_name>.txt`
  - Download the image to `IMAGE_OUTPUT_DIR/<concise_name>.jpg`
</image-loop>

## Report

- Report the total number of images generated
- Report the full path to the output directory

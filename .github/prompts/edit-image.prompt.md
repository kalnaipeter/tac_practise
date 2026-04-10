---
description: "Edit existing images via an image editing API. Example of a control flow prompt with prerequisite checks and loops."
---

# Edit Image

Edits existing images based on provided edit prompts using an image editing API.

## Variables

DROPPED_FILE_PATH: $1
IMAGE_OUTPUT_DIR: public/edited_images/<date_time>/

## Workflow

- Check these prerequisites and STOP immediately if you don't have them:
  - Image editing API/tool must be available
  - `DROPPED_FILE_PATH` must be provided. If not, STOP and ask the user.
- Read `DROPPED_FILE_PATH` to get the list of edit instructions.
- Create output directory: `IMAGE_OUTPUT_DIR`
- IMPORTANT: For every image edit detailed in the `DROPPED_FILE_PATH` do the following:

<image-loop>
  - Extract the source image path and edit prompt from the file
  - Call the image editing API with the source image and edit prompt
  - Wait for completion
  - Save the edit prompt to `IMAGE_OUTPUT_DIR/edit_prompt_<concise_name>.txt`
  - Download the edited image to `IMAGE_OUTPUT_DIR/edited_<concise_name>.jpg`
</image-loop>

- After all edits are complete, open the output directory.

## Report

- Report the total number of images edited
- List source → output for each edit
- Report the full path to the output directory

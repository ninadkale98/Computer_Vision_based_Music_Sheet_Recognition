### Folder Structur ###

Directories are included in code relative to folder in which run.sh file is stored. No changes needed to do in code

music_sheet -> includes pdf of music sheet. I have included music sheet of song Twinkle Twinkle Litte Star

images -> Inlcude converted music sheet from pdf to png

temp -> includes images of bars, which are used to detect notes

function.py file includes all functions used in main.py

### Code running instruction ###

## Important variables
1. convert_sheet_to_image -> has to be enabled if pdf has to be converted to image

Default set to False as pdf has already been converted to images

2. extract_bar_images -> has to be enabled to extract bar images from entire image

Default set to False as bar image has already been calculated

3. play_notes -> If you want to play notes.

Default set to True

### How to run code

1. Download all libraries by installing all libraries in requirement.txt first

2. Execute run.sh file, Make sure volume is not muted. You should hear notes playing twinkle twinkle litte star
from functions import convert_pdf_to_images, extract_bars, detect_notes
import musicalbeeps


####### Convert Music PDF Sheet into image files ######
convert_sheet_to_image = False

if(convert_sheet_to_image):
    convert_pdf_to_images()

### Extract Bar images
extract_bar_images = False

if(extract_bar_images):
    extract_bars()

### Detect Notes
notes = detect_notes()

## Play Notes
play_notes = True
if(play_notes):
    player = musicalbeeps.Player(volume = 0.8,mute_output = False)
    for elem in notes:
        if(elem[1] == "f"):
            player.play_note(elem[0], 1)
        else:
            player.play_note(elem[0], 0.5)

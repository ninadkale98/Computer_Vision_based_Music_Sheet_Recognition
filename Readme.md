## Optical Music Sheet Recognition
This GitHub repository provides code for processing the music sheet of the song "Twinkle Twinkle Little Star." The code converts the sheet music from PDF format to images, extracts individual bars from the sheet, and can play the notes. This code can be scaled up to work on any generic music sheet. 

# Folder Structure
The repository's folder structure is designed to be self-contained. The music_sheet directory includes the PDF file containing the music sheet for "Twinkle Twinkle Little Star." The images directory contains the converted music sheet in PNG format. The temp directory includes images of bars used for note detection. The function.py file contains all the necessary functions used in the main code.

# Code Running Instructions
To run the code successfully, please pay attention to the following important variables:

- convert_sheet_to_image: This variable determines whether the PDF needs to be converted to images. By default, it is set to False as the PDF has already been converted.
- extract_bar_images: Enabling this variable allows the extraction of individual bar images from the entire music sheet. By default, it is set to False as the bar images have already been calculated.
- play_notes: If you wish to play the notes, set this variable to True. By default, it is set to True.

# How to Run the Code
To run the code, follow these steps:

- Download all the required libraries by installing them from the requirements.txt file.
- Execute the run.sh file. Make sure the volume is not muted, as you should hear the notes playing "Twinkle Twinkle Little Star."

# Contribution
- Contributions to this project are welcome! If you encounter any issues, have suggestions for improvements, or want to add new features, please feel free to open an issue or submit a pull request.
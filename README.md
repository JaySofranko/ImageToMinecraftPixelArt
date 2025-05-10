# ImageToMinecraftPixelArt
A local application that consists of a frontend and backend that takes a user's image, maps each pixel in the image to the appropriate minecraft block using euclidean geometry and average rgb values. The output image file is saved to the output folder.

## HOW TO INSTALL

git clone https://www.github.com/JaySofranko/ImageToMinecraftPixelArt.git

Open the folder, and run app.py

Once app.py is running, navigate to a web browser and type in the search bar: "127.0.0.1:5000" and press enter.

You should see this screen:
![GitHub_ImageToMinecraftPixelArt](https://github.com/user-attachments/assets/ddfcfdb4-7be5-4f0d-95d6-9dc7781c7e32)

Click "Browse" and select the image you would like to convert.

Once the image has been displayed on the frontend, use the size and quality sliders to determine the images dimensions and compression rate.
### ( A higher quality number means more compression and lower quality. A higher size number means a larger image. )

Once complete, press the upload button. You may wait upwards of 5-7 minutes depending on the quality and size options. These options were implemented to help save computer resources, as this can be a very cpu intensive task.

You will notice that the conversion is complete when a chart displays on the front-end. This chart shows how many blocks are needed to complete the build.

The output image that you will use for the build is saved in the output folder of this repository. 

# TROUBLESHOOTING

Make sure that before you use the program, you install the most recent version of Python.

You must also install the necessary packages.

You can do this by navigating to the repository directory in the terminal/command prompt:

cd path/to/your/project (Whatever you saved it as) Default: 

Then, install the dependencies using requirements.txt:

pip install -r requirements.txt


# Welcome to face_effect!

I've always thought instagram/tiktok blur face effect is very aesthetic. I decided to create it myself, and the end result is in this repo, and you can use it yourself!

# How to use it?

First you need to clone and install the project.
```shell
git clone https://github.com/mtxslv/face_effect
cd face_effect
poetry install .
```
Cast a shell to access the dependencies

```shell
poetry shell
```

Once this is done, you can interact with the effect via CLI. There are two main ways of doing so:
- Webcam (real-time processing)
- Image folder (batch processing)

The simplest CLI call opens your webcam and lets you see the full effect: blur + greyscale. To do so, just run:

```shell
python face_effect/cli.py
```

If you wanna see the effect in normal colors, just turn off the greyscale:

```shell
python face_effect/cli.py --e none
```

Now let's apply it on an image batch. 
```shell
python face_effect/cli.py --s path
```
The terminal will ask you to input a valid full path. Once you do so, it asks an output path (another folder) to save the process images. If you want to save the images in the same place, just type a dot.

# Limitations

The way the code is structured, it supposes only one person is visible. Tests with more than just one person were not performed.

The deep learning model employed has its own limitations. To know about them, refer to its [Model Card here](https://drive.google.com/file/d/1d4-xJP9PVzOvMBDgIjz6NhvpnlG9_i0S/preview). 


# References

## Code
Face Detections based on [this example](https://github.com/google/mediapipe/blob/master/docs/solutions/face_detection.md).

## Test images

- [Billie Eilish](https://i.dailymail.co.uk/1s/2021/10/11/11/49019335-10079753-image-a-90_1633948283081.jpg) (from [DailyMail](https://www.dailymail.co.uk/tvshowbiz/article-10079753/Billie-Eilish-sees-streams-No-Time-Die-theme-song-PLUMMET.html))
- [The Weekend](https://www.rollingstone.com/wp-content/uploads/2020/02/TheWeeknd.jpg?w=1581&h=1054&crop=1) (from [Rolling Stones](https://www.rollingstone.com/music/music-news/rs-charts-top-100-the-weeknd-blinding-lights-980295/)).
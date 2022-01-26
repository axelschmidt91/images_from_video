import cv2
import logging
import os


def extraction(vidFile, numImages, outFolder):

    cap = cv2.VideoCapture(vidFile)

    """ get total frame count and saving interval for images"""
    # framesPerSecond= int(cap.get(cv2.CAP_PROP_FPS))
    frameCount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    savingInterval = int(frameCount / numImages)
    logging.info(f"Saving interval is {savingInterval} frames")

    success, image = cap.read()
    count = 0

    while success:
        if not count % savingInterval:
            imageName = f"frame{count:06}.jpg"
            logging.info(f"Write image {imageName}")
            cv2.imwrite(os.path.join(outFolder, imageName), image)     # save frame as JPEG file      
        success, image = cap.read()
        logging.debug('Read a new frame: ', success)
        count += 1


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file",
        nargs="+",
        help="folder to search for files")
    parser.add_argument(
        "-nI",
        type=int,
        nargs="?",
        default=30,
        dest="numImages",
        help="Number of images the video should be subdivided into. Default=30.",
    )
    parser.add_argument(
        "-del",
        action="store_const",
        const=True,
        default=False,
        dest="deletImages",
        help="Delete previous images for selected video files before extract new ones. Useful if number of images has changed for the particular videos. Default=False",
    )

    levels = {
        'critical': logging.CRITICAL,
        'error': logging.ERROR,
        'warning': logging.WARNING,
        'info': logging.INFO,
        'debug': logging.DEBUG
    }
    parser.add_argument(
        '--log',
        choices=levels.keys(),
        default="info",
        dest="log",
        help=("Provide logging level. Default='info'.")
    )

    args = parser.parse_args()
    files = args.file
    numImages = args.numImages
    deletImages = args.deletImages

    # Set up logging
    if not os.path.isdir('log'):
        os.mkdir('log')

    logging.basicConfig(
        level=levels[args.log],
        format='%(asctime).19s [%(levelname)s]: %(message)s',
        handlers=[
            logging.FileHandler('log/vid2imgs.log'),
            logging.StreamHandler()])

    logging.info('Start vid2imgs logging')

    for i, file in enumerate(files):

        logging.info(f"progress: {i+1:3} / {len(files)}")

        path, fileName = os.path.split(file)

        imageFolderName = f"images_{fileName.split('.')[0]}"
        imagePath = os.path.join(path, imageFolderName)

        if not os.path.isdir(imagePath):
            logging.info(f"Create Folder for images {imagePath}")
            os.mkdir(imagePath)
        elif deletImages:
            logging.info(f"Delete images in folder {imagePath}")
            for f in os.listdir(imagePath):
                os.remove(os.path.join(imagePath, f))

        logging.info(f"Start extracting {numImages} imges for video {file}")
        extraction(file, numImages, imagePath)

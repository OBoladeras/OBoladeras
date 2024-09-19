import os
from PIL import Image
from PIL.ExifTags import TAGS


def get_categories():
    categories = {}
    for entry in os.scandir("static/gallery"):
        if entry.is_dir():
            categories[entry.name] = get_images(entry.name)

    return categories


def get_images(category: str):
    data = []

    for entry in os.scandir(f"static/gallery/{category}"):
        if entry.is_file():
            tmp = {
                "name": entry.name,
                "path": entry.path,
                "size": os.path.getsize(entry.path),
            }

            image = Image.open(entry)
            exif_data = image._getexif()
            if exif_data:

                exif = {}
                for tag, value in exif_data.items():
                    decoded = TAGS.get(tag, tag)
                    exif[decoded] = value

                tmp["iso"] = exif.get("ISOSpeedRatings")
                tmp["aperture"] = exif.get("FNumber")
                tmp["shutter_speed"] = exif.get("ExposureTime")
            else:
                tmp["iso"] = None
                tmp["aperture"] = None
                tmp["shutter_speed"] = None

            data.append(tmp)

    return data


def set_resolution() -> str:
    max_size = 1920

    for folder in os.scandir("static/gallery"):
        if folder.is_dir():
            for entry in os.scandir(folder.path):
                path = entry.path
                if entry.is_file():

                    img = Image.open(path)
                    original_width, original_height = img.size

                    if original_width > max_size:
                        percent = max_size / float(original_width)
                        new_height = int((float(original_height) * percent))

                        size = (max_size, new_height)
                    elif original_height > max_size:
                        percent = max_size / float(original_height)
                        new_width = int((float(original_width) * percent))
                        size = (new_width, max_size)

                    if original_width > max_size or original_height > max_size:
                        exif_data = img.info.get('exif', None)

                        img = img.resize(size)
                        print(f"Resized to: {size}")

                        if exif_data:
                            img.save(path, exif=exif_data)
                        else:
                            img.save(path)

                        print(f"Saved: {path}")
                    else:
                        print(
                            f"Image {path} is already smaller than the max size.")


if __name__ == "__main__":
    set_resolution()

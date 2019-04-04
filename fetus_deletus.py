import os

def static_clear():
    for root, dirs, files in os.walk("static"):
        for f in files:
            for i in ["JPG", "jpeg", "jpg", "JPEG", "PNG", "png"]:
                if i in f.split("."):
                    try:
                        os.remove(f"static/{f}")
                        print(f"removed {f}")
                    except FileNotFoundError:
                        pass

# st
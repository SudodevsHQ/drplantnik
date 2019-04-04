import os

def static_clear():
    for root, dirs, files in os.walk("static"):
        for f in files:
            for i in ["JPG", "jpeg", "jpg", "JPEG"]:
                if i in f.split("."):
                    os.remove(f"static/{f}")
                    print(f"removed {f}")

# static_clear()
from scrapper import Google
import asyncio
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from keras import backend as K
from keras.models import load_model
from keras.preprocessing import image
from keras import optimizers
import numpy as np
import cv2
from fetus_deletus import static_clear
import matplotlib.pyplot as plt
from chunk import d
# predicting images

OUT_OF_SCOPE = False

def graph(classes, dict):
    top_indices = np.argsort(classes[0])[-3:]
    top_values = classes[0][top_indices][-3:]

    # """UNKNOWN SAMPLE CODE"""
    # print(int(str(clss[np.argmax(clss)]).split("e")))
    # print(str(top_values[2]).split("e"))
    # tlist = top_values.tolist()
    # print(tlist)
    # if int(str(tlist[2]).split("e")[1]) <= -3:
    #     OUT_OF_SCOPE = True

    print(top_indices)
    print(top_values)

    x = np.arange(len(top_indices))
    y = top_values

    plt.bar(x, top_values, width=0.6, alpha=0.5)
    plt.xlabel('Disease')
    plt.xticks(x, [dict[str(i)][1]
                   for i in top_indices], fontsize=10)

    plt.title('Probability')
    # plt.show()
    plt.savefig('static/chart.png')


def classes(filename):
    # dimensions of our images

    img_width, img_height = 256, 256

    # load the model we saved
    model = load_model('model_1D.h5')
    model.load_weights("modelw_1D.h5")
    sgd = optimizers.SGD(lr=0.25, momentum=0.6, decay=0.0, nesterov=False)

    model.compile(loss='mean_squared_error',
                  optimizer=sgd,
                  metrics=['accuracy'])

    img = cv2.imread(f"static/{filename}")

    img = cv2.resize(img, (img_width, img_height))
    x = image.img_to_array(img)
    # """NOISE"""
    # b,g,r = cv2.split(img)           # get b,g,r
    # rgb_img = cv2.merge([r,g,b])     # switch it to rgb
    # dst = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)
    # b,g,r = cv2.split(dst)           # get b,g,r
    # rgb_dst = cv2.merge([r,g,b]) 
    
    # x = image.img_to_array(dst)w
    x = np.expand_dims(x, axis=0)

    images = np.vstack([x])
    classes = model.predict_classes(images, batch_size=10)
    clss = model.predict(images, batch_size=10)
    


# print the classes, the images belong to

    disease_dict = d
    graph(clss, disease_dict)

    K.clear_session()

    return disease_dict[str(classes[0])]


UPLOAD_FOLDER = "static"

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'JPG', 'JPEG'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    static_clear()
    return render_template("index.html")


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        print(file)
        try:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('diagnosed', filename=filename))
            else:
                return render_template("404.html")

        except Exception:
            return render_template("404.html")


    

@app.route('/diagnosed/<filename>')
def diagnosed(filename):
    disease = classes(filename)
    if not OUT_OF_SCOPE:
        try:
            medication = Google().g(disease[0] + " medication")
        except Exception:
            medication = ["Google Failed to", " response", "."]

        # print(medication)
        if disease[1]:
            common = disease[1]
        else:
            common = None
        try:
            med = disease[2]
        except Exception:
            med = None
    else:
        disease = "Unknown"
        medication = "Provided sample is out of the trained dataset scope."
    return render_template("diagnosed.html", name=disease[0], filename=filename, list=medication, common=common, para=med)


if __name__ == '__main__':
    app.run(debug=True)

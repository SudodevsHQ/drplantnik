from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import cv2
# dimensions of our images
img_width, img_height = 256, 256

# load the model we saved
model = load_model('model_keras.h5')
model.load_weights("model_weights.h5")
model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

# predicting images

def classes(filename):
    img = cv2.imread(f"D:/SudoDevsWorkspace/Hackathon/flask_hackathon/static/{filename}")

    img = cv2.resize(img, (img_width, img_height))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    images = np.vstack([x])
    classes = model.predict_classes(images, batch_size=10)
    print(classes)


# print the classes, the images belong to

    

    disease_dict = {
        '0': 'Venturia inaequalis',
        '1': 'Botryosphaeria obtusa',
        '2': 'Gymnosporangium juniperi-virginianae ',
        '3': 'healthy',
        '4': 'healthy',
        '5': 'healthy',
        '6': 'Podoshaera clandestine',
        '7': 'Cercospora zeae-maydis',
        '8': 'Puccinia sorghi',
        '9': 'healthy',
        '10': 'Exserohilum turcicum',
        '11': 'Guignardia bidwellii',
        '12': 'Phaeomoniella aleophilum, Phaeomoniella chlamydospora',
        '13': 'healthy',
        '14': 'Pseudocercospora vitis ',
        '15': 'Candidatus Liberibacter spp',
        '16': 'Xanthomonas campestris',
        '17': 'healthy',
        '18': ' Xanthomonas campestris',
        '19': 'healthy',
        '20': 'Alternaria solani',
        '21': 'healthy',
        '22': 'Phytophthora infestans',
        '23': 'healthy',
        '24': 'healthy',
        '25': 'Erysiphe cichoracearum',
        '26': 'healthy',
        '27': 'Diplocarpon earlianum',
        '28': 'Xanthomonas campestris pv. vesicatoria',
        '29': 'Alternaria solani',
        '30': 'Phytophthora infestans',
        '31': 'Passalora fulva',
        '32': 'Septoria lycopersici',
        '33': 'Tetranychus urticae',
        '34': 'Corynespora cassiicola',
        '35': 'Mosaic Virus',
        '36': 'Yellow Leaf Curl Virus',
        '37': 'healthy'
    }

    return disease_dict[str(classes[0])]


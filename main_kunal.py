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
import fetus_deletus

# predicting images

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
    x = np.expand_dims(x, axis=0)

    images = np.vstack([x])
    classes = model.predict_classes(images, batch_size=10)
    print(classes)


# print the classes, the images belong to

    disease_dict = {
'0': ['Venturia inaequalis', "Apple scab disease","""Choose resistant varieties when possible.
Rake under trees and destroy infected leaves to reduce the number of fungal spores available to start the disease cycle over again next spring.
Water in the evening or early morning hours (avoid overhead irrigation) to give the leaves time to dry out before infection can occur.
Spread a 3- to 6-inch layer of compost under trees, keeping it away from the trunk, to cover soil and prevent splash dispersal of the fungal spores.
For best control, spray liquid copper soap early, two weeks before symptoms normally appear. Alternatively, begin applications when disease first appears, and repeat at 7 to 10 day intervals up to blossom drop.
Bonide® Sulfur Plant Fungicide, a finely ground wettable powder, is used in pre-blossom applications and must go on before rainy or spore discharge periods. Apply from pre-pink through cover (2 Tbsp/ gallon of water), or use in cover sprays up to the day of harvest.
Organocide® Plant Doctor is an earth-friendly systemic fungicide that works its way through the entire plant to combat a large number of diseases on ornamentals, turf, fruit and more. Apply as a soil drench or foliar spray (3-4 tsp/ gallon of water) to prevent and attack fungal problems.
Containing sulfur and pyrethrins, Bonide® Orchard Spray is a safe, one-hit concentrate for insect attacks and fungal problems. For best results, apply as a protective spray (2.5 oz/ gallon) early in the season. If disease, insects or wet weather are present, mix 5 oz in one gallon of water. Thoroughly spray all parts of the plant, especially new shoots.
"""],
        '1': ['Botryosphaeria obtusa', "Frog Eye Leaf spot","""The best way to rid your trees of black rot is to cut out the offending areas or cankers during the winter. Make sure to dispose of these properly, either by disposing in trash bags, burning, or burying them. It is also important to take away all mummified fruit, for the same reason of limiting the spread of fungal spores. Additionally, when your tree is fruiting, you should remove fruit that is damaged or invaded by insects, so that the fungus will not spread there. While you could try organically-approved fungicides, such as copper-based sprays or lime sulphur, these are still quite harsh and should be considered a last resort. The best method is to keep a sanitary tree environment all year round and consistently remove all sources of fungus spores.
"""],
        '2': ['Gymnosporangium juniperi-virginianae ', "Cedar Apple rust","""Choose resistant cultivars when available.
Rake up and dispose of fallen leaves and other debris from under trees.
Remove galls from infected junipers. In some cases, juniper plants should be removed entirely.
Apply preventative, disease-fighting fungicides labeled for use on apples weekly, starting with bud break, to protect trees from spores being released by the juniper host. This occurs only once per year, so additional applications after this springtime spread are not necessary.
On juniper, rust can be controlled by spraying plants with a copper solution (0.5 to 2.0 oz/ gallon of water) at least four times between late August and late October.
Safely treat most fungal and bacterial diseases with SERENADE Garden. This broad spectrum bio-fungicide uses a patented strain of Bacillus subtilis that is registered for organic use. Best of all, SERENADE is completely non-toxic to honey bees and beneficial insects.
Containing sulfur and pyrethrins, Bonide® Orchard Spray is a safe, one-hit concentrate for insect attacks and fungal problems. For best results, apply as a protective spray (2.5 oz/ gallon) early in the season. If disease, insects or wet weather are present, mix 5 oz in one gallon of water. Thoroughly spray all parts of the plant, especially new shoots.
"""],
        '3': ['healthy', None],
        '4': ['healthy', None],
        '5': ['healthy', None],
        '6': ['Podoshaera clandestine', "Powdery Mildew","""Susceptible cultivars such as Granny Smith, Cripps Pink, Honeycrisp and Golden Delicious make for almost 50% of the total organic acreage in Washington. Therefore, enhanced disease management programs should be implemented. Beside sanitation practices such the removal of infected shoots to reduce the inoculum size in early spring, sulfur is widely used to control powdery mildew in organic orchards. In addition to potential phytotoxicity, especially when temperature above 80°F occur in orchards, sulfur may not effectively control the disease under high disease pressure conditions. Other bio-pesticides to control powdery mildew organically exist (Table 3). Preventive applications and rotations of the different bio-pesticides from tight cluster to third cover spray should help keep powdery mildew under the economic threshold. Finally, observe precaution when growing moderately resistant cultivars such as Gala, which is widely grown organically in Washington, next to highly susceptible cultivars because inoculum drift between blocks can increase the pressure in block planted to moderately resistant cultivars."""],
        '7': ['Cercospora zeae-maydis', "Corn gray leaft spot","""Genetic resistance is the most cost-effective means of managing grey leaf spot (White et al., 1996). However, there are few hybrids in the USA that can be considered to be resistant to grey leaf spot (Perkins et al., 1995). Resistance is usually polygenic and additive in nature (Ayers et al., 1985; Bubeck et al., 1993; Anderson, 1995) but there have been reports of resistance being due to a dominant gene (Elwinger et al., 1990; Gevers and Lake, 1994). Rate-reducing polygenic resistance acts by adding small increments of resistance to the plant, which lead to an improvement in the level and stability of resistance. Major gene resistance, on the other hand, depends on a single gene and can be overcome by a single gene mutation in the pathogen. For this reason, single gene resistance is not stable and breeding for polygenic resistance is more desirable (Latterell and Rossi, 1983; Ayers et al., 1985)."""],
        '8': [' ', "Maize Rust"],
        '9': ['healthy', None],
        '10': ['Exserohilum turcicum', "Corn Northern Leaf blight","""Crop rotation to reduce previous corn residues and disease inoculum
Tillage to help break down crop debris and reduce inoculum load
Fungicide application to reduce yield loss and improve harvestability
Consider hybrid susceptibility, previous crop, tillage, field history, application cost, corn price"""],
        '11': ['Guignardia bidwellii', "Blackrot","""The most efficient way to control black rot is through a combination of good cultural practice and chemical methods. Good cultural practice includes: sanitation – removal of all mummies and infected leaf from the vines, choosing resistant varieties, selecting a site with good air circulation, removal of weeds and tall grass, and wise pruning of the vines. For successful black rot management program also fungicides can be used, where the proper timing of spraying is essential. It’s crucial to control primary infection, which can prevent secondary infections later in the season. In case of infection, protective spraying has to begin before bloom through four weeks after the bloom. Fungicides should be used only when the risk of black rot infection is high, what result in lower numbers of applications during the season and protection of the environment. For determination of high-risk infection periods, available disease prediction models should be used."""],
        '12': ['Phaeomoniella aleophilum, Phaeomoniella chlamydospora', "PCR","""A thirty-minute hot water treatment at 51°C did not eliminate these
pathogens from dormant wood cuttings. Cuttings first inoculated with Pa. chlamydospora or Pm. inflatipes or both
fungi, and then subjected to a hot water treatment were either incubated in crispers, or planted for six to eight weeks.
Vascular discoloration was scored followed by isolation from the cuttings onto potato dextrose agar amended with 0.1
g l-1 tetracycline (PDA-tet). Isolations confirmed the presence of the pathogens in the inoculated, hot-water treated
cuttings as well as in the inoculated, untreated control cuttings. This finding, along with earlier research on the
direct effect of hot water on the mycelium of these species, leads to the conclusion that hot water treatments are
ineffective in eliminating vine decline pathogens from dormant wood."""],
        '13': ['healthy', None],
        '14': ['Pseudocercospora vitis ', "Isariopsis leaf spot","""Pseudocercospora is often able to survive 2 years in the plant debris that is scattered on the ground. Removing and destroying leaf debris and pruning out dead branches may be the best and easiest strategy in reducing disease. Pseudocercospora leaf spots rarely become severe enough to cause the decline of the plant. However, if repeated severe infections occur, preventative spring fungicide applications may help prevent disease. However, no fungicides have been specifically tested for leaf spot on Japanese tree lilac. Pseudocercospora fungal leaf diseases on ornamental plants are controlled with fungicide applications in the spring- starting when the leaves first emerge from the buds and repeated every 14 days (or however the label instructs) through the rainy period of spring."""],
        '15': ['Candidatus Liberibacter spp', "Citrus greening"],
        '16': ['Xanthomonas campestris', "Bacterial Spot"],
        '17': ['healthy', None],
        '18': [' Xanthomonas campestris', "Bacterial Spott"],
        '19': ['healthy', None],
        '20': ['Alternaria solani', "Early Blight","""Prune or stake plants to improve air circulation and reduce fungal problems.
Make sure to disinfect your pruning shears (one part bleach to 4 parts water) after each cut.
Keep the soil under plants clean and free of garden debris. Add a layer of organic compost to prevent the spores from splashing back up onto vegetation.
Drip irrigation and soaker hoses can be used to help keep the foliage dry.
For best control, apply copper-based fungicides early, two weeks before disease normally appears or when weather forecasts predict a long period of wet weather. Alternatively, begin treatment when disease first appears, and repeat every 7-10 days for as long as needed.
Containing copper and pyrethrins, Bonide® Garden Dust is a safe, one-step control for many insect attacks and fungal problems. For best results, cover both the tops and undersides of leaves with a thin uniform film or dust. Depending on foliage density, 10 oz will cover 625 sq ft. Repeat applications every 7-10 days, as needed.
SERENADE Garden is a broad spectrum, preventative bio-fungicide recommended for the control or suppression of many important plant diseases. For best results, treat prior to foliar disease development or at the first sign of infection. Repeat at 7-day intervals or as needed.
Remove and destroy all garden debris after harvest and practice crop rotation the following year.
Burn or bag infected plant parts. Do NOT compost."""],
        '21': ['healthy', None],
        '22': ['Phytophthora infestans', "Potato late blight fungus","""Plant resistant cultivars when available.
Remove volunteers from the garden prior to planting and space plants far enough apart to allow for plenty of air circulation.
Water in the early morning hours, or use soaker hoses, to give plants time to dry out during the day — avoid overhead irrigation.
Destroy all tomato and potato debris after harvest"""],
        '23': ['healthy', None],
        '24': ['healthy', None],
        '25': ['Erysiphe cichoracearum', "Cucurbits","""Choose plants that are resistant to powdery mildew
Avoid planting vulnerable varieties in the shade
Manage aphid problems, as they can carry the spores into your garden
Provide moisture to leaves on a regular basis
Remove dried or diseased plant matter immediately upon seeing it
Use a variety of home or professional treatments if your plants have a serious mildew problem"""],
        '26': ['healthy', None],
        '27': ['Diplocarpon earlianum', "Tomato leaf mould","""Plant in full sunlight in well-drained soil with good air circulation.
B. Prevent weed growth by cultural or chemical methods.
C. Take care in spacing runner plants in matted-row culture. Do not allow an over-population of
plants.
D Always remove the old infected leaves from runner plants before setting.
"""],
        '28': ['Xanthomonas campestris pv. vesicatoria', "Bacterial Spot",""""""],
        '29': ['Alternaria solani', "Early Blight","""Prune or stake plants to improve air circulation and reduce fungal problems.
Make sure to disinfect your pruning shears (one part bleach to 4 parts water) after each cut.
Keep the soil under plants clean and free of garden debris. Add a layer of organic compost to prevent the spores from splashing back up onto vegetation.
Drip irrigation and soaker hoses can be used to help keep the foliage dry.
For best control, apply copper-based fungicides early, two weeks before disease normally appears or when weather forecasts predict a long period of wet weather. Alternatively, begin treatment when disease first appears, and repeat every 7-10 days for as long as needed.
Containing copper and pyrethrins, Bonide® Garden Dust is a safe, one-step control for many insect attacks and fungal problems. For best results, cover both the tops and undersides of leaves with a thin uniform film or dust. Depending on foliage density, 10 oz will cover 625 sq ft. Repeat applications every 7-10 days, as needed.
SERENADE Garden is a broad spectrum, preventative bio-fungicide recommended for the control or suppression of many important plant diseases. For best results, treat prior to foliar disease development or at the first sign of infection. Repeat at 7-day intervals or as needed.
Remove and destroy all garden debris after harvest and practice crop rotation the following year."""],
        '30': ['Phytophthora infestans', "Late Blight","""Plant resistant cultivars when available.
Remove volunteers from the garden prior to planting and space plants far enough apart to allow for plenty of air circulation.
Water in the early morning hours, or use soaker hoses, to give plants time to dry out during the day — avoid overhead irrigation.
Destroy all tomato and potato debris after harvest (see Fall Garden Cleanup)."""],
        '31': ['Passalora fulva', "Leaf Mould","""It has been shown that in the glasshouse, disease incidence can be decreased (and yield increased) by limiting the periods of high relative humidity. There was less leaf mould at a constant 20°C compared with a 20°C (day) and 13°C (night) regime (Winspear et al., 1970). However, other means have been tested. Vakalounakis (1992) grew two tomato cultivars in a greenhouse covered with a long-wave infrared absorbing (IRA)-vinyl film, which absorbs infrared emission by soil and plants during the night, and in a control greenhouse covered with a common agricultural (CA)-polyethylene film. At the end of the crop seasons, total disease index for leaf mould, caused by P. fulva (amongst other fungi), on both cultivars was much less in the IRA-vinyl greenhouse than in the CA-vinyl greenhouse. Another method used soil sterilization by solar heating by polyethylene mulching, followed by covering the soil again with plastic and planting seedlings through holes made in the covers. Hasan (1989) found that this reduced the severity of tomato leaf mould (P. fulva) as well as tomato yellow leaf curl bigeminivirus and early blight (Alternaria solani)."""],
        '32': ['Septoria lycopersici', "Septoria Leaf Spot","""The best control measure for tomato blight is prevention (see below).
Remove and destroy infected leaves (be sure to wash your hands afterwards).
Once blight is present and progresses, it becomes more resistant to biofungicide and fungicide. Treat it as soon as possible and on a schedule.
Organic fungicides. Treat organically with copper spray, which you can purchase online, at the hardware store, or home improvement center. Follow label directions. You can apply until the leaves are dripping, once a week and after each rain. Or you can treat it organically with a biofungicide like Serenade. Follow label instructions.
Chemical fungicides. Some gardeners prefer chemical fungicides, the best of which for tomatoes is chlorothalonil (sold as Fungonil, Daconil, or under other brand names. Check labels. You may also choose Mancozeb or Maneb, although these have longer wait times before you can harvest tomatoes safely than does chlorothalonil."""],
        '33': ['Tetranychus urticae', "Two Spotted Spider Mite","""Spider mites are easily introduced with materials, tools and people. Early detection of the mites, before noticeable damage occurs, is important for successful control. For monitoring use a good hand lens. 
Dust, e.g. from roads, favors mite outbreaks. 
Spider mites thrive on plants under stress; vigorous, adequately irrigated plants are far less susceptible. As naturally occuring predators play an important role in regulating spider mite populations, necessary pesticide treatments should be chosen and applied judiciously."""],
        '34': ['Corynespora cassiicola', "Target Spot","""Train cucumber plants to grow on a trellis or cage to increase air circulation around the plants. The leaves can dry out more easily after irrigation when draped over a trellis or cage. Faster drying reduces excess moisture and fungal development.

2
Avoid working in gardens or fields while infested plants are wet. Fungal spores often spread easily in water, so gardening while infected plants are wet can help the infection spread.

3
Remove infected plant debris from the garden to prevent the next crop of cucumbers from having the disease. Do not use the infected plant matter for compost. Instead, destroy the debris, or throw it away in sealed bags to prevent the fungus from spreading.

4
Spray cucumber plants with a fungicide if cultural controls are not enough to get rid of the fungus. Some fungicides that work to control corynespora include ones that contain fluoxastrobin, chlorothalonil or boscalid. Since different fungicides work in different ways and come in a variety of concentrations, it is best to follow manufacturer directions regarding fungicide applications. Before buying a fungicide, check the label to make sure it works for corynespora and is safe for use on cucumbers. Boscalid can be applied up to six times per season with a maximum amount of 3.5 ounces per acre per application."""],
        '35': ['Mosaic Virus', "Mosaic Virus","""Fungicides will NOT treat this viral disease.
Plant resistant varieties when available or purchase transplants from a reputable source.
Do NOT save seed from infected crops.
Spot treat with least-toxic, natural pest control products, such as Safer Soap, Bon-Neem and diatomaceous earth, to reduce the number of disease carrying insects.
Harvest-Guard® row cover will help keep insect pests off vulnerable crops/ transplants and should be installed until bloom.
Remove all perennial weeds, using least-toxic herbicides, within 100 yards of your garden plot.
The virus can be spread through human activity, tools and equipment. Frequently wash your hands and disinfect garden tools, stakes, ties, pots, greenhouse benches, etc. (one part bleach to 4 parts water) to reduce the risk of contamination.
Avoid working in the garden during damp conditions (viruses are easily spread when plants are wet).
Avoid using tobacco around susceptible plants. Cigarettes and other tobacco products may be infected and can spread the virus.
Remove and destroy all infected plants (see Fall Garden Cleanup). Do NOT compost."""],
        '36': ['Yellow Leaf Curl Virus', "Yellow Leaf Curl Virus","""symptomatic plants should be carefully covered by a clear or black plastic bag and tied at the stem at soil line. Cut off the plant below the bag and allow bag with plant and whiteflies to desiccate to death on the soil surface for 1-2 days prior to placing the plant in the trash. Do not cut the plant off or pull it out of the garden and toss it on the compost! The goal is to remove the plant reservoir of virus from the garden and to trap the existing virus-bearing whiteflies so they do not disperse onto other tomatoes."""],
        '37': ['healthy', None]
    }
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


saa = ""


@app.route('/diagnosed/<filename>')
def diagnosed(filename):
    disease = classes(filename)
    medication = Google().g(disease[0] + " medication")
    print(medication)
    if disease[1]:
        common = disease[1]
    else:
        common = None
    return render_template("diagnosed.html", name=disease[0], filename=filename, list=medication, common=common)


if __name__ == '__main__':
    app.run(debug=True)

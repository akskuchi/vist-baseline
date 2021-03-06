from flask import Flask
from flask import render_template
import sys

sys.path.insert(0, '../')
import h5py
from story_visualization import StoryPlot

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_folder='vist_dataset')


@app.route("/show_story/<int:story_index>")
def show_story(story_index):
    story_plot = StoryPlot(stories_data_set_path='./vist_dataset/validate_data/val.story-in-sequence.json',
                           images_root_folder_path='./vist_dataset/validate_data')

    train_dataset = h5py.File('./image_embeddings_to_sentence/stories_to_index_valid.hdf5', 'r')
    story_ids = train_dataset['story_ids']

    hypotheses_models_dirs = ['2018-02-09_15:30:08-2018-02-10_01:04:10', '2018-02-07_13:55:01-2018-02-08_03:15:08']
    hypotheses_files = []
    for dir in hypotheses_models_dirs:
        hypotheses = open('../results/'+ dir +'/hypotheses_valid.txt').read().split('\n')
        hypotheses_files.append(hypotheses)

    story_id = story_ids[story_index]

    hypotheses_sentences = []
    for sentences in hypotheses_files:
        model_sentences = sentences[(story_index * 5): (story_index * 5) + 5]
        hypotheses_sentences.append(model_sentences)

    data = story_plot.get_story_data(str(story_id))
    data['image_filenames'] = map(lambda x: x[1:], data['image_filenames'])
    data['hypotheses_sentences'] = hypotheses_sentences

    print(data)

    return render_template('show_story.html', data=data)

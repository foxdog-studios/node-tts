from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import cPickle as pickle
import os

from nltk.corpus import cmudict
import nltk

nltk.download(info_or_id=['cmudict'],
              download_dir=os.path.expanduser('~/nltk_data'))

phonemes = cmudict.dict()

path = os.path.join(os.path.dirname(__file__), '..', 'phonemes.pkl')

with open(path, 'wb') as outfile:
    pickle.dump(phonemes, outfile, protocol=pickle.HIGHEST_PROTOCOL)


from os import makedirs
from os.path import join, exists

CELL_SIZE = 256

NUM_LAYERS = 2






L_RATE = 0.002

BATCH_SIZE = 50


SEQ_LEN = 5





def get_dir(directory):
    """
    Creates the given directory if it does not exist.

    @param directory: The path to the directory.
    @return: The path to the directory.
    """
    if not exists(directory):
        makedirs(directory)
    return directory

def set_save_name(name):
    """
    Edits all constants dependent on SAVE_NAME.

    @param name: The new save name.
    """
    global SAVE_NAME, MODEL_SAVE_DIR

    SAVE_NAME = name
    MODEL_SAVE_DIR = get_dir(join(SAVE_DIR, 'models/', SAVE_NAME))



SAVE_DIR = get_dir('../save/')

SAVE_NAME = 'default/'

MODEL_SAVE_DIR = get_dir(join(join(SAVE_DIR, 'models'), SAVE_NAME))


MODEL_SAVE_FREQ = 5000






UNK = '*UNK*'

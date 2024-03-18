from .functionality_setup import get_main_key_input_setup
from .algorithmus_setup import get_main_algo_setup

from runtime_stats import update_input_data, update_algo_data

update_input_data(get_main_key_input_setup())
update_algo_data(get_main_algo_setup())

from .visual_setup import get_main_visual_setup
from runtime_stats import update_visual_data

update_visual_data(get_main_visual_setup())
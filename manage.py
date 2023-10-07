import settings
from scrape.util import get_page, get_data, save_data, iter_pages, download
from segment.util import mask_test
import sanitize.util as sutil


# To download csv file with urls of images
# iter_pages(get_page, get_data, save_data)

# To download images in file specified in settings
# csvf = settings.SAVE_URL + '/' + settings.SAVE_NAM (path to file name you saved your csv)
# download(csvf)

# To segment image with masks output (needs improvment)
# mask_test()

# To make images 256 x 256 resolution, cluster them and possibly get rid of outliers
# sutil.cut_from_middle()
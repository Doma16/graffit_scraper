import settings
from scrape.util import get_page, get_data, save_data, iter_pages, download
from segment.util import mask_test


# To download csv file with urls of images
# iter_pages(get_page, get_data, save_data)

# To download images in file specified in settings
# csvf = settings.SAVE_URL + '/' + settings.SAVE_NAM (path to file name you saved your csv)
# download(csvf)

# To segment image with masks output (needs improvment)
# mask_test()
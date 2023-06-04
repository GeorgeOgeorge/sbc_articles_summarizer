
import os
import re
from re import Match
import cv2
from pytesseract import image_to_string
from pdf2image import convert_from_path

# fazer assincorno
# extrair texto  https://towardsdatascience.com/extracting-text-from-scanned-pdf-using-pytesseract-open-cv-cd670ee38052
# deletar arquivos de pagina temporario

def preprocess_image(original_img):
    image = cv2.cvtColor(original_img, code=cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, ksize=(9,9), sigmaX=0)
    image = cv2.adaptiveThreshold(
        image, maxValue=255, C=30, blockSize=11,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv2.THRESH_BINARY_INV,
    )
    kernel = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(15,6))
    image = cv2.dilate(image, kernel=kernel, iterations=5)

    return image


def extract_contours(original_img):
    contours_found = cv2.findContours(original_img, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
    contours = contours_found[0] if len(contours_found) == 2 else contours_found[1]

    sorted_contours_by_y = sorted(contours, key=lambda contour: cv2.boundingRect(contour)[1])

    return sorted_contours_by_y


def write_contours(image, contour):
    x_start, y_start, width, hight = cv2.boundingRect(contour)
    x_end, y_end = x_start+width, y_start+hight

    cv2.rectangle(image, pt1=(x_start, y_start), pt2=(x_end, y_end), color=(255, 0, 255), thickness=3)

    return [(x_start, y_start), (x_end, y_end)]


def mark_page_contours(page, page_index):
    page_name = f'{page_index}_page.jpg'
    page_file_location = f'./temp/{page_name}'
    processed_page_location = f'./temp/{page_index}.jpg'

    page.save(page_file_location, 'JPEG')
    page_img = orignal_img = cv2.imread(page_file_location)

    page_img = preprocess_image(page_img)

    contours = extract_contours(page_img)

    contours_coordinates = [write_contours(orignal_img, contour) for contour in contours]

    cv2.imwrite(processed_page_location, orignal_img)
    # os.remove(os.path.abspath(page_file_location))

    return {'image_path': processed_page_location, 'contours_coordinates': contours_coordinates}


def extract_contour_text(image, contour):
    croped_img = image[contour[0][1]:contour[1][1], contour[0][0]:contour[1][0]]

    _, new_image = cv2.threshold(croped_img, thresh=120, maxval=255, type=cv2.THRESH_BINARY)

    return str(image_to_string(new_image, config='--psm 6'))


def preprocess_text(text: Match) -> str:
    if text:
        return text.group(1).replace('-\n', '').replace('\n', '').replace('\x0c', '')

    return ''


IS_TOPIC = r'(\d+(?:\.\d+)*\.\s\b\w{2}\w.*)(?=\n)'
EXTRACT_ABSTRACT = r'Abstract\.\s*(.*?)\x0c'

pages = convert_from_path('./temp/article.pdf', 400)
processed_pages_info = [mark_page_contours(page, index) for index, page in enumerate(pages)]

document_dict = {}
topic_text_buffer = []

for page in processed_pages_info:
    marked_image = cv2.imread(page['image_path'])

    for contour in page['contours_coordinates']:
        extracted_text = extract_contour_text(marked_image, contour)

        print(extracted_text)

        if 'Abstract. ' in extracted_text:
            text_search_result = re.search(EXTRACT_ABSTRACT, extracted_text, re.DOTALL | re.IGNORECASE)
            processed_text = preprocess_text(text_search_result)
            document_dict['abstract'] = processed_text

        if 'Conclusion' in extracted_text:
            text_search_result = re.search(EXTRACT_ABSTRACT, extracted_text, re.DOTALL | re.IGNORECASE)
            breakpoint()

        elif re.match(IS_TOPIC, extracted_text):
            extracted_text = extracted_text.replace('\n', '').replace('\x0c', '')
            document_dict[extracted_text] = ''

breakpoint()


{
    'sesao1': {
        'text': ''
        'children': [
            {}
        ],
        'images': [
            
        ]
    }
}
import PyPDF2
import easyocr
import requests
import numpy as np
import re
from PIL import Image
from bs4 import BeautifulSoup

class TextExtractor:
    def fromTextFile(self,file) -> str:
        file_content = file.read().decode('utf-8')
        return file_content
    
    def fromPDFFile(self,file) -> str:
        text = ''
        reader  = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
        return text
    
    def fromImageFileEasyOCR(self,image) -> str:
        text = ''
        pil_image = Image.open(image)
        image_array = np.asarray(pil_image)
        reader = easyocr.Reader(['en'], verbose=False)
        result = reader.readtext(image_array)
        for res in result:
            text += res[-2] + ' '
        return text
    
    def fromUrl(self,url) -> str | None:
        response = requests.get(url)
    
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')            
            text = soup.get_text()
            text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
            text = text.strip() # Remove leading and trailing whitespaces
            return text
        else:
            print("Failed to fetch the web page:", response.status_code)
            return None
        
    def fromHTMLFile(self,file) -> str:
        soup = BeautifulSoup(file, 'html.parser')
        text = soup.get_text()
        text = re.sub(r'\s+', ' ', text)
        # remove \n and \t
        text = re.sub(r'\n', ' ', text)
        text = text.strip()
        return text
    
if __name__ == '__main__':
    extractor = TextExtractor()
    extractor.fromImageFileEasyOCR('car.png')
    print(extractor.fromTextFile(open('./car.txt')))
    print(extractor.fromPDFFile(open('car.pdf', 'rb')))
    print(extractor.fromImageFile('car.png'))
    print(extractor.fromImageFileEasyOCR(open('car.png','rb')))
    print(extractor.fromUrl('https://en.wikipedia.org/wiki/Animal'))
    print(extractor.fromHTMLFile(open('content.html')))

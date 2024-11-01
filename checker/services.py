from google.cloud import vision
from datetime import datetime
import json
from google.oauth2 import service_account
from PIL import Image
import requests
import config
from io import BytesIO
credentials_dict=json.loads(config.GOOGLE_CREDENTIALS)
credentials=service_account.Credentials.from_service_account_info(credentials_dict)
def process_image(image_data):
    """
    Process image using Google Cloud Vision API and perform web detection.
    Takes binary image data and returns a list of search results where the image appears online.
    """
    try:
        # Initialize Google Cloud Vision client
        client = vision.ImageAnnotatorClient(credentials=credentials)
        
        # Create vision.Image from binary data
        image = vision.Image(content=image_data)
        
        # Perform web detection
        response = client.web_detection(image=image)
        web_detection = response.web_detection
        
        results = []
        
        # Process full matching images
        if web_detection.full_matching_images:
            for match in web_detection.full_matching_images:
                result = extract_image_data(match.url)
                if result:
                    results.append(result)
                    
        # Process partial matching images
        if web_detection.partial_matching_images:
            for match in web_detection.partial_matching_images:
                result = extract_image_data(match.url)
                if result:
                    results.append(result)
                    
        # Process pages with matching images
        if web_detection.pages_with_matching_images:
            for page in web_detection.pages_with_matching_images:
                result = extract_page_data(page)
                if result:
                    results.append(result)
                    
        return results
    
    except Exception as e:
        print(f"Error processing image: {e}")
        return []

def extract_image_data(url):
    """
    Extract metadata from image URL.
    Returns dictionary with platform, source, and date information.
    """
    try:
        # Make a request to get image
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        
        # Try to get date from image metadata
        exif = img._getexif()
        if exif:
            date_taken = exif.get(36867)  # EXIF tag for DateTimeOriginal
            if date_taken:
                date = datetime.strptime(date_taken, '%Y:%m:%d %H:%M:%S')
            else:
                date = datetime.now()
        else:
            date = datetime.now()
            
        # Extract domain as platform
        domain = url.split('/')[2]
        
        return {
            'platform': domain,
            'url': url,
            'date': date,
            'type': 'image_match'
        }
        
    except Exception as e:
        print(f"Error extracting image data: {e}")
        return None

def extract_page_data(page):
    """
    Extract metadata from webpage containing the image.
    Returns dictionary with platform, source, and date information.
    """
    try:
        url = page.url
        
        # Make a request to get page content
        response = requests.get(url)
        
        # Try to get last modified date from headers or page content
        date = response.headers.get('last-modified')
        if date:
            date = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S GMT')
        else:
            date = datetime.now()  # Use current date if no date found
            
        # Extract domain as platform
        domain = url.split('/')[2]
        
        return {
            'platform': domain,
            'url': url,
            'date': date,
            'type': 'page_match'
        }
        
    except Exception as e:
        print(f"Error extracting page data: {e}")
        return None

def build_image_timeline(search_results):
    """
    Build a timeline from the search results.
    Returns list of timeline entries sorted by date.
    """
    # Sort results by date
    search_results.sort(key=lambda x: x['date'])
    
    timeline = []
    for result in search_results:
        timeline.append({
            'platform': result['platform'],
            'url': result['url'],
            'date': result['date'].strftime('%Y-%m-%d %H:%M:%S'),
            'type': result['type']
        })
    
    return timeline

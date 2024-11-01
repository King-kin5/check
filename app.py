from flask import Flask,request
import logging
from flask import Flask, render_template,jsonify
from PIL import Image
import io
import os
from  checker.services import build_image_timeline, process_image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app=Flask(__name__,static_folder='static',template_folder='template')
ALLOWED_MIME_TYPES = {'image/png', 'image/jpeg', 'image/gif'}
@app.route('/')
def index():
    try:
        # Log template directory information
        template_dir = os.path.join(app.root_path, 'template')
        logger.info(f"Template directory path: {template_dir}")
        logger.info(f"Template directory exists: {os.path.exists(template_dir)}")
        if os.path.exists(template_dir):
            logger.info(f"Template directory contents: {os.listdir(template_dir)}")
        
        return render_template('interface.html')
    except Exception as e:
        logger.error(f"Error in index route: {str(e)}")
        return f"Error: {str(e)}", 500

@app.route('/home')
def home():
    try:
        template_dir = os.path.join(app.root_path, 'templats')
        logger.info(f"Template directory path: {template_dir}")
        logger.info(f"Template directory exists: {os.path.exists(template_dir)}")
        if os.path.exists(template_dir):
            logger.info(f"Template directory contents: {os.listdir(template_dir)}")
            
        return render_template('interface.html')
    except Exception as e:
        logger.error(f"Error in home route: {str(e)}")
        return f"Error: {str(e)}", 500

@app.route('/debug-info')
def debug_info():
    """Route to show debug information"""
    try:
        template_dir = os.path.join(app.root_path, 'template')
        static_dir = os.path.join(app.root_path, 'static')
        
        debug_info = {
            'app_root_path': app.root_path,
            'template_folder': app.template_folder,
            'template_dir_exists': os.path.exists(template_dir),
            'template_dir_contents': os.listdir(template_dir) if os.path.exists(template_dir) else [],
            'static_dir_exists': os.path.exists(static_dir),
            'static_dir_contents': os.listdir(static_dir) if os.path.exists(static_dir) else [],
            'environment': app.config.get('ENV'),
            'debug_mode': app.debug,
        }
        return jsonify(debug_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500



def allowed_file(file):
    logger.info(f"Received file type: {file.content_type}")  # Log the MIME type
    return file.content_type in ALLOWED_MIME_TYPES

@app.route('/process', methods=['POST'])
def process_image_route():
    logger.info(f"Files in request: {request.files}")  # Log all uploaded files
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    logger.info(f"File uploaded: {file.filename}, MIME type: {file.content_type}")  # Log file info

    # Check if the uploaded file has an allowed MIME type
    if not allowed_file(file):
        return jsonify({'error': 'Invalid file type. Allowed types: png, jpg, jpeg, gif'}), 400

    try:
        search_results = process_image(file.read())
        timeline = build_image_timeline(search_results)
        return jsonify({'success': True, 'timeline': timeline})
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return jsonify({'error': f'Error processing image: {str(e)}'}), 500


if __name__== '__main__':
    app.run(debug=True)

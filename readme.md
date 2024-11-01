# Image Search Timeline Application

This is a web-based application that uses the Google Cloud Vision API to perform web detection on uploaded images, identifying instances where the image appears across the internet. The application builds a timeline of matches found online and displays results in a visually appealing interface.

## Features

- **Image Web Detection:** Utilizes Google Cloud Vision API to perform web detection on images.
- **Image Timeline:** Creates a timeline of matched images and pages based on online search results.
- **Error Handling:** Provides robust error handling and user-friendly feedback for image processing.
- **Frontend UI:** Built with TailwindCSS and Alpine.js for an interactive drag-and-drop upload interface.

## Table of Contents

- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Endpoints](#endpoints)
- [File Structure](#file-structure)
- [Technologies Used](#technologies-used)
- [License](#license)

## Getting Started

### Prerequisites

1. **Python 3.6+** - Ensure Python is installed on your system.
2. **Google Cloud Vision API Credentials** - You’ll need a Google Cloud account with Vision API enabled. Download your service account key and store it in a safe location.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/image-search-timeline.git
   cd image-search-timeline

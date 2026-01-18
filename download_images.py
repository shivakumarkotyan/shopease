import os
import requests

def download_sample_images():
    """Download sample product images from placeholder services"""
    images = {
        'smartphone.jpg': 'https://via.placeholder.com/400x300/007bff/ffffff?text=Smartphone',
        'laptop.jpg': 'https://via.placeholder.com/400x300/28a745/ffffff?text=Laptop',
        'headphones.jpg': 'https://via.placeholder.com/400x300/dc3545/ffffff?text=Headphones',
        'tshirt.jpg': 'https://via.placeholder.com/400x300/ffc107/000000?text=T-Shirt',
        'jeans.jpg': 'https://via.placeholder.com/400x300/6f42c1/ffffff?text=Jeans',
        'book.jpg': 'https://via.placeholder.com/400x300/20c997/ffffff?text=Book',
        'gardentools.jpg': 'https://via.placeholder.com/400x300/fd7e14/ffffff?text=Garden+Tools',
        'smartwatch.jpg': 'https://via.placeholder.com/400x300/e83e8c/ffffff?text=Smart+Watch',
        'placeholder.jpg': 'https://via.placeholder.com/400x300/6c757d/ffffff?text=No+Image'
    }
    
    # Create images directory if it doesn't exist
    os.makedirs('static/images', exist_ok=True)
    
    for filename, url in images.items():
        filepath = os.path.join('static/images', filename)
        if not os.path.exists(filepath):
            try:
                print(f"Downloading {filename}...")
                response = requests.get(url)
                response.raise_for_status()
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"✓ Downloaded {filename}")
            except Exception as e:
                print(f"✗ Failed to download {filename}: {e}")
        else:
            print(f"✓ {filename} already exists")

if __name__ == '__main__':
    print("Setting up product images for ShopEase...")
    download_sample_images()
    print("Image setup complete!")
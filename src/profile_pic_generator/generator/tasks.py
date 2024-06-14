from celery import shared_task
from .models import ProfilePicture
from PIL import Image
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import io

@shared_task
def enhance_profile_picture(picture_id):
    picture = ProfilePicture.objects.get(id=picture_id)
    original_image = Image.open(picture.original_image)
    
    # Convert image to numpy array
    original_image_np = np.array(original_image)
    
    # Preprocess the image
    img = tf.image.convert_image_dtype(original_image_np, tf.float32)
    img = tf.image.resize(img, (256, 256))
    img = tf.expand_dims(img, 0)

    # Load the model from TensorFlow Hub
    model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
    
    # Apply the style transfer
    outputs = model(img, img)
    stylized_image = outputs[0]
    
    # Convert the result to a PIL image
    stylized_image_np = stylized_image.numpy()
    stylized_image_np = np.squeeze(stylized_image_np, 0)
    stylized_image_pil = Image.fromarray((stylized_image_np * 255).astype(np.uint8))

    # Save the enhanced image
    buffer = io.BytesIO()
    stylized_image_pil.save(buffer, format='JPEG')
    picture.enhanced_image.save(f"enhanced_{picture_id}.jpg", buffer)
    picture.save()



    
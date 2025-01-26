from groq import Groq
from PIL import Image
import io
import base64
from typing import Dict

from app.config.settings import settings


class FeatureExtractor:
    def __init__(self):
        """Initialize the Groq client for feature extraction."""
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = "llama-3.2-11b-vision-preview"

    def _encode_image_to_base64(self, image: Image.Image) -> str:
        """Convert PIL Image to base64 string."""
        # Convert RGBA to RGB if necessary
        if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1])  # paste using alpha channel as mask
            image = background

        buffered = io.BytesIO()
        image.save(buffered, format="JPEG", quality=95)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/jpeg;base64,{img_str}"

    def extract_features(self, image: Image.Image) -> Dict[str, str]:
        """
        Extract features from the input image using Groq's vision model.
        
        Args:
            image (Image.Image): PIL Image to analyze
            
        Returns:
            Dict[str, str]: Dictionary containing the extracted features as a description
        """
        # Convert image to base64
        image_base64 = self._encode_image_to_base64(image)
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "This is an image of a person. Describe the physical features of this person in a bulleted list. Feel free to be brutally honest."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_base64
                                }
                            }
                        ]
                    }
                ],
                temperature=1,
                max_completion_tokens=1024,
                top_p=1,
                stream=False,
                stop=None
            )
            
            # Extract the features description from the completion
            features_description = completion.choices[0].message.content
            
            return {
                "description": features_description
            }
            
        except Exception as e:
            raise Exception(f"Error extracting features: {str(e)}")
        

# client = Groq(api_key=settings.GROQ_API_KEY)
# completion = client.chat.completions.create(
#     model="llama-3.2-11b-vision-preview",
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "text",
#                     "text": "This is an image of a person. Describe the physical features of this person in a bulleted list. Feel free to be brutally honest."
#                 },
#                 {
#                     "type": "image_url",
#                     "image_url": {
#                         "url": "https://miro.medium.com/v2/resize:fit:2400/1*P0MjNza5DvxA5q24pI0DNA@2x.jpeg"
#                     }
#                 }
#             ]
#         }
#     ],
#     temperature=1,
#     max_completion_tokens=1024,
#     top_p=1,
#     stream=False,
#     stop=None,
# )

# print(completion.choices[0].message)



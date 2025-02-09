from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.base import ContentFile
import os

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    location = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(
        upload_to="avatars/", default="avatars/default.png")
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    
    def auto_generate_generic_avatar(self):
        """
        Generates a generic avatar image with the user's initials and saves it
        in the media/avatars directory.
        """
        # Image configuration
        image_size = (200, 200)
        background_color = (70, 130, 180)  # SteelBlue
        text_color = (255, 255, 255)         # White

        # Create a new image with a solid background
        image = Image.new("RGB", image_size, background_color)
        draw = ImageDraw.Draw(image)

        # Extract the user's initials from their username.
        # For multi-part usernames, this takes the first letter of each part.
        initials = ''.join([part[0].upper() for part in self.user.username.split()])
        if not initials:
            initials = self.user.username[0].upper()

        # Attempt to load a TrueType font. Adjust the font path and size if necessary.
        try:
            font = ImageFont.truetype("arial.ttf", 100)
        except IOError:
            font = ImageFont.load_default()

        # Calculate the size of the text.
        # Use draw.textbbox if available (Pillow ≥8.0.0); otherwise, try font.getsize.
        if hasattr(draw, "textbbox"):
            bbox = draw.textbbox((0, 0), initials, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        else:
            try:
                text_width, text_height = font.getsize(initials)
            except AttributeError:
                raise Exception("Your Pillow version does not support calculating text dimensions.")

        # Center the text on the image.
        text_position = (
            (image_size[0] - text_width) / 2,
            (image_size[1] - text_height) / 2
        )

        # Draw the initials onto the image.
        draw.text(text_position, initials, fill=text_color, font=font)

        # Save the image to an in-memory file.
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        # Construct a file name and ensure it's saved under the "avatars" folder.
        file_name = f"{self.user.username}_avatar.png"
        file_path = os.path.join("", file_name)

        # Save the generated image to the avatar field without saving the model immediately.
        self.avatar.save(file_path, ContentFile(buffer.getvalue()), save=False)
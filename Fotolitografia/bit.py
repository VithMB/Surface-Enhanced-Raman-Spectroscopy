from PIL import Image, ImageDraw

# 1. Create a black square canvas (300x300 pixels)
img = Image.new('RGB', (500, 500), color='black')
draw = ImageDraw.Draw(img)
 
draw.rectangle([0, 0, 500, 500], fill='black', outline='white', width=50)

# 3. Save the bitmap image
img.save('square_bitmap.bmp')

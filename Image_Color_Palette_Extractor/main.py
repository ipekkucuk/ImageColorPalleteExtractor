## ##Image Color Palette Extractor 
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import os

##görseli açıp yeniden boyutlandırıp numpy yapıyorum daha hızlı işlemek için
def load_image(image_path, resize=True, size=(100, 100)):
    try:
        image = Image.open(image_path).convert("RGB")  # PNG desteği + RGBA -> RGB dönüşüm
        if resize:
            image = image.resize(size)
        image_np = np.array(image)
        return image_np
    except Exception as e:
        print(f"❌ Image couldn't be downloaded: {e}")
        exit(1)

##çok koyu ve açığı yani uçtaki beyaz ve siyahı almıyor
def is_too_dark_or_light(rgb, dark_thresh=30, light_thresh=225):
 
    return all(channel <= dark_thresh for channel in rgb) or \
           all(channel >= light_thresh for channel in rgb)

##grilik fonskiyonu 
def is_grayscale(rgb, tolerance=15):
    rgb = [int(c) for c in rgb]
    return max(rgb) - min(rgb) < tolerance

#kaç tane grilik var saysın
def count_grayscale_colors(colors):
    return sum(1 for color in colors if is_grayscale(color))

##filtreleme 
def filter_out_grayscale(pixels):
    return np.array([p for p in pixels if not is_grayscale(p)])


##en baskın renkleri bulabilmek için kmeans algoritması ile kümeliyoruz
def get_dominant_colors(image_np, n_colors=5):
    pixels = image_np.reshape(-1, 3)  # Her pikselin RGB değerini vektöre dönüştür vektörizasyon bizim işimiz

     # Aşırı koyu veya aşırı açık olan pikselleri çıkar ve grayscale
    filtered_pixels = np.array([
        p for p in pixels 
        if not is_too_dark_or_light(p) and not is_grayscale(p)
    ])

    # Eğer filtrelemeden sonra çok az piksel kaldıysa, orijinali kullan
    if len(filtered_pixels) < 100:
        filtered_pixels = pixels

    model = KMeans(n_clusters=n_colors, random_state=42) ## minik easter egg de koydum hehe 
    model.fit(filtered_pixels)
    colors = model.cluster_centers_.astype(int)

    grayscale_count = count_grayscale_colors(colors)
    if grayscale_count >= 2:
        filtered_pixels_strict = np.array([
            p for p in filtered_pixels if not is_grayscale(p)
        ])

        if len(filtered_pixels_strict) >= 100:
            model = KMeans(n_clusters=n_colors, random_state=42)
            model.fit(filtered_pixels_strict)
            colors = model.cluster_centers_.astype(int)
            print(f"⚠️ {grayscale_count} grayscale tones detected. Recomputed the palette without grayscale tones.")
        else:
            print(f"⚠️ {grayscale_count} grayscale tones detected, but not enough color data remained to reprocess.")

    return colors
   

#Renk paletini görselleştiriyoruz (kare bloklar olarak gösteriyoruz)
def plot_palette(colors):
    plt.figure(figsize=(8, 2))  # Palet görselinin boyutu
    for i, color in enumerate(colors):
        plt.fill_between([i, i + 1], 0, 1, color=np.array(color) / 255)  # Rengi çiz
    plt.xlim(0, len(colors))
    plt.axis('off')  # Eksenleri kapat
    plt.show()  # Paleti göster


#RGB'den HEX'e dönüştürme fonksiyonu, renk kodlarını yazmak için
def rgb_to_hex(rgb_color):
    return '#%02x%02x%02x' % tuple(rgb_color)


#HEX renkleri terminalde yazdırıyoruz
def print_palette_hex(colors):
    hex_colors = [rgb_to_hex(color) for color in colors]
    print("Top dominant colors (HEX):")
    for i, (rgb, hex_code) in enumerate(zip(colors, hex_colors), 1):
        tag = " (grayscale)" if is_grayscale(rgb) else ""
        print(f"{i}. {hex_code}{tag}")      

# Tüm işlemleri bir araya getiren ana fonksiyon
def extract_color_palette(image_path, n_colors=5):
    image_np = load_image(image_path)
    colors = get_dominant_colors(image_np, n_colors=n_colors)
    print_palette_hex(colors)
    plot_palette(colors)

## Çalıştırılabilir dosya olarak kullanılmasını sağlıyoruz
if __name__ == "__main__":
    image_path = input("🎨Enter the name of the image (e.g 11.jpg): ").strip()
    
    try:
        n = int(input(" How many colors do you want? (Enter a number between 3 and 9) "))
        if not 3 <= n <= 9:
            raise ValueError
    except ValueError:
        print("❌ Please enter a valid number between 3 and 9. 2.jpg")
        exit(1)

    extract_color_palette(image_path, n_colors=n)
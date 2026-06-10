import os
import google.generativeai as genai
from flask import current_app
from PIL import Image

class GeminiAIService:
    @staticmethod
    def analyze_plant(plant_name, symptoms, image_path=None):
        api_key = current_app.config.get('GEMINI_API_KEY')
        if not api_key or api_key == 'your_gemini_api_key_here':
            return "Error: Gemini API Key belum dikonfigurasi. Silakan periksa file .env."
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""Kamu adalah pakar pertanian profesional. Analisis gejala tanaman berikut dan berikan:
1. Kemungkinan penyakit
2. Tingkat keparahan
3. Solusi penanganan
4. Pencegahan
5. Rekomendasi pupuk

Nama Tanaman: {plant_name}
Gejala: {symptoms}"""

        try:
            if image_path and os.path.exists(image_path):
                img = Image.open(image_path)
                response = model.generate_content([prompt, img])
            else:
                response = model.generate_content(prompt)
                
            return response.text
        except Exception as e:
            return f"Terjadi kesalahan saat menghubungi layanan AI: {str(e)}"

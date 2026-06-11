import os
import base64
import json
import requests
from flask import current_app

class GeminiAIService:
    @staticmethod
    def analyze_plant(plant_name, symptoms, image_path=None):
        # 1. Ambil API Key OpenRouter dari konfigurasi aplikasi (.env)
        api_key = current_app.config.get('GEMINI_API_KEY')
        if not api_key:
            return "Error: API Key OpenRouter belum dikonfigurasi. Silakan periksa file .env."
        
        # 2. Rancang template prompt analisis tanaman
        prompt = f"""Kamu adalah pakar pertanian profesional. Analisis gejala tanaman berikut dan berikan:
1. Kemungkinan penyakit
2. Tingkat keparahan
3. Solusi penanganan
4. Pencegahan
5. Rekomendasi pupuk

Nama Tanaman: {plant_name}
Gejala: {symptoms}"""

        # 3. Susun struktur konten pesan (Default teks)
        contents = [{"type": "text", "text": prompt}]

        # 4. Jika pengguna mengunggah gambar, ubah ke Base64 sesuai standar OpenRouter
        if image_path and os.path.exists(image_path):
            try:
                with open(image_path, "rb") as img_file:
                    base64_image = base64.b64encode(img_file.read()).decode('utf-8')
                
                # Deteksi ekstensi gambar untuk penentuan MIME type
                ext = os.path.splitext(image_path)[1].lower().replace('.', '')
                mime_type = f"image/{ext}" if ext in ['jpg', 'jpeg', 'png', 'webp'] else "image/jpeg"
                
                contents.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{base64_image}"
                    }
                })
            except Exception as e:
                return f"Gagal memproses lampiran gambar: {str(e)}"

        # 5. Konfigurasi Header & Payload OpenRouter
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "google/gemini-2.5-flash:free",
            "messages": [
                {
                    "role": "user",
                    "content": contents
                }
            ],
            "max_tokens":1000
        }

        # 6. Tembak langsung ke Endpoint Resmi OpenRouter
        # 6. Tembak langsung ke Endpoint Resmi OpenRouter
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                data=json.dumps(payload),
                timeout=30
            )
            
            res_json = response.json()
            if response.status_code == 200:
                # 🟢 FIX MANTEP: Cek dulu apakah 'choices' beneran ada di dalam JSON
                if 'choices' in res_json:
                    return res_json['choices'][0]['message']['content']
                elif 'error' in res_json:
                    # Jika OpenRouter menyelundupkan eror di dalam status 200
                    return f"OpenRouter Error: {res_json['error'].get('message')}"
                else:
                    return f"Format JSON tidak dikenal: {json.dumps(res_json)}"
            else:
                error_msg = res_json.get('error', {}).get('message', 'Terjadi kesalahan internal pada OpenRouter.')
                return f"OpenRouter Error ({response.status_code}): {error_msg}"
                
        except Exception as e:
            return f"Terjadi kesalahan saat menghubungi layanan AI: {str(e)}"
# FarmAssist AI (Enterprise Grade)

Sistem Konsultasi Pertanian Cerdas Berbasis Cloud Computing dan Generative AI untuk Mendukung Ketahanan Pangan (SDGs).

## Architecture & Enterprise Patterns
Aplikasi ini sudah di-refactor menuju Cloud Native multi-tier architecture:
- **Repository Pattern:** Memisahkan logika database (SQLAlchemy) dari Route/Controller.
- **Service Layer Pattern:** Memisahkan integrasi eksternal (AI Service, Storage Service, Notification Service, Monitoring Service).
- **REST API:** Menyediakan JSON blueprint pada path `/api`.
- **CI/CD:** Menyertakan `.github/workflows/deploy.yml` pipeline.

## API Documentation
| Endpoint | Method | Keterangan |
|----------|--------|------------|
| `/api/health` | GET | Cek status health backend. |
| `/api/consultations` | GET | Mendapatkan list konsultasi pengguna dalam format JSON (Membutuhkan Login Session). |

## Fitur UI
Semua fitur lama (Auth, Dashboard, Consult, History, Admin) tetap berjalan melalui *routes* utama berbasis *Blueprint*.

Silakan cek `ARCHITECTURE.md` dan `ERD.md` untuk diagram teknis.

📊 Sales Data Pipeline – Google Cloud Platform

![requirement_updated](https://github.com/user-attachments/assets/fa272707-498d-47d2-ac38-12e5f304bef4)


End-to-end sales data ingestion and analytics pipeline built using Google Cloud Platform.

This project demonstrates a complete cloud-native workflow from file upload to automated reporting using an event-driven architecture.

---

## 🚀 Project Overview

Shop managers upload sales data files (CSV/Excel) through a web portal.  
Uploaded data is automatically processed and made available in dashboards for regional and global analysis.

**Pipeline Flow**

Flask Upload Portal → Cloud Storage → Cloud Function (ETL) → BigQuery → Looker Studio

---

## 🏗 Architecture

![pipeline-diagram](https://github.com/user-attachments/assets/e28dbe26-2587-4119-ab4d-e72fe4848c18)

---

## 🔁 End-to-End Data Flow

### 1️⃣ Ingestion – Flask Web Portal (Localhost)

- Built using Flask  
- Runs locally via VS Code  
- Accepts CSV/Excel uploads  
- Pushes files to Google Cloud Storage  
- Provides upload success/failure feedback  

---

### 2️⃣ Raw Storage – Google Cloud Storage (GCS)

- Stores uploaded files as raw data (staging layer)  
- Organizes files with batch/date structure  
- Event-driven trigger enabled  

---

### 3️⃣ Processing – Cloud Function (ETL)

Triggered automatically on file upload.

- Extract data from uploaded file  
- Validate schema  
- Clean and transform records  
- Load structured data into BigQuery  

This follows an **ETL architecture**, since transformations occur before final warehouse storage.

---

### 4️⃣ Data Warehouse – BigQuery

**Dataset:** `sales`

Contains:

- `orders-cleaned` (cleaned fact table)  
- `USA_Sales_View`  
- `UK_Sales_View`  
- `France_Sales_View`  
- `Aus_Sales_View`  
- `Master_Sales_View` (global consolidated view)  

Design approach:

- Raw → Cleaned fact table  
- Country-level summary views  
- Master view for dashboard consumption  

---

### 5️⃣ Visualization – Looker Studio

Connected directly to `Master_Sales_View`.

- Regional sales reporting  
- Global aggregation  
- KPI dashboards  
- Filtering by region/date/product  
- Drill-down capability  

![Untitled_Report_page-0001](https://github.com/user-attachments/assets/25cfe3d1-208a-4320-ad3a-ea4337829136)
![Untitled_Report_page-0002](https://github.com/user-attachments/assets/e165ba5c-cc3c-49e2-a6fd-36708f0e1611)

---

## 🔄 Alternative Ingestion Approaches Considered

Although this project uses file-based ingestion via GCS trigger, other approaches were evaluated:

- **API-Based Ingestion** – Real-time REST-based data submission for transactional systems.
- **Streaming (Kafka/PubSub)** – Event-driven, near real-time ingestion for high-frequency systems.
- **Direct BigQuery Load (ELT)** – Load raw data directly into BigQuery and transform using SQL.
- **Scheduled Batch Jobs** – Periodic ingestion from legacy or reporting systems.

The GCS-triggered ETL approach was selected for its simplicity, automation, scalability, and suitability for batch reporting workflows.

---

## 🛠 Technology Stack

- Flask (Web UI)
- Google Cloud Storage
- Cloud Functions (Python)
- BigQuery
- Looker Studio
- VS Code

---

## 🧠 Data Engineering Concepts Strengthened

- ETL architecture  
- Event-driven design  
- Separation of raw and processed layers  
- Batch processing  
- Data modeling with views  
- Warehouse abstraction  
- Cloud-native pipeline thinking  

---

## 🎯 Key Highlights

- Fully automated event-driven pipeline  
- Serverless ETL processing  
- Structured warehouse modeling  
- Region-level reporting  
- Clean separation of ingestion, processing, and visualization layers  
- Built under time constraints without Firebase  

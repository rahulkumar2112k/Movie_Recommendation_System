
# 🎬 Content-Based Movie Recommendation System

A content-based movie recommendation system built with **Python 🐍**, **Machine Learning 🤖**, and **Streamlit 📊**.  
It suggests movies 🍿 similar to the one selected by the user, based on movie metadata similarity 📝✨.

🌐 **Try the Project Live:** [Movie Recommendation System](https://movierecommendationsystem-rahul2112k.streamlit.app/)


---

# 🛠️ Tech Stack

- Python 🐍

- Pandas / NumPy for data manipulation

- Scikit-learn for computing similarity

- Streamlit for interactive UI

---
## 📊 Dataset 📁

This project uses the **TMDB 5000 Movies dataset** (file: `tmdb_5000_movies.csv`) from [Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata).  

### 🔑 Selected Features
From the dataset, only the following columns were used for building the recommendation system:

- 🎬 **id** → Unique identifier for each movie  
- 🎨 **genres** → Categories of the movie (e.g., Action, Comedy, Drama)  
- 🏷️ **keywords** → Tags/keywords describing the movie  
- 📝 **overview** → Short description of the plot  
- 📛 **title** → Movie name  

These features were combined to create a **content-based profile** for each movie.  

---

## 🧠 Model Preprocessing & Training ⚙️

### 1️⃣ Data Cleaning
- Loaded the dataset using **Pandas**  
- Selected only required columns: `id`, `genres`, `keywords`, `overview`, `title`  
- Handled **missing values** and removed invalid entries  

### 2️⃣ Text Preprocessing
- Converted `genres` and `keywords` JSON-like structures into plain text  
- Combined all selected features into a single **text column** for each movie  
- Applied **stemming and lowercase conversion** for normalization  

### 3️⃣ Feature Extraction
- Used **TfidfVectorizer** from `scikit-learn` to transform text into numerical feature vectors  
- Each movie is now represented as a vector in high-dimensional space  

### 4️⃣ Similarity Computation
- Calculated **cosine similarity** between all movie vectors  
- Built a **similarity matrix** to measure how close two movies are in terms of content  

### 5️⃣ Model Saving
```python
import pickle

# Save preprocessed movie dataframe
pickle.dump(movies_df, open('movies.pkl', 'wb'))

# Save similarity matrix
pickle.dump(similarity_matrix, open('similarity.pkl', 'wb'))
```
---
## 🌐 Building the Streamlit Web App 🎨

The recommendation engine is deployed as a **Streamlit web app**.  
It loads the preprocessed files (`movies.pkl` & `similarity.pkl`) and provides an interactive UI for movie selection.

---

### 🔹 App Workflow
1. Load `movies.pkl` and `similarity.pkl`  
2. User selects a movie title from dropdown  
3. System finds the top 5 most similar movies using **cosine similarity**  
4. Fetch **movie posters** using TMDB API (based on `movie_id`)  
5. Display recommended movies with posters in a nice layout  

---

### 🔹 Fetching Movie Posters
We use the [TMDB API](https://developer.themoviedb.org/) to fetch posters.  
Every movie in the dataset has a unique **`id`**, which maps directly to TMDB’s database.

Example function:
```python
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=YOUR_API_KEY&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500" + poster_path
    return full_path
```
---
## 📂 Project Structure 🗂️

Movie_Recommendation_System/  

│── app.py                   
│── movies.pkl               
│── similarity.pkl             
│── requirements.txt       
│── README.md                 
│── .gitignore               
│── .gitattributes       

---

## 🧑‍💻 How to Clone and Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/rahulkumar2112k/Movie_Recommendation_System.git
```

### 2. Navigate to the Project Directory
```bash
cd Movie_Recommendation_System
```

### 3. Set Up a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
```

Activate the virtual environment:

- On Windows:
```bash
venv\Scripts\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```

### 4. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Streamlit App
```bash
streamlit run app.py
```

Open in your browser at:
```
http://localhost:8501
```
---

# ✨ Hope you found this project interesting!  
# 😊 Thank you for checking it out.





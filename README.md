# NiaSafe

NiaSafe is a comprehensive web application designed to detect and manage toxic comments in real-time using advanced machine learning techniques. Built with a DistilBERT model fine-tuned for toxicity classification, it categorizes comments into various toxicity types such as toxic, severe_toxic, obscene, threat, insult, and identity_hate. The application provides a user-friendly dashboard for monitoring flagged content, viewing analytics through interactive charts, and managing alerts.

## Features

- **Real-time Toxicity Detection**: API endpoint for instant comment analysis
- **Interactive Dashboard**: View flagged comments, severity distributions, and trends
- **Alert System**: Automated notifications for high-severity incidents
- **Data Persistence**: MongoDB integration for storing flagged comments
- **Responsive UI**: Modern interface built with Tailwind CSS and Chart.js
- **Machine Learning Pipeline**: Preprocessing, training, and inference scripts included

## Prerequisites

Before setting up the project, ensure you have the following installed:

- **Python 3.8 or higher**
- **MongoDB** (local installation or cloud service like MongoDB Atlas)
- **Node.js and npm** (for Vercel CLI deployment)
- **Git** (for version control)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd NiaSafe
   ```

2. **Set up the backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Configure MongoDB**:
   - Install MongoDB locally or create a MongoDB Atlas cluster
   - Update `database/connection.py` with your connection details if using a remote instance
   - Ensure MongoDB is running on the default port (27017) for local setup

4. **Prepare the ML model**:
   - The application expects a trained DistilBERT model in the `./models/` directory
   - Run the training script if needed: `python backend/train.py`
   - Alternatively, download a pre-trained model and place it in the models directory

## Environment Setup

- **Local Development**: Ensure MongoDB is running locally. The application connects to `localhost:27017` by default.
- **Production**: Use environment variables for database credentials and other sensitive information.
- **Model Dependencies**: The ML model requires significant computational resources. Ensure adequate GPU/CPU resources for training and inference.

## Running Locally

1. **Start the backend API**:
   ```bash
   cd backend
   python app.py
   ```
   The Flask server will start on `http://localhost:5000`.

2. **Serve the frontend**:
   - For development, use a static server:
     ```bash
     cd frontend
     python -m http.server 8000
     ```
   - Open `http://localhost:8000` in your browser
   - Note: API calls will be proxied to the backend running on port 5000

3. **Access the application**:
   - Dashboard: `http://localhost:8000` (frontend)
   - API Documentation: Available at `/predict` endpoint (POST requests with JSON payload)

## Deployment

The live application is deployed at: [https://nia-safe.vercel.app/](https://nia-safe.vercel.app/)

### Deploying to Vercel

Vercel provides seamless deployment for both static sites and serverless functions. Since NiaSafe has a static frontend and a Python backend, follow these steps:

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Authenticate with Vercel**:
   ```bash
   vercel login
   ```

3. **Prepare for deployment**:
   - For the frontend: Vercel can deploy static HTML/CSS/JS directly
   - For the backend: Adapt the Flask app for Vercel's serverless functions
     - Create an `api/` directory in the project root
     - Move Flask routes to serverless function files (e.g., `api/predict.py`)
     - Update imports and dependencies accordingly

4. **Deploy the application**:
   ```bash
   vercel
   ```
   - Follow the prompts to configure the project
   - Vercel will detect the static frontend and serverless backend automatically
   - For production databases, update connection strings to use environment variables

5. **Alternative Backend Deployment**:
   If adapting Flask to serverless proves complex, deploy the backend separately:
   - Use Heroku, Railway, or another Python-compatible platform
   - Update the frontend's API calls to point to the deployed backend URL

6. **Environment Variables**:
   Set up environment variables in Vercel dashboard for:
   - Database connection strings
   - API keys (if any)
   - Model paths

## Project Structure

```
NiaSafe/
├── backend/                 # Flask API and ML components
│   ├── app.py              # Main Flask application
│   ├── alerts.py           # Alert system logic
│   ├── preprocess.py       # Data preprocessing scripts
│   ├── train.py            # Model training script
│   ├── requirements.txt    # Python dependencies
│   └── tests/              # Unit tests
├── database/               # Database connection and utilities
│   ├── connection.py       # MongoDB connection setup
│   └── helpers.py          # Database helper functions
├── frontend/               # Static web interface
│   ├── index.html          # Main dashboard page
│   ├── report_form.html    # Report submission form
│   ├── form.html           # Additional forms
│   └── js/                 # JavaScript files
│       ├── api.js          # API interaction
│       ├── charts.js       # Chart rendering
│       └── alerts.js       # Alert handling
├── models/                 # ML model files (not in repo)
├── .gitignore              # Git ignore rules
├── LICENSE                 # Project license
└── README.md               # This file
```

## Usage

- **Dashboard**: View and filter flagged comments, monitor severity trends, and check active alerts
- **API Usage**: Send POST requests to `/predict` with JSON payload:
  ```json
  {
    "text": "Your comment text here"
  }
  ```
  Response includes toxicity probabilities and alert status
- **Data Management**: Flagged comments are automatically stored in MongoDB with timestamps and severity scores

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run tests: `python -m pytest backend/tests/`
5. Commit your changes: `git commit -am 'Add new feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## License

This project is licensed under the terms specified in the LICENSE file.
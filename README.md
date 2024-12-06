# Web Deface Detection Using Deep Learning

## Overview

This project focuses on detecting web defacement using deep learning techniques. The model is designed to classify whether a website's page is clean or has been defaced by attackers. By using Convolutional Neural Networks (CNN), the model is trained to differentiate between legitimate and tampered web pages.

## Table of Contents

- [Project Overview](#overview)
- [Setup Instructions](#setup-instructions)
- [Project Structure](#project-structure)
- [Report Generation](#report-generation)
- [Model Evaluation](#model-evaluation)
- [Contributing](#contributing)
- [License](#license)

## Setup Instructions

Follow these instructions to get the project up and running on your local machine:

### 1. Clone the repository

Clone the repository to your local machine using Git:
```bash
git clone https://github.com/yourusername/web-deface-detection.git
```

### 2. Install dependencies
Install the required Python packages by running:
```bash
pip install -r requirements.txt
```

### 3. Prepare Dataset
```bash
python data_collection.py
```
When data_collection done, use this:
```bash
python data_preprocessing.py
```

### 4. Train the model
Once the dataset is prepared, you can start training the model with the following command:
```bash
python train_model.py
```
This will train the model and save it as web_defacement_model in the models/ directory.

### 5. Evaluate the model
When model was saved, you can evaluate the model with these following commands:
```bash
python evaluate_model.py
```
```bash
python save_training_report.py
```
These will save the report of trained model in the reports/ directory.

### 6. Test the model
To test the trained model and make detection, run my-flask-app for deploy a simple web
cd to my-flask-app
```bash
python app.py
```
http://127.0.0.1:5000/
You will need to upload test image and press button. Ctrl+c for end session.

### Project Structure
Here is the directory structure of the project:
````
web-deface-detect/
├── dataset/               # Folder containing clean and defaced iimages
├── logs/                  # Folder containing log
├── models/                # Folder to save the trained model
│   └── web_defacement_model
├── reports/               # Folder for generated reports
├── scripts/               # Python scripts
├── requirements.txt       # Python dependencies
├── URLs.txt               # URLs for dataset
├── my-flask-app           # Simple app for testing
└── README.md              # Project documentation
````

### Report Generation
After the training and prediction, reports will be generated in the reports/ directory. You will get:
Training Report: Contains accuracy and loss metrics during training.

### Model Evaluation
You can evaluate the model's performance using metrics such as:

Accuracy
Precision
Recall
F1-score
These metrics will give you an insight into the model's classification performance on clean and defaced web pages.

### Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes.
Commit your changes (git commit -am 'Add new feature').
Push to the branch (git push origin feature-branch).
Create a pull request.

### License
This project is licensed under the MIT License - see the LICENSE file for details.

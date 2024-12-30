# Brain Tumor Classification

![image](https://github.com/user-attachments/assets/8d70b23d-2ea4-43eb-9f0c-2251b6c7a7a2)

## Overview

**Brain Tumor Classification** is an advanced web application designed to assist neurosurgeons in diagnosing brain tumors from MRI scans. By combining **classical machine learning** with **generative AI**, this application delivers accurate predictions and visual explanations to aid in clinical decision-making.

### Live Demo
[Brain Tumor Classification App](https://brain-tumor-classification-dhruv-mojila.streamlit.app/)

### Dataset
[Kaggle: Brain Tumor MRI Dataset](https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset)

### Explanation
[Youtube Video](https://youtu.be/zSlVZ41B-LU?si=pLiK3CxHHWgxna9r)

## Features

1. **Upload MRI Scans**: Neurosurgeons can upload an MRI scan and receive predictions for tumor classification.
2. **Prediction Details**:
   - **Predicted Class**: Glioma, Meningioma, Pituitary, or No Tumor.
   - **Confidence Scores**: Displayed for all tumor classes in a bar chart.
   - **Highlighted Regions**: Segmented areas in the MRI scan indicating tumor presence.
3. **AI-Generated Reports**: Generative AI provides detailed reports based on uploaded scans and segmented images.
4. **Model Comparison**: Neurosurgeons can choose from multiple models for prediction.

## Models Used

### 1. **Transfer Learning - Xception**
- **Train Accuracy**: 98.60%
- **Validation Accuracy**: 96.49%
- **Test Accuracy**: 97.10%
- **Loss**:
  - Train: 0.1395
  - Validation: 0.2918
  - Test: 0.4662

### 2. **ResNet50**
- **Train Accuracy**: 98.20%
- **Validation Accuracy**: 97.86%
- **Test Accuracy**: 97.71%
- **Loss**:
  - Train: 0.0638
  - Validation: 0.0647

### 3. **Custom CNN Model**
- **Train Accuracy**: 98.35%
- **Validation Accuracy**: 95.11%
- **Test Accuracy**: 95.73%
- **Loss**:
  - Train: 0.1707
  - Validation: 0.2427
  - Test: 0.2596

## Technology Stack

- **Programming Language**: Python
- **Frameworks**: TensorFlow, Streamlit
- **Development Tools**: Jupyter Notebook, VS Code, Google Colab
- **Hosting**: Streamlit Cloud
- **Others**: Groq, Kaggle

## Challenges Faced
- **Hardware Limitations**: My laptop uses an NVIDIA GeForce GTX 1650 GPU, which is supported by TensorFlow only with specific configurations.
- **Dependency Management**: As TensorFlow’s latest versions do not natively support GPU on Windows, I had to install tensorflow<2.11 and configure CUDA and cuDNN libraries manually.
- **WSL Installation Issues**: Attempts to set up TensorFlow in Windows Subsystem for Linux (WSL) failed due to compatibility issues.
- **Resolution**: After thorough research and experimentation, I identified the correct versions of dependencies, using this helpful tutorial: [TensorFlow Installation in Windows](https://www.youtube.com/watch?v=0S81koZpwPA). Feel free to contact me if you face similar challenges.

## How It Works

1. **Upload**: Neurosurgeons upload MRI scans via the Streamlit interface.
2. **Prediction**:
   - The app processes the image using the selected model (Xception, ResNet50, or Custom CNN).
   - It returns the predicted class and confidence scores for each category.
3. **Visualization**:
   - The MRI scan is displayed with highlighted tumor regions.
   - A bar chart shows the confidence scores for all classes.
4. **Report Generation**:
   - An AI-generated report is created based on the MRI scan and prediction results using **Llama Vision**.

## Future Scope

1. **Interactive Explanation**:
   - Integrating a chat functionality for neurosurgeons to ask questions related to AI predictions.
2. **Dashboard**:
   - A comparative dashboard to analyze outputs and confidence scores across all models.
3. **Enhanced Models**:
   - Adding more advanced models for better accuracy and robust comparison.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/dhruvmojila/brain-tumor-classification.git
   ```
2. Navigate to the project directory:
   ```bash
   cd brain-tumor-classification
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Example Predictions

| Class         | Confidence |
|---------------|------------|
| **Glioma**    | 99.85%     |
| **Meningioma**| 0.11%      |
| **No Tumor**  | 0.01%      |
| **Pituitary** | 0.02%      |

## Contribution

Contributions are welcome! If you’d like to add new features, improve documentation, or optimize code, please feel free to open a pull request or create an issue.

## Contact

- **Developer**: Dhruv Mojila  
- **Email**: [dhruvmojila098@gmail.com](mailto:dhruvmojila098@gmail.com)
- **LinkedIn**: [https://www.linkedin.com/in/dhruv-mojila/](https://www.linkedin.com/in/dhruv-mojila/)

## Acknowledgements

- Kaggle for providing the dataset.
- TensorFlow and Streamlit communities for their robust frameworks.
- Neurosurgeons and medical professionals for inspiring this project.

---

### Additional Resources

- [Live App](https://brain-tumor-classification-dhruv-mojila.streamlit.app/)
- [Dataset](https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset)


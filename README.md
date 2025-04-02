# 🧠 ML Workflow for Image Classification using Step Functions

This project demonstrates how to deploy and monitor a Machine Learning pipeline for **image classification** using **AWS Step Functions** and **Amazon SageMaker**. It uses the **CIFAR-100** dataset and mimics real-world scenarios in ML workflow orchestration with serverless architecture.

## 🗂️ Project Overview

The notebook walks through the following pipeline stages:

1. **Extract**: Download and unpack the CIFAR-100 dataset.
2. **Transform**: Reformat the image data for ingestion.
3. **Load**: Upload the processed data into S3 for downstream usage.
4. **Train**: Trigger SageMaker training jobs through AWS Step Functions.
5. **Evaluate & Monitor**: Evaluate model accuracy and dynamically branch logic.
6. **(Optional)**: Deploy the model if accuracy meets a certain threshold.

## 🖼️ Dataset

We use the **CIFAR-100 dataset** available [here](https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz), which consists of 100 classes of 32x32 color images. The ETL pipeline is built to process this data efficiently and stage it into an S3 bucket.

## 🚀 AWS Stack

- **Amazon S3** – for storing raw and processed data.
- **AWS Lambda** – for lightweight ETL and evaluation tasks.
- **Amazon SageMaker** – to train the image classification model.
- **AWS Step Functions** – to orchestrate and monitor the pipeline.

## 📦 Key Components

### ✅ Data Extraction

```python
def extract_cifar_data(url, filename="cifar.tar.gz"):
    r = requests.get(url)
    with open(filename, "wb") as file_context:
        file_context.write(r.content)
```

### ✅ Data Transformation & Upload

Images are processed and reshaped, then uploaded to S3 under a structured format that SageMaker expects.

### ✅ ML Model Training

A SageMaker training job is triggered via a Step Function state. The training script uses TensorFlow or PyTorch to build a Convolutional Neural Network (CNN).

### ✅ Model Evaluation

Accuracy and other metrics are computed and used as a branching condition in Step Functions:

```json
{
  "Variable": "$.ModelEvaluation.Accuracy",
  "NumericGreaterThanEquals": 0.80,
  "Next": "DeployModel"
}
```

## 🎯 Stretch Goals Achieved

- ✅ Dynamic branching based on evaluation metrics  
- ✅ Automated data staging into S3  
- ✅ Orchestration using AWS Step Functions  
- ✅ Monitoring via CloudWatch logs  
- ✅ Model training in SageMaker using custom training scripts

## 📷 Screenshots

Add these to your `assets/` folder and embed:

- Step Function execution graph
- Sample model predictions
- Confusion matrix or accuracy plot

## 🧪 How to Run

1. Launch a SageMaker Notebook (`ml.t3.medium` or higher)
2. Clone the repo and run `starter.ipynb`
3. Deploy Lambda functions for ETL and evaluation
4. Upload training and test data to S3
5. Define Step Function using provided JSON definition
6. Start execution from the AWS Console

## 🧰 Tools Used

- Python (pandas, NumPy, TensorFlow/PyTorch, boto3)
- AWS Lambda
- Amazon SageMaker
- Amazon S3
- AWS Step Functions

## 📌 Conclusion

This project provides a robust blueprint for building ML pipelines on AWS using modern, serverless tools. It's extensible, production-ready, and suitable for use cases involving continuous model improvement, real-time monitoring, and scalable training.

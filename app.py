
from flask import Flask, render_template, request, send_file
from src.exceptions import CustomException
from src.logger import logger as lg 
from src.pipelines.train_pipeline import TrainPipeline
from src.pipelines.predict_pipeline import PredictionPipeline

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"


@app.route('/train')
def train_route():
    try:
        train_pipeline = TrainPipeline()  # Instantiate TrainPipeline
        train_pipeline.run_pipeline()  # Run the training pipeline
        return "Training pipeline ran successfully"
    except CustomException as e:
        lg.error(e)  # Log the error
        return str(e)  # Return error message as response
    

@app.route('/predict', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        try:
            predict_pipeline = PredictionPipeline(request)  # Instantiate PredictionPipeline
            prediction_file_detail = predict_pipeline.run_pipeline()  # Run the prediction pipeline
            
            # Check if 'file_path' exists in prediction_file_detail
            if 'file_path' in prediction_file_detail:
                return send_file(prediction_file_detail['file_path'], as_attachment=True)  # Send the file as an attachment
            else:
                return "Prediction file path not found", 400
            
        except CustomException as e:
            lg.error(e)  # Log the error
            return str(e)  # Return error message as response

    # Render the upload.html template for GET requests
    return render_template('upload_file.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)





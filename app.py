from flask import Flask, request, render_template
import numpy as np
import tensorflow as tf

app = Flask(__name__)

# Load the dummy protein model
MODEL_PATH = "protein_model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

# Standard amino acid mapping to integers
AA_MAPPING = {char: idx+1 for idx, char in enumerate("ACDEFGHIKLMNPQRSTVWY")}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    # Get sequence from form and clean it
    raw_sequence = request.form.get("sequence", "").upper().strip()
    if not raw_sequence:
        return render_template("index.html", error="SYS_ERR: SEQUENCE_MISSING")

    # 1. Convert letters to integer arrays
    encoded = [AA_MAPPING.get(char, 0) for char in raw_sequence]
    
    # 2. Pad or truncate to exactly 50 amino acids (model requirement)
    seq_length = 50
    display_len = min(len(encoded), seq_length)
    
    if len(encoded) > seq_length:
        encoded = encoded[:seq_length]
    else:
        encoded = encoded + [0] * (seq_length - len(encoded))
        
    input_data = np.array(encoded).reshape(1, seq_length)

    # 3. Predict secondary structure
    predictions = model.predict(input_data)[0] 
    predicted_classes = np.argmax(predictions, axis=-1)
    
    # 4. Map back to Helix (H), Sheet (E), or Coil (C)
    struct_chars = ['H', 'E', 'C']
    predicted_structure = "".join([struct_chars[val] for val in predicted_classes[:display_len]])
    
    return render_template(
        "index.html",
        original_seq=raw_sequence[:display_len],
        predicted_struct=predicted_structure,
        seq_len=display_len
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
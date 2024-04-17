import streamlit as st
from PIL import Image
from deepface import DeepFace

def detect_emotion(image):
    """
    Detects emotions in the given image.
    """
    try:
        # Use DeepFace to predict emotions
        result = DeepFace.analyze(image)
        emotion = result['dominant_emotion']
        return emotion
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def main():
    st.title("Emotion Detection App")

    # Allow user to upload multiple images
    st.sidebar.title("Upload Images")
    uploaded_files = st.sidebar.file_uploader("Choose images", type=['jpg'], accept_multiple_files=True)

    if uploaded_files:
        # Display uploaded images and predicted emotions
        st.header("Predicted Emotions")

        # Create a grid layout
        col_num = 3
        col_width = 300
        col_margin = 10

        for i, file in enumerate(uploaded_files):
            # Display each image
            with st.beta_container():
                image = Image.open(file)
                st.image(image, caption=f"Image {i + 1}", width=col_width)
                
                # Detect emotion for each image
                emotion = detect_emotion(image)
                if emotion:
                    st.write(f"Emotion: {emotion}")
                else:
                    st.write("Failed to detect emotion")

                # Adjust layout
                if (i + 1) % col_num != 0:
                    st.markdown("<style>div.st-dm{margin-right: 15px;}</style>", unsafe_allow_html=True)
                if (i + 1) % col_num == 0:
                    st.markdown("<style>div.st-dm{clear: both;}</style>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

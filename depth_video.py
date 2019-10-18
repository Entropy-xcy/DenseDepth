from cv2 import *
from keras.models import load_model
from layers import BilinearUpSampling2D
from utils import predict, load_images, display_images, load_images_cv, distance_to_image
import numpy as np

def main():
    custom_objects = {'BilinearUpSampling2D': BilinearUpSampling2D, 'depth_loss_function': None}
    print('Loading model...')

    # Load model into GPU / CPU
    model = load_model('nyu.h5', custom_objects=custom_objects, compile=False)

    cap = VideoCapture(0)
    while True:
        frames = []
        ret, frame = cap.read()
        frame = resize(frame, (480, 640))
        orig = resize(frame, (640, 400))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.clip(np.asanyarray(frame, dtype=float) / 255, 0, 1)
        frames.append(frame)
        frames = np.stack(frames, axis=0)
        print(frames.shape)
        outputs = predict(model, frames)
        out_img = outputs[0]
        out_img = distance_to_image(out_img)
        out_img = resize(out_img, (640, 400))
        imshow("out", out_img)
        imshow("Original", orig)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    destroyAllWindows()


if __name__ == "__main__":
    main()
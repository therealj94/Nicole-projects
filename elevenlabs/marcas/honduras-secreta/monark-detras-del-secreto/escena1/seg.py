import cv2, numpy as np, mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
opt = vision.ImageSegmenterOptions(base_options=mpt.BaseOptions(model_asset_path='/tmp/x/selfie_multiclass.tflite'), output_confidence_masks=True, running_mode=vision.RunningMode.VIDEO)
seg = vision.ImageSegmenter.create_from_options(opt)
c = cv2.VideoCapture('../real/t1_1080.mov'); out = []; i = 0
while True:
    ok, f = c.read()
    if not ok: break
    r = seg.segment_for_video(mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(f, cv2.COLOR_BGR2RGB)), int(i * 1000 / 30))
    bg = r.confidence_masks[0].numpy_view()
    out.append(((1 - bg) * 255).astype(np.uint8)); i += 1
np.save('person.npy', np.array(out)); print(len(out))

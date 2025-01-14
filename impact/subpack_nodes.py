import os
import folder_paths
import impact.core as core
import impact.subcore as subcore
from impact.utils import add_folder_path_and_extensions

version_code = 20

print(f"### Loading: ComfyUI-Impact-Pack (Subpack: V0.4)")

model_path = folder_paths.models_dir
add_folder_path_and_extensions("ultralytics_bbox", [os.path.join(model_path, "ultralytics", "bbox")], folder_paths.supported_pt_extensions)
add_folder_path_and_extensions("ultralytics_segm", [os.path.join(model_path, "ultralytics", "segm")], folder_paths.supported_pt_extensions)
add_folder_path_and_extensions("ultralytics", [os.path.join(model_path, "ultralytics")], folder_paths.supported_pt_extensions)


class UltralyticsDetectorProvider:
    @classmethod
    def INPUT_TYPES(s):
        bboxs = ["bbox/"+x for x in folder_paths.get_filename_list("ultralytics_bbox")]
        segms = ["segm/"+x for x in folder_paths.get_filename_list("ultralytics_segm")]

        print("bboxs", bboxs)
        print("bboxs ultra", folder_paths.get_filename_list("ultralytics_bbox"))

        print("segms", segms)
        print("segms 2", folder_paths.get_filename_list("ultralytics_segm"))

        print("segms 2", folder_paths.get_filename_list("ultralytics"))

        return {"required": {"model_name": (set(bboxs + segms + folder_paths.get_filename_list("ultralytics")), )}}
    RETURN_TYPES = ("BBOX_DETECTOR", "SEGM_DETECTOR")
    FUNCTION = "doit"

    CATEGORY = "ImpactPack"

    def doit(self, model_name):
        model_path = folder_paths.get_full_path("ultralytics", model_name)
        model = subcore.load_yolo(model_path)

        if model_name.startswith("bbox"):
            return subcore.UltraBBoxDetector(model), core.NO_SEGM_DETECTOR()
        else:
            return subcore.UltraBBoxDetector(model), subcore.UltraSegmDetector(model)


NODE_CLASS_MAPPINGS = {
    "UltralyticsDetectorProvider": UltralyticsDetectorProvider
}


NODE_DISPLAY_NAME_MAPPINGS = {

}

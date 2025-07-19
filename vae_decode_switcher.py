# vae_decode_switcher.py
#
# Place this file in your ComfyUI/custom_nodes/VAE-Decode-Switch/ directory.

try:
    import torch
except ImportError:
    print("[Warning] VAE Decode Switcher: PyTorch is not installed. Error handling will be limited.")
    torch = None

from nodes import VAEDecode, VAEDecodeTiled

class VAEDecodeSwitcher:
    """
    A custom node that allows switching between the standard VAE decoder
    and the tiled VAE decoder without changing workflow connections.
    """

    @classmethod
    def INPUT_TYPES(s):
        """
        Defines all possible input types for the node.
        The frontend will hide/show them as needed.
        """
        return {
            "required": {
                "samples": ("LATENT",),
                "vae": ("VAE",),
                "select_decoder": (["default", "tiled"],),
            },
            "optional": {
                "tile_size": ("INT", {"default": 512, "min": 64, "max": 4096, "step": 64}),
                "overlap": ("INT", {"default": 64, "min": 0, "max": 4096, "step": 8}),
                "temporal_size": ("INT", {"default": 64, "min": 1, "max": 4096, "step": 1}),
                "temporal_overlap": ("INT", {"default": 8, "min": 0, "max": 4096, "step": 1}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "switch_and_decode"
    CATEGORY = "Logic/Switchers"

    def switch_and_decode(self, samples, vae, select_decoder, **kwargs):
        print("\n--- VAE Decode Switcher ---")
        print(f"Selected Decoder: {select_decoder}")
        
        if select_decoder == "tiled":
            print("Executing Tiled VAE Decode.")
            tiled_decoder = VAEDecodeTiled()
            try:
                result = tiled_decoder.decode(
                    vae, 
                    samples, 
                    tile_size=kwargs.get('tile_size', 512),
                    overlap=kwargs.get('overlap', 64),
                    temporal_size=kwargs.get('temporal_size', 64),
                    temporal_overlap=kwargs.get('temporal_overlap', 8)
                )
                print("Tiled decoding successful.")
                return result
            except TypeError as e:
                print(f"\n[ERROR] VAE Decode Switcher: 'tiled' decoder failed: {e}\n")
                if torch:
                    return (torch.zeros(1, 64, 64, 3, dtype=torch.float32, device="cpu"), )
                else:
                    raise e
        else:
            print("Executing Default VAE Decode.")
            default_decoder = VAEDecode()
            result = default_decoder.decode(vae, samples)
            print("Default decoding successful.")
            return result

NODE_CLASS_MAPPINGS = {
    "VAEDecodeSwitcher": VAEDecodeSwitcher
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VAEDecodeSwitcher": "VAE Decode Switch"
}

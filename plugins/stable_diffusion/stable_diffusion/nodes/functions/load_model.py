import torch

from bluepynt import BaseFunctionNode, InputArgumentPin, OutputArgumentPin


class LoadModelNode(BaseFunctionNode):
    def __init__(self):
        super().__init__(node_id="bluepynt.stable_diffusion.LoadModelNode", name="Load Model",
                         description="Loads a model from a file")
        self.in_pins = (
            InputArgumentPin(pin_id="path", name="Path", argument_type=str),
        )
        self.out_pins = (
            OutputArgumentPin(pin_id="model", name="Model", argument_type=Model),
        )

    def execute(self):
        self.output_pin("model").set_value(self.argument_pin("path").value)

    def load_model_from_config(self, config, ckpt, device=torch.device("cuda"), verbose=False):
        print(f"Loading model from {ckpt}")
        pl_sd = torch.load(ckpt, map_location="cpu")
        if "global_step" in pl_sd:
            print(f"Global Step: {pl_sd['global_step']}")
        sd = pl_sd["state_dict"]
        model = instantiate_from_config(config.model)
        m, u = model.load_state_dict(sd, strict=False)
        if len(m) > 0 and verbose:
            print("missing keys:")
            print(m)
        if len(u) > 0 and verbose:
            print("unexpected keys:")
            print(u)

        if device == torch.device("cuda"):
            model.cuda()
        elif device == torch.device("cpu"):
            model.cpu()
            model.cond_stage_model.device = "cpu"
        else:
            raise ValueError(f"Incorrect device name. Received: {device}")
        model.eval()
        return model
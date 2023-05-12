from flowlauncher import FlowLauncher
from flow_types import QueryResponse, QueryComponents
from MemePy.MemeGenerator import MemeFactory, get_meme_factory, MemeLib
from MemePy.MemeModel import MemeImage

import win32clipboard
from tempfile import gettempdir
from pathlib import Path
from PIL import Image

from io import BytesIO


class MemeFlow(FlowLauncher):

    def query(self, query: str) -> list[QueryResponse]:
        if query == "":
            return [
                {
                    "title": "Enter a template name.",
                }
            ]

        components = self.get_args(query)
        if components["template"] in MemeLib:
            template: MemeImage = MemeLib[components["template"]]
            required_args = template.count_non_optional()
            optional_args = len(template.text_zones) - required_args
            if(len(components["arguments"]) < required_args):
                return [
                    {
                        "title": components["template"],
                        "subTitle": f"Required arguments: {required_args}" +
                                    (f"\nOptional arguments: {optional_args}" if optional_args > 0 else ""),
                        "icoPath": template.image_file_path
                    }
                ]
            else:
                factory = MemeFactory(template, components["arguments"])

                # Save the image to a local temp file so we can copy it to clipboard later
                buffer = BytesIO()
                factory.output_image.save(buffer, format="JPEG")

                temp_image_path = Path(
                        gettempdir(),
                        f"{components['template']}_{'_'.join(components['arguments'])}.jpg"
                    )

                with open(temp_image_path, "wb") as f:
                    f.write(buffer.getbuffer())

                return [
                    {
                        "title": components["template"],
                        "subTitle": f"Click enter to copy to clipboard!",
                        "icoPath": str(temp_image_path),
                        "jsonRPCAction": {
                            "method": "copy_image_to_clipboard",
                            "parameters": [str(temp_image_path)]
                        }
                    }
                ]
        else:
            return [
                {
                    "title": "Please enter a valid template name.",
                }
            ]

    def get_args(self, query: str) -> QueryComponents:
        words = query.split(" ")
        template = words[0]
        args = []
        if(len(words) > 1):
            args = words[1:]
        return {
            "template": template,
            "arguments": args
        }
    
    def copy_image_to_clipboard(self, image_path: str):
        image = Image.open(image_path)
        
        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        image_bytes = output.getvalue()[14:]
        output.close()

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, image_bytes)
        win32clipboard.CloseClipboard()
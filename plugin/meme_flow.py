from datetime import datetime

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

        components = self.parse_query(query)
        if components["template"] in MemeLib:
            template: MemeImage = MemeLib[components["template"]]

            required_args = template.count_non_optional()
            optional_args = len(template.text_zones) - required_args

            if(len(components["args"]) < required_args):
                return [
                    {
                        "title": components["template"],
                        "subTitle": f"Required arguments: {required_args}, Given: {len(components['args'])}" +
                                    (f"\nOptional arguments: {optional_args}" if optional_args > 0 else ""),
                        "icoPath": template.image_file_path
                    }
                ]
            else:
                factory = MemeFactory(template, components["args"])

                # Save the image to a local temp file so we can copy it to clipboard later
                buffer = BytesIO()
                factory.output_image.save(buffer, format="JPEG")

                now = datetime.now()
                temp_image_path = Path(
                        gettempdir(),
                        now.strftime(r"%Y_%m_%d_%H_%M_%S")
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

    def parse_query(self, query: str) -> QueryComponents:
        words = query.split(" ", maxsplit=1)
        template = words[0]
        args = []
        if(len(words) > 1):
            args = words[1].split("|")
            for i in range(len(args)):
                args[i] = args[i].strip()
        return {
            "template": template,
            "args": args
        }
    
    def copy_image_to_clipboard(self, image_path: str) -> None:
        image = Image.open(image_path)
        
        # Convert the image to a format we can put on the clipboard
        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        image_bytes = output.getvalue()[14:]
        output.close()

        # Put data on clipboard
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, image_bytes)
        win32clipboard.CloseClipboard()
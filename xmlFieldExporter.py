# Description: command line python script to interrogate xml file and search for tag, writing out all values present for that tag anywhere in the xml or optionally all deduplicated value
import sys
import xml.etree.ElementTree as ET

def extract_xml_tag(xml_file, tag_name, dedup):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        output_filename = f"{tag_name}.txt"

        if dedup:
            output_filename = f"{tag_name}-deduped.txt"
            extracted_contents = set()
            for element in root.iter(tag_name):
                if element.text is not None:  # Check if element text is not None
                    extracted_contents.add(element.text)
        else:
            extracted_contents = [element.text for element in root.iter(tag_name) if element.text is not None]

        with open(output_filename, "w") as output_file:
            for content in extracted_contents:
                output_file.write(content + "\n")

        num_lines_written = len(extracted_contents)
        print(f"Contents of '{tag_name}' tag written to '{output_filename}'.")
        print(f"Number of lines written to '{output_filename}': {num_lines_written}")

    except FileNotFoundError:
        print(f"Error: '{xml_file}' not found.")
    except ET.ParseError:
        print(f"Error: '{xml_file}' is not a valid XML file.")

if __name__ == "__main__":
    # Check if correct number of arguments are provided
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python script.py <xml_file> <tag_name> [--dedup]")
        sys.exit(1)

    xml_file = sys.argv[1]
    tag_name = sys.argv[2]
    dedup = False

    if len(sys.argv) == 4 and sys.argv[3] == "--dedup":
        dedup = True

    extract_xml_tag(xml_file, tag_name, dedup)

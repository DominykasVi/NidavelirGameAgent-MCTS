import os

def create_single_navigation_html(folder):
    # List all HTML files in the specified folder
    html_files = [f for f in os.listdir(folder) if f.endswith('.html')]
    html_files.sort()  # Ensure the files are in alphabetical order

    navigation_html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>HTML Files Navigation</title>
</head>
<body>
    <h1 id="fileTitle">Select a File</h1>
    <iframe id="viewer" style="width:100%; height:80vh; border:none;"></iframe>
    <div>
        <button onclick="navigate(-1)">Previous</button>
        <button onclick="navigate(1)">Next</button>
    </div>
    <script>
    var files = {files_json};
    var currentIndex = -1; // Start before the first index

    function navigate(direction) {{
        currentIndex += direction;
        if (currentIndex < 0) currentIndex = files.length - 1;
        else if (currentIndex >= files.length) currentIndex = 0;
        document.getElementById('viewer').src = files[currentIndex];
        document.getElementById('fileTitle').innerText = files[currentIndex];
    }}
    
    // Initialize with the first file
    navigate(1);
    </script>
</body>
</html>
    """.format(files_json=str(html_files).replace("'", '"'))  # Convert Python list to JSON array format

    # Save the navigation HTML file
    output_file_name = os.path.join(folder, os.path.basename(folder) + "_navigation.html")
    with open(output_file_name, "w") as html_file:
        html_file.write(navigation_html_template)

    return output_file_name  # Return the name of the generated HTML file

# Example usage
folder_name = "Logs\\Visualizations\\6c060df2-3690-4088-b057-9a56b7cc6bf0"  # Adjust this to the path of your folder
output_file = create_single_navigation_html(folder_name)
print(f"Navigation HTML file created: {output_file}")

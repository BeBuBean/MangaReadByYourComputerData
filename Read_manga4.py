import os
from pathlib import Path
import re
import json

def extract_number_from_name(name):
    match = re.search(r'\d+', name)
    return int(match.group()) if match else float('inf')

def generate_html(folder_path):
    folder = Path(folder_path)
    if not folder.exists():
        print("The specified folder does not exist.")
        return

    subfolders = sorted(
        [f for f in folder.iterdir() if f.is_dir()],
        key=lambda f: extract_number_from_name(f.name)
    )

    if not subfolders:
        print("No subfolders found in the specified folder.")
        return

    folder_list = [str(subfolder.resolve().as_posix()) for subfolder in subfolders]

    # Tạo HTML điều hướng
    chapter_selector_html = """
    <div class="chapter-selector">
        <label for="chapter-select">Chọn Chương: </label>
        <select id="chapter-select" onchange="goToChapter()">
    """
    for i, subfolder in enumerate(subfolders):
        short_name = subfolder.name if len(subfolder.name) <= 20 else subfolder.name[:20] + "..."
        chapter_selector_html += f'<option value="{i}" title="{subfolder.name}">{short_name}</option>'
    chapter_selector_html += """
        </select>
        <div class="navigation-buttons">
            <button onclick="navigate(-1)">⟵ Trước</button>
            <button onclick="navigate(1)">Sau ⟶</button>
        </div>
    </div>
    """

    for idx, subfolder in enumerate(subfolders):
        images = sorted(
            [f for f in subfolder.iterdir() if f.suffix.lower() in [".jpg", ".jpeg", ".png", ".gif",".mov"]],
            key=lambda f: extract_number_from_name(f.name)
        )

        if not images:
            continue  # Bỏ qua thư mục nếu không có ảnh

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Viewer - {subfolder.name}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            
        }}

        .image-container {{
            width: 100%;
            max-width: 800px;
            margin: 1px 0; /* khoảng cách giữa các bức ảnh */
        }}
        .image-container img {{
            width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }}
        .chapter-selector {{
            position: fixed;
            top: 10px;
            left: 10px;
            background: white;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            z-index: 1000;
        }}
        .navigation-buttons {{
            margin-top: 10px;
            display: flex;
            gap: 10px;
        }}
        .navigation-buttons button {{
            padding: 10px;
            border: none;
            border-radius: 5px;
            background-color: #007bff;
            color: white;
            cursor: pointer;
            font-size: 16px;
            transition: 0.3s;
        }}
        .navigation-buttons button:hover {{
            background-color: #0056b3;
        }}
        .scroll-to-top {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 50px;
            height: 50px;
            background-color: #007bff;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            cursor: pointer;
            font-size: 20px;
            transition: opacity 0.3s, transform 0.3s;
            opacity: 0;
            pointer-events: none;
        }}

        .scroll-to-top.visible {{
            opacity: 1;
            pointer-events: auto;
        }}

        .scroll-to-top:hover {{
            background-color: #0056b3;
            transform: scale(1.1);
        }}

        .chapter-search {{
            margin-top: 10px;
            display: flex;
            gap: 10px;
        }}

        .chapter-search input {{
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 5px;
            flex: 1;
        }}

        .chapter-search button {{
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            background-color: #007bff;
            color: white;
            cursor: pointer;
            font-size: 16px;
            transition: 0.3s;
        }}

        .chapter-search button:hover {{
            background-color: #0056b3;
        }}
        
        .progress-counter {{
            position: fixed;
            bottom: 10px;
            left: 10px;
            
            color: #000000;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 16px;
            z-index: 1000;
        }}
            
        .progress-container {{
            position: fixed;
            bottom: 37px;
            left: 10px;
            
            color: white;
            padding: 5px ;
            border-radius: 5px;
            font-size: 16px;
            z-index: 1000;
            display: flex;
            gap: 10px;
            align-items: center;
        }}
        .progress-container input {{
            width: 50px;
            text-align: center;
        }}

        


    </style>
    <script>
        const folders = {json.dumps(folder_list)};
        let currentFolderIndex = {idx};

        function navigate(offset) {{
            currentFolderIndex = (currentFolderIndex + offset + folders.length) % folders.length;
            window.location.href = folders[currentFolderIndex] + "/image_viewer.html";
        }}

        function goToChapter() {{
            const chapterSelect = document.getElementById('chapter-select');
            currentFolderIndex = chapterSelect.selectedIndex;
            window.location.href = folders[currentFolderIndex] + "/image_viewer.html";
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            // Cập nhật selector khi load trang
            document.getElementById('chapter-select').selectedIndex = currentFolderIndex;

            // Lắng nghe sự kiện nhấn phím
            document.addEventListener('keydown', (event) => {{
                const key = event.key.toLowerCase();
                if (key === 'arrowleft' || key === 'a') {{
                    navigate(-1); // Nút mũi tên trái
                }} else if (key === 'arrowright' || key === 'd') {{
                    navigate(1); // Nút mũi tên phải
                }}
            }});

            // Hiển thị hoặc ẩn nút kéo lên trang đầu
            const scrollToTopBtn = document.querySelector('.scroll-to-top');
            window.addEventListener('scroll', () => {{
                if (window.scrollY > 300) {{
                    scrollToTopBtn.classList.add('visible');
                }} else {{
                    scrollToTopBtn.classList.remove('visible');
                }}
            }});
        }});

        // Cuộn lên đầu trang khi nút được nhấn
        function scrollToTop() {{
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        function searchChapter() {{
            const searchInput = document.getElementById('chapter-search').value.trim().toLowerCase();
            if (!searchInput) {{
                alert('Vui lòng nhập tên hoặc số chương.');
                return;
            }}

            // Tìm chương khớp với từ khóa nhập
            const matchedIndex = folders.findIndex(folder => {{
                const folderName = folder.split('/').pop().toLowerCase(); // Lấy tên thư mục cuối cùng
                return folderName.includes(searchInput);
            }});

            if (matchedIndex !== -1) {{
                // Tìm thấy chương, chuyển đến chương đó
                currentFolderIndex = matchedIndex;
                window.location.href = folders[currentFolderIndex] + '/image_viewer.html';
            }} else {{
                alert('Không tìm thấy chương phù hợp.');
            }}
        }}


            document.addEventListener('DOMContentLoaded', () => {{
                document.getElementById('chapter-select').selectedIndex = currentFolderIndex;
                let images = document.getElementsByClassName('image-container');
                let totalImages = images.length;
                let progressCounter = document.createElement('div');
                progressCounter.id = 'progress-counter';
                progressCounter.className = 'progress-counter';
                progressCounter.innerText = `1/${{totalImages}}`;
                document.body.appendChild(progressCounter);
                
                function updateProgressCounter() {{
                    let scrollPosition = window.scrollY + window.innerHeight / 2;
                    let closestIndex = 0;
                    for (let i = 0; i < images.length; i++) {{
                        let rect = images[i].getBoundingClientRect();
                        if (rect.top + rect.height / 2 > 0) {{
                            closestIndex = i;
                            break;
                        }}
                    }}
                    progressCounter.innerText = `${{closestIndex + 1}}/${{totalImages}}`;
                }}
                
                updateProgressCounter();
                window.addEventListener('scroll', updateProgressCounter);
            }});

        function jumpToImage() {{
    let imageIndex = parseInt(document.getElementById('image-jump-input').value, 10);
    let images = document.getElementsByClassName('image-container');
    let totalImages = images.length;

    if (!isNaN(imageIndex) && imageIndex >= 1 && imageIndex <= totalImages) {{
        images[imageIndex - 1].scrollIntoView({{ behavior: 'smooth', block: 'center' }});
    }} else {{
        alert("Số ảnh không hợp lệ! Hãy nhập số từ 1 đến " + totalImages);
    }}
}}





    </script>
</head>
<body>
    {chapter_selector_html}
    <div class="scroll-to-top" onclick="scrollToTop()">⬆️</div>
    <div class="chapter-search">
        <input type="text" id="chapter-search" placeholder="Nhập tên hoặc số chương...">
        <button onclick="searchChapter()">Tìm</button>
    </div>
        <div class="progress-container">
        
        <input type="number" id="image-jump-input" placeholder="Nhập số ảnh..." min="1">
        <button onclick="jumpToImage()">Go</button>
    </div>


"""

        for image in images:
            html_content += f"""
    <div class="image-container">
        <img src="{image.name}" alt="{image.name}">
    </div>
    
"""


        html_content += """
</body>
</html>
"""

        output_file = subfolder / "image_viewer.html"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)

    print(f"HTML files created successfully in: {folder_path}")

# Chạy chương trình
if __name__ == "__main__":
    folder_path = input("Enter the folder path containing subfolders with images: ").strip()
    generate_html(folder_path)
